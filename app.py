import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize the Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


@app.route("/")
def index():
    """Serve the main frontend interface."""
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """Analyze the uploaded food image using Gemini 2.0 Flash."""
    # Validate request
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    goal = request.form.get("goal", "stay_healthy")
    meal_time = request.form.get("meal_time", "Breakfast")

    if file.filename == "":
        return jsonify({"error": "No image selected"}), 400

    try:
        # Read the image as bytes
        img_bytes = file.read()

        # Construct the specific prompt
        prompt = f"""You are a nutrition expert specializing in Indian food.
Analyze this food image. The user's health goal is: {goal}
They are eating this as: {meal_time}

Respond ONLY in this exact JSON format, no other text, no markdown:
{{
  "dish_name": "name of the dish",
  "is_indian": true or false,
  "calories": estimated calories as integer,
  "protein_g": protein in grams as integer,
  "fat_g": fat in grams as integer,
  "sugar_g": sugar in grams as integer,
  "health_score": integer 1-10 adjusted for their goal,
  "score_reason": "one sentence why this score for their goal",
  "warning": "main health warning for goal, or empty string",
  "context_note": "one sentence about eating this at meal_time",
  "swap_dish": "healthier Indian food alternative name",
  "swap_calories": estimated calories of swap as integer,
  "swap_score": integer 1-10 health score of swap,
  "calorie_saving": integer calories saved by choosing swap"
}}

Scoring rules:
- lose_weight: penalize high calories, fat, refined carbs heavily
- build_muscle: reward high protein, penalize empty calories
- manage_diabetes: penalize high sugar, white rice, maida heavily
- stay_healthy: balanced scoring"""

        # Pass inline image data with mime type to Gemini vision capabilities
        image_part = genai.types.Part.from_bytes(
            data=img_bytes, mime_type=file.mimetype or "image/jpeg"
        )

        # Call Gemini model
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=[image_part, prompt]
        )

        # Clean response and strip markdown fences
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        # Parse JSON
        result_json = json.loads(text)
        return jsonify(result_json)

    except Exception as e:
        print(f"Analysis Error: {e}")
        # Fallback response in case of failure or invalid JSON
        fallback = {
            "dish_name": "Unknown food",
            "is_indian": False,
            "calories": 0,
            "protein_g": 0,
            "fat_g": 0,
            "sugar_g": 0,
            "health_score": 0,
            "score_reason": "Could not analyze the image.",
            "warning": "Please upload a clear food photo.",
            "context_note": "",
            "swap_dish": "",
            "swap_calories": 0,
            "swap_score": 0,
            "calorie_saving": 0,
        }
        return jsonify(fallback)


if __name__ == "__main__":
    # Run with debug disabled to prevent arbitrary code execution
    app.run(debug=False)

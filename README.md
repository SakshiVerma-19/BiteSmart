# BiteSmart

BiteSmart is an AI-powered Indian food health analyzer. Upload an image of your food, select your health goal and meal time, and BiteSmart uses Google's Gemini 2.5 Flash to provide you with a comprehensive nutritional analysis, a customized health score, and healthier meal alternatives!

##  Features
- **AI Vision Analysis**: Powered by the Google GenAI SDK (`gemini-2.5-flash`), it instantly identifies the dish from an uploaded image.
- **Goal-Oriented Scoring**: Health scores are dynamically adjusted based on your personal goals (e.g., losing weight, building muscle, managing diabetes, or staying healthy).
- **Nutritional Insights**: Get estimated calories, protein, fat, and sugar content.
- **Smart Swaps**: Suggests healthier Indian food alternatives along with the estimated calorie savings.

## 🛠 Tech Stack
- **Backend**: Python, Flask, Gunicorn
- **AI**: Google GenAI SDK
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Docker

##  Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SakshiVerma-19/BiteSmart.git
   cd BiteSmart
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Google Gemini API Key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the Application:**
   ```bash
   python app.py
   ```
   The app will run locally at `http://127.0.0.1:5000/`.

##  Docker Deployment
BiteSmart includes a `Dockerfile` and is production-ready using Gunicorn.

1. **Build the image**:
   ```bash
   docker build -t bitesmart .
   ```
2. **Run the container**:
   ```bash
   docker run -p 8080:8080 -e PORT=8080 -e GEMINI_API_KEY=your_api_key_here bitesmart
   ```

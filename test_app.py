import os
import base64
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

dummy_jpg_base64 = '/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA='
img_bytes = base64.b64decode(dummy_jpg_base64)

try:
    image_part = types.Part.from_bytes(
        data=img_bytes,
        mime_type='image/jpeg'
    )
    prompt = 'hello'
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[image_part, prompt]
    )
    print('Response text:', response.text)
except Exception as e:
    print('Exception occurred:', type(e), e)

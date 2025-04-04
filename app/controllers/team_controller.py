import requests
import os
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

image_folder = 'static/images'
os.makedirs(image_folder, exist_ok=True)

def generate_image_from_text(name):
    """Generera bild från text med hjälp av Hugging Face API."""
    try:
        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
            json={"inputs": f"portrait of {name}"}
        )
        response.raise_for_status()  # Kasta ett fel om statuskoden inte är 2xx
        
        print("API response status:", response.status_code)
        print("API response content-type:", response.headers.get('Content-Type'))

        if response.status_code == 200:
            if 'image' in response.headers.get('Content-Type', ''):
                print("API returned an image.")
                image_filename = os.path.join(image_folder, f"{name.replace(' ', '_')}_portrait.jpg")
                with open(image_filename, "wb") as f:
                    f.write(response.content)
                return image_filename
            else:
                return "API response is not an image."
        else:
            print("API returned an error:", response.text)
            return "API error: " + response.text

    except Exception as e:
        print("Error:", e)
        return str(e)


def get_team_members():
    """Returnera en lista med teammedlemmar och deras bilder samt telefonnummer."""
    team_members = [
        {"name": "David Abdulkarim", "role": "AI-utvecklare", "description": "Arbetar med AI och maskininlärning.", "phone": "073-542 34 17"},
        {"name": "Henrik Bellander", "role": "Frontend-utvecklare", "description": "Designar användargränssnitt.", "phone": "073-211 04 78"},
        {"name": "Elias Aval", "role": "Backend-utvecklare", "description": "Bygger serverdelarna.", "phone": "070-733 23 11"},
        {"name": "Magnus Kurtz", "role": "Projektledare", "description": "Hanterar projektledning.", "phone": "070-670 6666"}
    ]

    for member in team_members:
        member['image'] = f"static/images/{member['name'].replace(' ', '_')}_portrait.jpg"
    return team_members
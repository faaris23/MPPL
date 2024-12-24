from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from google.cloud import vision
import google.generativeai as genai



app = Flask(__name__)
CORS(app)

# Konfigurasi API
genai.configure(api_key="AIzaSyBn7mC8ROA_dZnkikTN3CErGRnUvGoCiwU")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)

vision_client = vision.ImageAnnotatorClient()

def analyze_image(image_path):
    """Menggunakan Google Vision API untuk analisis gambar"""
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = vision_client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    return ', '.join(labels)

@app.route('/api/generate', methods=['POST'])
def generate():
    image = request.files['image']
    platform = request.form['platform']
    style = request.form['style']

    # Simpan gambar sementara
    image_path = f"./{image.filename}"
    image.save(image_path)

    # Analisis gambar
    description = analyze_image(image_path)

    # Hasilkan caption menggunakan OpenAI API
    prompt = f"Generate a {style} caption and hashtags for {platform}. The image is described as: {description}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1
    )
    result = response.choices[0].text.strip()

    # Parsing hasil
    caption, hashtags = result.split('Hashtags:')
    return jsonify({
        'caption': caption.strip(),
        'hashtags': hashtags.strip().split(', ')
    })

if __name__ == '__main__':
    app.run(debug=True)

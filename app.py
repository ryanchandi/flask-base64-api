from flask import Flask, request, jsonify
import base64
import requests

app = Flask(__name__)

# Functie om afbeelding om te zetten naar base64
def convert_image_to_base64(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code != 200:
            return None, f"Unable to fetch image, status code: {response.status_code}"
        
        image_content = response.content
        base64_image = base64.b64encode(image_content).decode('utf-8')
        return base64_image, None
    except Exception as e:
        return None, f"Error fetching image: {str(e)}"

@app.route('/convert_to_base64', methods=['POST'])
def convert_to_base64():
    try:
        # Haal de image URL op uit de JSON request body
        data = request.json
        image_url = data.get('image_url')

        if not image_url:
            return jsonify({
                'error': "No 'image_url' provided in request body"
            }), 400

        # Zet de afbeelding om naar base64
        base64_image, error = convert_image_to_base64(image_url)
        
        if error:
            return jsonify({
                'error': error
            }), 500

        # Geef het resultaat terug als JSON
        return jsonify({
            'base64_url': f"data:image/jpeg;base64,{base64_image}"
        })
    except Exception as e:
        return jsonify({
            'error': f"An unexpected error occurred: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

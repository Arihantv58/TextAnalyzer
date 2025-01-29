from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load environment variables
load_dotenv()
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')

# Create Azure client
credential = AzureKeyCredential(ai_key)
ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

@app.route('/analyze', methods=['POST'])
def analyze_text():
    try:
        data = request.json
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Get language
        detected_language = ai_client.detect_language(documents=[text])[0]
        language = detected_language.primary_language.name

        # Get sentiment
        sentiment_analysis = ai_client.analyze_sentiment(documents=[text])[0]
        sentiment = sentiment_analysis.sentiment

        # Get key phrases
        phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases

        # Get entities
        entities = [
            {"text": entity.text, "category": entity.category}
            for entity in ai_client.recognize_entities(documents=[text])[0].entities
        ]

        # Get linked entities
        linked_entities = [
            {"name": linked_entity.name, "url": linked_entity.url}
            for linked_entity in ai_client.recognize_linked_entities(documents=[text])[0].entities
        ]

        return jsonify({
            "language": language,
            "sentiment": sentiment,
            "key_phrases": phrases,
            "entities": entities,
            "linked_entities": linked_entities
        })

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


if __name__ == '__main__':
    app.run(debug=True)

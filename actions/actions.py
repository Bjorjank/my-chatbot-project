import requests
import logging
from rasa_sdk import Action
from rasa_sdk.events import UserUtteranceReverted

logger = logging.getLogger(__name__)

class ActionDefaultFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get('text')
        response = self.call_huggingface_api(user_message)

        if response:
            dispatcher.utter_message(response)
        else:
            dispatcher.utter_message("Maaf, saya tidak memiliki jawaban untuk pertanyaan ini.")

        logger.info("User Message: %s, Response: %s", user_message, response)
        return [UserUtteranceReverted()]

    def call_huggingface_api(self, message):
        url = "https://api-inference.huggingface.co/models/openai-community/gpt2"
        headers = {"Authorization": "Bearer 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"}
        data = {"inputs": message}

        try:
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                response_json = response.json()
                print("Response from Hugging Face:", response_json)  # Logging untuk debugging
                
                # Memeriksa apakah response JSON memiliki key yang sesuai
                if isinstance(response_json, list) and 'generated_text' in response_json[0]:
                    return response_json[0]['generated_text']
                else:
                    print("Generated text not found in response.")
                    return None
            else:
                print(f"Error in API request: {response.status_code}, {response.text}")  # Error handling yang lebih baik
                return None
        except Exception as e:
            print(f"Exception during API request: {str(e)}")
            return None

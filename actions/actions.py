import requests
from rasa_sdk import Action
from rasa_sdk.events import UserUtteranceReverted

class ActionDefaultFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        # Panggil model AI (Hugging Face) untuk mendapatkan jawaban
        user_message = tracker.latest_message.get('text')
        response = self.call_huggingface_api(user_message)

        if response:
            dispatcher.utter_message(response)
        else:
            dispatcher.utter_message("Maaf, saya tidak memiliki jawaban untuk pertanyaan ini.")

        # Kembalikan jawaban dari AI
        return [UserUtteranceReverted()]

    def call_huggingface_api(self, message):
        # URL API Hugging Face
        url = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
        
        # Authorization Header jika API membutuhkan API Key
        headers = {
            "Authorization": "Bearer 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"
        }
        
        # Data yang dikirim
        data = {
            "inputs": message
        }

        try:
            # Panggil API
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                response_json = response.json()
                # Akses key 'choices' untuk mengambil teks yang dihasilkan
                if isinstance(response_json, list) and len(response_json) > 0:
                    choices = response_json[0].get('choices', [])
                    if len(choices) > 0:
                        return choices[0]['text']  # Mengambil teks dari choices
                    else:
                        print("No choices found in response.")
                        return None
                else:
                    print("Invalid response format.")
                    return None
            else:
                print(f"Error from API: {response.status_code}, {response.text}")
                return None

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return None

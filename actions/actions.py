import logging
from rasa_sdk import Action
from rasa_sdk.events import UserUtteranceReverted, SlotSet
from huggingface_hub import InferenceClient

logger = logging.getLogger(__name__)

# API Client untuk Qwen dari Hugging Face
client = InferenceClient(api_key="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")

class ActionCheckAnswer(Action):
    def name(self):
        return "action_check_answer"

    def run(self, dispatcher, tracker, domain):
        # Mengambil intent yang dikenali
        intent = tracker.get_intent_of_latest_message()

        # Mengecek apakah intent punya jawaban di domain
        known_responses = domain.get("responses", {}).get(f"utter_{intent}", [])

        if known_responses:
            # Jika ada respons yang sudah terdefinisi untuk intent ini
            dispatcher.utter_message(text=known_responses[0]["text"])
        else:
            # Fallback ke AI jika tidak ditemukan jawaban
            response = self.call_qwen_api(tracker.latest_message.get('text'))
            if response:
                dispatcher.utter_message(response)
            else:
                dispatcher.utter_message("Maaf, saya tidak memiliki jawaban untuk pertanyaan ini.")
        
        # Selalu kembalikan event list untuk memperbarui state
        return [SlotSet("last_intent", intent)]  # atau return []

    def call_qwen_api(self, message):
        try:
            # Memanggil API Qwen dengan menggunakan InferenceClient
            responses = client.chat_completion(
                model="Qwen/Qwen2.5-1.5B-Instruct",
                messages=[{"role": "user", "content": message}],
                max_tokens=500,
                stream=False  # Kita tidak perlu menggunakan streaming di sini
            )

            # Parsing respons yang diterima dari API Qwen
            if responses.choices:
                generated_response = responses.choices[0].message["content"]
                return generated_response.strip()  # Menghapus spasi kosong yang berlebihan
            else:
                return None
        except Exception as e:
            logger.error(f"Error during Qwen API call: {e}")
            return None

class ActionDefaultFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        # Mendapatkan pesan user yang terakhir
        user_message = tracker.latest_message.get('text')

        # Panggil AI Qwen jika tidak ada jawaban di bot
        response = self.call_qwen_api(user_message)

        if response:
            dispatcher.utter_message(response)
        else:
            dispatcher.utter_message("Maaf, saya tidak memiliki jawaban untuk pertanyaan ini.")

        logger.info("User Message: %s, Response: %s", user_message, response)
        
        # Selalu kembalikan event list untuk memperbarui state
        return [UserUtteranceReverted()]  # atau return []

    def call_qwen_api(self, message):
        try:
            # Memanggil API Qwen dengan menggunakan InferenceClient
            responses = client.chat_completion(
                model="Qwen/Qwen2.5-1.5B-Instruct",
                messages=[{"role": "user", "content": message}],
                max_tokens=500,
                stream=False  # Kita tidak perlu menggunakan streaming di sini
            )

            # Parsing respons yang diterima dari API Qwen
            if responses.choices:
                generated_response = responses.choices[0].message["content"]
                return generated_response.strip()  # Menghapus spasi kosong yang berlebihan
            else:
                return None
        except Exception as e:
            logger.error(f"Error during Qwen API call: {e}")
            return None

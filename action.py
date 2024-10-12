from transformers import pipeline
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Load Hugging Face model (gpt-2 as an example)
model = pipeline("text-generation", model="gpt2")

class ActionAskHuggingFace(Action):

    def name(self):
        return "action_ask_hugging_face"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        # Get the latest message from the user
        user_message = tracker.latest_message.get('text')

        # Use the model to generate a response
        response = model(user_message, max_length=50, num_return_sequences=1)
        ai_response = response[0]['generated_text']

        # Send the AI's response back to the user
        dispatcher.utter_message(text=ai_response)

        return []

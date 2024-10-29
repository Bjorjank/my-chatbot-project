from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Verifikasi token saat menghubungkan webhook (GET)
@app.route('/webhooks/whatsapp/webhook', methods=['GET'])
def verify():
    verify_token = "my_verification_token"  # Token yang kamu masukkan di Facebook Developer
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == "subscribe" and token == verify_token:
        return str(challenge), 200  # Kirim 'challenge' jika token valid
    else:
        return "Verification failed", 403

# Menerima dan merespon pesan dari WhatsApp (POST)
@app.route("/webhooks/whatsapp/webhook", methods=["POST"])
def whatsapp_webhook():
    data = request.get_json()  # Ambil data dari request

    # Pastikan data yang diterima adalah pesan dari WhatsApp
    if 'messages' in data['entry'][0]['changes'][0]['value']:
        messages = data['entry'][0]['changes'][0]['value']['messages']
        
        for message in messages:
            # Ambil pesan teks dari WhatsApp
            if message.get("text"):
                user_message = message["text"]["body"]
                sender_id = message["from"]

                # Kirim pesan user ke Rasa melalui API Rasa
                rasa_response = requests.post("http://localhost:5005/webhooks/rest/webhook", 
                                              json={"sender": sender_id, "message": user_message})
                
                # Dapatkan respon dari Rasa dan kirim kembali ke pengguna via WhatsApp
                for response_message in rasa_response.json():
                    send_whatsapp_message(sender_id, response_message.get("text"))

    return "Success", 200

# Fungsi untuk mengirim pesan kembali ke WhatsApp
def send_whatsapp_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v13.0/493567327164540/messages"
    headers = {
        "Authorization": "Bearer EAAIr5p6tizYBOxkvby9VJ0oJ5VGEUvfnDZBXpfsCyOVaWzZAOIICZBryZCn1JfIn3qXOpZA847TalxW5ld1HatPN9PCZCgDRF0b1ZAWUUFXR6KcfrBunLpqmrTPeUARjqLlim2XwZATPdxPOHNZBVLlZCCVee2Ot5TVUWbEOJYMBmoqnUbZCiob7RyAYggFJ5qYIBPfqxwgwZBiq5qRp9laBG98s7BqeyKYZD",  # Access token dari Facebook Developer
        "Content-Type": "application/json"
    }
    
    message_data = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "text": {"body": message_text}
    }
    
    response = requests.post(url, headers=headers, json=message_data)
    return response.status_code

if __name__ == "__main__":
    app.run(port=5006, debug=True)

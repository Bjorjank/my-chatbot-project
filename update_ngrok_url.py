import requests
import yaml

# Fungsi untuk mendapatkan URL ngrok terbaru
def get_ngrok_url():
    try:
        response = requests.get('http://127.0.0.1:4040/api/tunnels')
        tunnels = response.json()['tunnels']
        for tunnel in tunnels:
            if tunnel['proto'] == 'https':
                return tunnel['public_url']
    except Exception as e:
        print(f"Error getting ngrok URL: {e}")
        return None

# Fungsi untuk memperbarui file YAML
def update_yaml_file(file_path, new_url):
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)

        # Update URL di file YAML (misalnya di credentials atau endpoints)
        if 'rest' in config:
            config['rest']['webhook_url'] = f"{new_url}/webhooks/whatsapp/webhook"
        if 'webhook' in config:
            config['webhook']['url'] = f"{new_url}/webhooks/whatsapp/webhook"

        with open(file_path, 'w') as file:
            yaml.dump(config, file)

        print(f"Successfully updated {file_path} with new ngrok URL.")
    except Exception as e:
        print(f"Error updating {file_path}: {e}")

if __name__ == "__main__":
    ngrok_url = get_ngrok_url()
    if ngrok_url:
        # Path to credentials.yml and endpoints.yml
        credentials_file = 'credentials.yml'
        endpoints_file = 'endpoints.yml'

        # Update both files
        update_yaml_file(credentials_file, ngrok_url)
        update_yaml_file(endpoints_file, ngrok_url)
    else:
        print("Failed to get ngrok URL.")

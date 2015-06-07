from pushover import Client

def send(api_token, user_token, message, title):
    
    client = Client(user_token, api_token=api_token)
    client.send_message(message, title=title)
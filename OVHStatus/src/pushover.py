from pushover import init, Client

def send(api_token, user_token, message, title):
    
    init(api_token)
    Client(user_token).send_message(message, title=title)
    
    return
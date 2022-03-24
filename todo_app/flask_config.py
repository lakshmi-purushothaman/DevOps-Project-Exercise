import os


class Config:
    def __init__(self):
        """Base configuration variables."""
        SECRET_KEY = os.getenv('SECRET_KEY')
        #API Key and token for Trello
        TRELLO_API_KEY=os.environ.get('TRELLO_API_KEY')
        TRELLO_TOKEN=os.environ.get('TRELLO_TOKEN')
        
        if not SECRET_KEY:
            raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
        if not TRELLO_API_KEY:
            raise ValueError("No TRELLO_API_KEY set for Flask application. Follow the setup instructions")
        if not TRELLO_TOKEN:
            raise ValueError("No TRELLO_TOKEN set for Flask application. Follow the setup instructions")
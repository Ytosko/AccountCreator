import firebase_admin
from firebase_admin import credentials, auth

# Global variable to keep track of Firebase app initialization
default_app_initialized = False

def initialize_firebase():
    global default_app_initialized
    if not default_app_initialized:
        # Initialize Firebase only if it's not already initialized
        cred = credentials.Certificate('./service.json')
        firebase_admin.initialize_app(cred)
        default_app_initialized = True

def create_user(email, password):
    return auth.create_user(email=email, password=password)

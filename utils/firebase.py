import firebase_admin
from firebase_admin import credentials, messaging
from config import FIREBASE_CREDENTIALS_PATH


_initialized = False


def init_firebase():
    """Initialize Firebase Admin SDK. Call once at app startup."""
    global _initialized
    if _initialized:
        return

    if not FIREBASE_CREDENTIALS_PATH:
        print("Warning: FIREBASE_CREDENTIALS_PATH is not set. Push notifications will not work.")
        return

    try:
        cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
        _initialized = True
        print("Firebase Admin SDK initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize Firebase Admin SDK: {e}")


def send_push_notification(fcm_token: str, title: str, body: str):
    """Send a push notification via Firebase Cloud Messaging.

    Returns True on success, False on failure.
    """
    if not _initialized:
        print("Firebase not initialized. Skipping notification.")
        return False

    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=fcm_token,
        )
        response = messaging.send(message)
        print(f"Notification sent successfully: {response}")
        return True
    except messaging.UnregisteredError:
        print(f"FCM token is no longer valid: {fcm_token[:20]}...")
        return False
    except Exception as e:
        print(f"Failed to send notification: {e}")
        return False

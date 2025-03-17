import os
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore


def get_firebase_config():
    config = {
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID"),
        "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    }
    return config


# Inicializar Firebase Auth
firebase = pyrebase.initialize_app(get_firebase_config())
auth = firebase.auth()


def format_private_key(private_key):
    """Formatea la clave privada para asegurar el formato correcto."""
    if not private_key:
        raise ValueError("FIREBASE_PRIVATE_KEY no está configurada")

    # Diagnóstico seguro (no muestra la clave completa)
    print(f"Longitud de la clave privada: {len(private_key)}")
    print(f"Primeros caracteres: {private_key[:27]}...")
    print(f"Últimos caracteres: ...{private_key[-25:]}")
    print("Contiene saltos de línea:", "\n" in private_key)

    # Asegurarse de que la clave tenga el formato correcto
    if not private_key.startswith('-----BEGIN PRIVATE KEY-----'):
        private_key = private_key.replace('\\n', '\n')
        if not private_key.startswith('-----BEGIN PRIVATE KEY-----'):
            raise ValueError(
                "El formato de FIREBASE_PRIVATE_KEY es incorrecto. Debe comenzar con '-----BEGIN PRIVATE KEY-----'"
            )

    if not private_key.strip().endswith('-----END PRIVATE KEY-----'):
        raise ValueError(
            "El formato de FIREBASE_PRIVATE_KEY es incorrecto. Debe terminar con '-----END PRIVATE KEY-----'"
        )

    return private_key


# Inicializar Firestore solo si no está ya inicializado
def initialize_firestore():
    if not firebase_admin._apps:
        try:
            private_key = format_private_key(
                os.getenv("FIREBASE_PRIVATE_KEY", ""))

            cred = credentials.Certificate({
                "type":
                "service_account",
                "project_id":
                os.getenv("FIREBASE_PROJECT_ID"),
                "private_key_id":
                os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                "private_key":
                private_key,
                "client_email":
                os.getenv("FIREBASE_CLIENT_EMAIL"),
                "client_id":
                os.getenv("FIREBASE_CLIENT_ID"),
                "auth_uri":
                "https://accounts.google.com/o/oauth2/auth",
                "token_uri":
                "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url":
                "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url":
                os.getenv("FIREBASE_CLIENT_CERT_URL")
            })

            firebase_admin.initialize_app(cred)
            print("Firebase Admin inicializado correctamente")
            return firestore.client()
        except Exception as e:
            print(f"Error al inicializar Firestore: {str(e)}")
            if "private_key" in str(e).lower():
                print(
                    "Error relacionado con la clave privada. Verifique el formato."
                )
            raise

    return firestore.client()


# Inicializar Firestore
try:
    db = initialize_firestore()
    print("Conexión a Firestore establecida")
except Exception as e:
    print(f"Error crítico al inicializar Firestore: {str(e)}")
    db = None


def login_user(email, password):
    """Inicia sesión de usuario con email y contraseña."""
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(f"Usuario autenticado correctamente: {email}")
        return user
    except Exception as e:
        error_message = str(e)
        if "INVALID_PASSWORD" in error_message:
            raise Exception("Contraseña incorrecta")
        elif "EMAIL_NOT_FOUND" in error_message:
            raise Exception("El correo electrónico no está registrado")
        else:
            print(f"Error de autenticación: {error_message}")
            raise Exception("Error al iniciar sesión")


def register_user(email, password):
    """Registra un nuevo usuario con email y contraseña."""
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print(f"Usuario registrado correctamente: {email}")
        return user
    except Exception as e:
        error_message = str(e)
        if "EMAIL_EXISTS" in error_message:
            raise Exception("El correo electrónico ya está registrado")
        elif "WEAK_PASSWORD" in error_message:
            raise Exception("La contraseña debe tener al menos 6 caracteres")
        else:
            print(f"Error de registro: {error_message}")
            raise Exception("Error al registrar usuario")


def get_user_data(user_id):
    """Obtiene los datos del usuario desde Firestore."""
    if db is None:
        print("Advertencia: Firestore no está inicializado")
        return None

    try:
        doc = db.collection('users').document(user_id).get()
        return doc.to_dict() if doc.exists else None
    except Exception as e:
        print(f"Error al obtener datos del usuario: {str(e)}")
        return None


def save_user_data(user_id, data):
    """Guarda los datos del usuario en Firestore."""
    if db is None:
        raise Exception(
            "No se puede guardar datos: Firestore no está inicializado")

    try:
        db.collection('users').document(user_id).set(data, merge=True)
        print(f"Datos guardados correctamente para el usuario: {user_id}")
    except Exception as e:
        print(f"Error al guardar datos del usuario: {str(e)}")
        raise Exception("Error al guardar los datos")

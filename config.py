import os
from typing import Dict, List, Tuple

try:
	from dotenv import load_dotenv
	load_dotenv()
except Exception:
	# dotenv is optional in production; environment may already be set
	pass


def _get_bool(value: str, default: bool = False) -> bool:
	if value is None:
		return default
	return str(value).strip().lower() in {"1", "true", "yes", "on"}


def get_flask_debug() -> bool:
	return _get_bool(os.getenv("FLASK_DEBUG"), False)


def get_email_config() -> Tuple[str, str, List[str], str, int]:
	server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
	port = int(os.getenv("SMTP_PORT", "587"))
	sender = os.getenv("EMAIL_FROM", "")
	password = os.getenv("EMAIL_PASSWORD", "")
	recipients_raw = os.getenv("EMAIL_TO", "")
	recipients = [r.strip() for r in recipients_raw.split(",") if r.strip()]
	return sender, password, recipients, server, port


def get_firebase_config() -> Dict[str, str]:
	config = {
		"apiKey": os.getenv("FIREBASE_API_KEY", ""),
		"authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", ""),
		"databaseURL": os.getenv("FIREBASE_DATABASE_URL", ""),
		"projectId": os.getenv("FIREBASE_PROJECT_ID", ""),
		"storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", ""),
		"messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", ""),
		"appId": os.getenv("FIREBASE_APP_ID", ""),
	}
	# Remove empty keys to avoid accidental leaks; Pyrebase expects keys present though.
	return {k: v for k, v in config.items() if v}

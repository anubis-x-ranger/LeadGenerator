
import re
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:

    if not url:
        return False

    try:

        parsed = urlparse(url)

        return all([
            parsed.scheme,
            parsed.netloc
        ])

    except:
        return False


def normalize_phone(phone: str) -> str:

    if not phone:
        return ""

    phone = re.sub(r"[^\d+]", "", phone)

    return phone.strip()


def clean_text(text: str) -> str:

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_domain(url: str) -> str:

    if not url:
        return ""

    parsed = urlparse(url)

    return parsed.netloc.replace("www.", "")


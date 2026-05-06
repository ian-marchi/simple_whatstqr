"""Core helpers for generating WhatsApp QR codes locally."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from urllib.parse import quote

import qrcode

_BRAZIL_COUNTRY_CODE = "55"
_MIN_LOCAL_DIGITS = 10
_MAX_E164_DIGITS = 15


def create_whatsapp_qr(
    phone_number: str,
    contact_name: str,
    include_message: bool = False,
    message_text: str | None = None,
    output_dir: str | Path = ".",
    file_name: str | None = None,
) -> Path:
    """Generate a local PNG QR code that opens a WhatsApp chat."""
    normalized_phone_number = _normalize_phone_number(phone_number)
    whatsapp_url = _build_whatsapp_url(
        normalized_phone_number,
        include_message=include_message,
        message_text=message_text,
    )
    output_path = _resolve_output_path(
        output_dir=output_dir,
        file_name=file_name,
        contact_name=contact_name,
        phone_number=normalized_phone_number,
    )
    _save_qr_image(whatsapp_url, output_path)
    return output_path.resolve()


def _normalize_phone_number(phone_number: str) -> str:
    raw_value = (phone_number or "").strip()
    digits_only = re.sub(r"\D", "", raw_value)
    has_explicit_country_code = raw_value.startswith("+") or raw_value.startswith("00")

    if not digits_only:
        raise ValueError("phone_number must contain digits.")

    if has_explicit_country_code:
        normalized = digits_only
    elif len(digits_only) in {_MIN_LOCAL_DIGITS, _MIN_LOCAL_DIGITS + 1}:
        normalized = f"{_BRAZIL_COUNTRY_CODE}{digits_only}"
    else:
        normalized = digits_only

    minimum_digits = _MIN_LOCAL_DIGITS + 1 if has_explicit_country_code else len(_BRAZIL_COUNTRY_CODE) + _MIN_LOCAL_DIGITS

    if len(normalized) < minimum_digits:
        raise ValueError("phone_number does not contain enough digits for a WhatsApp number.")

    if len(normalized) > _MAX_E164_DIGITS:
        raise ValueError("phone_number must contain at most 15 digits.")

    return normalized


def _build_whatsapp_url(
    phone_number: str,
    include_message: bool,
    message_text: str | None,
) -> str:
    base_url = f"https://wa.me/{phone_number}"

    if not include_message:
        return base_url

    if message_text is None or not message_text.strip():
        raise ValueError("message_text is required when include_message is True.")

    encoded_message = quote(message_text.strip(), safe="")
    return f"{base_url}?text={encoded_message}"


def _resolve_output_path(
    output_dir: str | Path,
    file_name: str | None,
    contact_name: str,
    phone_number: str,
) -> Path:
    target_dir = Path(output_dir).expanduser()
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / _build_file_name(contact_name, phone_number, file_name)


def _build_file_name(
    contact_name: str,
    phone_number: str,
    file_name: str | None,
) -> str:
    if file_name:
        provided_name = Path(file_name).name
        stem = _sanitize_file_stem(Path(provided_name).stem)
        return f"{stem}.png"

    contact_stem = _sanitize_file_stem(contact_name)
    return f"{contact_stem}_{phone_number}.png"


def _sanitize_file_stem(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_only.lower().strip()
    sanitized = re.sub(r"[^a-z0-9]+", "_", lowered).strip("_")
    return sanitized or "contato"


def _save_qr_image(whatsapp_url: str, output_path: Path) -> None:
    qr_code = qrcode.QRCode(box_size=10, border=4)
    qr_code.add_data(whatsapp_url)
    qr_code.make(fit=True)

    image = qr_code.make_image(fill_color="black", back_color="white")
    image.save(output_path)

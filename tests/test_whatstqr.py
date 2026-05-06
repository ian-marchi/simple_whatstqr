from __future__ import annotations

import unittest
from uuid import uuid4
from pathlib import Path

from whatstqr import create_whatsapp_qr
from whatstqr.core import _build_whatsapp_url, _normalize_phone_number

TEST_TMP_ROOT = Path.cwd() / ".tmp_tests"
TEST_TMP_ROOT.mkdir(exist_ok=True)


def _make_output_dir() -> Path:
    output_dir = TEST_TMP_ROOT / f"case_{uuid4().hex}"
    output_dir.mkdir(parents=True, exist_ok=False)
    return output_dir


class NormalizePhoneNumberTests(unittest.TestCase):
    def test_adds_brazil_country_code_for_local_number(self) -> None:
        self.assertEqual(_normalize_phone_number("(11) 99999-9999"), "5511999999999")

    def test_preserves_number_with_explicit_country_code(self) -> None:
        self.assertEqual(_normalize_phone_number("+1 (415) 555-2671"), "14155552671")

    def test_rejects_numbers_that_are_too_short(self) -> None:
        with self.assertRaises(ValueError):
            _normalize_phone_number("12345")


class BuildWhatsappUrlTests(unittest.TestCase):
    def test_url_without_message_has_no_text_parameter(self) -> None:
        self.assertEqual(
            _build_whatsapp_url("5511999999999", include_message=False, message_text=None),
            "https://wa.me/5511999999999",
        )

    def test_url_with_message_encodes_special_characters(self) -> None:
        self.assertEqual(
            _build_whatsapp_url(
                "5511999999999",
                include_message=True,
                message_text="Ola, Joao! Tudo bem? Amanha as 10h.",
            ),
            "https://wa.me/5511999999999?text=Ola%2C%20Joao%21%20Tudo%20bem%3F%20Amanha%20as%2010h.",
        )

    def test_message_is_required_when_include_message_is_true(self) -> None:
        with self.assertRaises(ValueError):
            _build_whatsapp_url("5511999999999", include_message=True, message_text="   ")


class CreateWhatsappQrTests(unittest.TestCase):
    def test_creates_png_in_requested_directory(self) -> None:
        temp_dir = _make_output_dir()
        try:
            result = create_whatsapp_qr(
                phone_number="(11) 99999-9999",
                contact_name="Joao Silva",
                output_dir=temp_dir,
            )

            expected_path = (temp_dir / "joao_silva_5511999999999.png").resolve()
            self.assertEqual(result, expected_path)
            self.assertTrue(result.exists())
            self.assertEqual(result.suffix, ".png")
        finally:
            generated_file = temp_dir / "joao_silva_5511999999999.png"
            if generated_file.exists():
                generated_file.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()

    def test_sanitizes_contact_name_for_windows_safe_file_names(self) -> None:
        temp_dir = _make_output_dir()
        try:
            result = create_whatsapp_qr(
                phone_number="(11) 99999-9999",
                contact_name="Joao:/ Silva?*",
                output_dir=temp_dir,
            )

            self.assertEqual(result.name, "joao_silva_5511999999999.png")
        finally:
            generated_file = temp_dir / "joao_silva_5511999999999.png"
            if generated_file.exists():
                generated_file.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()

    def test_respects_custom_file_name_and_forces_png_extension(self) -> None:
        temp_dir = _make_output_dir()
        try:
            result = create_whatsapp_qr(
                phone_number="(11) 99999-9999",
                contact_name="Maria",
                output_dir=temp_dir,
                file_name="Meu QR Final.jpeg",
            )

            self.assertEqual(result.name, "meu_qr_final.png")
        finally:
            generated_file = temp_dir / "meu_qr_final.png"
            if generated_file.exists():
                generated_file.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()


if __name__ == "__main__":
    unittest.main()

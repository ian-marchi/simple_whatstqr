# whatstqr

Generate WhatsApp QR Codes in one line of Python.

`whatstqr` is a small Python library that creates local PNG QR Codes pointing to a WhatsApp chat, with or without a pre-filled message.

## Why use it?

- Simple API: one function to generate a QR Code
- Works locally: saves PNG files directly on your machine
- WhatsApp-ready: builds `wa.me` links correctly
- Friendly defaults: handles Brazilian numbers without DDI by adding `55`
- Flexible output: lets you choose folder and file name

## Installation

### Local development install

From the project root:

```bash
pip install -e .
```

If you use a specific Python executable, install with the same interpreter you will use to run your script:

```powershell
& C:\path\to\python.exe -m pip install -e .
```

This is important on Windows when you have more than one Python installed.

## Quick start

```python
from whatstqr import create_whatsapp_qr

qr_path = create_whatsapp_qr(
    phone_number="(11) 99999-9999",
    contact_name="Joao Silva",
    include_message=True,
    message_text="Ola! Vim pelo QR Code.",
)

print(qr_path)
```

Example output:

```text
C:\your-folder\joao_silva_5511999999999.png
```

## Usage examples

### Create a QR Code without a message

```python
from whatstqr import create_whatsapp_qr

create_whatsapp_qr(
    phone_number="(11) 98888-7777",
    contact_name="Maria",
)
```

This generates a QR Code that opens the WhatsApp chat only.

### Create a QR Code with a pre-filled message

```python
from whatstqr import create_whatsapp_qr

create_whatsapp_qr(
    phone_number="(11) 98888-7777",
    contact_name="Maria",
    include_message=True,
    message_text="Oi Maria, tudo bem?",
)
```

This generates a QR Code that opens the chat with the message already filled in.

### Save the file in another folder

```python
from whatstqr import create_whatsapp_qr

create_whatsapp_qr(
    phone_number="(11) 98888-7777",
    contact_name="Maria",
    output_dir="output",
)
```

### Use a custom file name

```python
from whatstqr import create_whatsapp_qr

create_whatsapp_qr(
    phone_number="(11) 98888-7777",
    contact_name="Maria",
    file_name="qr_maria_final",
)
```

The library will save the file as `qr_maria_final.png`.

## API

```python
create_whatsapp_qr(
    phone_number: str,
    contact_name: str,
    include_message: bool = False,
    message_text: str | None = None,
    output_dir: str | Path = ".",
    file_name: str | None = None,
) -> Path
```

### Parameters

- `phone_number`: WhatsApp number to use in the QR Code
- `contact_name`: contact name used to build the output file name
- `include_message`: if `True`, adds a pre-filled message to the WhatsApp link
- `message_text`: message content used when `include_message=True`
- `output_dir`: folder where the PNG file will be saved
- `file_name`: custom file name for the generated PNG

### Return value

- Returns a `Path` pointing to the generated PNG file

## Phone number behavior

The library normalizes the phone number before generating the URL:

- Removes spaces, `+`, parentheses, and dashes
- If the number has 10 or 11 digits, it assumes Brazil and prefixes `55`
- If the number already has DDI, it preserves the informed value
- Rejects invalid numbers that are too short

## File naming behavior

By default, the file name is built like this:

```text
{sanitized_contact_name}_{normalized_phone}.png
```

Example:

```text
joao_silva_5511999999999.png
```

Invalid filename characters are sanitized automatically to keep the output safe on Windows.

## Running tests

From the project root:

```bash
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Project structure

```text
simple_whatstqr/
├── src/
│   └── whatstqr/
│       ├── __init__.py
│       └── core.py
├── tests/
├── LICENSE
├── pyproject.toml
└── README.md
```

## Publishing notes

Before publishing this repository on GitHub, you should:

1. Replace the placeholder GitHub URLs in `pyproject.toml`
2. Update the copyright line in `LICENSE` if needed
3. Create your GitHub repository and push the project

## License

MIT

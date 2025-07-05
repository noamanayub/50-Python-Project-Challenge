# QR Code Generator

This project generates a customized QR code for a LinkedIn profile using Python. The QR code, background, and title text colors are fully customizable, and the final image is saved in the `Output` folder as a PNG, JPG, or PDF file (based on your settings).

## Features

- Generates a QR code for a specified URL.
- Easily customize QR code color, background color, and title text color using variables.
- Adds a centered title and optional logo above the QR code.
- Saves the final image in the `Output` folder as PNG, JPG, or PDF (high quality, DPI customizable).
- Adjustable QR code size, error correction level, and output quality.

## Requirements

- Python 3.x
- [qrcode](https://pypi.org/project/qrcode/)
- [Pillow (PIL)](https://pypi.org/project/Pillow/)

## Installation

Install the required packages using pip:

```sh
pip install -r requirements.txt
```

## Customization

You can change the following variables at the top of `QRCode.py` to adjust the appearance and output:

- `QR_DATA` – The data or URL to encode
- `TITLE_TEXT` – Title text above the QR code
- `LOGO_PATH` – Path to the logo image (set to `None` for no logo)
- `QR_COLOR` – QR code color
- `BG_COLOR` – Background color
- `TEXT_COLOR` – Title text color
- `QR_SIZE` – QR code size in pixels
- `ERROR_CORRECTION` – Error correction level (`L`, `M`, `Q`, `H`)
- `SAVE_FORMAT` – Output format (`png`, `jpg`, `pdf`)
- `DPI` – Output quality (dots per inch)
- `QUALITY` – Image quality for jpg/png (1-100)

## Output

The generated QR code image will be saved in the `Output` folder. Example:

![LinkedIn QR Code](Output/linkedin_qr.png)

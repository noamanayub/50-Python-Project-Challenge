import qrcode as qr
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os

# --- Customizable Settings ---
QR_DATA = 'https://www.linkedin.com/in/noamanayub'  # Data for QR code
TITLE_TEXT = "Linkedin"                             # Title above QR code
LOGO_PATH = "linkedin_logo.png"                     # Logo file path (set to None for no logo)
QR_COLOR = "#0A66C2"                                # QR code color
BG_COLOR = "white"                                  # Background color
TEXT_COLOR = "#0A66C2"                              # Title text color
QR_SIZE = 400                                       # QR code size in pixels
ERROR_CORRECTION = qr.constants.ERROR_CORRECT_H     # L, M, Q, H
SAVE_FORMAT = "pdf"                                 # Options: "png", "jpg", "pdf"
DPI = 600                                           # Output quality (dots per inch)
QUALITY = 100                                       # Image quality for jpg/png (1-100)

def add_logo_and_title_to_img(img, title_text, logo_path, bg_color, text_color, font, qr_size):
    # Load and resize logo
    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo_height = 32
            aspect_ratio = logo.width / logo.height
            logo = logo.resize((int(logo_height * aspect_ratio), logo_height), Image.LANCZOS)
        except Exception:
            logo = None
            logo_height = 0
    else:
        logo = None
        logo_height = 0

    # Calculate title and logo placement
    title_height = 40
    if logo:
        spacing = 10
        draw = ImageDraw.Draw(img)
        text_width = draw.textlength(title_text, font=font)
        total_width = logo.width + spacing + text_width
    else:
        spacing = 0
        draw = ImageDraw.Draw(img)
        text_width = draw.textlength(title_text, font=font)
        total_width = text_width

    # Create new image with extra space for title and logo
    new_img = Image.new("RGB", (img.width, img.height + title_height), bg_color)
    draw = ImageDraw.Draw(new_img)

    # Draw logo and title centered
    y_offset = int((title_height - (logo.height if logo else 0)) // 2)
    x_start = int((img.width - total_width) // 2)

    if logo:
        new_img.paste(logo, (x_start, y_offset), mask=logo)
        draw.text((x_start + logo.width + spacing, (title_height - font.size) // 2), title_text, fill=text_color, font=font)
    else:
        draw.text(((img.width - text_width) / 2, (title_height - font.size) / 2), title_text, fill=text_color, font=font)

    # Paste the QR code below the title and logo
    new_img.paste(img, (0, title_height))
    return new_img

# --- Generate QR code ---
qr_img = qr.QRCode(
    version=1,
    error_correction=ERROR_CORRECTION,
    box_size=10,
    border=4
)
qr_img.add_data(QR_DATA)
qr_img.make(fit=True)
img = qr_img.make_image(fill_color=QR_COLOR, back_color=BG_COLOR).convert("RGB")
img = img.resize((QR_SIZE, QR_SIZE), Image.LANCZOS)

try:
    font = ImageFont.truetype("arial.ttf", 32)
except IOError:
    font = ImageFont.load_default()

final_img = add_logo_and_title_to_img(img, TITLE_TEXT, LOGO_PATH, BG_COLOR, TEXT_COLOR, font, QR_SIZE)

# Ensure the Output directory exists
output_dir = "Output"
os.makedirs(output_dir, exist_ok=True)

filename = os.path.join(output_dir, f'linkedin_qr.{SAVE_FORMAT}')
if SAVE_FORMAT == "pdf":
    final_img.save(filename, "PDF", resolution=DPI)
    print(f"QR code generated and saved as '{filename}' (DPI: {DPI})")
elif SAVE_FORMAT in ["jpg", "jpeg", "png"]:
    final_img.save(filename, dpi=(DPI, DPI), quality=QUALITY)
    print(f"QR code generated and saved as '{filename}' (DPI: {DPI}, Quality: {QUALITY})")
else:
    final_img.save(filename)
    print(f"QR code generated and saved as '{filename}'")
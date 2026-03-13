from PIL import Image
from pdf2image import convert_from_path
import os

input_folder = "PNG"

# Ensure the folder exists
if not os.path.isdir(input_folder):
    raise FileNotFoundError(f"Folder '{input_folder}' not found.")

# --- Convert all PNGs to PDFs ---
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith(".png"):
        png_path = os.path.join(input_folder, file_name)
        pdf_path = os.path.join(input_folder, os.path.splitext(file_name)[0] + ".pdf")

        if not os.path.exists(pdf_path):
            with Image.open(png_path) as img:
                img.convert("RGB").save(pdf_path)
            print(f"Converted PNG → PDF: {file_name} → {os.path.basename(pdf_path)}")

# --- Convert all PDFs to PNGs (if PNGs missing) ---
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith(".pdf"):
        pdf_path = os.path.join(input_folder, file_name)
        png_path = os.path.join(input_folder, os.path.splitext(file_name)[0] + ".png")

        if not os.path.exists(png_path):
            # Convert first page of the PDF to PNG (extend if multi-page needed)
            images = convert_from_path(pdf_path)
            if images:
                images[0].save(png_path, "PNG")
                print(f"Converted PDF → PNG: {file_name} → {os.path.basename(png_path)}")

print("Folder synchronized: all images now exist as both PNG and PDF.")


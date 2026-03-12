import fitz
import os
from PIL import Image
from io import BytesIO


INPUT_PDF = "Scientific_Reports.pdf"
OUTPUT_DIR = "figures"


def ensure_output_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def extract_images_from_page(page, page_index, output_dir):

    image_list = page.get_images(full=True)

    saved_files = []

    if not image_list:
        return saved_files

    for img_index, img in enumerate(image_list):

        xref = img[0]

        base_image = page.parent.extract_image(xref)

        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        image = Image.open(BytesIO(image_bytes))

        filename = f"page{page_index+1:03d}_fig{img_index+1}.{image_ext}"

        filepath = os.path.join(output_dir, filename)

        image.save(filepath)

        saved_files.append(filepath)

    return saved_files


def extract_all_figures(pdf_path, output_dir):

    doc = fitz.open(pdf_path)

    extracted_files = []

    for page_index in range(len(doc)):

        page = doc.load_page(page_index)

        files = extract_images_from_page(page, page_index, output_dir)

        extracted_files.extend(files)

    return extracted_files


def main():

    ensure_output_dir(OUTPUT_DIR)

    files = extract_all_figures(INPUT_PDF, OUTPUT_DIR)

    print("\nExtraction complete\n")

    for f in files:
        print(f)

    print(f"\nTotal figures extracted: {len(files)}")


if __name__ == "__main__":
    main()

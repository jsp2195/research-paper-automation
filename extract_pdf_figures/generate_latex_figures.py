import os
import re

# -----------------------------
# Configuration
# -----------------------------

FIGURE_FOLDER = "figures"
OUTPUT_FILE = "output/figures.tex"

IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".pdf"]

FIGURE_WIDTH = "0.7\\textwidth"


# -----------------------------
# Utility Functions
# -----------------------------

def ensure_output_dir(path):
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)


def is_image_file(filename):
    return any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)


def filename_to_caption(filename):
    """
    Convert file names into readable captions.

    Example:
        stress_curve.png -> Stress curve
        yield_surface_plot.png -> Yield surface plot
    """

    name = os.path.splitext(filename)[0]

    name = name.replace("_", " ")
    name = name.replace("-", " ")

    name = re.sub(r"\s+", " ", name)

    return name.capitalize()


def generate_latex_block(filepath, caption):

    block = f"""
\\begin{{figure}}[htbp]
\\centering
\\includegraphics[width={FIGURE_WIDTH}]{{{filepath}}}
\\caption{{{caption}}}
\\label{{fig:{caption.lower().replace(" ", "_")}}}
\\end{{figure}}
"""

    return block


# -----------------------------
# Main Logic
# -----------------------------

def generate_latex_from_folder():

    if not os.path.exists(FIGURE_FOLDER):
        raise FileNotFoundError(f"Folder not found: {FIGURE_FOLDER}")

    files = sorted(os.listdir(FIGURE_FOLDER))

    latex_blocks = []

    for file in files:

        if not is_image_file(file):
            continue

        filepath = os.path.join(FIGURE_FOLDER, file)

        caption = filename_to_caption(file)

        block = generate_latex_block(filepath, caption)

        latex_blocks.append(block)

    return latex_blocks


# -----------------------------
# Save Output
# -----------------------------

def save_latex_file(blocks):

    ensure_output_dir(OUTPUT_FILE)

    with open(OUTPUT_FILE, "w") as f:

        f.write("% Auto-generated LaTeX figure blocks\n\n")

        for block in blocks:
            f.write(block)
            f.write("\n")


# -----------------------------
# Entry Point
# -----------------------------

def main():

    blocks = generate_latex_from_folder()

    save_latex_file(blocks)

    print("LaTeX figure blocks generated")
    print(f"Total figures: {len(blocks)}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

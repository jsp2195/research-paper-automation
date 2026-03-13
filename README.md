# Research Paper Automation

Research Paper Automation is a lightweight Python repository of utility scripts for repetitive academic PDF workflows: extracting embedded figures, generating slide decks from figures and nearby captions, exporting PDF annotations/comments, verifying annotation exports, and synchronizing PNG/PDF figure formats. It is a practical research workflow scaffold (not a packaged library) intended to speed up day-to-day paper reading, presentation prep, and manuscript drafting.

## Main Problem This Repository Solves

Researchers often spend significant time on manual formatting and extraction tasks around papers (copying figures, collecting comments, building slides, and generating LaTeX figure blocks). This repository consolidates those chores into focused scripts so the workflow is faster and more reproducible.

## Workflow at a Glance

1. **Figure extraction** from a PDF using PyMuPDF.
2. **Slide generation** by pairing extracted figures with nearby caption-like text.
3. **Annotation export** (JSON/CSV/readable TXT) from commented PDFs.
4. **Annotation verification** by comparing exported records against the source PDF.
5. **Image format synchronization** between PNG and PDF files for publication workflows.

## Repository Structure

```text
research-paper-automation/
├── README.md
├── .gitignore
└── scripts/
    ├── pdf_figures/
    │   ├── extract_figures.py
    │   ├── generate_slides.py
    │   └── generate_latex_figures.py
    ├── pdf_annotations/
    │   ├── pdf_comments.py
    │   └── pdf_comment_verify.py
    └── image_format_sync/
        └── png2pdf2png.py
```

## Setup / Installation

### 1) Clone

```bash
git clone https://github.com/<your-username>/research-paper-automation.git
cd research-paper-automation
```

### 2) Install dependencies

Install the packages used by the scripts (no `requirements.txt` is currently included):

```bash
pip install pymupdf pillow pdf2image python-pptx pandas
```

> Note: `pdf2image` also requires Poppler on your system.

## Data / Inputs

The scripts currently use hard-coded input names/paths inside each file (for example `Scientific_Reports.pdf`, `PNG/`, and output filenames). Place your input files/folders in the repository root unless you update those constants in the script configurations.

Typical expected inputs:
- `Scientific_Reports.pdf` for figure extraction, slide generation, and annotation extraction.
- `PNG/` directory for PNG↔PDF synchronization.

## Training / Usage

This repository does **not** contain model training code. It is a document-processing utilities project.

Run scripts from the repository root:

### Extract figures from PDF

```bash
python scripts/pdf_figures/extract_figures.py
```

### Generate slides from detected figures + captions

```bash
python scripts/pdf_figures/generate_slides.py
```

### Generate LaTeX figure blocks from a figure directory

```bash
python scripts/pdf_figures/generate_latex_figures.py
```

### Extract PDF comments/annotations to JSON, CSV, and text

```bash
python scripts/pdf_annotations/pdf_comments.py
```

### Verify extracted annotations against source PDF

```bash
python scripts/pdf_annotations/pdf_comment_verify.py
```

### Synchronize PNG and PDF files in a folder

```bash
python scripts/image_format_sync/png2pdf2png.py
```

## Outputs / Results

Depending on script execution, outputs include:
- Extracted figure images (for example, in `figures/` or `extracted_figures/`).
- Slide deck: `paper_presentation.pptx`.
- LaTeX snippet file: `output/figures.tex`.
- Annotation exports: `pdf_annotations.json`, `pdf_annotations.csv`, `pdf_annotations_readable.txt`.

## Notes / Limitations

- Scripts are configuration-by-edit (constants in each script), not CLI-argument driven.
- Paths are relative to the current working directory when running scripts.
- This is an MVP-style toolkit of standalone scripts rather than a packaged framework.
- Some files (notably annotation verification) include exploratory or iterative script content; behavior is preserved as-is.
- No automated test suite is currently included.

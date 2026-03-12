# Research Paper Automation Toolkit

A lightweight Python toolkit that automates common academic workflows for reading, presenting, and writing research papers.

This repository contains utilities for extracting figures from PDFs, converting papers into presentation slides, extracting comments and highlights, generating LaTeX figure blocks, and synchronizing image formats commonly required by journals.

The goal is to eliminate repetitive tasks researchers perform when reading papers, preparing presentations, and writing manuscripts.

---

# Features

## 1. `extract_figures.py`

Extract all embedded images from a research paper PDF.

The script scans every page of a PDF and saves all detected images into a `figures/` directory.

Output example:

```
figures/
  page001_fig1.png
  page001_fig2.png
  page002_fig1.png
```

This script uses PyMuPDF to identify embedded image objects and saves them with page-based naming.

Typical uses:

* collecting figures from papers
* extracting plots for presentations
* building figure datasets

Source: fileciteturn1file2

---

## 2. `generate_slides.py`

Automatically convert a research paper into a PowerPoint presentation.

Pipeline:

```
PDF
  → detect figures
  → detect nearby captions
  → generate slides
```

Each slide contains:

* figure image
* detected caption

Output:

```
paper_presentation.pptx
```

The script uses spatial proximity between images and nearby text blocks to infer figure captions.

Typical uses:

* paper presentations
* journal clubs
* lab meetings

Source: fileciteturn1file4

---

## 3. `pdf_comments.py`

Extract annotations, highlights, and comments from an annotated PDF.

The script exports annotations in multiple formats:

```
pdf_annotations.json
pdf_annotations.csv
pdf_annotations_readable.txt
```

Extracted information includes:

* page number
* annotation type
* highlighted text
* comment text
* author
* timestamp

This is useful for exporting literature notes or extracting collaborator feedback.

Source: fileciteturn1file1

---

## 4. `generate_latex_figures.py`

Generate LaTeX figure blocks automatically from a folder of images.

Example input:

```
figures/
  stress_curve.png
  yield_surface.png
```

Generated LaTeX:

```
\begin{figure}
\centering
\includegraphics[width=0.7\textwidth]{figures/stress_curve.png}
\caption{Stress curve}
\label{fig:stress_curve}
\end{figure}
```

File names are automatically converted into readable captions.

Typical uses:

* writing papers
* thesis preparation
* rapid figure insertion

Source: fileciteturn1file3

---

## 5. `png2pdf2png.py`

Synchronize image formats within a folder by ensuring each image exists in both PNG and PDF format.

Behavior:

* converts PNG → PDF if PDF does not exist
* converts PDF → PNG if PNG does not exist

This is useful when journals require PDF figures while LaTeX workflows use PNG.

Source: fileciteturn1file0

---

# Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/research-paper-automation.git
cd research-paper-automation
```

Install dependencies:

```
pip install -r requirements.txt
```

Required libraries:

* pymupdf
* pillow
* pdf2image
* python-pptx
* pandas

---

# Example Workflow

Typical workflow when analyzing a new research paper:

```
1. Extract figures

python extract_figures.py

2. Generate presentation slides

python generate_slides.py

3. Export annotations and highlights

python pdf_comments.py

4. Generate LaTeX figure blocks

python generate_latex_figures.py
```

---

# Repository Structure

```
research-paper-automation/

extract_figures.py
generate_slides.py
pdf_comments.py
generate_latex_figures.py
png2pdf2png.py

examples/

example_paper.pdf

figures/
output/
```

---

# Use Cases

This toolkit is designed for:

* PhD students
* postdoctoral researchers
* academic labs
* research groups

Typical uses include:

* literature reviews
* paper presentations
* manuscript preparation
* extracting datasets of figures

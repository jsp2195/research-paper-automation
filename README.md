# Research Paper Automation Toolkit

A lightweight Python toolkit that automates common academic workflows for reading, presenting, and writing research papers.

This repository contains utilities for extracting figures from PDFs, converting papers into presentation slides, extracting comments and highlights, generating LaTeX figure blocks, and synchronizing image formats commonly required by journals.

The goal is to eliminate repetitive tasks that researchers perform when reading papers, preparing presentations, and writing manuscripts.

---

# Features

## 1. Extract Figures From PDFs

Automatically detect and extract embedded images from academic papers.

Output:

```
figures/
  page001_fig1.png
  page001_fig2.png
  page002_fig1.png
```

Useful for:

* literature reviews
* collecting datasets of figures
* preparing presentation slides

---

## 2. Generate Slides From Papers

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
* caption

Output:

```
paper_presentation.pptx
```

Useful for:

* paper presentations
* journal clubs
* lab meetings

---

## 3. Extract PDF Annotations

Extract comments, highlights, and notes from annotated papers.

Output formats:

```
pdf_annotations.json
pdf_annotations.csv
pdf_annotations_readable.txt
```

Captured fields:

* page
* annotation type
* highlighted text
* comment
* author
* date

Useful for:

* literature notes
* supervisor feedback
* collaborative paper reviews

---

## 4. Generate LaTeX Figure Blocks

Automatically generate LaTeX figure environments from a folder of images.

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
\end{figure}
```

Useful for:

* writing papers
* thesis preparation
* rapid figure insertion

---

## 5. PNG ↔ PDF Synchronization

Automatically ensure that images exist in both PNG and PDF format.

Useful for:

* journal submission requirements
* LaTeX workflows

---

# Installation

Clone the repository:

```
git clone https://github.com/yourusername/research-paper-automation.git
cd research-paper-automation
```

Install dependencies:

```
pip install -r requirements.txt
```

Dependencies:

* pymupdf
* pillow
* pdf2image
* python-pptx
* pandas

---

# Repository Structure

```
research-paper-automation/

paper_tools/

    pdf/
        extract_figures.py
        extract_annotations.py

    slides/
        pdf_to_slides.py

    latex/
        latex_from_figures.py

    images/
        sync_png_pdf.py

examples/

    example_paper.pdf

outputs/

    extracted_figures/
    paper_presentation.pptx
    annotations.json
    figures.tex
```

---

# Example Workflows

## Extract Figures

```
python paper_tools/pdf/extract_figures.py
```

---

## Generate Slides

```
python paper_tools/slides/pdf_to_slides.py
```

---

## Extract PDF Annotations

```
python paper_tools/pdf/extract_annotations.py
```

---

## Generate LaTeX Figures

```
python paper_tools/latex/latex_from_figures.py
```

---

# Example Pipeline

Typical workflow when reading a new paper:

```
1. Extract figures from the PDF
2. Generate slides for a presentation
3. Export annotations and comments
4. Insert selected figures into LaTeX
```

---

# Use Cases

This toolkit is designed for:

* PhD students
* researchers
* postdoctoral researchers
* research labs

Typical use cases include:

* literature reviews
* paper presentations
* manuscript preparation
* extracting figures for datasets

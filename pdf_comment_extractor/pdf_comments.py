import fitz
import json
import pandas as pd
import re

INPUT_PDF = "Scientific_Reports.pdf"

OUTPUT_JSON = "pdf_annotations.json"
OUTPUT_CSV = "pdf_annotations.csv"
OUTPUT_TXT = "pdf_annotations_readable.txt"


def normalize(text):
    if not text:
        return ""
    return " ".join(text.replace("\n", " ").split())


def sentence_split(paragraph):
    return re.split(r'(?<=[.!?])\s+', paragraph)


def extract_page_structure(page):

    blocks = page.get_text("blocks")

    paragraphs = []

    for b in blocks:
        text = normalize(b[4])
        rect = fitz.Rect(b[:4])

        if text:
            paragraphs.append({
                "text": text,
                "rect": rect,
                "sentences": sentence_split(text),
                "x0": b[0],
                "x1": b[2]
            })

    return paragraphs


def find_paragraph(paragraphs, rect):

    for p in paragraphs:
        if rect.intersects(p["rect"]):
            return p

    return None


def find_sentence(paragraph, highlight):

    text = paragraph["text"]
    sentences = paragraph["sentences"]

    running_offset = 0

    for i, s in enumerate(sentences):

        start = text.lower().find(s.lower(), running_offset)

        if start == -1:
            continue

        end = start + len(s)

        if highlight and highlight.lower() in s.lower():
            return s, i, start, end

        running_offset = end

    if highlight:
        start = text.lower().find(highlight.lower())
        if start != -1:
            end = start + len(highlight)
            return "", -1, start, end

    return "", -1, -1, -1

def extract_section(page):

    blocks = page.get_text("blocks")

    for b in blocks[:5]:

        txt = normalize(b[4])

        if txt and len(txt.split()) < 10:
            return txt

    return ""


def extract_highlight(page, annot):

    verts = annot.vertices
    if not verts:
        return "", fitz.Rect(0, 0, 0, 0), []

    rects = []
    words = page.get_text("words")

    selected_words = []
    seen = set()

    for i in range(0, len(verts), 4):

        quad = verts[i:i+4]

        xs = []
        ys = []

        for p in quad:

            if isinstance(p, tuple):
                x, y = p
            else:
                x, y = p.x, p.y

            xs.append(x)
            ys.append(y)

        rect = fitz.Rect(min(xs), min(ys), max(xs), max(ys))
        rects.append(rect)

        for w in words:

            wrect = fitz.Rect(w[:4])

            if rect.intersects(wrect):

                key = (round(wrect.y0, 3), round(wrect.x0, 3), w[4])

                if key not in seen:
                    selected_words.append(key)
                    seen.add(key)

    selected_words.sort()

    highlighted = " ".join([w[2] for w in selected_words])

    union_rect = rects[0]
    for r in rects[1:]:
        union_rect |= r

    boxes = [[r.x0, r.y0, r.x1, r.y1] for r in rects]

    return normalize(highlighted), union_rect, boxes


def extract_annotations(pdf):

    doc = fitz.open(pdf)

    annotations = []

    for page_index in range(len(doc)):

        page = doc[page_index]

        section = extract_section(page)

        paragraphs = extract_page_structure(page)

        annot = page.first_annot

        while annot:

            info = annot.info

            annot_type = annot.type[1]

            comment = normalize(info.get("content"))

            author = normalize(info.get("title"))

            date = info.get("creationDate")

            parent = None

            if annot.irt_xref:
                parent = annot.irt_xref

            highlighted = ""
            sentence = ""
            paragraph = ""
            sentence_index = -1
            sentence_char_start = -1
            sentence_char_end = -1
            paragraph_char_start = -1
            paragraph_char_end = -1
            bbox = []

            if annot_type == "Highlight":

                highlighted, rect, bbox = extract_highlight(page, annot)

                p = find_paragraph(paragraphs, rect)

                if p:

                    paragraph = p["text"]
                    paragraph_char_start = p["x0"]
                    paragraph_char_end = p["x1"]

                    sentence, sentence_index, s_start, s_end = find_sentence(p, highlighted)
                    sentence_char_start = s_start
                    sentence_char_end = s_end
                    
            entry = {

                "page": page_index + 1,
                "section": section,

                "type": annot_type,
                "author": author,
                "date": date,

                "highlighted_text": highlighted,
                "sentence_text": sentence,
                "paragraph_text": paragraph,

                "paragraph_char_start": paragraph_char_start,
                "paragraph_char_end": paragraph_char_end,

                "sentence_index": sentence_index,
                "sentence_char_start": sentence_char_start,
                "sentence_char_end": sentence_char_end,

                "comment": comment,

                "thread_parent": parent,

                "bbox": bbox
            }

            annotations.append(entry)

            annot = annot.next

    return annotations


def save_outputs(data):

    with open(OUTPUT_JSON, "w") as f:
        json.dump(data, f, indent=2)

    pd.DataFrame(data).to_csv(OUTPUT_CSV, index=False)

    with open(OUTPUT_TXT, "w") as f:

        for i, a in enumerate(data):

            f.write(f"\nCOMMENT {i+1}\n")

            f.write(f"Page: {a['page']}\n")
            f.write(f"Section: {a['section']}\n")

            f.write(f"Author: {a['author']}\n")
            f.write(f"Date: {a['date']}\n")

            f.write("\nHighlighted:\n")
            f.write(a["highlighted_text"] + "\n")

            f.write("\nSentence:\n")
            f.write(a["sentence_text"] + "\n")

            f.write("\nParagraph:\n")
            f.write(a["paragraph_text"] + "\n")

            f.write("\nSentence Index:\n")
            f.write(str(a["sentence_index"]) + "\n")

            f.write("\nComment:\n")
            f.write(a["comment"] + "\n")

            f.write("\nThread Parent:\n")
            f.write(str(a["thread_parent"]) + "\n")

            f.write("\nBounding Boxes:\n")
            f.write(str(a["bbox"]) + "\n")

            f.write("\n" + "-"*80 + "\n")


def main():

    annotations = extract_annotations(INPUT_PDF)

    save_outputs(annotations)

    print("Annotations extracted:", len(annotations))


if __name__ == "__main__":
    main()

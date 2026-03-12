import fitz
import json
import pandas as pd

INPUT_PDF = "Scientific_Reports.pdf"

OUTPUT_JSON = "pdf_annotations.json"
OUTPUT_CSV = "pdf_annotations.csv"
OUTPUT_TXT = "pdf_annotations_readable.txt"


def words_in_rect(page, rect):

    words = page.get_text("words", sort=True)

    results = []

    for w in words:
        word_rect = fitz.Rect(w[:4])
        if rect.intersects(word_rect):
            results.append(w)

    return " ".join(w[4] for w in results)
    
def extract_annotations(pdf):

    doc = fitz.open(pdf)

    annotations = []

    for page_index in range(len(doc)):

        page = doc[page_index]

        annot = page.first_annot

        while annot:

            info = annot.info

            comment = info.get("content", "")
            author = info.get("title", "")
            date = info.get("creationDate", "")

            annot_type = annot.type[1]

            highlighted_text = ""

            if annot_type == "Highlight":

                verts = annot.vertices
                text_parts = []

                if verts:

                    for v in verts:

                        # v may look like ((x1,y1),(x2,y2),(x3,y3),(x4,y4))
                        if isinstance(v, tuple) and len(v) == 4:

                            xs = [p[0] for p in v]
                            ys = [p[1] for p in v]

                            rect = fitz.Rect(
                                min(xs),
                                min(ys),
                                max(xs),
                                max(ys)
                            )

                            text_parts.append(words_in_rect(page, rect))

                highlighted_text = " ".join(text_parts)

            entry = {

                "page": page_index + 1,
                "type": annot_type,
                "author": author,
                "date": date,
                "highlighted_text": highlighted_text,
                "comment": comment
            }

            annotations.append(entry)

            annot = annot.next

    return annotations


def save_outputs(data):

    with open(OUTPUT_JSON, "w", encoding="utf8") as f:
        json.dump(data, f, indent=2)

    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_CSV, index=False)

    with open(OUTPUT_TXT, "w", encoding="utf8") as f:

        for i, a in enumerate(data):

            f.write(f"COMMENT {i+1}\n")
            f.write(f"Page: {a['page']}\n")
            f.write(f"Type: {a['type']}\n")
            f.write(f"Author: {a['author']}\n")
            f.write(f"Date: {a['date']}\n\n")

            f.write("Highlighted Text:\n")
            f.write(a["highlighted_text"] + "\n\n")

            f.write("Comment:\n")
            f.write(a["comment"] + "\n")

            f.write("\n" + "-"*80 + "\n\n")


def main():

    annotations = extract_annotations(INPUT_PDF)

    save_outputs(annotations)

    print("Annotations extracted:", len(annotations))


if __name__ == "__main__":
    main()

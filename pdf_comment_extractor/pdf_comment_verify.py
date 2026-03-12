import fitz

pdf_path = "Scientific_Reports.pdf"

doc = fitz.open(pdf_path)

for page_index, page in enumerate(doc):

    annot = page.first_annot

    while annot:

        print("\n==============================")
        print("Page:", page_index + 1)
        print("Type:", annot.type)

        print("\nINFO DICT")
        for k, v in annot.info.items():
            print(k, ":", v)

        print("\nTEXT METHOD")
        try:
            print(annot.get_text())
        except:
            pass

        print("\nPOPUP")
        try:
            popup = annot.popup
            if popup:
                print("popup rect:", popup.rect)
        except:
            pass

        print("\nRAW OBJECT")
        try:
            print(doc.xref_object(annot.xref))
        except:
            pass

        annot = annot.next
        
import fitz
import json

pdf_path = "Scientific_Reports.pdf"

doc = fitz.open(pdf_path)

annotations = []

for page_num, page in enumerate(doc, start=1):

    annot = page.first_annot

    while annot:

        info = annot.info

        comment = ""

        # primary comment
        if info.get("content"):
            comment = info["content"]

        # fallback: text body
        if not comment:
            try:
                comment = annot.get_text()
            except:
                pass

        # fallback: subject field
        if not comment and info.get("subject"):
            comment = info["subject"]

        annotations.append({
            "page": page_num,
            "type": annot.type[1],
            "author": info.get("title"),
            "comment": comment,
            "date": info.get("creationDate")
        })

        annot = annot.next

with open("annotations_full.json", "w") as f:
    json.dump(annotations, f, indent=2)

print("Total annotations extracted:", len(annotations))

import fitz
import pandas as pd

pdf = fitz.open("Scientific_Reports.pdf")
csv = pd.read_csv("pdf_annotations.csv")

pdf_comments = []

for page in pdf:
    annot = page.first_annot
    while annot:
        txt = annot.info.get("content", "")
        if txt:
            pdf_comments.append(txt.strip())
        annot = annot.next

missing = []

for c in pdf_comments:
    if not csv["comment"].str.contains(c[:20], regex=False).any():
        missing.append(c)

print("Missing comments:", len(missing))

for m in missing:
    print("\nMISSING:")
    print(m)
    
    
import fitz
import json
import csv
from pathlib import Path

PDF_PATH = "Scientific_Reports.pdf"
EXTRACTED_JSON = "pdf_annotations.json"
EXTRACTED_CSV = "pdf_annotations.csv"


def normalize(text):
    if text is None:
        return ""
    return " ".join(text.strip().split()).lower()


def load_pdf_annotations(pdf_path):
    doc = fitz.open(pdf_path)
    records = []

    for page_number, page in enumerate(doc, start=1):
        annot = page.first_annot
        while annot:
            info = annot.info
            records.append({
                "page": page_number,
                "type": annot.type[1],
                "author": normalize(info.get("title")),
                "comment": normalize(info.get("content")),
            })
            annot = annot.next

    return records


def load_json_annotations(path):
    with open(path) as f:
        data = json.load(f)

    records = []
    for item in data:
        records.append({
            "page": item.get("page"),
            "type": item.get("type"),
            "author": normalize(item.get("author")),
            "comment": normalize(item.get("comment")),
        })
    return records


def load_csv_annotations(path):
    records = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "page": int(row["page"]),
                "type": row["type"],
                "author": normalize(row["author"]),
                "comment": normalize(row["comment"]),
            })
    return records


def verify(pdf_records, extracted_records):

    unmatched = []
    matched = 0

    for rec in extracted_records:
        found = False
        for pdf_rec in pdf_records:
            if (
                rec["page"] == pdf_rec["page"]
                and rec["author"] == pdf_rec["author"]
                and normalize(rec["comment"]) == normalize(pdf_rec["comment"])
            ):
                found = True
                break

        if found:
            matched += 1
        else:
            unmatched.append(rec)

    print("\nVerification Results")
    print("--------------------")
    print("PDF annotations:", len(pdf_records))
    print("Extracted annotations:", len(extracted_records))
    print("Matched:", matched)
    print("Unmatched:", len(unmatched))

    if unmatched:
        print("\nUnmatched entries:")
        for u in unmatched:
            print(u)


def main():

    pdf_records = load_pdf_annotations(PDF_PATH)

    if Path(EXTRACTED_JSON).exists():
        extracted_records = load_json_annotations(EXTRACTED_JSON)
    else:
        extracted_records = load_csv_annotations(EXTRACTED_CSV)

    verify(pdf_records, extracted_records)


if __name__ == "__main__":
    main()

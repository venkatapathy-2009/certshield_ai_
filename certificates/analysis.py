import hashlib
from pathlib import Path
from PIL import Image
from pypdf import PdfReader

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

def analyze_document(uploaded_file):
    """
    MVP triage only. No heuristic can establish authenticity.
    OCR works on images if the Tesseract executable is installed.
    PDF text extraction works for text-based PDFs; scanned PDFs need OCR integration.
    """
    name = Path(uploaded_file.name).name
    ext = Path(name).suffix.lower()
    file_hash = hashlib.sha256()
    uploaded_file.seek(0)
    for chunk in uploaded_file.chunks():
        file_hash.update(chunk)
    uploaded_file.seek(0)
    digest = file_hash.hexdigest()

    checks = []
    extracted = ""
    risk = 50
    checks.append({"label": "File type", "result": f"Accepted file extension: {ext}", "ok": True})
    checks.append({"label": "SHA-256 document fingerprint", "result": digest, "ok": True})

    try:
        if ext in IMAGE_EXTS:
            try:
                with Image.open(uploaded_file) as im:
                    checks.append({"label": "Image metadata", "result": f"Format: {im.format}; dimensions: {im.width} × {im.height}", "ok": True})
                    if im.width < 300 or im.height < 300:
                        risk += 10
                        checks.append({"label": "Image resolution", "result": "Low resolution may make review difficult.", "ok": False})
                    else:
                        checks.append({"label": "Image resolution", "result": "Resolution is sufficient for a basic review.", "ok": True})
            except Exception:
                risk += 15
                checks.append({"label": "Image integrity", "result": "Could not read image metadata.", "ok": False})
            uploaded_file.seek(0)
            try:
                import pytesseract
                with Image.open(uploaded_file) as im:
                    extracted = pytesseract.image_to_string(im)[:20000]
                checks.append({"label": "OCR text extraction", "result": f"Extracted approximately {len(extracted.strip())} characters.", "ok": bool(extracted.strip())})
            except Exception:
                checks.append({"label": "OCR text extraction", "result": "Unavailable. Install Tesseract OCR separately and ensure it is on PATH.", "ok": False})
        elif ext == ".pdf":
            try:
                uploaded_file.seek(0)
                reader = PdfReader(uploaded_file)
                pages = []
                for page in reader.pages[:20]:
                    pages.append(page.extract_text() or "")
                extracted = "\n".join(pages)[:20000]
                checks.append({"label": "PDF text extraction", "result": f"Read {len(reader.pages)} page(s); extracted {len(extracted.strip())} characters. Scanned PDFs may need OCR.", "ok": bool(extracted.strip())})
            except Exception:
                risk += 10
                checks.append({"label": "PDF parsing", "result": "Could not parse PDF text; manual review recommended.", "ok": False})
        else:
            checks.append({"label": "Text extraction", "result": "This file type was accepted, but automated text extraction is not enabled for it yet.", "ok": False})

    except Exception:
        risk += 10
        checks.append({"label": "Basic analysis", "result": "Some checks could not be completed.", "ok": False})

    checks.extend([
        {"label": "Image forensics / template matching", "result": "Not implemented in this MVP; no claim of tampering detection is made.", "ok": False},
        {"label": "QR / serial verification", "result": "Not connected to an official issuer endpoint.", "ok": False},
        {"label": "Official record matching", "result": "Not performed. Only the issuing authority can confirm its record.", "ok": False},
    ])
    risk = max(0, min(100, risk))
    summary = (
        "Preliminary triage only. This system checked basic file properties and attempted text extraction. "
        "It did not confirm authenticity or query an official government database. Please verify the "
        "certificate number through a trusted official channel and request human review if needed."
    )
    return {"status": "review", "risk_score": risk, "sha256": digest,
            "extracted_text": extracted, "summary": summary, "checks": checks}

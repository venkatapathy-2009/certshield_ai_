# CertShield / `ai_dect_cert`

Django hackathon MVP based on the CertShield concept: account login, upload workflow, per-user history, SHA-256 file fingerprint, basic metadata checks, optional image OCR, PDF text extraction, and a reviewer/admin area.

## Setup on Windows / VS Code

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/

If PowerShell blocks activation, use:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

## Login and admin
- Register: `/accounts/register/`
- Login: `/accounts/login/`
- Dashboard: `/dashboard/`
- History: `/history/`
- Admin/reviewer interface: `/admin/` (create a superuser first)

## Supported uploads
PDF, JPG/JPEG, PNG, WEBP, DOC/DOCX, PPT/PPTX, TXT; max 10 MB. Only image OCR and basic PDF text extraction are wired in. For image OCR, install the Tesseract OCR application separately and ensure it is on PATH. OCR failure is handled gracefully.

## Prototype limitations
The displayed risk score is a triage heuristic, not a probability that a document is fake. This MVP does not implement image forensics, template matching, QR/serial verification, cryptographic PDF signature validation, or government API access. It always leaves new uploads in manual review. Admin users can record review notes and official-verification status; this is not automatically inferred by AI.

For production: use HTTPS, a secret from environment variables, `DEBUG=False`, secure private file storage, malware scanning, rate limiting, retention/deletion controls, audit logging, and authorized issuer integrations. Follow applicable Indian data-protection requirements. Avoid collecting Aadhaar/PAN in an early MVP.

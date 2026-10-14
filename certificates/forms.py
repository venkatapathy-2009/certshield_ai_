from pathlib import Path
from django import forms
from .models import CertificateDocument

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".webp", ".doc", ".docx", ".ppt", ".pptx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024

class CertificateUploadForm(forms.ModelForm):
    class Meta:
        model = CertificateDocument
        fields = ["title", "document_type", "file"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Semester 1 marksheet"}),
            "document_type": forms.Select(),
            "file": forms.ClearableFileInput(attrs={"accept": ".pdf,.jpg,.jpeg,.png,.webp,.doc,.docx,.ppt,.pptx,.txt"}),
        }

    def clean_file(self):
        f = self.cleaned_data["file"]
        ext = Path(f.name).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise forms.ValidationError("Unsupported file type. Choose PDF, an image, DOC/DOCX, PPT/PPTX, or TXT.")
        if f.size > MAX_FILE_SIZE:
            raise forms.ValidationError("File is too large. Maximum size is 10 MB.")
        return f

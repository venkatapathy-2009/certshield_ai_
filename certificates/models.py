from django.conf import settings
from django.db import models

class CertificateDocument(models.Model):
    DOCUMENT_TYPES = [
        ("birth", "Birth certificate"), ("marksheet", "Marksheet"),
        ("community", "Community / caste certificate"), ("income", "Income certificate"),
        ("residence", "Residence / domicile certificate"), ("identity", "Identity document"),
        ("property", "Property / land document"), ("permit", "Government letter / permit"),
        ("other", "Other document"),
    ]
    STATUS_CHOICES = [
        ("review", "Suspicious — manual review needed"),
        ("likely_genuine", "Likely genuine — issuer verified"),
        ("likely_forged", "Likely forged — reviewer decision"),
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="certificate_documents")
    title = models.CharField(max_length=160)
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to="certificate_uploads/%Y/%m/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="review")
    risk_score = models.PositiveSmallIntegerField(default=50)
    sha256 = models.CharField(max_length=64, blank=True)
    extracted_text = models.TextField(blank=True)
    analysis_summary = models.TextField(blank=True)
    checks = models.JSONField(default=list, blank=True)
    official_verified = models.BooleanField(default=False)
    reviewer_note = models.TextField(blank=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.title} ({self.owner})"

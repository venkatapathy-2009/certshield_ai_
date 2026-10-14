from django.contrib import admin
from .models import CertificateDocument

@admin.register(CertificateDocument)
class CertificateDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "document_type", "status", "risk_score", "official_verified", "uploaded_at")
    list_filter = ("document_type", "status", "official_verified", "uploaded_at")
    search_fields = ("title", "owner__username", "sha256")
    readonly_fields = ("uploaded_at", "sha256", "extracted_text", "checks")
    fieldsets = (
        ("Submission", {"fields": ("owner", "title", "document_type", "file", "uploaded_at")}),
        ("Automated triage", {"fields": ("status", "risk_score", "sha256", "extracted_text", "checks", "analysis_summary")}),
        ("Authorized reviewer", {"fields": ("official_verified", "reviewer_note")}),
    )

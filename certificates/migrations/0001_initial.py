from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="CertificateDocument",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("document_type", models.CharField(choices=[("birth", "Birth certificate"), ("marksheet", "Marksheet"), ("community", "Community / caste certificate"), ("income", "Income certificate"), ("residence", "Residence / domicile certificate"), ("identity", "Identity document"), ("property", "Property / land document"), ("permit", "Government letter / permit"), ("other", "Other document")], max_length=30)),
                ("file", models.FileField(upload_to="certificate_uploads/%Y/%m/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(choices=[("review", "Suspicious — manual review needed"), ("likely_genuine", "Likely genuine — issuer verified"), ("likely_forged", "Likely forged — reviewer decision")], default="review", max_length=20)),
                ("risk_score", models.PositiveSmallIntegerField(default=50)),
                ("sha256", models.CharField(blank=True, max_length=64)),
                ("extracted_text", models.TextField(blank=True)),
                ("analysis_summary", models.TextField(blank=True)),
                ("checks", models.JSONField(blank=True, default=list)),
                ("official_verified", models.BooleanField(default=False)),
                ("reviewer_note", models.TextField(blank=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="certificate_documents", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-uploaded_at"]},
        ),
    ]

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CertificateUploadForm
from .models import CertificateDocument
from .analysis import analyze_document

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "certificates/home.html")

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out.")
    return redirect("home")

@login_required
def dashboard(request):
    form = CertificateUploadForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        doc = form.save(commit=False)
        doc.owner = request.user
        result = analyze_document(doc.file)
        doc.status = result["status"]
        doc.risk_score = result["risk_score"]
        doc.sha256 = result["sha256"]
        doc.extracted_text = result["extracted_text"]
        doc.analysis_summary = result["summary"]
        doc.checks = result["checks"]
        doc.save()
        messages.success(request, "Document checks completed. This report is preliminary, not an authenticity decision.")
        return redirect("document_detail", pk=doc.pk)
    docs = CertificateDocument.objects.filter(owner=request.user)[:5]
    return render(request, "certificates/dashboard.html", {
        "form": form, "documents": docs,
        "total": CertificateDocument.objects.filter(owner=request.user).count()
    })

@login_required
def history(request):
    docs = CertificateDocument.objects.filter(owner=request.user)
    return render(request, "certificates/history.html", {"documents": docs})

@login_required
def document_detail(request, pk):
    doc = get_object_or_404(CertificateDocument, pk=pk, owner=request.user)
    return render(request, "certificates/detail.html", {"doc": doc})

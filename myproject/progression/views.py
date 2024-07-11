# progression/views.py
from django.shortcuts import render


def progress(request):
    return render(request, "progression/progress.html", {})

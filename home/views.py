"""Home Views"""

from django.shortcuts import render


# Create your views here.
def index(request):
    """View to return Homepage"""
    return render(request, "home/index.html")

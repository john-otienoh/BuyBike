"""Home Views"""
from typing import Any
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

# Create your views here.
class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        return render(request, self.template_name)

class AboutView(TemplateView):
    template_name = 'home/about.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["stats"] = [
            {"value": "200k", "label": "Customers"},
            {"value": "50+", "label": "Countries"},
            {"value": "15", "label": "Years"},
            {"value": "4.9★", "label": "Avg. Rating"},
        ]
        return context

class ContactView(TemplateView):
    template_name = 'home/contact.html'

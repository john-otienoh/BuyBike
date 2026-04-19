from django.urls import path
from . import views

app_name = 'newsletters'

urlpatterns = [
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
]
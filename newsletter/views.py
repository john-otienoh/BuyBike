from django.shortcuts import redirect
from django.contrib import messages
from django.views import View
from .forms import NewsletterForm
from .models import NewsletterSubscriber

# Create your views here.
class NewsLetterSubscribeView(View):
    def post(self, request):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "You're subscribed! Welcome to the BuyBike community.")
            else:
                subscriber.is_active = True
                subscriber.save()
                messages.info(request, "You're already subscribed")
        else:
            messages.error(request, "Please enter a valid email address.")
        return redirect(request.META.get('HTTP_REFERER', 'home:home'))
    
from django.shortcuts import render, redirect
from django.urls import reverse
import stripe
from django.conf import settings


def donate_with_product(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == "POST":
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": "price_1PEEkEDnw0ite3t6mb2I1ZtA",  # enter yours here!!!
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse('donation_success')),
            cancel_url=request.build_absolute_uri(reverse('donation_cancelled')),
        )
        return redirect(checkout_session.url, code=303)
    return redirect(reverse('donation_form'))

def donation_success(request):
    return render(request, 'donations/donation_success.html')

def donation_cancelled(request):
    return render(request, 'donations/donation_cancelled.html')


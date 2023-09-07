from django.shortcuts import render
import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import Product, Basket

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET

FRONTEND_CHECKOUT_SUCCESS_URL = settings.CHECKOUT_SUCCESS_URL
FRONTEND_CHECKOUT_FAILED_URL = settings.CHECKOUT_FAILED_URL


class CreateCheckoutSession(APIView):
  def post(self, request):
    data_dict = dict(request.data)
    product_id = data_dict['product_id']

    try:
      product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
      return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
      checkout_session = stripe.checkout.Session.create(
        line_items=[{
          'price_data': {
            'currency': 'usd',
            'product_data': {
              'name': product.name,
            },
            'unit_amount': product.price * 100
          },
          'quantity': 1
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/checkout/success/',
        cancel_url='http://127.0.0.1:8000/checkout/cancel/',
      )
      return Response({'checkout_url': checkout_session.url}, status=status.HTTP_201_CREATED)
    except Exception as e:
      print(e)
      return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def success_view(request):
    return render(request, 'success.html')


def cancel_view(request):
    return render(request, 'cancel.html')


class WebHook(APIView):
  def post(self , request):
    event = None
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
      event = stripe.Webhook.construct_event(
        payload, sig_header, webhook_secret
        )
    except ValueError as err:
        # Invalid payload
        raise err
    except stripe.error.SignatureVerificationError as err:
        # Invalid signature
        raise err

    # Handle the event
    if event.type == 'payment_intent.succeeded':
      payment_intent = event.data.object
      print("--------payment_intent ---------->" , payment_intent)
    elif event.type == 'payment_method.attached':
      payment_method = event.data.object
      print("--------payment_method ---------->" , payment_method)
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event.type))

    return JsonResponse(success=True, safe=False)
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from pywebpush import webpush, WebPushException
from .models import PushSubscription

@csrf_exempt
def save_subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # Optionally, link subscription to request.user if authenticated
        sub, created = PushSubscription.objects.get_or_create(
            subscription_json=data
        )
        return JsonResponse({"status": "saved"})
    return JsonResponse({"error": "Invalid method"}, status=405)

def send_test_push(request):
    """Send a push to the most recent subscription"""
    sub = PushSubscription.objects.last()
    if not sub:
        return JsonResponse({"error": "No subscriptions"}, status=400)

    try:
        webpush(
            subscription_info=sub.subscription_json,
            data=json.dumps({"title": "Hello!", "body": "This is a test notification 🚀"}),
            vapid_private_key=settings.WEBPUSH_SETTINGS["VAPID_PRIVATE_KEY"],
            vapid_claims={"sub": f"mailto:{settings.WEBPUSH_SETTINGS['VAPID_ADMIN_EMAIL']}"}
        )
        return JsonResponse({"status": "Notification sent"})
    except WebPushException as e:
        return JsonResponse({"error": str(e)}, status=500)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def msg(request):
    print(request)
    data = {"fulfillmentText": "This is a response from webhook."}
    # data = {"fulfillmentMessages": [{"text": {"text": ["Hello there."]}}]}
    return JsonResponse(data)

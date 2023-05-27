import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .logic import ResponseFormulator


@csrf_exempt
def msg(request):
    body_json = json.loads(request.body.decode())
    reply = ResponseFormulator(body_json).reply()
    response_json = {"fulfillmentText": reply}
    return JsonResponse(response_json)

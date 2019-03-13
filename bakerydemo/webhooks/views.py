import requests
import json

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bakerydemo.base.models import StandardPage

@csrf_exempt
def whatsapp(request):
    token = settings.WEBHOOKS_WHATSAPP_TOKEN
    url = 'https://whatsapp.praekelt.org/v1/messages'
    try:
        body = json.loads(request.body.decode('utf-8'))
        message = body["messages"][0]["text"]["body"]
        contact = body["contacts"][0]["wa_id"]
    except:
        return HttpResponse('No body in request')
    if message:
        try:
            # TODO: use actual search API here for more relevant results
            body = StandardPage.objects.get(title__icontains==request['text']).introduction
        except:
            body = 'We could not find an Article matching that keyword. Please type in a different keyword...'
        data = {
            "preview_url": False,
            "recipient_type": "individual",
            "to": contact,
            "type": "text",
            "text": {
                "body": body
            }
        }
        headers={
            'Authorization': 'Bearer %s' % token,
            'Content-Type': 'application/json'
        }
        response = requests.post(
            url, data=json.dumps(data), headers=headers)
        return HttpResponse(response)
    else:
        data = {
            "preview_url": False,
            "recipient_type": "individual",
            "to": contact,
            "type": "text",
            "text": {
                "body": "Please type in keyword to search..."
            }
        }
        headers={
            'Authorization': 'Bearer %s' % token,
            'Content-Type': 'application/json'
        }
        response = requests.post(
            url=url, data=json.dumps(data), headers=headers)
        return HttpResponse(response)

    return HttpResponse('I did nothing :/')
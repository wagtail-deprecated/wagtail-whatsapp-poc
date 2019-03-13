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
    if request.GET.get('text', None) and request['text'] == 'search':
        # blah blah
        pass
    else:
        if request.GET.get('text', None):
            data = {
                "preview_url": False,
                "recipient_type": "individual",
                "to": "xxx",
                "type": "text",
                "text": {
                    "body": StandardPage.objects.get(live=True, title=request['text']).introduction
                }
            }
            headers={
                'Authorization': 'Bearer %s' % token,
                'Content-Type': 'application/json'
            }
            response = requests.post(
                url, data=data, headers=headers)
        else:
            data = {
                "preview_url": False,
                "recipient_type": "individual",
                "to": "xxx",
                "type": "text",
                "text": {
                    "body": "Please send the word search to begin."
                }
            }
            headers={
                'Authorization': 'Bearer %s' % token,
                'Content-Type': 'application/json'
            }
            response = requests.post(
                url=url, data=json.dumps(data), headers=headers)
            return HttpResponse(response)

    return HttpResponse('ok!')
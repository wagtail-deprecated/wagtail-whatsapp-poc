import requests
import json

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bakerydemo.breads.models import BreadPage
from bakerydemo.webhooks.decorators import is_engage_api


@csrf_exempt
@is_engage_api
def whatsapp(request):
    token = settings.WEBHOOKS_WHATSAPP_TOKEN
    url = 'https://whatsapp.praekelt.org/v1/messages'
    try:
        body = json.loads(request.body.decode('utf-8'))
        message = body["messages"][0]["text"]["body"]
        contact = body["contacts"][0]["wa_id"]
        name =  body["contacts"][0]["profile"]["name"]
    except:
        return HttpResponse('No body in request')
    if message:
        if 'join' in message:
            body = "Welcome %s. I can help you find information about bread. Please type in a type of bread that you would like to know more about, and I will send you a message with some details about that bread! \xF0\x9F\x98\x83" % name
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
            try:
                # TODO: use actual search here for more relevant results
                # TODO: return URL of the page that would give a preview
                # TODO: return whole body not just introduction
                body = BreadPage.objects.get(title__icontains=message).introduction
            except:
                # TODO: send a better welcome message and use name so it's more personal
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
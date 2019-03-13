import requests
import json
from django.http import HttpResponse
from bakerydemo.base.models import StandardPage


def whatsapp(request):
    token = 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJFbmdhZ2VkIiwiZXhwIjoxNTU0MDc2Nzk5LCJpYXQiOjE1NTI0ODA5OTEsImlzcyI6IkVuZ2FnZWQiLCJqdGkiOiIxMjQyNjk4ZC0yMmM1LTQ4ZGYtYmJiYi1lMTE3NmFhNjVhNDYiLCJuYmYiOjE1NTI0ODA5OTAsInN1YiI6Im51bWJlcjoxNDMiLCJ0eXAiOiJhY2Nlc3MifQ.Jaj1zkgpjJQEQlgZxu5WV16IbXYu7Sjw-sskOnO7q7DMkZiYc79tBXlMK3yZ_453vz4UA4nOsPWjxWkxGhLtFQ'
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
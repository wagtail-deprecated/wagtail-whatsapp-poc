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
            "preview_url": True,
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
        elif 'search' in message:
            # TODO: return whole body not just introduction
            search_word = message[7:]
            results = BreadPage.objects.live().search(search_word)
            if len(results) == 1:
                body = results[0].introduction
                body += "\n" + results[0].get_full_url()
            elif len(results) > 1:
                body = "We've found %s articles:" % len(results)
                for result in results:
                    body += "\n\n" + result.introduction
                    body += "\n" + result.get_full_url()
            else:
                body = "Sorry, we couldn't find an article matching that keyword"
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
            headers = {
                'Authorization': 'Bearer %s' % token,
                'Content-Type': 'application/json'
            }
            data = {
                "preview_url": False,
                "recipient_type": "individual",
                "to": contact,
                "type": "text",
                "text": {
                    "body": "I got into the else",
                }
            }
            response = requests.post(
                url, data=data, headers=headers)
            try:
                page = BreadPage.objects.get(title__icontains=message)
                if page.image:
                    # get image from admin
                    image_response = requests.get(page.image.url)
                    data = {
                        "preview_url": False,
                        "recipient_type": "individual",
                        "to": contact,
                        "type": "text",
                        "text": {
                            "body": "im after image_response",
                        }
                    }
                    response = requests.post(
                        url, data=json.dumps(data), headers=headers)
                    print('$$$$$$')
                    print(image_response)
                    print('$$$$$$')
                    
                    # upload image
                    image_upload_response = requests.post(
                        url, 
                        data=image_response.raw, 
                        headers=headers
                    )
                    data = {
                        "preview_url": False,
                        "recipient_type": "individual",
                        "to": contact,
                        "type": "text",
                        "text": {
                            "body": "im after image_upload",
                        }
                    }
                    response = requests.post(
                        url, data=json.dumps(data), headers=headers)
                    print('######')
                    print(image_upload_response)
                    print('########')
                    
                    # get image id from response
                    image_id = image_upload_response['media'][0]['id']
                    print('****')
                    print(image_id)
                    print('****')
                    data = {
                        "preview_url": False,
                        "recipient_type": "individual",
                        "to": contact,
                        "type": "text",
                        "text": {
                            "body": "im after image_upload_response",
                        }
                    }
                    response = requests.post(
                        url, data=json.dumps(data), headers=headers)
                    data = {
                        "preview_url": False,
                        "recipient_type": "individual",
                        "to": contact,
                        "type": "text",
                        "text": {
                            "body": "about to send image message",
                        }
                    }
                    response = requests.post(
                        url, data=json.dumps(data), headers=headers)
                    # send media message with caption
                    data = {
                        "preview_url": False,
                        "recipient_type": "individual",
                        "to": contact,
                        "type": "image",
                        "image": {
                            "id": image_id,
                            "caption": page.introduction
                        }
                    }
                    
                    response = requests.post(
                        url, data=json.dumps(data), headers=headers)
                    return HttpResponse(response)

                else:
                     # send text message if no image
                    data = {
                        "preview_url": False,
                        "recipient_type": "individual",
                        "to": contact,
                        "type": "text",
                        "text": {
                            "body": "page has no image, but Im sending you something that is text",
                        }
                    }
                    response = requests.post(
                        url, data=json.dumps(data), headers=headers)
            except:
                # no result or more than one result found
                data = {
                    "preview_url": False,
                    "recipient_type": "individual",
                    "to": contact,
                    "type": "text",
                    "text": {
                        "body": 'Please try again by typing search followed by keyword',
                    }
                }
                response = requests.post(
                    url, data=data, headers=headers)

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
import hmac
import base64

from hashlib import sha256

from django.conf import settings
from django.core.exceptions import PermissionDenied


def valid_signature(body, signature):
    h = hmac.new(settings.WEBHOOKS_WHATSAPP_HMAC.encode(), body, sha256)
    return base64.b64encode(h.digest()) == signature.encode()


def is_engage_api(function):
    def wrap(request, *args, **kwargs):
        signature = request.META.get('HTTP_X_ENGAGE_HOOK_SIGNATURE', None)
        
        if not signature:
            raise PermissionDenied("Engage Hook Signature request header is required.")
        
        if not valid_signature(request.body, signature):
            raise PermissionDenied("Received an invalid signature for this request.")
        
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
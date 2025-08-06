import json
from django.conf import settings
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from django.http import HttpResponse

BLOCK_SIZE = 16

def _aes_encrypt_bytes(raw: bytes) -> bytes:
    key = settings.AES_SECRET_KEY.encode("utf-8")
    iv = settings.AES_IV.encode("utf-8")
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    enc = cipher.encrypt(pad(raw, BLOCK_SIZE))
    return enc

class AESEncryptResponseMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resp = self.get_response(request)

        content_type = resp.get("Content-Type", "")
        if request.path.startswith("/admin") or "text/html" in content_type:
            return resp
        try:
            if hasattr(resp, "data"):
                payload = json.dumps(resp.data, default=str).encode("utf-8")
            else:
                payload = resp.content
                if not (content_type.startswith("application/json") or content_type.startswith("application/vnd.api+json")):
                    return resp
        except Exception:
            return resp

        encrypted = _aes_encrypt_bytes(payload)
        out = HttpResponse(encrypted, content_type="application/octet-stream")
        out.status_code = resp.status_code
        return out


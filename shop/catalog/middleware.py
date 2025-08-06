import json
from django.conf import settings
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from django.http import HttpResponse



BLOCK_SIZE=16


def _aes_encrypt_bytes(raw: bytes)->bytes:
    key=settings.AES_SECRET_KEY.encode("utf-8")
    iv=settings.AES_IV.encode("utf-8")
    cipher=AES.new(key, AES.MODE_CBC,iv=iv)
    enc=cipher.encrypt(pad(raw,BLOCK_SIZE))
    return enc





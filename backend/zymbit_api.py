
import ecdsa
from fastapi import HTTPException
from zymkey import Zymkey

zk = Zymkey()
public_key_bytes = zk.get_public_key(slot=0, foreign=False)


def sign_document_bytes(data: bytes) -> bytearray:
    try:
        return zk.sign(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def verify_signature(data: bytes, signature: bytes) -> bool:
    try:
        result = zk.verify(data, signature, False)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

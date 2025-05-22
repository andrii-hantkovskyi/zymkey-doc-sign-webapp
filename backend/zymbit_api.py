
import ecdsa
import zymkey
from fastapi import HTTPException

zk = zymkey.client
public_key_bytes = zk.get_public_key(slot=0, foreign=False)
verifying_key = ecdsa.VerifyingKey.from_string(public_key_bytes, curve=ecdsa.NIST256p)


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

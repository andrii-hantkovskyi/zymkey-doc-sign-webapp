# mock sign_document_bytes, verify_signature functions from zymbit_api.py
import hashlib

import ecdsa
from fastapi import HTTPException

# Generate a temporary signing key (only for testing!)
private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
public_key = private_key.get_verifying_key()


def sign_document_bytes(data: bytes) -> bytes:
    try:
        return private_key.sign(data, hashfunc=hashlib.sha256)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mock sign error: {str(e)}")


def verify_signature(data: bytes, signature_hex: str) -> bool:
    try:
        signature_bytes = bytes.fromhex(signature_hex)
        return public_key.verify(signature_bytes, data, hashfunc=hashlib.sha256)
    except ecdsa.BadSignatureError:
        return False
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Mock verify error: {str(e)}")

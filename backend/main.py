import io
from secrets import token_urlsafe

from auth import admin_required
from auth import router as auth_router
from fastapi import APIRouter, Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from models import User
from settings import CORS_ALLOWED_ORIGINS, CORS_ALLOWED_REGEX_ORIGINS, CORS_USE_REGEX, ZYMBIT_CONNECNTED

if not ZYMBIT_CONNECNTED:
    from mock_api import sign_document_bytes, verify_signature
else:
    from zymbit_api import sign_document_bytes, verify_signature

app = FastAPI()
cors_origins_kwargs = {'allow_origins': CORS_ALLOWED_ORIGINS} if not CORS_USE_REGEX else {'allow_origin_regex': CORS_ALLOWED_REGEX_ORIGINS}
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    **cors_origins_kwargs,
)
app.include_router(auth_router)


@app.post("/admin/sign_document")
async def sign_document(
    file: UploadFile = File(...), user: User = Depends(admin_required)
):
    content = await file.read()
    signature = sign_document_bytes(content)
    print('='*100)
    print(signature)
    print('='*100)

    sig_buffer = io.BytesIO(signature)
    sig_buffer.seek(0)

    return StreamingResponse(
        sig_buffer,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={token_urlsafe(16)}"},
    )


@app.post("/verify_sign")
async def verify_sign(
    file: UploadFile = File(...), signature_file: UploadFile = File(...)
):
    content = await file.read()
    signature = await signature_file.read()

    try:
        valid = verify_signature(content, signature)
        return {"valid": valid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Verification failed: {str(e)}")

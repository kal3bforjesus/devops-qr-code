from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import qrcode
import os
from io import BytesIO
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="QR Code Generator API")

# Allowing CORS for local testing with Next.js frontend
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model to properly parse JSON body from the frontend
class URLRequest(BaseModel):
    url: str

# Azure Blob Storage Configuration
AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME", "qrcodes")

@app.post("/generate-qr/")
async def generate_qr(request: URLRequest):
    url = request.url
    
    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR Code to BytesIO object (in-memory, no local file needed)
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Generate a safe file name for Azure Blob 
    # (Azure is stricter than S3 about special characters in blob names)
    safe_filename = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_")
    file_name = f"qr_codes/{safe_filename}.png"

    try:
        # Initialize Azure Blob Service Client
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_name)
        
        # Upload to Azure Blob Storage
        blob_client.upload_blob(img_byte_arr, overwrite=True)
        
        # Generate the Azure Blob URL
        blob_url = blob_client.url
        
        return {"qr_code_url": blob_url}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate or upload QR code: {str(e)}")
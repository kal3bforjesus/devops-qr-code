import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Load the .env file
load_dotenv()

# Get the variable
conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

print("--- DEBUGGING INFO ---")
print(f"1. Is variable empty? {conn_str is None or conn_str == ''}")
print(f"2. First 50 chars: {conn_str[:50] if conn_str else 'N/A'}")
print(f"3. Starts with quote? {conn_str.startswith('"') if conn_str else 'N/A'}")
print("----------------------")

if conn_str:
    try:
        # Try to create the client
        client = BlobServiceClient.from_connection_string(conn_str)
        # Try to list containers (simple network test)
        containers = list(client.list_containers())
        print("✅ SUCCESS! Connected to Azure.")
        print(f"Found containers: {[c.name for c in containers]}")
    except Exception as e:
        print(f"❌ FAILED: {e}")
else:
    print("❌ ERROR: The .env file was not read correctly.")
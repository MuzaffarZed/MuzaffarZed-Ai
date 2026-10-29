import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from gradio_client import Client

client = Client("Plachta/Seed-VC")
api_info = client.view_api(return_format="dict")
print("API Endpoints:")
for ep in api_info.get("named_endpoints", {}):
    print("Endpoint:", ep)
    params = api_info["named_endpoints"][ep].get("parameters", [])
    for p in params:
        print("  - Parameter:", p.get("label"), "| Type:", p.get("type"), "| Default:", p.get("default"))

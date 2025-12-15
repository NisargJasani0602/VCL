import os
import xmlrpc.client
import requests

VCL_URL = os.getenv("VCL_URL", "https://vcl.ncsu.edu/scheduling/index.php?mode=xmlrpccall")
VCL_TOKEN = os.getenv("VCL_TOKEN")
VERIFY = os.getenv("VCL_VERIFY_SSL", "true").lower() in ("1", "true", "yes")
if not VCL_TOKEN:
    raise SystemExit("Missing VCL_TOKEN")

def call(method, args):
    body = xmlrpc.client.dumps(tuple(args), methodname=method)
    headers = {
        "Content-Type": "text/xml",
        "X-APIVERSION": "2",
        "X-Authorization": f"Bearer {VCL_TOKEN}",
    }
    r = requests.post(VCL_URL, headers=headers, data=body, timeout=30, verify=VERIFY)
    r.raise_for_status()
    data, _ = xmlrpc.client.loads(r.content)
    return data[0]

# Pick one request id you want to connect to:
REQUEST_ID = 4155676  # change this
CLIENT_IP = os.getenv("VCL_CLIENT_IP")  # set this env var

if not CLIENT_IP:
    raise SystemExit("Set VCL_CLIENT_IP to your public IP (see instructions below).")

resp = call("XMLRPCgetRequestConnectData", [REQUEST_ID, CLIENT_IP])
print(resp)

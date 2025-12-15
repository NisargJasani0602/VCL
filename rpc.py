import os
import xmlrpc.client
import requests

VCL_URL = "https://vcl.ncsu.edu/scheduling/index.php?mode=xmlrpccall"
VCL_TOKEN = os.getenv("VCL_TOKEN")

if not VCL_TOKEN:
    raise RuntimeError("VCL_TOKEN not set")

HEADERS = {
    "Content-Type": "text/xml",
    "X-Authorization": f"Bearer {VCL_TOKEN}",
    "X-APIVERSION": "2",
}

def call(method: str, args: list = []):
    body = xmlrpc.client.dumps(tuple(args), methodname=method)

    r = requests.post(
        VCL_URL,
        headers=HEADERS,
        data=body,
        timeout=20
    )

    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}")

    data, _ = xmlrpc.client.loads(r.content)
    return data[0]

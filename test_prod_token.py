import xmlrpc.client
import requests
import os

VCL_URL = "https://vcl.ncsu.edu/scheduling/index.php?mode=xmlrpccall"
VCL_TOKEN = os.getenv("VCL_TOKEN")

body = xmlrpc.client.dumps(
    ("hello",),
    methodname="XMLRPCtest"
)

headers = {
    "Content-Type": "text/xml",
    "X-Authorization": f"Bearer {VCL_TOKEN}",
    "X-APIVERSION": "2",
}

print("Sending request to production VCL...")

r = requests.post(
    VCL_URL,
    headers=headers,
    data=body,
    timeout=20
)

print("HTTP STATUS:", r.status_code)
print("RAW RESPONSE:\n", r.text)

try:
    data, _ = xmlrpc.client.loads(r.content)
    print("\nPARSED RESPONSE:", data)
except Exception as e:
    print("\nFailed to parse XMLRPC:", e)

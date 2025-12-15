import os
import xmlrpc.client
import requests
from datetime import datetime

VCL_URL = os.getenv("VCL_URL", "https://vcl.ncsu.edu/scheduling/index.php?mode=xmlrpccall")
VCL_TOKEN = os.getenv("VCL_TOKEN")  # your prod token value

if not VCL_TOKEN:
    raise SystemExit("Missing VCL_TOKEN in env")

def call(method, args):
    body = xmlrpc.client.dumps(tuple(args), methodname=method)
    headers = {
        "Content-Type": "text/xml",
        "X-APIVERSION": "2",
        "X-Authorization": f"Bearer {VCL_TOKEN}",
    }
    r = requests.post(VCL_URL, headers=headers, data=body, timeout=30)  # verify=True by default for prod
    r.raise_for_status()
    data, _ = xmlrpc.client.loads(r.content)
    return data[0]

def ts(u):
    return datetime.fromtimestamp(int(u)).strftime("%Y-%m-%d %H:%M:%S") if u else "?"

res = call("XMLRPCgetRequestIds", [])
if res.get("status") != "success":
    print("Error:", res)
    raise SystemExit(1)

reqs = res.get("requests", [])
print(f"Found {len(reqs)} request(s)\n")

for r in reqs:
    print(f"- requestid={r['requestid']}  image={r['imagename']}  state={r['state']}")
    print(f"  start={ts(r['start'])}  end={ts(r['end'])}  os={r.get('OS','')}\n")

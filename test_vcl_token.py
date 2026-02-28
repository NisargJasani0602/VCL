import xmlrpc.client
import requests
import os

VCL_URL = "https://vcl.ncsu.edu/scheduling/index.php?mode=xmlrpccall"
VCL_TOKEN = os.getenv("VCL_TOKEN")
# ----------------------------------------------------

def test_token():
    body = xmlrpc.client.dumps(
        ("hello from token",),
        methodname="XMLRPCtest"
    )

    headers = {
        "Content-Type": "text/xml",
        "X-Authorization": f"Bearer {VCL_TOKEN}",
        "X-APIVERSION": "2",
    }

    r = requests.post(
        VCL_URL,
        headers=headers,
        data=body,
        verify=False,     # sandbox only
        timeout=20
    )

    print("HTTP STATUS:", r.status_code)

    if r.status_code != 200:
        print("Raw response:")
        print(r.text)
        return

    try:
        data, method = xmlrpc.client.loads(r.content)
        print("RPC RESPONSE:")
        print(data)
    except Exception as e:
        print("Failed to decode XMLRPC:", e)
        print(r.text)


if __name__ == "__main__":
    test_token()

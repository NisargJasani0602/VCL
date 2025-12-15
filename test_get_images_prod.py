from rpc import call

images = call("XMLRPCgetImages")
for img in images:
    print(f"{img['id']:>3}  {img['name']}")
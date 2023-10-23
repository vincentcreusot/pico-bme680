import ssl, socket, ubinascii


KEY_PATH = "certs/thing1.key.pem"
CERT_PATH = "certs/thing1.crt"
#CA_PATH = "certs/AmazonRootCA1.pem"
CA_PATH = "certs/ca.crt"
HOST, PORT = "iot.amazonaws.com", 8883

def read_pem(file):
    print(f"Reading : {file}")
    with open(file, "r") as input:
        text = input.read().strip()
        split_text = text.split("\n")
        base64_text = "".join(split_text[1:-1])
        return ubinascii.a2b_base64(base64_text)
    
key1 = read_pem(KEY_PATH)
cert1 = read_pem(CERT_PATH)
ca = read_pem(CA_PATH)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = socket.getaddrinfo(HOST, PORT)[0][-1]
print(addr)
s.connect(addr)
print(s)
sock = ssl.wrap_socket(s, server_side=False, key=key1, cert=cert1, cert_reqs=ssl.CERT_REQUIRED, cadata=ca, server_hostname=HOST)
print (sock)
print("Finished")
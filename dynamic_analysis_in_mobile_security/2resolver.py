import base64

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

key = str(fib(150))

encrypted = base64.b64decode(
    "cVZaW1dDQllZTFdRW1xeUlBbX21CWFtHalRZXUJFRFhNX1ZcbllGQ15cUUNSRFpcVks="
).decode('utf-8')

flag = "".join(chr(ord(key[i % len(key)]) ^ ord(c)) for i, c in enumerate(encrypted))
print(flag)
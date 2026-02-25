import random
from socket import *

# ----------------------------
# 1. Read file and generate OTP key (your original code)
# ----------------------------
with open("Zelenskyy1.txt", "r") as f:
    message = f.read()

length = len(message)

def randomChars(length):
    letters = ''.join([chr(i) for i in range(256)])  # all 0-255 characters
    return ''.join(random.choices(letters, k=length))

otpkey = randomChars(length)

message_bytes = message.encode("latin-1")  
key_bytes = otpkey.encode("latin-1")

# ----------------------------
# 2. OTP encryption (XOR) — exactly your while loop
# ----------------------------
i = 0
cipherbytes = b""
while i < len(message_bytes):
    m = message_bytes[i]
    k = key_bytes[i]
    c = m ^ k
    cipherbytes += bytes([c])
    i += 1

# ----------------------------
# 3. Extended Vigenère encryption of OTP key — exactly your while loop
# ----------------------------
extended = "secret"
extendedkey = extended.encode("utf-8")
finalcrypt = b""

x = 0
while x < len(key_bytes):
    k_byte = key_bytes[x]
    e_byte = extendedkey[x % len(extendedkey)]
    c_byte = (k_byte + e_byte) % 256
    finalcrypt += bytes([c_byte])
    x += 1

# ----------------------------
# 4. Send via sockets using client1 and client2
# ----------------------------
serverName = "localhost"

# --- client1 sends encrypted OTP key on port 3500 ---
client1 = socket(AF_INET, SOCK_STREAM)
client1.connect((serverName, 3500))
client1.sendall(finalcrypt)  # send all bytes
client1.close()
print("Encrypted OTP key sent on port 3500.")

# --- client2 sends OTP-encrypted message on port 3501 ---
client2 = socket(AF_INET, SOCK_STREAM)
client2.connect((serverName, 3501))
client2.sendall(cipherbytes)  # send all bytes
client2.close()
print("Encrypted message sent on port 3501.")

from socket import *

# ----------------------------
# 1. Receive Encrypted OTP Key (Port 3500)
# ----------------------------
serverPortKey = 3500
serverSocketKey = socket(AF_INET, SOCK_STREAM)
serverSocketKey.bind(("", serverPortKey))
serverSocketKey.listen(1)

print("Waiting for encrypted OTP key on port 3500...")
connectionKey, addr = serverSocketKey.accept()

encrypted_key = b""
while True:
    data = connectionKey.recv(4096)
    if not data:
        break
    encrypted_key += data

connectionKey.close()
serverSocketKey.close()
print("Encrypted OTP key received.")


# ----------------------------
# 2. Receive Encrypted Message (Port 3501)
# ----------------------------
serverPortMsg = 3501
serverSocketMsg = socket(AF_INET, SOCK_STREAM)
serverSocketMsg.bind(("", serverPortMsg))
serverSocketMsg.listen(1)

print("Waiting for encrypted message on port 3501...")
connectionMsg, addr = serverSocketMsg.accept()

cipherbytes = b""
while True:
    data = connectionMsg.recv(4096)
    if not data:
        break
    cipherbytes += data

connectionMsg.close()
serverSocketMsg.close()
print("Encrypted message received.")


# ----------------------------
# 3. Decrypt OTP Key using Extended Vigenère
# ----------------------------
extended = "secret"
extendedkey = extended.encode("utf-8")

decrypted_key = b""

i = 0
while i < len(encrypted_key):
    c_byte = encrypted_key[i]
    e_byte = extendedkey[i % len(extendedkey)]
    k_byte = (c_byte - e_byte) % 256   # Extended Vigenère Decryption
    decrypted_key += bytes([k_byte])
    i += 1

print("OTP key decrypted.")


# ----------------------------
# 4. Decrypt Message using OTP (XOR)
# ----------------------------
final_message_bytes = b""

x = 0
while x < len(cipherbytes):
    c = cipherbytes[x]
    k = decrypted_key[x]
    m = c ^ k
    final_message_bytes += bytes([m])
    x += 1

# Save Zelenskyy2.dat
with open("Zelenskyy2.dat", "wb") as f:
    f.write(final_message_bytes)

print("Decrypted file saved as Zelenskyy2.dat")

# ----------------------------
# 5. Print Final Message
# ----------------------------
final_message = final_message_bytes.decode("latin-1")
print("\n----- FINAL DECODED MESSAGE -----\n")
print(final_message)

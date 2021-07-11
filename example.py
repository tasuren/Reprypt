# Repryptの使用例です。

import reprypt
from time import time


# TEXTは暗号化する文字列で、KEYがパスワードです。
TEXT = input("TEXT>")
KEY = input("KEY >")
print(f"Reprypt example\n  TEXT	: {TEXT}\n  KEY	: {KEY}")
start = time()


# 暗号化する。
encryption_result = reprypt.encrypt(TEXT, KEY)
print("Encryption result :", encryption_result)


# 複合化する。
result = reprypt.decrypt(encryption_result, KEY)
print("Decryption result :", result)


print("Speed	:", time() - start)

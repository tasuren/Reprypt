# Repryptの使用例です。

import reprypt


# TEXTは暗号化する文字列で、KEYがパスワードです。
TEXT = "I wanna be the guy!"
KEY = "I love girl."
print(f"Reprypt\n  TEXT	: {TEXT}\n  KEY	: {KEY}")


# 暗号化する。
encryption_result = reprypt.encrypt(TEXT, KEY)
print("Encryption result :", encryption_result)


# 複合化する。
result = reprypt.decrypt(encryption_result, KEY)
print("Decryption result :", result)

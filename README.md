# Reprypt
Python Encryption Module / Pythonの暗号化モジュール

`pip install reprypt`

# How to use / 使い方
```python
import reprypt

# Encryption / 暗号化
encrypted = reprypt.encrypt( "This is the message" , "This is the password" )
print("Encrypted : " + encrypted)

# Decryption / 復号化
decrypted = reprypt.decrypt( encrypted , "This is the password" )
print("Decrypted : " + decrypted)
```

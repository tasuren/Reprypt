# Reprypt
Python Encryption Module

`pip install reprypt`

# How to use
```python
import reprypt

encrypted = reprypt.encrypt( "This is the message" , "This is the password" )
print("Encrypted : " + encrypted)

decrypted = reprypt.decrypt( encrypted , "This is the password" )
print("Decrypted : " + decrypted)
```

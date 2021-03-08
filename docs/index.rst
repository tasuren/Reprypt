# Reprypt - Python Encrypting Module  
This is the python encrypting module.  
You can install by run `pip install reprypt`.  

# How to use  
```python
import reprypt

# Encryption / 暗号化
encrypted = reprypt.encrypt( "This is the message" , "This is the password" )
print("Encrypted : " + encrypted)

# Decryption / 復号化
decrypted = reprypt.decrypt( encrypted , "This is the password" )
print("Decrypted : " + decrypted)
```

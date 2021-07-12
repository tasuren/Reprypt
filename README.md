# Reprypt
Pythonの暗号化モジュールです。    
`=QSuIB3=S3W5YBiYZSB0gSGUaV5Z`のような暗号をパスワードで作成することができます。  
レファレンス：[https://tasuren.github.io/reprypt](https://tasuren.github.io/reprypt/)
リポジトリ　：[https://github.com/tasuren/reprypt](https://github.com/tasuren/reprypt)
作者のサイト：[http://tasuren.f5.si/](http://tasuren.f5.si/)

## Getting started
インストールは以下を実行するだけです。
```terminal
pip install reprypt
```

## Example
```python
import reprypt

# Encryption / 暗号化
encrypted = reprypt.encrypt("I wanna be the guy!", "Ohk")
print(encrypted)
# -> =QSuIB3=S3W5YBiYZSB0gSGUaV5Z

# Decryption / 復号化
decrypted = reprypt.decrypt(encrypted, "Ohk")
print(decrypted)
# -> I wanna be the guy!
```

## Benchmark
速度のベンチマーク結果です。  
`I wanna be the guy!`を`Ohk`のパスワードで暗号化します。  
使用するコードは[GitHub](https://github.com/tasuren/reprypt)にあります。  
### Enviroment
```
CPU : Intel Core i7-3610QM
RAM : 8GB
```
### Result
```terminal
$ python3 benchmark.py
Result	: =QSuIB3=S3W5YBiYZSB0gSGUaV5Z
Speed	: 0.00008678436279296875
```

## LICENSE
MIT License

## Console
Repryptはインストールするとコンソールからも使用することができます。
`reprypt help`で使用方法を確認することができます。

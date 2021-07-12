# Reprypt

from typing import Union, Optional, Tuple
from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode


version = "2.1.0b2"


class DecryptError(Exception):
    pass


def convert_unicode(text: str, length: int = None) -> str:
    """
    文字列をUnicodeポイントに変換します。
    Reprypt内部で使われるものです。
    注意：これは暗号化/複合化する際に難読化するのに使うものではありません。
    """
    r = ""
    if length is None:
        length = len(text)
    for ti in range(length):
        r += str(ord(text[ti]))
    return r


def convert_b64(text: str, un: bool = False) -> str:
    """
    文字列をBase64でエンコード/デコードします。
    これはRepryptの暗号化/復号化する際に難読化するのに使用できるものです。

    Examples
    --------
    >>> reprypt.encrypt("You are fine.", "Ma?", converter=reprypt.convert_b64)
    "yWS=FW=g9L1GBmZ5IlaW"
    """
    return convert_hex(text, un, what_isd=(b64decode, b64encode))


def convert_hex(text: str, un: bool,
                what_isd: object = (unhexlify, hexlify)) -> str:
    """
    文字列を十六進数に変換します。
    これはRepryptの暗号化/複合化する際に難読化するのにデフォルトで使用されるものです。
    もしこれを他のもので使いたい場合はconvert_b64を使うなどしましょう。

    See Also
    --------
    convert_b64 : 文字列をBase64でエンコード/デコードします。
    """
    will_hexlify = what_isd[0] if un else what_isd[1]
    text = will_hexlify(text.encode()).decode()
    del will_hexlify
    return text


def replace(text: str, length: int, original: int, target: int) -> str:
    """
    文字列のとある位置にある文字をとある位置の文字と交換します。
    これはRepryptの内部で使われるものです。
    """
    after = text[target]
    end = target + 1
    end = text[end:] if end < length else ""
    text = text[:target] + text[original] + end
    end = original + 1
    end = text[end:] if end < length else ""
    text = text[:original] + after + end
    del end, after
    return text


def parse_key(key: str, key_length: int, text_length: int) -> Tuple[str, int]:
    """
    keyを暗号/復号時に最適なkeyに変換します。
    Repryptの内部で使用されるものです。
    """
    error = 0
    while key_length < text_length:
        error = text_length - key_length
        if error > key_length:
            error -= error - key_length
        key = key + key[0 - error:]
        key_length += error
    del key_length, error
    return key[:text_length], text_length


def encrypt(text: str, key: str, *, convert: bool = True,
            converter: object = convert_hex, log: bool = False) -> str:
    """
    暗号化します。

    Parameters
    ----------
    text : str
        暗号化する文字列です。
    key : str
        暗号化する際に使用するパスワードです。
        複合時に必要となります。
    convert : bool, default True
        暗号化する前の文章をconverterに入れた関数を使用して他のものに変換するかどうかです。
        これを無効にした場合は暗号結果は元の文章にある文字しか含まれていません。
        含まれている文字から内容を推測される可能性があるのでこれを有効にするのを推奨します。
    converter : object, default convert_hex
        convertがTrueの際に何を使用して変換を行うかです。
        デフォルトはconvert_hexです。(`reprypt.convert_hex`)
        他にBase64に変換する(`reprypt.convert_b64`)があります。
        自分の作ったものを使う場合は以下のようにした関数を使用してください。
        `変換対象: str, 変換をするか逆変換か: bool`
    log : bool, default False
        暗号化の途中経過を出力するかどうかです。

    Returns
    -------
    text : str
        暗号結果です。
    """
    if convert:
        text = converter(text, False)
    key, text_length = convert_unicode(key), len(text)
    key_length, key_index = len(key), -1
    key, key_length = parse_key(key, key_length, text_length)
    if log:
        print("Encrypt target	:", text)
        print("Encrypt key	:", key)
    for index in range(text_length):
        key_index += 1
        target = int(key[key_index])
        if target >= text_length:
            target = int(target / 2)
        text = replace(text, text_length, index, target)
        if log:
            print("  Replaced", index, "->", target, ":", text)
    if log:
        print("Result\t:", text)
    return text


def decrypt(text: str, key: str, convert: bool = True,
            converter: object = convert_hex, log: bool = False) -> Union[str]:
    """
    暗号を複合化します。

    Parameters
    ----------
    text : str
        復号化する暗号の文字列です。
        もしstr型が渡された場合は引数encodeに渡されているもので文字列にエンコードします。
    key : str
        暗号化する際に使用するパスワードです。
        復号時時に必要となります。
    convert : bool, default True
        暗号化時にもしこれを有効にした場合はこれを有効にする必要があります。
        変換に使用されるのはconverterに入れたものが使われます。
    converter : object, default convert_hex
        convertにTrueが入れられた際の変換に使用する関数です。
        デフォルトは十六進数に変換するものです。(`reprypt.convert_hex`)
        他にBase64に変換するものがあります。`reprypt.encrypt`のconverterに詳細があります。
    log : bool, default False
        復号の途中経過を出力します。

    Returns
    -------
    text : str
        復号結果です。

    Raises
    ------
    DecryptError
        復号に失敗すると発生します。
        keyがあっていないまたはencodeが暗号化時とあっていない際に発生します。

    See Also
    --------
    encrypt : 暗号化します。

    Notes
    -----
    引数のconvertをFalseにした場合はKeyが間違っている場合でもDecryptErrorが発生しませんので注意してください。
    """
    key, text_length = convert_unicode(key), len(text)
    key, key_index = parse_key(key, len(key), text_length)
    if log:
        print("Decrypt target	:", text)
        print("Decrypt key	:", key)
    for index in reversed(range(text_length)):
        key_index -= 1
        target = int(key[key_index])
        if target >= text_length:
            target = int(target / 2)
        text = replace(text, text_length, target, index)
        if log:
            print("  Replaced", target, "->", index, ":", text)
    if convert:
        try:
            text = converter(text, True)
        except Exception as e:
            raise DecryptError("復号化に失敗しました。keyがあっているかencodeが暗号化時と同じかどうか確認してください。:" + str(e))
    if log:
        print("Result\t:", text)
    return text


def old_encrypt(text: str, pa: str, log: bool = False) -> str:
    """
    2.0.0までのRepryptの暗号化です。

    Parameters
    ----------
    text : str
        暗号化する文字列です。
    pa : str
        暗号化する際に使用するパスワードです。
    log : bool, default False
        暗号化途中のログ出力をするかどうかです。

    Returns
    -------
    text : str
        暗号化結果です。

    See Also
    --------
    old_decrypt : 2.0.0までのRepryptで作られた暗号を複合化するためのものです。
    encrypt : 最新のRepryptの暗号化です。
    """
    if log:
        print("Start encrypt")
    pa = convert_unicode(pa)
    text = list(b64encode(text.encode()).decode())
    for i in range(2):
        if i == 1:
            text.reverse()
        for ti in range(len(text)):
            for pi in range(len(pa)):
                pi = int(pa[pi])
                if len(text) < pi+1:
                    while pi+1 > len(text):
                        pi -= 1
                if pi == 0:
                    pi = len(text)-1
                if log:
                    print(f"  {i} - {ti+1} ... {text[pi]} -> {text[ti]}")
                m = text[ti]
                text[ti] = text[pi]
                text[pi] = m
    if log:
        print("Done")
    return "".join(text)

def old_decrypt(text: str, pa: str, log: bool = False) -> str:
    """
    2.0.0までのRepryptで暗号化されたものを複合化します。

    Parameters
    ----------
    text : str
        複合化する文字列です。
    pa : str
        複合化する際に使用するパスワードです。
    log : bool, default False
        複合化途中のログ出力をするかどうかです。

    Returns
    -------
    text : str
        複合化結果です。

    See Also
    --------
    decrypt : 最新のRepryptで作られた暗号を複合化するものです。
    """
    if log:
        print("Start Decrypt")
    pa = convert_unicode(pa)
    text = list(text)
    for i in range(2):
        if i == 1:
            text.reverse()
        l = list(range(len(text)))
        l.reverse()
        for ti in l:
            li = list(range(len(pa)))
            li.reverse()
            for pi in li:
                pi = int(pa[pi])
                if len(text) < pi+1:
                    while pi+1 > len(text):
                        pi -= 1
                if pi == 0:
                    pi = len(text)-1
                if log:
                    print(f"  {i} - {ti+1} ... {text[ti]} -> {text[pi]}")
                m = text[pi]
                text[pi] = text[ti]
                text[ti] = m
    if log:
        print("Done")
    try:
    	text = b64decode("".join(text).encode()).decode()
    except:
    	raise DecryptError("Failed to decode Base64. Please check if the password is correct.")
    return text


if __name__ == "__main__":
    print("Reprypt by tasuren")
    end = "False"
    while end != "True":
        cmd = input(">>>")
        if cmd == "help":
            print("help\t- How to message\nversion\t- Show version\nen\t- Encrypt\nde\t- Decrypt\nend\t- End")
        if cmd == "en":
            m = input("SENTENCE >")
            pa = input("PASSWORD >")
            m = encrypt(m, pa)
            print("RESULT : " + m)
        if cmd == "de":
            m = input("SENTENCE >")
            pa = input("PASSWORD >")
            de = decrypt(m, pa)
            print("RESULT : " + de)
        if cmd in ("version", "v"):
        	print("v" + str(version))
        if cmd == "end":
        	print("Bye")
        	end = "True"

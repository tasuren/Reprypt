"""
.. include:: ../README.md
"""
# Reprypt by tasuren

from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from typing import Union, Tuple


__version__ = "2.1.1"
"""Repryptのバージョンです。  
PEP440に準拠しています。"""
__all__ = (
    "encrypt", "decrypt",
    "convert_b64", "convert_hex",
    "old_encrypt", "old_decrypt",
    "__version__", "DecryptError"
)


class DecryptError(Exception):
    """
    復号化失敗時に発生する例外です。  
    暗号化時に使用したkeyまたはconverterが違う際などに発生します。  
    """
    pass


def convert_unicode(text: str, length: int = None) -> str:
    r = ""
    if length is None:
        length = len(text)
    for ti in range(length):
        r += str(ord(text[ti]))
    return r


def convert_b64(text: str, un: bool) -> str:
    """
    文字列をBase64でエンコード/デコードします。  
    これはRepryptの暗号化する際に難読化するのにデフォルト使用されるものです。  
    そのため普通は使いません。

    Parameters
    ----------
    test : str
        エンコードまたはデコードする対象の文字列です。
    un : bool
        これがFalseの場合はエンコード,Trueの場合はデコードをします。

    See Also
    --------
    convert_hex : 文字列を十六進数に変換します。Repryptの難読化に使用可能です。
    """
    return convert_hex(text, un, what_isd=(b64decode, b64encode))


def convert_hex(text: str, un: bool,
                what_isd: Tuple[object] = (unhexlify, hexlify)) -> str:
    """
    文字列を十六進数に変換します。  
    これはRepryptの暗号化する際に難読化するのに使用することができるものです。  

    Examples
    --------
    >>> reprypt.encrypt("You are fine.", "Ma?", converter=reprypt.convert_hex)
    '051e292e66f566757206296665'

    Parameters
    ----------
    text : str
        十六進数に変換する対象の文字列です。
    un : bool
        これがFalseの場合は十六進数に変換、Trueの場合は十六進数から元に戻します。
    what_isd : Tuple[object], default (binascii.unhexlify, binascii.hexlify)
        十六進数の変換に使うものです。  
        普通はここは変更しません。  
    """
    will_hexlify = what_isd[0] if un else what_isd[1]
    text = will_hexlify(text.encode()).decode()
    del will_hexlify
    return text


def replace(text: str, length: int, original: int, target: int) -> str:
    # 文字列の対象の位置にあるものを対象の位置と交換する関数です。
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
    # 暗号化/復号化時に最適な状態にパスワードを調整する関数です。
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
            converter: object = convert_b64, log: bool = False) -> str:
    """
    渡された文字列をRepryptで暗号化します。

    Parameters
    ----------
    text : str
        暗号化する文字列です。
    key : str
        暗号化する際に使用するパスワードです。  
        復号時に必要となります。
    convert : bool, default True
        暗号化する前の文章をconverterに入れた関数を使用して他のものに変換するかどうかです。  
        これを無効にした場合は暗号結果は元の文章にある文字しか含まれていません。  
        含まれている文字から内容を推測される可能性があるのでこれを有効にするのを推奨します。
    converter : object, default convert_b64
        convertがTrueの際に何を使用して変換を行うかです。  
        デフォルトはBase64でエンコードする`reprypt.convert_b64`です。  
        他に十六進数に変換する`reprypt.convert_hex`があります。  
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
            print("  Replaced", index, "->", str(target) + "\t:", text)
    return text


def decrypt(text: str, key: str, convert: bool = True,
            converter: object = convert_b64, log: bool = False) -> Union[str]:
    """
    暗号を復号化します。

    Parameters
    ----------
    text : str
        復号化する暗号の文字列です。
    key : str
        暗号化に設定したパスワードです。
    convert : bool, default True
        暗号化時にもしこれをTrueを設定した場合はこれを有効にする必要があります。  
        これがなんなのかの詳細は`reprypt.encrypt`のconvertにあります。
    converter : object, default convert_b64
        convertにTrueが入れられた際の変換に使用する関数です。  
        暗号化時と同じものにする必要があります。  
        デフォルトはBase64でデコードする`reprypt.convert_b64`が使われます。  
        他に十六進数に変換するものがあります。`reprypt.encrypt`のconverterに詳細があります。
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
        keyがあっていないまたはconverterが暗号化時とあっていない際に発生します。

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
            print("  Replaced", target, "->", str(index) + "\t:", text)
    if convert:
        try:
            text = converter(text, True)
        except Exception as e:
            code = ("復号化に失敗しました。keyがあっているかconverterが暗号化時と同じかどうか確認してください。:"
                    + str(e))
            raise DecryptError(code)
    return text


def old_encrypt(text: str, pa: str, log: bool = False) -> str:
    """
    2.0.0までのRepryptの暗号化です。

    Notes
    -----
    速度が遅いため最新の`reprypt.encrypt`を使用することを勧めます。

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
    old_decrypt : 2.0.0までのRepryptで作られた暗号を復号化するためのものです。
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
    2.0.0までのRepryptで暗号化されたものを復号化します。  

    Notes
    -----
    遅いため最新の`reprypt.decrypt`を使用するのを勧めます。  
    ですが、2.0.0までのバージョンのRepryptで作った暗号はこの関数でないと復号化できません。  
    ご注意ください。

    Parameters
    ----------
    text : str
        復号化する文字列です。
    pa : str
        復号化する際に使用するパスワードです。
    log : bool, default False
        復号化途中のログ出力をするかどうかです。

    Returns
    -------
    text : str
        復号化結果です。

    See Also
    --------
    decrypt : 最新のRepryptで作られた暗号を復号化するものです。
    """
    if log:
        print("Start Decrypt")
    pa = convert_unicode(pa)
    text = list(text)
    for i in range(2):
        if i == 1:
            text.reverse()
        l_ = list(range(len(text)))
        l_.reverse()
        for ti in l_:
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
    except Exception as e:
        code = ("Failed to decode Base64. "
                + "Please check if the password is correct."
                + ":" + str(e))
        raise DecryptError(code)
    return text


if __name__ == "__main__":
    import __main__

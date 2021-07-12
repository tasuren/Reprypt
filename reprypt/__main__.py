# Reprypt

from typing import Union, Tuple, List, Dict
from reprypt import *
from sys import argv


HELP = f"""# Reprypt v{__version__}
Pythonの暗号作成モジュールです。
GitHub : https://github.com/tasuren/reprypt
# 使用方法
## 引数一覧
version\t\tRepryptのバージョンを表示します。
help\t\tこのメッセージを表示します。
encrypt\t\t暗号化をします。
decrypt\t\t復号化をします。
## オプション
オプションはコマンドの最後につけることで使用できます。
dont-conv\t難読化するためにする変換をしないで暗号化します。
\t\tRepryptは文字列の文字を置き換えることでわからなくします。
\t\tなので置き換えるだけだと暗号化後の文字列にある漢字から内容を推測されてしまう可能性があります。
\t\tそのため機密情報などにはこのオプションをつけないことを推奨します。
conv-hex\t難読化に使用する変換で十六進数変換を使用します。
log\t\t暗号/復号の途中経過のログ出力を行います。
## 使用例
Normal\t: `reprypt encrypt 文字列 キー`
Option\t: `reprypt encrypt 文字列 キー dont-conv`
# ライセンス
MIT License
Copyright (c) 2021 tasuren"""


def option_manager(args: Union[Tuple[str], List[str]]) -> Dict[str, Union[bool, object]]:
    kwargs = {}
    if "dont-conv" in args:
        kwargs["convert"] = False
    if "conv-hex" in args:
        kwargs["converter"] = convert_hex
    if "log" in args:
        kwargs["log"] = True
    return kwargs


def main():
    varg = argv[1:]
    for word in ("python", "python3", "-m"):
        for arg in varg:
            if arg.startswith(word):
                varg.remove(arg)
    if varg:
        if varg[0] == "help":
            print(HELP)
        elif varg[0] in ("version", "ver", "-V", "--version"):
            print(__version__)
        elif varg[0] in ("encrypt", "en") and len(varg) > 2:
            print("Result :", encrypt(varg[1], varg[2], **option_manager(varg)))
        elif varg[0] in ("decrypt", "de") and len(varg) > 2:
            try:
                result = decrypt(varg[1], varg[2], **option_manager(varg))
            except Exception as e:
                print("Error :", e)
            else:
                print("Result :", result)
                del result
        else:
            print("Error : 使用方法が違います。`reprypt help`で確認してください。")
    else:
        print(HELP)


if __name__ == "__main__":
    main()

version = 2.0.0
title = """
______                            _   
| ___ \                          | |  
| |_/ /___ _ __  _ __ _   _ _ __ | |_ 
|    // _ \ '_ \| '__| | | | '_ \| __|
| |\ \  __/ |_) | |  | |_| | |_) | |_ 
\_| \_\___| .__/|_|   \__, | .__/ \__|
          | |          __/ | |        
          |_|         |___/|_|        
    by tasuren                 v"""+str(version)+"\n"

from base64 import b64encode, b64decode



class DecryptError(Exception):
	pass

def c16(text):
    r = ""
    for ti in range(len(text)):
        r += str(ord(text[ti]))
    return r

def encrypt(text,pa,log=False):
    if log:
        print("Start encrypt")
    pa = c16(pa)
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

def decrypt(text,pa,log=False):
    if log:
        print("Start Decrypt")
    pa = c16(pa)
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
    print(title)
    end = "False"
    while end != "True":
        cmd = input(">>>")
        if cmd == "help":
            print("help - How to message\nversion - Show version\nen - Encrypt\nde - Decrypt\nend - End")
        if cmd == "en":
            m = input("SENTENCE >")
            pa = input("PASSWORD >")
            m = encrypt(m,pa)
            print("RESULT : "+m)
        if cmd == "de":
            m = input("SENTENCE >")
            pa = input("PASSWORD >")
            de = decrypt(m,pa)
            print("RESULT : "+de)
        if cmd in ["version","v"]:
        	print("v"+str(version))
        if cmd == "end":
        	print("Bye")
        	end = "True"
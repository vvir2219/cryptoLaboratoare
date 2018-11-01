#!/bin/python2

import EncryptionAlgorithms as e
from appJar import gui

ciphers = ["caesar", "substitution", "affine", "belaso", "hill", "permutation"]

def helpfun(app, cipher):
    text = 'No such cipher ' + cipher
    if cipher == ciphers[0]:
        text = "Cipher key is an integer k with 0 <= |k| < |alphabet|"
    elif cipher == ciphers[1]:
        text = "Cipher key is another alphabet of length equal to the current alphabet"
    elif cipher == ciphers[2]:
        text = "Cipher key is a tuple of 2 integers (a, b) with 0 <= a, b < |alphabet| and gcd(a, |alphabet|) = 1. Key shall be given as two space separated integers"
    elif cipher == ciphers[3]:
        text = "Cipher key is a string of characters from the current alphabet"
    elif cipher == ciphers[4]:
        text = "Cipher key is a nxn matrix, with 0 < n < |alphabet| which is invertible and gcd(det K, |alphabet|) = 1.Key shall be given as a space separated sequence of n*n integers"
    elif cipher == ciphers[5]:
        text = "Cipher key is a n-permutation of range(n), 0 < n <= |alphabet|.Key shall be given as a space separated sequence of integers"

    app.infoBox(cipher.capitalize() + " cipher key format", text)

def getCipher(cipher, alphabet):
    if cipher == ciphers[0]:
        return e.CaesarCipher(alphabet)
    elif cipher == ciphers[1]:
        return e.SubstitutionCipher(alphabet)
    elif cipher == ciphers[2]:
        return e.AffineCipher(alphabet)
    elif cipher == ciphers[3]:
        return e.BelasoCipher(alphabet)
    elif cipher == ciphers[4]:
        return e.HillCipher(alphabet)
    elif cipher == ciphers[5]:
        return e.PermutationCipher(alphabet)

    raise e.ValidationException("No such cipher")

def getKey(cipher, keytext):
    if cipher == ciphers[0]:
        return int(keytext)
    elif cipher == ciphers[1]:
        return keytext
    elif cipher == ciphers[2]:
        return map(lambda x: int(x), keytext.split(' '))
    elif cipher == ciphers[3]:
        return keytext
    elif cipher == ciphers[4]:
        return map(lambda x: int(x), keytext.split(' '))
    elif cipher == ciphers[5]:
        return map(lambda x: int(x), keytext.split(' '))

    raise e.ValidationException("No such cipher")

def encrypt(app, decrypt_bool=False):
    try:
        cipher = getCipher(app.getOptionBox("option_cipher"), app.getEntry("entry_alphabet"))
        key = getKey(app.getOptionBox("option_cipher"), app.getEntry("entry_key"))
        
        encoded = ''
        if decrypt_bool:
            encoded = cipher.decrypt(key, app.getTextArea("textarea_text"))
        else:
            encoded = cipher.encrypt(key, app.getTextArea("textarea_text"))

        app.clearTextArea("textarea_text")
        app.setTextArea("textarea_text", encoded)
    except e.ValidationException as err:
        app.errorBox("Error", err)
    except ValueError as err:
        app.errorBox("Error", "Invalid key")

app=gui("EncryptionAlgorithms", "600x400")

app.setExpand("both")
app.setFont(14)

app.addLabel("label_alphabet", "Alphabet", 0, 0, 2)
app.addEntry("entry_alphabet", 0, 2, 4)
app.addLabel("label_key", "Key", 1, 0)
app.addButton("Help", lambda : helpfun(app, app.getOptionBox("option_cipher")), 1, 1)
app.addEntry("entry_key", 1, 2, 4)
app.addLabel("label_text", "Text", 2, 0, 2);
app.addOptionBox("option_cipher", ciphers, 3, 0, 2)
app.addTextArea("textarea_text", 2, 2, 4, 3)
app.addButton("Decrypt", lambda : encrypt(app, True), 5, 4)
app.addButton("Encrypt", lambda : encrypt(app), 5, 5)

app.go()






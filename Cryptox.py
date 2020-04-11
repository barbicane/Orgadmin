# encoding: utf-8



####importation des librairies:
import hashlib
import sys
from Crypto.Cipher import AES
from Crypto.Cipher import ARC2
from Crypto.Cipher import ARC4


####definition pour le hash
def checksum(message):
    return hashlib.sha224(message.encode("utf-8")).hexdigest()


####definition pour le cryptage
def crypt(message, Key=b'1a3b4c5e6d7f8g9h0i1j2k3l4m5n6o7p'):
    if len(message) == 0:
        return ""
    else:
        AESobj = AES.new(Key, AES.MODE_ECB)
        ARC2obj = ARC2.new(Key + Key)
        ARC4obj = ARC4.new(Key + Key + Key)
        m3 = ARC4obj.encrypt(ARC2obj.encrypt(AESobj.encrypt(message)))
        return m3


####defintion pour le decryptage
def decrypt(message, Key=b'1a3b4c5e6d7f8g9h0i1j2k3l4m5n6o7p'):
    if len(message) == 0:
        return ""
    else:
        AESobj = AES.new(Key, AES.MODE_ECB)
        ARC2obj = ARC2.new(Key + Key)
        ARC4obj = ARC4.new(Key + Key + Key)
        m3 = AESobj.decrypt(ARC2obj.decrypt(ARC4obj.decrypt(message)))
        return m3


####adaptation de la longeur du message pour qu il soit multiple de 16 (plus ajout du hash)
def adaptline(line, div):
    pre_chk = checksum(line)
    print("line: {}, pre_chk: {}".format(len(line),len(pre_chk)))
    lena = len(line + pre_chk)
    print("lena: ", lena)
    addnb = ((((lena / div) + 1) * div) - lena)
    print("addnb: ", addnb)
    if addnb > 0 and addnb < 10: addnb = addnb + div
    lenad = len(str(addnb))
    print("lenad: ", lenad)
    nline = str(addnb) + (int((addnb - lenad)) * " ") + line + pre_chk
    return nline


####suppression des caracteres ajouter lors de l'adaptation (plus verification du hash)
def realeaseline(line):
    n = line[0:2:1]
    new = line[int(n):int(len(line)):1]
    message = new[0:len(new) - 56:1]
    chk = new[len(new) - 56::1]
    if checksum(message) == chk:
        return message


####fonction de cryptage pour un fichier
def cryptfile(original_filename, Key, destination_filename):
    line_file = ""
    FILE_O = open(original_filename, "r")
    FILE_D = open(destination_filename, "w")
    for line in FILE_O:
        line_file = line_file + line
    line_file = adaptline(line_file, 16)
    crypt_line = crypt(line_file, Key)
    FILE_D.writelines(crypt_line)

    FILE_O.close()
    FILE_D.close()


# fonctionde decryptage pour un fichier
def decryptfile(original_filename, Key, destination_filename):
    line_file = ""
    FILE_O = open(original_filename, "r")
    FILE_D = open(destination_filename, "w")
    for line in FILE_O:
        line_file = line_file + line
    crypt_line = decrypt(line_file, Key)
    crypt_line = realeaseline(crypt_line)
    FILE_D.writelines(crypt_line)
    FILE_O.close()
    FILE_D.close()


# fonction main
# argument 1: ['c','C','Crypt','CRYPT'] pour crypter
#	      quoi que ce soit d'autre pour decrypter
#
# argument 2: cle à utiliser pour crypter ou decrypter (multiple de 16 caractères) (A-Z/a-z/1-9)
#
# argument 3: fichier d origine (a crypter)
#
# argument 4: fichier de destination (crypter)
######
if sys.argv[1] in ["c", "C", "Crypt", "CRYPT"]:
    cryptfile(sys.argv[3], sys.argv[2], sys.argv[4])
else:
    decryptfile(sys.argv[3], sys.argv[2], sys.argv[4])

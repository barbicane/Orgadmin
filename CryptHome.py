# encoding: utf-8

# encryptage et decryptage des fichier image
from datetime import datetime

from Crypto.Cipher import AES
from Crypto.Protocol import KDF
from io import BytesIO
from AppVar import Global


class CryptHome(object):
    __key = b"this is the secret key that doesn't be know by anyone!"

    @staticmethod
    def encryptFile(InfileName, filename=False):
        #print("_____ procedure de cryptage_____")
        dKey = CryptHome.__keyGen(CryptHome.__key)
        OutfileName, Ifile, Ofile = "", None, None
        lineFile = b""
        cipher = AES.new(dKey, AES.MODE_CFB)
        if not filename:
            OutfileName = Global.dataDirPath + "\\" + CryptHome.__fileNameGen()
        else:
            OutfileName = filename
        try:
            Ifile = open(InfileName, "rb")
            for line in Ifile.readlines():
                lineFile += line
        except IOError:
            print("error Infile")
            return False
        finally:
            Ifile.close()
        ClineFile = cipher.iv + cipher.encrypt(lineFile)
        try:
            Ofile = open(OutfileName, "wb")
            Ofile.write(ClineFile)
        except IOError:
            print("error Outfile")
            return False
        finally:
            Ofile.close()
        return OutfileName

    @staticmethod
    def decryptFile(fileName):
        #print("_____ procedure de decryptage_____")
        dKey = CryptHome.__keyGen(CryptHome.__key)
        lineFile, Ifile = b"", None
        cipher = AES.new(dKey, AES.MODE_CFB)
        try:
            Ifile = open(fileName, "rb")
            for line in Ifile.readlines():
                lineFile += line
        except IOError:
            return False
        finally:
            Ifile.close()
        return BytesIO(cipher.decrypt(lineFile)[16:])

    @staticmethod
    def __keyGen(passPhrase):
        key_size = 32
        iteration = 2206
        salt = b"this could be random but i don't believe in chance"
        dKey = KDF.PBKDF2(passPhrase, salt, key_size, iteration)
        return dKey

    @staticmethod
    def __fileNameGen():
        """systeme de nommage de fichier qui retourne un nom formaté par date année/mois/jour/heure/minute/seconde"""
        filename = str(datetime.today().year) + str(datetime.today().month) + str(datetime.today().day) + str(
            datetime.today().hour) + str(datetime.today().minute) + str(datetime.today().second) + ".bin"
        return filename

if __name__ == "__main__":
    rep = input("Would you Encrypt or Decrypt ? ")
    fName = input("enter the file name with the extension : ")
    if rep in ["encrypt", "e", "E"]:
        CryptHome.encryptFile(fName)
    else:
        file = open("contents\\image.png", "wb")
        data = CryptHome.decryptFile(fName)

        file.writelines(data.readlines())
        print("Ok")

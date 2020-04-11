# encoding: utf-8

#convertion des images au format adapté
import tempfile

from PIL import Image


class Convert(object):
    """convertir une image en fichier png pour etre lu par l'application"""

    @staticmethod
    def toPng(inFile):
        if inFile[-4:] in [".pdf", ".PDF"]:
            return Convert.__frompdf(inFile)
        else:
            return Convert.__fromimage(inFile)

    @staticmethod
    def __frompdf(inFile):
        """prend en charge la conversion des pdf"""
        print("disponible prochainement...")

    @staticmethod
    def __fromimage(inFile):
        """prend en charge la conversion des images"""
        tmp = tempfile.NamedTemporaryFile(delete=False)
        img = None
        try:
            img = Image.open(inFile)
        except IOError:
            return IOError
        #img.show()
        img.save(tmp, "PNG")
        img.close()
        return tmp.name

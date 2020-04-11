import tempfile
from io import BytesIO

from PIL import Image
import os
# le fichier est cree et ouvert simultanement
# si delete = False a la fermeture le fichier n'est pas suprimé
t = tempfile.NamedTemporaryFile(delete=False)
#t.close()
print(t.name)
#Image.open(os.path.expanduser("~\\Pictures\\PC-ALCO - WIN_20150711_182703_edited.jpg"))
img = Image.open(os.path.expanduser("~\\Pictures\\PC-ALCO - WIN_20150711_182703_edited.jpg"))
img.show()
#print(t.getvalue())
img.save(t, "PNG")
img.close()
#print(t.getvalue())
ddimg = Image.open(t)
ddimg.show()
ddimg.close()
t.close()
o = open(t.name, "rb")
print(o.readline())
a = input("would you close the file ?")

t.close()
o.close()
os.remove(t.name)

#img.save(os.path.expanduser("~\\Pictures\\test.png"))

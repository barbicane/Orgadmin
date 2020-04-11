# coding: utf8

__autor__ = "ALCODORI François"
__credits__ = ["ALCODORI François"]
__licences__ = "GPL"
__status__ = "Development"
__versions__ = "1.0.0"

from tkinter import *
from AddWin import AddDocuments
from AppVar import Global
from ExtraWidgets import Search, InfoViewer, ListAdd, AddBtn, Dialog


class MainWindows(Frame):
    """class generant la fenetre principale"""
    def __init__(self, boss=None,user=None, **options):
        self.user, self.boss, self.id = user, boss, {}
        self.gbd = boss.gbd
        Frame.__init__(self, **options)
        self.master.title("Orgadmin")
        self.width, self.height, = int((self.winfo_screenwidth() / 3) * 2), int((self.winfo_screenheight() / 3) * 2 + 30)
        # calcul du centrage de la fenetre
        self.widthC, self.heightC = int((self.master.winfo_screenwidth()-self.width)/2),\
                                    int((self.master.winfo_screenheight()-self.height)/2)

        #print(self.width, self.height)
        self.master.geometry("{}x{}+{}+{}".format(self.width, self.height, self.widthC, int(self.heightC/2)))
        # nom de l'application
        self.img = PhotoImage(file=Global.pathFile["shutdownIconBtn"])
        self.quit = Button(image=self.img, width=30, height=30, relief=FLAT, bg="red", command=self.disconnect)
        self.quit.image = self.img
        self.quit.pack(anchor=NW)
        Label(self, text="Bienvenue "+self.user, font=Global.fonts["default"]).pack()
        # instanciation des widgets
        self.panSearchAdd = Frame(self, height=int(self.height/4))
        self.panInfodocTache = Frame(self, height=int(self.height/4*3))
        # widget search
        self.search = Search(self.panSearchAdd, self.search)
        #self.search.entry.config(width=40)

        #widget add
        self.panBtn = Frame(self.panSearchAdd)
        self.addDoc = AddBtn(self.panBtn, bg="orange", width=80, height=80, command=self.callAddDoc, relief=FLAT)
        # widget servant a afficher les info sur les docment recherché
        heading = [["nomDocument", "Nom du Document"], ["date", "Date Validité"], ["emplacement", "Emplacement"]]
        column = [["nomDocument", 2], ["date", 6],
                  ["emplacement", 4]]
        # TODO mettre en place le systeme de todo list
        self.infoDoc = InfoViewer(self.panInfodocTache, treeHeading=heading, treeColumn=column, width=600, height=300, bg="white")
        # self.infoDoc.config(bg="red")
        self.infoDoc.pack(side=LEFT, anchor=N, fill=BOTH)
        self.tache = ListAdd(self.panInfodocTache, contextWindow="mainwin", width=20, height=11)
        self.tache.pack(side=RIGHT)

        #affichage des widgets
        self.panSearchAdd.pack(fill=BOTH, expand=True)
        self.panInfodocTache.pack(fill=BOTH, expand=True, padx=20)
        self.search.pack(padx=60, ipadx=100, anchor=CENTER, side=LEFT)
        self.panBtn.pack(padx=50, pady=25, side=RIGHT, fill=BOTH, expand=True)
        self.addDoc.pack()
        Label(self.panBtn, text="Ajouter", fg=Global.colors["AddBtn"]["AddBtn"], font=Global.fonts["default"]).pack()
        self.pack(expand=True)

    def search(self, req):
        """execute la recheche associé dans la base de données"""
        #print("search mainWin : {}".format(req))
        data = self.boss.search(req)
        #print("data ", data)
        self.infoDoc.clean()
        for d in data:
            self.infoDoc.set(d)


    def callAddDoc(self):
        """appelle la fenetre d'ajout de documents"""
        add = AddDocuments(self)
        self.wait_window(add)

    def disconnect(self):
        awr = Dialog(self, "Deconnection", "Souhaitez vous vraiment vous déconnecter ?")
        print(awr.result)
        if awr.result:
            self.master.destroy()
            self.boss.startAuthWindow()
        else:
            pass


if __name__ == "__main__":
    app = MainWindows()
    app.mainloop()

# coding: utf8

# gestion de la fenetre d'ajout de documents
import os

from Conversion import Convert
from CryptHome import CryptHome

__autor__ = "ALCODORI François"
__credits__ = ["ALCODORI François"]
__licences__ = "GPL"
__status__ = "Development"
__versions__ = "1.0.0"

from tkinter import *
from tkinter.ttk import Combobox
from ExtraWidgets import ListAdd, InfoViewer, AddBtn, ComboboxDate, Dialog, ListFileBox
from AppVar import Global


class AddDocuments(Toplevel):
    """class qui gere la fenetre d'ajout de documents"""

    def __init__(self, boss):
        Toplevel.__init__(self, boss)
        # print(self.winfo_reqwidth(), self.winfo_width())
        # memorise les id des widget pour retrouver leur phrase par defaut
        self.id = {}
        self.gbd = boss.gbd
        self.title(Global.defaultText["AddDocuments"]["title"])
        self.titre = Label(self, text=Global.defaultText["AddDocuments"]["title"], font=Global.fonts["default"])
        self.titre.pack(ipady=10)
        self.info = Label(self, text="")
        self.info.pack()
        self.filePath = {}
        self.mPanLeft = Frame(self)
        self.mPanRight = Frame(self)

        # champs nom doc
        self.eNameDoc = Entry(self.mPanLeft, width=25)
        self.id[self.eNameDoc.winfo_id()] = "eNameDoc"
        self.eNameDoc.insert(0, Global.defaultText["AddDocuments"][self.id[self.eNameDoc.winfo_id()]])
        self.eNameDoc.configure(fg="grey", bg="grey80", font=Global.fonts["default"], relief=FLAT)
        self.eNameDoc.pack(ipady=5)

        # label date
        self.lDate = Label(self.mPanLeft, text=Global.defaultText["AddDocuments"]["lDate"],
                           font=Global.fonts["default"])
        self.lDate.pack()
        # champs date
        panDate = Frame(self.mPanLeft)
        # date debut
        self.eDateB = ComboboxDate(panDate, dateformat="my")
        self.eDateB.cYear.current(2)
        self.id[self.eDateB.winfo_id()] = "eDateB"
        self.eDateB.pack(side=LEFT, ipady=5, padx=10)
        # mot liaison
        Label(panDate, text=Global.defaultText["AddDocuments"]["labelDate"],
              font=(Global.fonts["default"][0], 14)).pack(side=LEFT)
        # date fin
        self.eDateE = ComboboxDate(panDate, dateformat="my")
        self.eDateE.cYear.current(1)
        self.id[self.eDateE.winfo_id()] = "eDateE"
        self.eDateE.pack(side=LEFT, ipady=5, padx=10)
        panDate.pack()

        # panneau emplacement
        panEmpl = Frame(self.mPanLeft)
        Label(panEmpl, text=Global.defaultText["AddDocuments"]["labelEmpl"],
              font=(Global.fonts["default"][0], 14)).pack()
        heading = [["nomClasseur", "Nom du Classeur"], ["couleur", "Couleur"], ["emplacement", "Emplacement"],
                   ["date", "Date Validité"]]
        column = [["nomClasseur", 4], ["couleur", 4], ["emplacement", 4], ["date", 4]]
        self.listEmpl = InfoViewer(panEmpl, heading, column, width=400)
        self.insertInfo()
        self.listEmpl.pack(fill=X)
        panEmpl.pack(pady=10)

        # bouton addClasseur
        self.addClasseur = AddBtn(panEmpl, bg="orange", width=30, height=30, command=self.callAddClass, relief=FLAT)
        self.addClasseur.pack(side=RIGHT)
        # bouton delClasseur
        self.delClasseur = AddBtn(panEmpl, "del", bg="red", width=30, height=30, command=self.effacerClasseur,
                                  relief=FLAT, state=DISABLED)
        # permet d'activer ou desactiver le bouton delClasseur
        self.listEmpl.tree.bind("<<TreeviewSelect>>", lambda event: self.delClasseur.toggleState(value=1))
        self.listEmpl.tree.bind("<<TreeviewRefresh>>", lambda event: self.delClasseur.toggleState(value=0))
        self.delClasseur.pack(side=RIGHT)

        # affichage panneau gauche
        self.mPanLeft.pack(side=LEFT, ipadx=5, ipady=5)

        # placement du taglist
        self.tagList = ListAdd(self.mPanRight, "AddTags", height=5)
        self.id[self.tagList.winfo_id()] = "tagList"
        self.tagList.pack(pady=5, anchor=N)

        # composite ajout de fichier
        subPanDoc = Frame(self.mPanRight)
        # bouton ajout d'un fichier document
        # self.fileDoc = AddBtn(subPanDoc, "adddoc", width=30, height=30, command=self.setFilePath, relief=FLAT,
        #                       bg="lightgreen")
        # self.fileDoc.pack(side=LEFT)
        # label de fichier chargé
        # self.fileLabel = Label(subPanDoc, bg="white", width=23, text=Global.defaultText["AddDocuments"]["fileLabel"])
        # self.fileLabel.pack(ipady=8, side=RIGHT)
        # self.fileBox = ListFileBox(subPanDoc, command=self.setFilePath, height=5)
        self.fileBox = ListFileBox(subPanDoc, height=5)
        self.fileBox.pack(pady=5, anchor=N)
        subPanDoc.pack(pady=5)

        # placement bouton ajouter
        self.btnAjout = Button(self.mPanRight, command=self.getData, text="Ajouter")
        self.btnAjout.configure(bg="lightgreen", font=(Global.fonts["default"][0], 14), relief=FLAT)
        self.btnAjout.pack(ipadx=20, pady=5)

        # placement bouton Fermer
        self.btnClose = Button(self.mPanRight, command=self.destroy, text="Fermer")
        self.btnClose.configure(bg="darkred", fg="white", font=(Global.fonts["default"][0], 14), relief=FLAT)
        self.btnClose.pack(ipadx=20, pady=5)

        # affichage panneau droit
        self.mPanRight.pack(side=LEFT, ipadx=5, ipady=5)

        # attribut les evenements a tout les widget entry
        for w in (self.eNameDoc, self.eDateB, self.eDateE):
            w.bind("<Button-1>", self.emptyEntry)
            w.bind("<FocusOut>", self.emptyEntry)
        # print(self.winfo_reqwidth(), self.winfo_width())
        self.grab_set()

    def emptyEntry(self, event):
        """vide l'entry seulement si le texte present correspond au texte par defaut"""
        try:
            data = event.widget
        except:
            data = event
        if self.checkEmpty(data) == 1:
            data.configure(fg="grey")
            data.insert(0, Global.defaultText["AddDocuments"][self.id[data.winfo_id()]])
        elif self.checkEmpty(data) == 2:
            data.delete(0, END)
            data.configure(fg="black")
        else:
            pass

    def callAddClass(self):
        """appelle la fenetre ajout de classeurs"""
        add = AddClasseurs(self, self.listEmpl.set)
        self.wait_window(add)

    def checkEmpty(self, event):
        """verifie si le champ est vide ou contient le texte par defaut"""
        try:
            data = event.widget
        except:
            data = event
        if data.get() == "":
            return 1
        elif data.get() == Global.defaultText["AddDocuments"][self.id[data.winfo_id()]]:
            return 2
        else:
            return 0

    def getData(self):
        """permet de recuperer les donnees contenu dans les champs du formulaire"""
        champs = []
        dateV = "-".join([self.eDateB.get(), self.eDateE.get()])
        # print(dateV)
        # conversion des tagList en string
        tagList = ""
        for t in self.tagList.get():
            tagList += t + ";"
        tagList = tagList[:-1]
        # print(tagList)
        for data in (self.eNameDoc, dateV, tagList):
            if data.__class__ == "".__class__:
                champs.append(data)
            elif self.checkEmpty(data) == 0:
                champs.append(data.get())
            else:
                self.info.configure(text="Certaines informations sont manquantes ou incorrectes", fg="red")
                self.info.after(1500, lambda: self.info.configure(text="", fg="black"))
                return False

        reqClasseur = "SELECT classeurs_id FROM classeurs WHERE nom = \"{}\"".format(self.listEmpl.get()[0])
        champs.append(self.gbd.exeReq(reqClasseur)[0][0])
        self.filePath = self.fileBox.getFilePath()
        print(self.filePath)
        if len(self.filePath.keys()) != 0:
            files = []
            for k, v in self.filePath.items():
                print(k, v)
                pngFile = Convert.toPng(v)
                print(pngFile)
                files.append("\"{}\"".format(CryptHome.encryptFile(pngFile)))
                os.remove(pngFile)
            i = None
            champs.append(", ".join(files))

        else:
            i = -1
        self.gbd.insertData("documents", ["nom", "date_v", "tags", "classeurs_id", "pathfile"][:i], champs)
        self.info.configure(text="Le document a été ajouté", fg="green")
        self.info.after(1500, lambda: self.info.configure(text="", fg="black"))
        self.after(1500, self.clean)

    def recupClasseur(self):
        """recupere la liste des classeur dans la bdd"""
        req = "SELECT nom,couleur,emplacement,periode FROM classeurs"
        data = self.gbd.exeReq(req)
        #print(data)
        return data

    def insertInfo(self):
        """insere les données dans le tableau classeurs"""
        for v in self.recupClasseur():
            self.listEmpl.set(values=v)



    def updateInfo(self):
        """met a jour la list d'emplacement"""
        self.listEmpl.clean()
        self.insertInfo()

    def effacerClasseur(self, event=None):
        """efface le classeur selectionné de la base de donnée"""
        # verifier si il y a des documents dans le classeur avant de le supprimer
        # selction id classeur
        idClass = \
            self.gbd.exeReq("SELECT classeurs_id FROM classeurs WHERE nom = \"{}\"".format(self.listEmpl.get()[0]))[0][
                0]
        warning = Dialog(self, "Attention",
                         "Cette action est définitive et ne pourra pas être annulée\n Souhaitez-vous "
                         "Continuer ?").result
        # print("idClass ", idClass)
        if not warning:
            return 0
        # recherche de documents dans ce classeur
        docs = self.gbd.exeReq("SELECT * FROM documents WHERE classeurs_id = \"{}\"".format(idClass))
        # print("docs ", docs, "idClass ", idClass)
        if len(docs) != 0:
            eraseConfirm = Dialog(self, "Attention", "Des Documents sont présents dans ce classeur.\n"
                                                     "La suppression de ce dernier entraînera également la supression des "
                                                     "documents rattachés.\n\n"
                                                     "Souhaitez-vous Continuer ?").result
            if not eraseConfirm:
                return 0
            # suppression des docs relatif au classeur
            reqDoc = "DELETE FROM documents WHERE classeurs_id = \"{}\"".format(idClass)
            self.gbd.exeReq(reqDoc)
        # supression du classeur
        reqClass = "DELETE FROM classeurs WHERE classeurs_id = \"{}\"".format(idClass)
        resultDelete = self.gbd.exeReq(reqClass)
        # print("resultDelete ", resultDelete)
        self.updateInfo()

    def clean(self):
        """reinitialise la fenetre ajout de documents"""
        self.eNameDoc.delete(0, END)
        self.eNameDoc.configure(fg="grey")
        self.eNameDoc.insert(0, Global.defaultText["AddDocuments"][self.id[self.eNameDoc.winfo_id()]])
        self.eDateB.cMonth.current(0)
        self.eDateB.cYear.current(2)
        self.eDateE.cMonth.current(0)
        self.eDateE.cYear.current(1)
        self.tagList.clean()


class AddClasseurs(Toplevel):
    """class qui permet d'entrer un nouveau classeur dans la base de donnée"""

    def __init__(self, boss, command=None):
        Toplevel.__init__(self, boss)
        self.command = command
        self.title(Global.defaultText["AddDocuments"]["title"])
        self.colors = ["rouge", "jaune", "vert", "bleu", "blanc", "noir", "rose", "violet", "gris"]
        panNomClr = Frame(self)
        Label(self, text="Ajouter un classeur", font=Global.fonts["default"]).pack()
        self.infoL = Label(self, text="", fg="red")
        self.infoL.pack()
        panNomED = Frame(self)
        Label(panNomED, text="Non du classeur").pack(side=LEFT, padx=80)
        Label(panNomED, text="Couleur").pack(side=RIGHT)
        panNomED.pack()
        self.nomClass = Entry(panNomClr, bg="grey80", font=Global.fonts["default"], relief=FLAT)
        self.nomClass.pack(side=LEFT, pady=5, padx=5)
        self.nomClass.bind("<FocusIn>", self.reset)
        self.nomClass.bind("<Button-1>", self.reset)
        self.nomClass.bind("<FocusOut>", self.checkEmpty)
        self.colorSelect = StringVar(value=self.colors[0])
        self.color = Combobox(panNomClr, textvariable=self.colorSelect, values=self.colors, state="readonly", width=10,
                              height=10)
        self.color.pack(side=RIGHT, padx=5)

        panNomClr.pack()

        panNomED = Frame(self)
        Label(panNomED, text="Emplacement").pack(side=LEFT, padx=80)
        Label(panNomED, text="Date validité").pack(side=RIGHT)
        panNomED.pack()

        panEmpDate = Frame(self)
        self.Empl = Entry(panEmpDate, bg="grey80", font=Global.fonts["default"], relief=FLAT)
        self.Empl.bind("<FocusIn>", self.reset)
        self.Empl.bind("<Button-1>", self.reset)
        self.Empl.bind("<FocusOut>", self.checkEmpty)
        self.Empl.pack(side=LEFT, pady=5, padx=5)
        self.dateD = ComboboxDate(panEmpDate, dateformat="y")
        self.dateD.cYear.current(2)
        self.dateD.pack(side=LEFT, padx=2)
        self.dateF = ComboboxDate(panEmpDate, dateformat="y")
        self.dateF.cYear.current(1)
        self.dateF.pack(side=LEFT, padx=2)
        panEmpDate.pack(padx=5)
        panBtn = Frame(self)
        self.btnAdd = Button(panBtn, command=self.getData, text="Ajouter")
        self.btnAdd.configure(bg="lightgreen", font=(Global.fonts["default"][0], 14), relief=FLAT)
        self.btnAdd.pack(side=LEFT, ipadx=20, pady=5, padx=10)
        self.btnClose = Button(panBtn, command=self.close, text="Fermer")
        self.btnClose.configure(bg="darkred", fg="white", font=(Global.fonts["default"][0], 14), relief=FLAT)
        self.btnClose.pack(side=LEFT, ipadx=20, pady=5, padx=10)
        panBtn.pack(side=RIGHT)
        self.grab_set()

    def reset(self, event):
        """reinitialise les parametre de widget"""
        try:
            data = event.widget
        except:
            data = event
        data.configure(bg="grey80")

    def checkEmpty(self, event):
        """verifie si le champ est vide ou contient le texte par defaut"""
        try:
            data = event.widget
        except:
            data = event
        if data.get() == "":
            return 1
        else:
            return 0

    def getData(self):
        """fonction qui recupere les données dans les differents champ"""
        data, dates = [], []
        for d in (self.nomClass, self.color, self.Empl):
            if d == self.nomClass or d == self.Empl:
                if self.checkEmpty(d):
                    d.configure(bg="red")
                    self.infoL.configure(text="Un champs est manquant")
                    d.after(1000, lambda: d.configure(bg="grey80"))
                    self.infoL.after(1000, lambda: self.infoL.configure(text=""))
                    return False
            data.append(d.get())
        for dt in (self.dateD, self.dateF):
            dates.append(dt.get())
        data.append("-".join(dates))
        # controle que le nom de classeur n'hexiste pas deja dans la bdd
        req = "SELECT nom FROM classeurs WHERE nom = \"{}\"".format(data[0])
        #print(req, self.master.gbd.exeReq(req), data[0])
        try:
            if self.master.gbd.exeReq(req)[0][0] == data[0]:
                self.infoL.configure(text="Le classeur existe déja")
                self.after(1500, self.clean)
                return False
        except:
            self.infoL.configure(fg="green")
            self.infoL.configure(text="Ajout du classeur")
        # envoi des donnees a la base de donné
        self.master.gbd.insertData("classeurs", ["nom", "couleur", "emplacement", "periode"], data)
        try:
            self.command(values=data)
        except:
            return data
        finally:
            self.after(1500, self.clean)

    def clean(self):
        self.infoL.configure(text="")
        self.nomClass.delete(0, END)
        self.Empl.delete(0, END)
        self.color.current(0)
        self.dateD.cYear.current(2)
        self.dateF.cYear.current(1)

    def close(self):
        """ferme la fenetre"""
        self.grab_release()
        self.destroy()
        return self.master.grab_set()


if __name__ == "__main__":
    sat = AddDocuments(None)
    sat.mainloop()

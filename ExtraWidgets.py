# coding: utf8

# widget adapté à l'interface graphique
import pickle
import tempfile
from datetime import date, datetime
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Treeview, Combobox

# from reportlab.lib import pdfencrypt
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, flowables
from unidecode import unidecode

from AppVar import *
from CryptHome import CryptHome

__autor__ = "ALCODORI François"
__credits__ = ["ALCODORI François"]
__licences__ = "GPL"
__status__ = "Development"
__versions__ = "1.0.0"


class Search(Frame):
    """widget recherche des documents dans la base de données"""

    def __init__(self, boss, exeCommand, **options):
        """instance creant le widget search"""
        self.id, self.command = {}, exeCommand
        Frame.__init__(self, boss, **options)
        self.sIcon = PhotoImage(file=Global.pathFile["searchIcon"], width=30, height=30)
        self.entry = Entry(self, bg="grey80", fg="grey", font=Global.fonts["default"], relief=FLAT)
        self.id[self.entry.winfo_id()] = "entry"
        self.entry.insert(0, Global.defaultText["Search"]["entry"])
        # self.entry.bind("<Enter>", self.toggleColor)
        # self.entry.bind("<Leave>", self.toggleColor)
        self.searchBtn = Button(self, image=self.sIcon, relief=FLAT, bg=Global.colors["Search"]["searchBtn"],
                                command=self.search)
        self.id[self.searchBtn.winfo_id()] = "searchBtn"
        # self.searchBtn.bind("<Enter>", self.toggleColor)
        # self.searchBtn.bind("<Leave>", self.toggleColor)
        self.entry.bind("<Return>", self.search)

        for w in (self.entry, self.searchBtn):
            if w == self.entry:
                w.bind("<Button-1>", self.emptyEntry)
                w.bind("<FocusOut>", self.checkEmpty)
            w.bind("<Enter>", self.toggleColor)
            w.bind("<Leave>", self.toggleColor)

        # affichage des composants
        self.entry.pack(ipady=10, padx=5, fill=X, expand=True, side=LEFT)
        self.searchBtn.pack(padx=5, ipady=8, ipadx=8, side=RIGHT)
        self.pack()

    def search(self, event=None):
        """fonction qui declenche la recherche dans la base de données"""
        # print(self.entry.get())
        req = self.entry.get()
        # print(self.command)
        self.emptyEntry(widget=self.entry)
        self.command(req)

    def toggleColor(self, event):
        """modifie couleur du bouton quand souris entre ou sort"""
        if int(event.type) == 7:
            event.widget.configure(bg=Global.colors["Search"]["over_{}".format(self.id[event.widget.winfo_id()])])
        elif int(event.type) == 8:
            event.widget.configure(bg=Global.colors["Search"][self.id[event.widget.winfo_id()]])
        else:
            # print("error")
            pass

    def emptyEntry(self, event=None, widget=None):
        """vide l'entry passé en event"""
        if event:
            event.widget.delete(0, END)
            event.widget.configure(fg="black")
        else:
            widget.delete(0, END)
            widget.configure(fg="black")

    def checkEmpty(self, event):
        """verifie si champ vide remetttre texte par defaut"""
        if event.widget.get() == "":
            # print(self.eNameDoc.winfo_id())
            event.widget.configure(fg="grey")
            event.widget.insert(0, Global.defaultText["Search"]["entry"])
            # print("fait")
        else:
            pass


class ListAdd(Frame):
    """widget ListBox avec possibilité d'ajouter des elements dans cette liste"""

    def __init__(self, boss, contextWindow=None, **options):
        self.id = {}
        if not contextWindow:
            self.context = Global.defaultText["ListAdd"]["default"]
        else:
            self.context = Global.defaultText["ListAdd"][contextWindow]
        Frame.__init__(self, boss, **options)
        # panneau listbox + scroll
        panlb = Frame(self)
        # creation de la listBox width=self.width, height=5,
        self.lB = Listbox(panlb, relief=FLAT, font=(Global.fonts["default"][0], 12), **options)
        self.id[self.lB.winfo_id()] = "lB"
        self.lB.pack(pady=4, side=LEFT, fill=BOTH, expand=True)

        # creation de scrollbar
        self.scroll = Scrollbar(panlb)
        # parametrage de listbox
        self.lB.configure(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.lB.yview)
        self.scroll.pack(side=RIGHT, pady=4, fill=BOTH)

        panlb.pack(fill=BOTH, expand=True)

        # creation de l'entry
        self.entree = Entry(self, fg="grey", bg=Global.colors["ListAdd"]["entree"], relief=FLAT,
                            font=(Global.fonts["default"][0], 12))
        self.id[self.entree.winfo_id()] = "entree"
        self.entree.insert(0, self.context["entree"])
        self.entree.bind("<Return>", self.addItem)
        self.entree.pack(ipady=6, side=LEFT, fill=X, expand=True)

        # creation du bouton ajout
        self.icon = PhotoImage(file=Global.pathFile["addIcon"], width=30, height=30)
        self.addBtn = Button(self, image=self.icon, bg=Global.colors["ListAdd"]["addBtn"],
                             font=(Global.fonts["default"][0], 24), relief=FLAT, command=self.addItem)
        self.id[self.addBtn.winfo_id()] = "addBtn"
        self.addBtn.pack(side=RIGHT, padx=3)

        # liaison event color
        for w in (self.entree, self.addBtn):
            if w == self.entree:
                w.bind("<Button-1>", self.emptyEntry)
                w.bind("<FocusOut>", self.checkEmpty)
            w.bind("<Enter>", self.toggleColor)
            w.bind("<Leave>", self.toggleColor)

    def addItem(self, event=None):
        """ insere le texte dans la liste"""
        self.lB.insert(END, self.entree.get())
        self.emptyEntry(widget=self.entree)

    def toggleColor(self, event):
        """modifie couleur du bouton quand souris entre ou sort"""
        if int(event.type) == 7:
            event.widget.configure(bg=Global.colors["ListAdd"]["over_{}".format(self.id[event.widget.winfo_id()])])
        elif int(event.type) == 8:
            event.widget.configure(bg=Global.colors["ListAdd"][self.id[event.widget.winfo_id()]])
        else:
            # print("error")
            pass

    def emptyEntry(self, event=None, widget=None):
        """vide l'entry passé en event"""
        if event:
            event.widget.delete(0, END)
            event.widget.configure(fg="black")
        else:
            widget.delete(0, END)
            widget.configure(fg="black")

    def checkEmpty(self, event):
        """verifie si champ vide remetttre texte par defaut"""
        if event.widget.get() == "":
            event.widget.configure(fg="grey")
            event.widget.insert(0, self.context["entree"])
        else:
            pass

    def clean(self):
        self.lB.delete(0, END)
        self.entree.configure(fg="grey")
        self.entree.insert(0, self.context["entree"])

    def get(self):
        """recupere et retourne la liste des tags"""
        return self.lB.get(0, END)

class ListFileBox(ListAdd):
    """class qui permet de charger une liste de fichier"""

    def __init__(self, boss, **options):
        ListAdd.__init__(self, boss)
        self.icon = PhotoImage(file=Global.pathFile["addDocIcon"], width=30, height=30)
        self.addBtn.configure(image=self.icon, command=self.__setFilePath)
        self.id[self.addBtn.winfo_id()] = "addBtn"
        self.entree.pack_forget()
        self.delBtn = AddBtn(self, "del", width=30,bg=Global.colors["DelBtn"]["AddBtn"],
                             font=(Global.fonts["default"][0], 24), relief=FLAT)
        self.delBtn.toggleState(value=0)
        self.delBtn.pack(side=LEFT, fill=X, expand=True)
        self.addBtn.pack(side=RIGHT, fill=X, expand=True, padx=3)
        self.filePath = {}

    def __addItem(self, event=None, value=None):
        """ajoute un nouvel item dans la ListBox"""
        self.lB.insert(END, value)
        print("ok")


    def __setFilePath(self, event=None):
        """ouvre une fenetre popup et recupere le chemin de fichier"""
        path = filedialog.askopenfilename(parent=self, filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")],
                                          title="Choisir un Fichier")
        if path != "":
            showPath = path[path.rfind("/") + 1:]
            print(showPath)
            self.filePath[showPath] = path
            self.__addItem(value=showPath)
        else:
            pass

    def getFilePath(self):
        return self.filePath

class InfoViewer(Frame):
    """widget de visualisation d'information documents (nom document, date, emplacements)"""

    def __init__(self, boss, treeHeading, treeColumn, **options):
        self.sashObservable, self.childObservable = [], []
        Frame.__init__(self, boss, **options)
        self.header = []
        for h in treeHeading:
            self.header.append(h[0])
        # print(self.header)
        self.tree = Treeview(self, columns=self.header, show="headings", selectmode="browse")
        self.tree.bind("<Double-Button-1>", self.openItem)
        for th in treeHeading:
            self.tree.heading(th[0], text=th[1])
        for tc in treeColumn:
            widthRatio = int(self.winfo_reqwidth() / tc[1])
            self.tree.column(tc[0], width=widthRatio)

        # treeId = self.tree.insert("", "end", values=("Baccalauréat Technologique", "12/02/34", "dans le placard"))
        # self.tree.insert("", "end", values=("Baccalauréat Technologique", "12/02/34", "dans le placard"))
        self.tree.pack(anchor=N, fill=BOTH, expand=True)

    def sashObserver(self, event=None):
        """observe l'event passé en argument et mes a jour les autres panedWindow"""
        # identification du sash
        isSash, sashCoord = event.widget.identify(event.x, event.y), None
        # print(isSash)
        if isSash == "":
            return
        elif isSash[1] == "sash":
            # recuperation des coordonnée du sash
            sashCoord = event.widget.sash_coord(isSash[0])
        else:
            return
        # application au autre sash
        for w in self.sashObservable:
            if event.widget == w:
                pass
            else:
                w.sash_place(isSash[0], sashCoord[0], sashCoord[1])

    def childObserver(self, event):
        """observe les event des listbox et met a jour les autres"""
        selec = event.widget.curselection()
        for w in self.childObservable:
            if w == event.widget:
                pass
            else:
                for i in selec:
                    w.activate(i)

    def clean(self):
        """efface toute les entree du widget"""
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.tree.event_generate("<<TreeviewRefresh>>")
        return self.tree

    def set(self, values):
        """methode qui permet d'afficher dans le tableau des information formaté"""
        self.tree.insert("", "end", values=values)

    def get(self):
        """recupere les information contenu dans le tableau"""
        # print(self.tree.item(self.tree.focus(), "values")[0])
        return self.tree.item(self.tree.focus(), "values")

    def openItem(self, event):
        data = self.tree.item(self.tree.focus(), "values")
        req1 = "SELECT pathfile FROM documents WHERE documents.documents_id = \"{}\"".format(data[4])
        ViewWindows(self, self.master.master.gbd.exeReq(req1)[0][0])


class ViewWindows(Toplevel):
    """instancie une fenetre de visualisation du document decrypté"""

    def __init__(self, boss, img):
        Toplevel.__init__(self, boss)
        self.title("Document: " + boss.get()[0])
        # TODO creer systematiquement fichier temporaire pour enregistrer modif sur image et faciliter impression
        self.tmpFile = tempfile.TemporaryFile(mode="w+b")
        # TODO prevoir pivotage image, page suivante, page precedente, zoom si possible
        self.btn = []
        cmd = ["sauvegarde", "imprimer", "tourner a gauche", "tourner a droite"]
        self.toolbox = Frame(self)
        c = 0
        for i in Global.menuIcon:
            im = PhotoImage(file=i)
            print(c, cmd[c])
            self.btn.append(Button(self.toolbox, image=im, relief=FLAT, command=self.saveDoc))
            self.btn[-1].image = im
            self.btn[-1].pack(side=LEFT, padx=5)
            c += 1
        self.toolbox.pack(fill=X)
        if img != None:
            if Global.dataDirPath not in img:
                img = Global.dataDirPath + "\\" + img
            decryptedImg = CryptHome.decryptFile(img)
            self.dataimg = b''
            if not decryptedImg:
                self.image = PhotoImage(file=Global.noImage)
            else:
                for line in decryptedImg.readlines():
                    self.dataimg += line
                # ecriture dans le fichier temporaire
                self.tmpFile.write(self.dataimg)
                self.image = PhotoImage(data=self.dataimg)
        else:
            self.image = PhotoImage(file=Global.noImage)
        can = Canvas(self, width=self.image.width(), height=self.image.height())
        can.create_image(self.image.width() / 2, self.image.height() / 2, image=self.image)
        can.pack()

    def saveDoc(self):
        """ouvre la fenetre de sauvegarde du document"""
        # TODO recuperer extension de l'image
        fileOptions = {'defaultextension': '.png',
                       'filetypes': [("PNG", ".png")],
                       'initialdir': os.path.expanduser("~"),
                       'initialfile': self.master.get()[0],
                       'parent': self.master,
                       'title': 'Enregistrer le fichier...'}
        path = filedialog.asksaveasfilename(**fileOptions)
        if path != '':
            writeFile = open(path, "wb")
            writeFile.write(self.dataimg)
            writeFile.close()
        else:
            return

    def printDoc(self):
        """lance l'impression du document"""
        os.startfile(self.master.get()[0], "print")

class AuthenticationWindows(Frame):
    """fenetre d'authentification utilisateur"""

    def __init__(self, boss=None, command=None):
        Frame.__init__(self, boss=None)
        self.user, self.pswd, self.pswdConf = StringVar(self), StringVar(self), StringVar(self)
        self.infoLabel, self.command = None, command
        # recherche ou creation d'un fichier texte contenant un dictionnaire avec un couple user passwd
        # decryptage et lecture du fichier
        # ecriture et encryptage du fichier
        # non du fichier
        self.userDataDictPath = Global.dataDirPath + "\\" + "UsrData.bin"
        self.userDataDict = self.__getUsrDataDict()
        Label(self, text="Orgadmin", font=(Global.fonts["default"][0], 20)).pack()
        self.currPan = self.__panConnect()
        self.currPan.pack()
        self.pack(padx=40, pady=10)
        self.mainloop()

    def connect(self):
        """connecte l'utilisateur a sa base de donnée"""
        if self.user.get() in self.userDataDict.keys():
            if self.pswd.get() == self.userDataDict[self.user.get()]:
                self.master.destroy()
                dbName = "Data" + self.user.get() + ".db".replace(" ", "")
                dbName = dbName.replace(" ", "")
                dbName = unidecode(dbName)
                userName = self.user.get().capitalize()
                self.command(userName, dbName)
            else:
                self.infoLabel.configure(text="Le mot de passe est incorrect", fg="dark red")
                self.infoLabel.after(1500, lambda: self.infoLabel.configure(text=""))
        else:
            self.infoLabel.configure(text="Le nom d'utilisateur est incorrect", fg="dark red")
            self.infoLabel.after(1500, lambda: self.infoLabel.configure(text=""))

    def addUser(self):
        """verifie correspondance des mots de passes doublons utilisateur et ajoute l'utilisateur """
        if self.user.get() == "":
            self.infoLabel.configure(text="Entrez un nom d'utilisateur", fg="dark red")
            self.infoLabel.after(1500, lambda: self.infoLabel.configure(text=""))
        elif self.user.get() in self.userDataDict.keys():
            self.infoLabel.configure(text="Nom d'utilisateur existant", fg="dark red")
            self.infoLabel.after(1500, lambda: self.infoLabel.configure(text=""))
        elif self.pswd.get() != self.pswdConf.get():
            self.infoLabel.configure(text="Mot de passe différent", fg="dark red")
            self.infoLabel.after(1500, lambda: self.infoLabel.configure(text=""))
        else:
            self.userDataDict[self.user.get()] = self.pswd.get()
            self.__setUsrDataDict()
            self.infoLabel.configure(text="Nouvel utilisateur ajouté", fg="dark green")
            self.infoLabel.after(1500, lambda: self.infoLabel.configure(text=""))

    def __connectPan(self):
        """initialise le panneau connection"""
        self.currPan.pack_forget()
        self.currPan = self.__panConnect()
        self.currPan.pack()

    def __newUserPan(self):
        """initialise le panneau nouvel utilisateur"""
        self.currPan.pack_forget()
        self.currPan = self.__panNewUser()
        self.currPan.pack()

    def __panConnect(self):
        """initialise le panneau pan connect"""
        panConnect = Frame(self)
        Label(panConnect, text="Veuillez vous identifier:", font=Global.fonts).pack()  # pady=20)
        self.infoLabel = Label(panConnect, text="")
        self.infoLabel.pack()
        # pan user
        panUser = Frame(panConnect)
        Label(panUser, text="Nom d'utilisateur").pack(side=LEFT, padx=10)
        Entry(panUser, textvariable=self.user, width=25, bg="grey80", relief=FLAT).pack(side=LEFT)
        panUser.pack(expand=True, anchor=E, pady=5)
        # pan passwd
        panPasswd = Frame(panConnect)
        Label(panPasswd, text="Mot de passe").pack(side=LEFT, padx=10)
        Entry(panPasswd, textvariable=self.pswd, show="●", width=25, bg="grey80", relief=FLAT).pack(side=LEFT)
        panPasswd.pack(expand=True, anchor=E)
        Button(panConnect, text="Connecter", bg=Global.colors["ListAdd"]["addBtn"], relief=FLAT,
               command=self.connect).pack(pady=10)
        Button(panConnect, text="Nouvel Utilisateur", bg=None, fg="dark blue", relief=FLAT,
               command=self.__newUserPan).pack(side=RIGHT)
        return panConnect

    def __panNewUser(self):
        panNU = Frame(self)
        Label(panNU, text="Ajouter nouvel utilisateur", font=Global.fonts).pack()
        self.infoLabel = Label(panNU, text="")
        self.infoLabel.pack()
        panUser = Frame(panNU)
        Label(panUser, text="Nom d'utilisateur").pack(side=LEFT, padx=10)
        Entry(panUser, textvariable=self.user, width=25, bg="grey80", relief=FLAT).pack(side=RIGHT)
        panUser.pack(expand=True, anchor=E, pady=5)

        panPasswd = Frame(panNU)
        Label(panPasswd, text="Mot de passe").pack(side=LEFT, padx=10)
        Entry(panPasswd, textvariable=self.pswd, show="●", width=25, bg="grey80", relief=FLAT).pack(side=RIGHT)
        panPasswd.pack(expand=True, anchor=E, pady=5)

        panPasswdConf = Frame(panNU)
        Label(panPasswdConf, text="Confirmer le mot de passe").pack(side=LEFT, padx=10)

        Entry(panPasswdConf, textvariable=self.pswdConf, show="●", width=25, bg="grey80", relief=FLAT).pack(side=RIGHT)
        panPasswdConf.pack(expand=True, anchor=E, pady=5)

        self.adduser = Button(panNU, text="Ajouter Utilisateur", bg=Global.colors["ListAdd"]["addBtn"], relief=FLAT,
                              command=self.addUser)
        self.adduser.pack(pady=10)
        Button(panNU, text="Retour", bg=None, fg="dark blue", relief=FLAT, command=self.__connectPan).pack(side=RIGHT)
        return panNU

    def __getUsrDataDict(self):
        """decrypte et recupere le dictionnaire userPswd present dans le fichier"""
        if not os.path.exists(self.userDataDictPath):
            return {}
        else:
            with tempfile.TemporaryFile() as file:
                file.write(CryptHome.decryptFile(self.userDataDictPath).getvalue())
                file.seek(0)
                return pickle.load(file)

    def __setUsrDataDict(self):
        """ecrit et crypte le dictionnaire userPswd dans le fichier"""
        with open(self.userDataDictPath, "wb") as file:
            pickle.dump(self.userDataDict, file)
        CryptHome.encryptFile(self.userDataDictPath, self.userDataDictPath)


class AddBtn(Button):
    """ creer un boutton ajouter"""

    def __init__(self, boss, mode="add", **options):
        self.id = {}
        if mode == "del":
            if options.get("width") < 60:
                self.addIcon = PhotoImage(file=Global.pathFile["delIcon"])
            else:
                self.addIcon = PhotoImage(file=Global.pathFile["delIconBtn"])
        elif mode == "add":
            if options.get("width") < 60:
                self.addIcon = PhotoImage(file=Global.pathFile["addIcon"])
            else:
                self.addIcon = PhotoImage(file=Global.pathFile["addIconBtn"])
        else:
            if options.get("width") < 60:
                self.addIcon = PhotoImage(file=Global.pathFile["addDocIcon"])
            else:
                self.addIcon = PhotoImage(file=Global.pathFile["addDocIconBtn"])
        # self.id[self.addIcon.winfo_id()] = "addIcon"
        Button.__init__(self, boss, image=self.addIcon, **options)
        self.color = self.cget("bg")
        self.bind("<Enter>", self.toggleColor)
        self.bind("<Leave>", self.toggleColor)

    def toggleColor(self, event):
        """modifie couleur du bouton quand souris entre ou sort"""
        if int(event.type) == 7:
            clr = self.color
            if 'light' in self.color:
                clr = self.color[5:]
                # print(clr)
            event.widget.configure(bg="dark " + clr)  # Global.colors["AddBtn"]["over_AddBtn"])
        elif int(event.type) == 8:
            event.widget.configure(bg=self.color)
        else:
            # print("error")
            pass

    def toggleState(self, event=None, value=None):
        """inverse l'etat du bouton"""
        if not value:
            if self.cget("state") == "disabled":
                self.configure(state=NORMAL)
            else:
                self.configure(state=DISABLED)
        else:
            if value == 1:
                self.configure(state=NORMAL)
            else:
                self.configure(state=DISABLED)


class ComboboxDate(Frame):
    """widget combox pour selectionner date"""

    def __init__(self, boss, dateformat="my", **kwargs):
        Frame.__init__(self, boss, **kwargs)
        year, month, day = [], [], []
        for y in range(date.today().year + 1, date.today().year - 20, -1):
            year.append(y)
        for m in range(1, 13):
            month.append(m)
        for d in range(1, 32):
            day.append(d)
        self.strVars = [StringVar(value=day[0]), StringVar(value=month[0]), StringVar(value=year[0])]
        self.cDay = Combobox(self, textvariable=self.strVars[0], values=day, width=2)
        self.cMonth = Combobox(self, textvariable=self.strVars[1], values=month, width=2)
        self.cYear = Combobox(self, textvariable=self.strVars[2], values=year, width=4)
        if "d" in dateformat:
            self.cDay.pack(side=LEFT)
        if "m" in dateformat:
            self.cMonth.pack(side=LEFT)
        if "y" in dateformat:
            self.cYear.pack(side=LEFT)

    def get(self):
        """recupere les information contenu dans les champs"""
        data = []
        for v in self.strVars:
            if v.get() != '':
                data.append(v.get())
            else:
                continue

        return "/".join(data)


class Dialog(Toplevel):
    def __init__(self, parent, title=None, text="Warning"):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.text = text
        self.result = None
        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=15, pady=15)
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))
        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        label = Label(master, text=self.text)
        return label.pack()

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Annuler", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()


    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
        return 0

    #
    # command hooks

    def validate(self):

        return 1  # override

    def apply(self):
        self.result = 1  # override


# cette classe ne sera pas utilisé pour l'instant
# class PdfConversion(object):
#     """fournit des outils pour traiter les pdf dans l'application"""
#
#     def imageConversion(self, imgPath):
#         """convertit l'image en fichier pdf"""
#         width, height = A4
#         # enregister nom pdf dans la base de donnée!!
#         pdfName = self.__namingPdf__()
#         doc = SimpleDocTemplate(pdfName, pagesize=(height, width))
#         elem = [flowables.Macro('canvas.saveState()'), flowables.Macro('canvas.restoreState()')]
#
#         pdfencrypt.encryptDocTemplate(doc, "test", "ownertest")
#         doc.build(elem, onFirstPage=self.__drawPageFrame__(imgPath))
#
#     def pdfEncryption(self):
#         """crypte le pdf"""
#
#     def pdfDecyption(self):
#         """decrypte le fichier"""
#
#     def __drawPageFrame__(canvas, doc):
#         width, height = A4
#         canvas.saveState()
#         canvas.drawImage(doc, 0, 0, height, width, preserveAspectRatio=True, anchor='c')
#         canvas.restoreState()
#
#     def __namingPdf__(self):
#         """systeme de nommage de pdf qui retourne un nom formaté par date année/mois/jour/heure/minute/seconde"""
#         pdfname = "File_" + str(datetime.today().year) + str(datetime.today().month) + str(datetime.today().day) + str(
#             datetime.today().hour) + str(datetime.today().minute) + str(datetime.today().second) + ".pdf"
#         return pdfname
#

if __name__ == "__main__":
    AuthenticationWindows().mainloop()

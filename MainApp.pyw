# encoding: utf8
import os
from tkinter import Tk

from ExtraWidgets import AuthenticationWindows

__autor__ = "ALCODORI François"
__credits__ = ["ALCODORI François"]
__licences__ = "GPL"
__status__ = "Development"
__versions__ = "1.0.0"

# pilote l'ensemble de l'application
from GestionSQLiteBD import GestionBD
from AppVar import Global
from MainWin import MainWindows


class Main(object):
    """class principale"""
# TODO pensser aux objets multipages!
    # TODO clic droit sur panneaux fichier > Modifier: modifie le document en renvoyant sur panneaux ajout de fichier
    # TODO                                   Effacer: demande confirmation avant suppression
    def __init__(self):
        self.activeWin, self.gbd, self.tableName = None, None, list(Global.tableDescr.keys())

        # cree le dossier orgadmin dan AppData\local si il n'hexiste pas
        if not os.path.exists(Global.dataDirPath):
            os.makedirs(Global.dataDirPath)
        self.startAuthWindow()

    def search(self, req=None):
        """effectue la recherche dans la base de donnée"""
        reqCreated = "SELECT documents.nom, date_v, classeurs.nom, documents.tags, documents.documents_id FROM documents INNER JOIN classeurs ON " \
                     "documents.classeurs_id = classeurs.classeurs_id WHERE documents.nom LIKE \"%{0}%\"" \
                     " OR documents.tags LIKE \"%{0}%\" OR documents.date_v LIKE \"%{0}%\"".format(req)
        dataReturn = self.gbd.exeReq(reqCreated)
        self.gbd.close()
        return dataReturn

    def startMainWindow(self, user, dbName):
        """initialise la base de donnée avec le nom associé et lance la fenetre principale"""
        try:
            self.activeWin.destroy()
        except:
            pass
        # connecte ou cree la base de donnée
        self.gbd = GestionBD(Global.dataDirPath+"\\"+dbName)#"Data.db")
        for table in self.tableName:
            self.gbd.createTable(table, Global.tableDescr.get(table))
        self.activeWin = MainWindows(self, user=user).mainloop()

    def startAuthWindow(self):
        try:
            self.activeWin.destroy()
        except :
            pass
        self.activeWin = AuthenticationWindows(command=self.startMainWindow)

Main()

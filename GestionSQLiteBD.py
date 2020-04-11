# coding: utf8

"""GestionSQLiteBD est une class interface gerant une base de donnée de type SQLite pour un usage local"""

__autor__ = "Acodori François"
__credits__ = ["Alcodori François"]
__licence__ = "GPL"
__versions__ = "1.0.0"
__status__ = "Development"

import sqlite3
from AppVar import Global


class GestionBD(object):
    def __init__(self, dbName):
        self.db = None
        self.dbName = dbName
        self.tableLink = Global.tableLinkV2
        self.error = False
        self.cursor = None
        self.connection()
        self.close()

    def connection(self):
        # tentative de connexion a la base de données
        try:
            self.db = sqlite3.connect(self.dbName)
        except Exception:
            #print("Database connection error : {}".format(Exception))
            self.error = True
        else:
            self.cursor = self.db.cursor()

    def createTable(self, table, field):
        """methode generaliste pour creer une base de données"""
        req = "CREATE TABLE IF NOT EXISTS {} (".format(table)
        # preparation de la longueur de la req
        for c in field:
            req += " ".join(c) + ", "
        req = req[:-2] + ")"
        # print(req)
        # execution de la requete une fois req prete
        # print(req)
        self.exeReq(req)

    def insertData(self, table, field, data):
        """methode qui entre des données dans une base de données"""
        req = "INSERT INTO {} (".format(table)
        for f in field:
            req += str(f)+","
        req = req[:-1] + ") VALUES(" + "?,"*len(field)
        req = req[:-1] + ")"
        # print(req)
        self.exeReq(req, data)

    def updateData(self, table, field, data):
        """methode mettant a jour la table en argument par nouvelle valeurs est conserve un historique des données"""

# Fonction selectData trop complexe a mettre en oeuvre pour l'instant...
    def selectData(self, fieldSelected, tablesSelect, whereClause=None):
        """construit la requete select et gere les jointure"""
        req = "SELECT "
        # placement des champs dans la requete
        for f in fieldSelected:
            req += "{},".format(f)
        req = req[:-1] + " "
        req += "FROM "
        # placement de la table dans la requete
        req += "{} ".format(tablesSelect[0])
        # si plus d'une table alors injection de INNER JOIN
        if len(tablesSelect) > 1:
            key = tablesSelect[0] + "_id"
            valLinkTab = self.tableLink[key]
            t = 1
            while t <= len(tablesSelect):
                req += "INNER JOIN "
                req += "{} ".format(tablesSelect[t])
                req += "ON "
                # besoin de verifier dans tableLink

                # tablesSelect[t]_id = tablesSelect[t-1]_id
            for t in tablesSelect:
                req += "INNER JOIN "
                if t in req:
                    pass
                req += "{} ".format(t)
                # ajout clause ON pour faire correspondre les champs
                req += "ON "

                for t in tablesSelect:
                    for link in self.tableLink[t]:
                        req += link + " "

        # ajout de la clause WHERE
        if whereClause != None:
            req += "WHERE "
            #print("where clause : {}".format(whereClause))
            req += whereClause
        #print("request: {}".format(req))
        return req

    def exeReq(self, req, data=None):
        """ execute la requete et verifiant la levé d'exception"""
        self.connection()
        try:
            if data==None:
                self.cursor.execute(req)
                reg = self.cursor.fetchall()
                return reg
            else:
                reg = self.cursor.execute(req, data)
                reg = self.cursor.fetchall()
                return reg
        except Exception as err:
            print("SQL Query execution error: {}".format(err))
            return err
        finally:
            self.commit()
            self.close()

    def commit(self):
        """transfere les donnée dans la base de données"""
        self.db.commit()

    def close(self):
        """ferme le curseur de la bdd"""
        self.cursor.close()

if __name__ == "__main__":
    gbd = GestionBD("contents\\bdd_orgadmin.sql")
    #print(gbd.selectData(["nom", "prenom","date_v"], ["utilisateurs", "documents"]))
    #print(gbd.exeReq("SELECT utilisateurs.nom,prenom,documents.nom FROM utilisateurs,documents"))
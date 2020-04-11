# coding: utf8

#module contenant les variables d'application OrgAdmin
import os.path

__autor__ = "Alcodori François"
__licence__ = "GPL"
__credit__ = ("Alcodori François",)
__versions__ = "1.0.0"
__status__ = "development"

import tkinter


class Global(object):
    # dico contenant le descriptif des table et les liens referentiel
    # nom des table tj au pluriel, sans accents
    # date au format strings ("YYYY-MM-DD HH:MM:SS.SSS")
    # espace entre nom des table "_"
    # cle primaire avec nom table + "_id" (pour commande USING (*_id))
    # les jointures sont symbolisé par les clé id. si meme nom de clé dans table de jointure obligeatoire
    tableDescr = {"utilisateurs": (
        ("nom", "TEXT"), ("prenom", "TEXT"), ("date_n", "TEXT"), ("utilisateurs_id", "INTEGER NOT NULL PRIMARY KEY")),
        "classeurs": (("nom", "TEXT"), ("couleur", "TEXT"), ("emplacement", "TEXT"), ("periode", "TEXT"),
                      ("utilisateurs_id", "INTEGER"), ("classeurs_id", "INTEGER NOT NULL PRIMARY KEY")),
        "documents": (
            ("nom", "TEXT"), ("date_v", "TEXT"), ("documents_id", "INTEGER NOT NULL PRIMARY KEY"), ("tags", "TEXT"),
            ("utilisateurs_id", "INTEGER"), ("classeurs_id", "INTEGER"), ("pathfile", "TEXT"))}

    # jointure entre les tables
    tableLink = {"utilisateurs": ("utilisateurs.utilisateurs_id = classeurs.utilisateurs_id",
                                  "utilisateurs.utilisateurs_id = documents.utilisateurs_id"),
                 "classeurs": ("classeurs.classeurs_id = documents.classeurs_id",
                               "classeurs.utilisateurs_id = utilisateurs.utilisateurs_id"),
                 "documents": ("documents.utilisateurs_id = utilisateurs.utilisateurs_id",
                               "documents.classeurs_id = classeurs.classeurs_id")}
    # jointure des tables V2 (referencement par clé id plutot que par tables)
    tableLinkV2 = {"utilisateurs_id": ("utilisateurs", "documents", "classeurs"),
                   "classeurs_id": ("utilisateurs", "documents"),
                   "documents_id": ("documents")}
    # instauration contexte tkinter
    # fen = tkinter.Tk()

    # dimension ecran
    # sWidth = int((fen.winfo_screenwidth() / 3) * 2)
    # sHeight = int((fen.winfo_screenheight() / 3) * 2)


    # dictionnaire des couleurs
    # convention nommage pour pouvoir reacher les etat: enter_entry
    colors = {"Search": {"entry": "grey80",
                         "over_entry": "grey60",
                         "searchBtn": "lightgreen",
                         "over_searchBtn": "darkgreen",
                         },

              "MainWindows": {"blue"
                              },

              "ListAdd": {"entree": "grey80",
                          "over_entree": "grey60",
                          "lB": "lightgreen",
                          "over_lB": "darkgreen",
                          "addBtn": "lightgreen",
                          "over_addBtn": "darkgreen",
                          },
              "AddBtn": {"AddBtn": "orange",
                         "over_AddBtn": "dark orange"},
              "DelBtn": {"AddBtn": "red",
                         "over_AddBtn": "dark red"}
              }

    # dictionnaire des polices
    fonts = {"default": ("calibri", 17)}
    # index des chemins de fichier
    pathFile = {"searchIcon": "contents\\search-icon30x30.png",
                "addIcon": "contents\\add-button30x30.png",
                "addIconBtn": "contents\\add-button60x60.png",
                "delIcon": "contents\\del-button30x30.png",
                "delIconBtn": "contents\\del-button60x60.png",
                "addDocIcon": "contents\\addDoc-button30x30.png",
                "addDocIconBtn": "contents\\addDoc-button60x60.png",
                "shutdownIconBtn": "contents\\shutdown-button24x24.png"
                }

    # chemin de la base de donne
    dataDirPath = os.path.expanduser("~\\AppData\\Local\\Orgadmin")
    # si un document n'a pas dimage dispo
    noImage = "contents\\noImage.png"
    menuIcon = ("contents\\save.png", "contents\\print.png", "contents\\rotateRight.png", "contents\\rotateLeft.png")
    # dictionnaire des textes par defaut
    defaultText = {"AddDocuments": {"title": "Ajouts de Documents",
                                    "eNameDoc": "Entrez un nom de document...",
                                    "lDate": "Dates de validité",
                                    "labelDate": "au",
                                    "eDateB": "jj/mm/aaaa",
                                    "eDateE": "jj/mm/aaaa",
                                    "labelEmpl": "Choisissez son emplacement ou creez en un:",
                                    "tagList": "",
                                    "fileLabel": "Ajoutez le fichier du document"
                                    },
                   "AddClasseurs": {"title": "Ajouts de Classeurs"},
                   # dans listAdd le texte par default depend du contexte passé en argument
                   "ListAdd": {"default": {"entree": "Entrez le nom du document..."},
                               "mainwin": {"entree": "Ajoutez une tâche..."},
                               "AddTags": {"entree": "Ajoutez des Tags..."},
                               "AddClasseurs": {"entree": "Ajouter un Classeur, Tiroir, Chemise..."}
                               },
                   "Search": {"entry": "Recherchez un document..."}
                   }

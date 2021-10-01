# coding=utf-8

#Partie Traitement Mot Clé
import sqlite3
from google_translate_py import Translator
import re
from database import connection,updateInsertTable

chemin = input("Chemin d'accès BD NAMIP: ")
#chemin = "C:/Users/aurel/github/guideApp/assets/database/NAMIP.db"
con,cur = connection(chemin)

def changementWordbyMotCléDescription(Desc,liste,IdObjet):
    for x in liste:
        if Desc.find(x[0]) != -1 and IdObjet != x[1]:
            Desc = Desc.replace(x[0], "|" + str(x[1]) + "|")
    return Desc

def listeAllMotCléPossible():
    list = []
    for row in cur.execute("SELECT ID,Nom from GENERAL"):
        nom = re.sub(r"(.*?)\s?\(.*?\)", r"\1", row[1])
        list.append((nom,row[0]))
    return list

def traiterDescMotClé(listeToutMotClé):
    listDesc = []
    listMotCléObjet = []
    for row in cur.execute("SELECT ID,DescFR,DescEN,DescNL from GENERAL"):
        frDescMotClé = changementWordbyMotCléDescription(row[1],listeToutMotClé,row[0])
        enDescMotClé = changementWordbyMotCléDescription(row[2],listeToutMotClé,row[0])
        nlDescMotClé = changementWordbyMotCléDescription(row[3],listeToutMotClé,row[0])
        listDesc.append((frDescMotClé,enDescMotClé,nlDescMotClé,row[0]))
        for x in listeToutMotClé:
            if (x[1],row[0],x[0]) not in listMotCléObjet and row[1].find(x[0]) != -1 and x[1] != row[0] :
                listMotCléObjet.append((x[1],row[0],x[0]))
    return listDesc,listMotCléObjet

if con != None and cur != None:
    list = listeAllMotCléPossible()
    listDesc,listeMotCléObjet = traiterDescMotClé(list)
    UpdateRequete = "UPDATE GENERAL SET DescMotFR = ? , DescMotEN = ?,DescMotNL = ? WHERE ID = ?"
    InsertRequete = "REPLACE INTO MOTCLE VALUES (?, ?, ?)"
    updateInsertTable(con,cur,UpdateRequete,listDesc)
    updateInsertTable(con,cur,InsertRequete,listeMotCléObjet)
    print("Traitement Description Effectué")
    con.close()
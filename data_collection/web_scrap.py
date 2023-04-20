import requests
import unidecode
import random
import data
import time
import os
import sqlite3
from bs4 import BeautifulSoup

__all__ = ["Scraping"]

PROTOCOL = "HTTP"
URL1 = "https://www.onisep.fr"

def url1_correcteur(url1:str) -> str:
    url1 = url1.lower()
    url1 = url1.replace("–", "-")
    url1 = url1.replace(" ", "-")
    url1 = url1.replace("---", "-")
    url1 = url1.replace("’","-")
    url1 = unidecode.unidecode(url1)
    return url1


class Scraping:
    def __init__(self, url1:str, protocol:str, port=None) -> None:

        self.url1 = url1
        self.protocol =  protocol
        self.port = port 

        self.reponse = requests.get(self.url1)
        self.soup = BeautifulSoup(self.reponse.text, "lxml")

    def __is_ok(self) -> bool:
        return self.reponse.ok
    
    def return_header(self) -> str:
        if self.__is_ok():
            return self.reponse.headers

    def write_html_code_on_file(self, file_name:str) -> bool:
        if self.__is_ok():
            html_code = self.reponse.text

            with open(file_name, "w", encoding="utf-8") as file:
                file.write(html_code)

            print(f"[*] Le code HTML de {self.url1} a été copyé dans {file_name}............")

            return True
        return False
    
    def scrape(self, elmt_selector:list[str]) -> dict:
        elmt_return = {key:value for (key,value) in zip(elmt_selector, None)}

        if self.__is_ok():

            for i in range(len(elmt_selector)):
                elmt_return[elmt_selector[i]] = self.soup.find_all(elmt_selector[i])

        return elmt_return
    
    def parse(self, elmt:str, atribu:str) -> list:
        finds = [i.find(atribu) for i in elmt]
        return finds
    
    def print_on_csv_file(self):
        pass

    def sublimeTextElmt(self):
        pass

    def find_all_url1(self):
        pass

if __name__ == "__main__":
    database = "../database.db"
    PROTOCOL = "HTTP"


    #Secteurs
    URL1 = "https://www.cidj.com/metiers/metiers-par-secteur"
    secteurs = []
    reponse =  requests.get(URL1)
    if reponse.ok:
        soup = BeautifulSoup(reponse.text, "lxml")
        uls = soup.find_all("h2")
        for ul in uls:
            secteur = ul.text
            secteurs.append(secteur)
    with sqlite3.connect(database) as db:
        cursor = db.cursor()
        for i in range(len(secteurs)):
            requete = "insert into Secteurs (Nom) values (?)"
            cursor.execute(requete, [(secteurs[i])])
        db.commit()

    #Métiers
    with sqlite3.connect(database) as db:

        cursor = db.cursor()
        requete = "select * from Secteurs"
        cursor.execute(requete)
        secteurs = cursor.fetchall()

    metiers = []
    for i in range(len(secteurs)):
        URL1 = "https://www.cidj.com/metiers/metiers-par-secteur/"+url1_correcteur(secteurs[i][1])
        index = secteurs[i][0]
        reponse =  requests.get(URL1)

        if reponse.ok:

            soup = BeautifulSoup(reponse.text, "lxml")
            nb_pages = len(soup.find_all("li",attrs="pager__item"))-2
        
        if nb_pages > 0:
            for j in range(nb_pages):
                url1 = URL1+"?page="+str(j)
                reponse =  requests.get(url1)
                if reponse.ok:
                    soup = BeautifulSoup(reponse.text, "lxml")
                    h2s = soup.find_all("h2")
                    for h2 in h2s:
                        metier = h2.find('a')
                        metier = metier.text
                        metiers.append([metier,index])
        else:
            url1 = URL1
            reponse =  requests.get(url1)
            if reponse.ok:
                soup = BeautifulSoup(reponse.text, "lxml")
                h2s = soup.find_all("h2")
                for h2 in h2s:
                    metier = h2.find('a')
                    metier = metier.text
                    metiers.append([metier,index])
    with sqlite3.connect(database) as db:
        cursor = db.cursor()
        for i in range(len(metiers)):
            requete = "insert into Métiers (Nom, ID_formation) values (?, ?)"
            cursor.execute(requete, [(metiers[i][0]), (metiers[i][1])])
        db.commit()
  
    #Description Métier
    URL1 = "https://www.cidj.com"
    url2 = "https://www.cidj.com/metiers/metiers-par-secteur"

    continue_Bool = False
    response = requests.get(url2)
    secteur_métier_link = []
    metiers_links = {}
    descriptions = {}

    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
        class_Cat = soup.find_all("div", attrs="cat")
        for cat in class_Cat:
            link =  URL1+cat.find("a")["href"]
            secteur_métier_link.append(link)
        continue_Bool = True

    if continue_Bool:
        for link in secteur_métier_link:
            response = requests.get(link)
            if response.ok:
                soup = BeautifulSoup(response.text, "lxml")
                nb_pages = len(soup.find_all("li",attrs="pager__item"))-2

                if nb_pages > 0:
                    for j in range(nb_pages):
                        url1 = link+"?page="+str(j)
                        reponse =  requests.get(url1)
                        if reponse.ok:
                            soup = BeautifulSoup(reponse.text, "lxml")
                            div_btn = soup.find_all("h2")
                            for metier_link in div_btn:
                                lien = "https://www.cidj.com"+metier_link.find("a")["href"]
                                text = metier_link.find("a").text
                                metiers_links[text] = lien
                else:
                    div_btn = soup.find_all("h2")
                    for metier_link in div_btn:
                        lien = "https://www.cidj.com"+metier_link.find("a")["href"]
                        text = metier_link.find("a").text
                        metiers_links[text] = lien
            else:
                continue_Bool = False
    
    if continue_Bool:
        for title,link in metiers_links.items():
            response = requests.get(link)
            if response.ok:
                soup = BeautifulSoup(response.text, "lxml")
                description = soup.find("div", attrs="body-wrapper-content")
                descriptions[title] = description.text
            else:
                continue_Bool = False

    if continue_Bool:
        with sqlite3.connect(database) as conn:
            cursor = conn.cursor()
            request = "select * from Metiers"
            cursor.execute(request)
            metiers = cursor.fetchall()

            noms =  [nom[1] for nom in metiers]
            index = 1

            for title,description in descriptions.items():
                if title != 'Chef / Cheffe de projet CRM':
                    request = "UPDATE Metiers SET ID_Description = ? WHERE Nom = ?"
                    cursor.execute(request, [(index), (title)])
                    ID = metiers[noms.index(title)][0]

                    request = "insert into Descriptions (Description, ID_Metier) values (?, ?)"
                    cursor.execute(request, [(description), (ID)])
                    index += 1
            conn.commit()

    #simulation de données
    formatage = {"a":0, "b":1, "c":2, "d":3}
    
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        request = "select * from Categories_metiers"
        cursor.execute(request)
        ret = cursor.fetchall()

        categories = [ret[i][1] for i in range(len(ret))]

        send_packet = {}
        for i in range(len(categories)):
            send_packet[categories[i]] = []
            for j in range(4):
                question_rep = []
                for key,value in data.question_catégories.items():
                    question_rep.append(random.choice(list(formatage.values())))
                send_packet[categories[i]].append(question_rep)
        
        for key,value in send_packet.items():
            ID = ret[categories.index(key)][0]
            for donp in value:
                gloglo = []
                for repoj in donp:
                    gloglo.append((repoj))
                gloglo = [(ID)]+gloglo

                request = "insert into Profils_types_categories (ID_Categories_metiers,Field3,Field4,Field5,Field6,Field7,Field8,Field9,Field10,Field11,Field12) values (?,?,?,?,?,?,?,?,?,?,?)"
                cursor.execute(request, gloglo)
        
        conn.commit()

        cursor = conn.cursor()
        request = "select * from Metiers"
        cursor.execute(request)
        ret = cursor.fetchall()

        categories = [ret[i][1] for i in range(len(ret))]

        send_packet = {}
        for i in range(len(categories)):
            send_packet[categories[i]] = []
            for j in range(4):
                question_rep = []
                for key,value in data.question_metier.items():
                    question_rep.append(random.choice(list(formatage.values())))
                send_packet[categories[i]].append(question_rep)

        for key,value in send_packet.items():
            ID = ret[categories.index(key)][0]
            for donp in value:
                gloglo = []
                for repoj in donp:
                    gloglo.append((repoj))
                gloglo = [(ID)]+gloglo

                request = "insert into Profils_types_metiers (ID_Metier,Field3,Field4,Field5,Field6,Field7,Field8,Field9,Field10,Field11,Field12,Field13,Field14,Field15,Field16,Field17,Field18,Field19,Field20,Field21,Field22) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                cursor.execute(request, gloglo)
        
        conn.commit()

        PIE = "https://www.data.gouv.fr/fr/"

    categories = {}
    count = 0
    for key,value in data.question_catégories.items():
        new_key = (f"Q#{count}", key)
        categories[new_key] = []
        slice_in = 0
        for reponse in value:
            form_repo = [f"R#{slice_in} Q#{count}", reponse]
            categories[new_key].append(form_repo)
            slice_in += 1
        count += 1
    
    metier = {}
    for key,value in data.question_metier.items():
        new_key = (f"Q#{count}", key)
        metier[new_key] = []
        slice_in = 0
        for reponse in value:
            form_repo = [f"R#{slice_in} Q#{count}", reponse]
            metier[new_key].append(form_repo)
            slice_in += 1
        count += 1

    print(categories)
    print("\n\n")
    print(metier)
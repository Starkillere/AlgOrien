import requests
import time
import os
import sqlite3
from bs4 import BeautifulSoup

__all__ = ["Scraping"]

PROTOCOL = "HTTP"
URL = "https://www.onisep.fr"

class Scraping:
    def __init__(self, url:str, protocol:str, port=None) -> None:

        self.url = url
        self.protocol =  protocol
        self.port = port 

        self.reponse = requests.get(self.url)
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

            print(f"[*] Le code HTML de {self.url} a été copyé dans {file_name}............")

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

    def find_all_url(self):
        pass

if __name__ == "__main__":
    database = "../database.db"
    PROTOCOL = "HTTP"

    #Secteurs
    """
    URL = "https://www.cidj.com/metiers/metiers-par-secteur"
    secteurs = []
    reponse =  requests.get(URL)
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
    """

    #Métiers
    with sqlite3.connect(database) as db:
        cursor = db.cursor()
        requete = "select * from Secteurs"
        cursor.execute(requete)
        secteurs = cursor.fetchall()

    
    for i in range(len(secteurs)):
        URL = "https://www.cidj.com/metiers/metiers-par-secteur/"+secteurs[i][1].lower().replace(" ", "")
        print("****",URL,"****")
        metiers = []
        reponse =  requests.get(URL)
        if reponse.ok:
            soup = BeautifulSoup(reponse.text, "lxml")
            h2s = soup.find_all("h2")
            for h2 in h2s:
                metier = h2.find('a')
                metier = metier.text
                metiers.append(metier)
                print(metier)
        time.sleep(1)
        
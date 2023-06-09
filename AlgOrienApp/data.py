# -*- coding:utf-8 -*-
import sqlite3
from . import KnnOrien

__all__ = ["formatage", "find_orientation", "question_catégories", "question_metier"]


def formatage(data:list) -> dict:
    categories = [int(data[i].split(" ")[0].split("#")[1]) for i in range(0, 10)]
    metiers = [int(data[i].split(" ")[0].split("#")[1]) for i in range(10, 30)]
    re_data = {"Profils_types_categories":categories, "Profils_types_metiers":metiers}
    return re_data

def find_orientation(user_data:list, database:str) -> str:
    exe_data = formatage(user_data)
    tables = list(exe_data.keys())

    ID_Categories_metiers = KnnOrien.Algo_knn_orien(exe_data["Profils_types_categories"], database, tables[0], 10)
    ID_Metier = KnnOrien.Algo_knn_orien(exe_data["Profils_types_metiers"], database, tables[1], 20, ["ID_Categories_metiers", ID_Categories_metiers])
    
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        requete = "select Description from Descriptions WHERE ID_Metier = ?"
        cursor.execute(requete, [(ID_Metier)])

        description = cursor.fetchone()
        description = "".join(list(description)).split("\n")
        the_description = []
        for i in range(len(description)):
            if description[i] !=  '':
                the_description.append(description[i])

        del the_description[-1]
        del the_description[-1]

        the_description[0] = the_description[0].split(",")

    return the_description


question_catégories = {('Q#0', 'Quel type de travail souhaitez-vous faire ?'): [['R#0 Q#0', 'Un travail manuel'], ['R#1 Q#0', 'Un travail de bureau'], ['R#2 Q#0', 'Un travail créatif'], ['R#3 Q#0', 'Un travail technologique']], ('Q#1', "Quel est votre niveau d'éducation ?"): [['R#0 Q#1', "Diplôme d'études secondaires"], ['R#1 Q#1', 'Diplôme universitaire'], ['R#2 Q#1', "Certificat d'études spécialisées"], ['R#3 Q#1', 'Aucun diplôme']], ('Q#2', 'Quel type de responsabilité souhaitez-vous avoir ?'): [['R#0 Q#2', 'Des responsabilités importantes'], ['R#1 Q#2', 'Des responsabilités limitées'], ['R#2 Q#2', 'Aucune responsabilité'], ['R#3 Q#2', 'Des responsabilités occasionnelles']], ('Q#3', "Quelle est la taille de l'entreprise qui vous intéresse ?"): [['R#0 Q#3', 'Grande entreprise'], ['R#1 Q#3', 'Petite entreprise'], ['R#2 Q#3', 'Entreprise individuelle'], ['R#3 Q#3', 'Plusieurs entreprises']], ('Q#4', 'Quel est le cadre de travail qui vous intéresse ?'): [['R#0 Q#4', 'En équipe'], ['R#1 Q#4', 'Seul'], ['R#2 Q#4', 'En ligne'], ['R#3 Q#4', 'En personne']], ('Q#5', 'Quel type de salaire espérez-vous ?'): [['R#0 Q#5', 'Un salaire régulier'], ['R#1 Q#5', 'Un salaire à commission'], ['R#2 Q#5', "Un salaire à l'heure"], ['R#3 Q#5', 'Un salaire fixe']], ('Q#6', "Quel type d'environnement de travail vous intéresse ?"): [['R#0 Q#6', 'Environnement dynamique'], ['R#1 Q#6', 'Environnement calme'], ['R#2 Q#6', 'Environnement stimulant'], ['R#3 Q#6', 'Environnement flexible']], ('Q#7', 'Quel type de bénéfices supplémentaires recherchez-vous ?'): [['R#0 Q#7', 'Des vacances payées'], ['R#1 Q#7', 'Des primes de rendement'], ['R#2 Q#7', 'Des avantages sociaux'], ['R#3 Q#7', "Des options d'achat d'actions"]], ('Q#8', 'Quel est le type de carrière que vous souhaitez ?'): [['R#0 Q#8', 'Une carrière ascendante'], ['R#1 Q#8', 'Une carrière stable'], ['R#2 Q#8', 'Une carrière variée'], ['R#3 Q#8', 'Une carrière à long terme']], ('Q#9', 'Quel type de secteur souhaitez-vous rejoindre ?'): [['R#0 Q#9', 'Secteur public'], ['R#1 Q#9', 'Secteur privé'], ['R#2 Q#9', 'Secteur humanitaire'], ['R#3 Q#9', 'Secteur entrepreneurial']]}

question_metier = {('Q#10', 'Quel type de travail vous intéresse le plus ?'): [['R#0 Q#10', 'Les métiers manuels'], ['R#1 Q#10', 'Les métiers à distance'], ['R#2 Q#10', 'Les métiers artistiques'], ['R#3 Q#10', 'Les métiers auxiliaires']], ('Q#11', 'Quel est votre style de communication préféré ?'): [['R#0 Q#11', 'Verbal'], ['R#1 Q#11', 'Écrit'], ['R#2 Q#11', 'Visuel'], ['R#3 Q#11', 'Tâches à effectuer']], ('Q#12', 'Quel type de métier vous intéresse le plus ?'): [['R#0 Q#12', 'Les métiers de service'], ['R#1 Q#12', 'Les métiers techniques'], ['R#2 Q#12', 'Les métiers commerciaux'], ['R#3 Q#12', "Les métiers de l'informatique"]], ('Q#13', "Quel est votre niveau d'études ?"): [['R#0 Q#13', "Diplomé d'un niveau d'études supérieur"], ['R#1 Q#13', "Diplomé d'un niveau d'études intermédiaire"], ['R#2 Q#13', "Diplomé d'un niveau d'études secondaire"], ['R#3 Q#13', 'Autodidacte']], ('Q#14', "Quel type d'environnement de travail vous convient le mieux ?"): [['R#0 Q#14', 'Un environnement en équipe'], ['R#1 Q#14', 'Un environnement autonome'], ['R#2 Q#14', 'Un environnement stimulant'], ['R#3 Q#14', 'Un environnement flexible']], ('Q#15', 'Quel type de salaire souhaitez-vous ?'): [['R#0 Q#15', 'Un salaire fixe et élevé'], ['R#1 Q#15', 'Un salaire évolutif'], ['R#2 Q#15', 'Un salaire bas mais avec des primes'], ['R#3 Q#15', 'Un salaire avec des avantages en nature']], ('Q#16', 'Quel type de métiers vous intéresse le plus ?'): [['R#0 Q#16', "Les métiers de l'enseignement"], ['R#1 Q#16', 'Les métiers de la finance'], ['R#2 Q#16', "Les métiers de l'informatique"], ['R#3 Q#16', 'Les métiers du divertissement']], ('Q#17', "Quel type d'emploi souhaitez-vous ?"): [['R#0 Q#17', 'Un emploi à temps plein'], ['R#1 Q#17', 'Un emploi à temps partiel'], ['R#2 Q#17', 'Un emploi à domicile'], ['R#3 Q#17', "Un emploi à l'étranger"]], ('Q#18', 'Quel type de métiers vous intéresse le plus ?'): [['R#0 Q#18', 'Les métiers du secteur public'], ['R#1 Q#18', 'Les métiers du secteur privé'], ['R#2 Q#18', "Les métiers de l'Humanitaire"], ['R#3 Q#18', "Les métiers de l'entrepreneuriat"]], ('Q#19', 'Quelle est votre expérience professionnelle la plus marquante ?'): [['R#0 Q#19', 'Une mission réussie'], ['R#1 Q#19', 'Une promotion'], ['R#2 Q#19', 'Une reconversion professionnelle'], ['R#3 Q#19', 'Un projet innovant']], ('Q#20', "Quel type d'ambiance de travail vous convient le mieux ?"): [['R#0 Q#20', 'Une ambiance dynamique'], ['R#1 Q#20', 'Une ambiance calme'], ['R#2 Q#20', 'Une ambiance stimulante'], ['R#3 Q#20', 'Une ambiance collaborative']], ('Q#21', "Quels sont les facteurs qui motivent le plus votre choix d'un métier ?"): [['R#0 Q#21', 'Le salaire'], ['R#1 Q#21', 'La flexibilité'], ['R#2 Q#21', "L'autonomie"], ['R#3 Q#21', 'La reconnaissance']], ('Q#22', 'Quel type de métiers vous intéresse le plus ?'): [['R#0 Q#22', "Les métiers de l'ingénierie"], ['R#1 Q#22', 'Les métiers de la santé'], ['R#2 Q#22', "Les métiers de l'éducation"], ['R#3 Q#22', 'Les métiers du commerce']], ('Q#23', "Quel type d'organisation préférez-vous ?"): [['R#0 Q#23', 'Une organisation hiérarchisée'], ['R#1 Q#23', 'Une organisation horizontale'], ['R#2 Q#23', 'Une organisation à objectifs'], ['R#3 Q#23', 'Une organisation à mission']], ('Q#24', 'Quel type de management vous convient le mieux ?'): [['R#0 Q#24', 'Un management par objectifs'], ['R#1 Q#24', 'Un management par projet'], ['R#2 Q#24', 'Un management par la qualité'], ['R#3 Q#24', 'Un management par la formation']], ('Q#25', 'Quel type de métiers vous intéresse le plus ?'): [['R#0 Q#25', 'Les métiers de la technologie'], ['R#1 Q#25', 'Les métiers des médias'], ['R#2 Q#25', 'Les métiers du marketing'], ['R#3 Q#25', 'Les métiers de la vente']], ('Q#26', 'Quel type de personnes appréciez-vous le plus ?'): [['R#0 Q#26', 'Les personnes créatives'], ['R#1 Q#26', 'Les personnes communicatives'], ['R#2 Q#26', 'Les personnes ambitieuses'], ['R#3 Q#26', 'Les personnes logiques']], ('Q#27', 'Quel type de métiers vous intéresse le plus ?'): [['R#0 Q#27', "Les métiers de l'architecture"], ['R#1 Q#27', 'Les métiers de la gestion'], ['R#2 Q#27', "Les métiers de l'informatique"], ['R#3 Q#27', "Les métiers de l'écriture"]], ('Q#28', 'Quel type de tâches vous intéresse le plus ?'): [['R#0 Q#28', 'Les tâches analytiques'], ['R#1 Q#28', 'Les tâches créatives'], ['R#2 Q#28', 'Les tâches organisationnelles'], ['R#3 Q#28', 'Les tâches administratives']], ('Q#29', 'Quel type de travail vous intéresse le plus ?'): [['R#0 Q#29', 'Le travail en équipe'], ['R#1 Q#29', 'Le travail autonome'], ['R#2 Q#29', 'Le travail à domicile'], ['R#3 Q#29', 'Le travail à distance']]}
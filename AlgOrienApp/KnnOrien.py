# -*- coding:utf-8 -*-

from math import sqrt
import sqlite3

__all__ = ["Algo_knn_orien"]

def Import_and_format_data(database:str, table:str) -> dict:
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        request =  "select * from ?"
        cursor.execute(request, [(table)])
        data =  cursor.fetchall()

    keys, values = [(data[i][0], data[i][1]) for i in range(len(data))], [(data[i][j] for j in range(len(data[0]))) for i in range(len(data))]
    dict_data = {k:v for (k,v) in zip(keys, values)}

    return dict_data

def Distance(re_data:list[int], user_data:list[int]) -> int:
    somme = 0

    for i in range(len(re_data)):
        somme += (re_data[i]-user_data[i])**2

    racine = sqrt(somme)
    distance =  round(racine)

    return distance


def Frequence(nn:list) -> tuple:
    ID = 0
    frequence = 0

    for i in range(len(nn)):
        if nn.count(nn[i]) > frequence:
            frequence = nn.count(nn[i])
            ID = nn[i]
    
    return ID

def Algo_knn_orien(k:int, user_data:list[int], database:str, table:str) -> tuple:
    assert type(k) == int
    assert type(user_data) == list
    assert type(database) == str
    assert type(table) == str

    data =  Import_and_format_data(database, table)
    keys, values = list(data.keys()), list(data.values())

    nnp = []
    for i in range(len(values)):
        distance = Distance(values[i], user_data)
        new_nnp = {"ID":keys[i], "DISTANCE":distance}
        nnp.append(new_nnp)
    
    nnp.sort(reverse = False, key=lambda x : x["DISTANCE"])
    k_nnp = [nnp[i]["ID"][1] for i in range(k)]
    the_nnp = Frequence(k_nnp)

    return the_nnp
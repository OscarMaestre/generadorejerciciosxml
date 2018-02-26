#!/usr/bin/env python3
#coding=utf-8

import ElementoXML
from random import randint, shuffle


def get_boolean_azar():
    num_entero=randint(0, 1)
    if num_entero==0: return True
    return False


def get_posibles_unidades(unidades):
    
    min=0
    max=len(unidades)-1
    pos_azar=randint(min, max)    
    return unidades[pos_azar]

def get_posibles_unidades_peso():
    unidades=[
        ["g", "kg", "ton"],
        ["g", "kg"],
        ["kg", "ton"],
    ]
    return get_posibles_unidades(unidades)

def get_posibles_unidades_moneda():
    unidades=[
        ["yen", "euro", "libra"],
        ["dolar", "euro"],
        ["libra", "euro"],
    ]
    return get_posibles_unidades(unidades)

def get_posibles_paises():
    paises=[
        ["USA", "UK", ]
    ]

def get_atributo_peso():
    atributo=ElementoXML.Atributo()
    atributo.set_optativo(get_boolean_azar())
    atributo.set_nombre("peso")
    atributo.set_valor(randint(1, 20))
    return atributo

def get_atributo_unidad():
    atributo=ElementoXML.Atributo()
    atributo.set_optativo(get_boolean_azar())
    atributo.set_nombre("unidad")
    atributo.set_posibles_valores(get_posibles_unidades_peso())
    return atributo
    
def get_atributo_moneda():
    atributo=ElementoXML.Atributo()
    atributo.set_optativo(get_boolean_azar())
    atributo.set_nombre("moneda")
    atributo.set_posibles_valores(get_posibles_unidades_moneda())
    return atributo
    
def get_atributo_pais():
    atributo=ElementoXML.Atributo()
    atributo.set_optativo(get_boolean_azar())
    atributo.set_nombre("pais")
    atributo.set_posibles_valores(get_posibles_unidades_moneda())
    return atributo
    
def get_seccion_azar_vector(vector):
    shuffle(vector)
    max_longitud=randint(1, len(vector))
    return vector[0:max_longitud]

def get_atributos(posibilidades):
    
    lista_atributos=[]
    posibilidades=get_seccion_azar_vector(posibilidades)
    
    for generador in posibilidades:
        
        atributo=generador()
        lista_atributos.append(atributo)
        
    for a in lista_atributos:
        print(a.get_descripcion())
    return lista_atributos

def get_atributos_peso():
    posibilidades=[
        get_atributo_moneda, get_atributo_peso
    ]
    return get_atributos(posibilidades)


    

if __name__ == '__main__':
    get_atributos_peso()
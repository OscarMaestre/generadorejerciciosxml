#!/usr/bin/env python3
#coding=utf-8

ANY_TYPE="anyType"


class TipoBasicoW3C(object):
    def get_esquema(self):
        plantilla="<xsd:element name=\"{0}\" type=\"{1}\" />"
        descripcion="{0}".format(self.nombre_tipo_basico, self.nombre_elemento)
        return descripcion
    
class TipoString(TipoBasicoW3C):
    def __init__(self, nombre_elemento):
        self.nombre_tipo_basico="string"
        self.nombre_elemento=nombre_elemento
        
class TipoInteger(TipoBasicoW3C):
    def __init__(self, nombre_elemento):
        self.nombre_tipo_basico="integer"
        self.nombre_elemento=nombre_elemento

class TipoSimpleNumericoConRestriccion(TipoBasicoW3C):
    def __init__(self, nombre_tipo, nombre_base):
        self.nombre_tipo=nombre_tipo
        self.nombre_base=nombre_base
        self.minimo=None
        self.maximo=None
        
    def add_minInclusive(self, valor):
        self.minimo=valor
    def add_maxInclusive(self, valor):
        self.maximo=valor
        
    def get_esquema(self):
        plantilla="""<xsd:simpleType name="{0}"><xsd:restriction base="{1}"><xsd:restriction>{2}{3}</xsd:simpleType>"""
        minimo=""
        if self.minimo!=None:
            minimo="<xsd:minInclusive value=\"{0}\"/>"
        minimo=""
        if self.maximo!=None:
            maximo="<xsd:maxInclusive value=\"{0}\"/>"

        esquema=plantilla.format(self.nombre_tipo, self.nombre_base, minimo, maximo)
        return esquema
            
        
class Atributo(object):
    def __init__(self):
        self.optativo=False
        self.tipo=None
        self.posibles_valores=None
        
    def set_optativo(self, optativo):
        self.optativo=optativo
        
    def set_posibles_valores(self, posibles_valores):
        self.posibles_valores=posibles_valores
        
    def set_tipo(self, cadena_tipo):
        self.tipo=cadena_tipo
        
    def set_nombre(self, nombre):
        self.nombre=nombre
    
    def set_valor(self, valor):
        self.valor=valor
    
    def set_nombre_valor(self, nombre, valor):
        self.set_nombre(nombre)
        self.set_valor(valor)
        
    def get_descripcion(self):
        descripcion=""
        if self.optativo:
            descripcion+="Atributo {0} (optativo).".format(self.nombre)
        else:
            descripcion+="Atributo {0}. ".format(self.nombre)
        if self.tipo:
            descripcion+="Tipo {0}".format(self.tipo)
            
        if self.posibles_valores:
            descripcion+="Posibles valores:" + ",".join(self.posibles_valores)
            
        return descripcion
    def __str__(self):
        atributo="{0}=\"{1}\"".format(self.nombre, self.valor)
        
class ElementoXML(object):
    def set_etiqueta(self, etiqueta):
        self.etiqueta=etiqueta
        
    def set_contenido(self, contenido):
        self.contenido=contenido
        
    def anadir_atributo(self, atributo):
        if self.atributos==None:
            self.atributos=[]
        self.atributos.append(atributo)
    
    def get_cadena_atributos(self):
        cadenas_atributos=[]
        for k, v in enumerate(self.diccionario_atributos):
            cadena_atributos='{0}="{1}"'.format()
            cadenas_atributos.append
    def get_xml(self):
        return "<{0}>{1}</{0}>".format(etiqueta, contenido, etiqueta)
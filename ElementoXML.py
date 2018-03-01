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

class TipoSimpleConRestriccion(TipoBasicoW3C):
    def __init__(self, nombre_tipo, nombre_base):
        self.nombre_tipo=nombre_tipo
        self.nombre_base=nombre_base
        self.minimo=None
        self.maximo=None
        self.restricciones=[]
    
    def get_esquema(self):
        plantilla="""<xsd:simpleType name="{0}"><xsd:restriction base="{1}">{2}</xsd:restriction></xsd:simpleType>"""
        restricciones="".join(self.restricciones)

        esquema=plantilla.format(self.nombre_tipo, self.nombre_base, restricciones)
        return esquema
    
class TipoSimpleIntegerConRestriccion(TipoSimpleConRestriccion):
    def __init__(self, nombre_tipo, nombre_base):
        super().__init__(nombre_tipo, nombre_base)
        
    def add_minInclusive(self, valor):
        self.minimo=valor
        xsd_minimo="<xsd:minInclusive value=\"{0}\"/>"
        restriccion=xsd_minimo.format(self.minimo)
        self.restricciones.append(restriccion)
        
    def add_maxInclusive(self, valor):
        self.maximo=valor
        xsd_maximo="<xsd:minInclusive value=\"{0}\"/>"
        restriccion=xsd_maximo.format(self.maximo)
        self.restricciones.append(restriccion)
        
    
        
class TipoSimpleFloatConRestriccion(TipoSimpleIntegerConRestriccion):
    def __init__(self, nombre_tipo):
        super().__init__(nombre_tipo, "xsd:float")
        
    def add_digitos_totales(self, digitos_totales):
        xsd_digitos="<xsd:totalDigits value=\"{0}\"/>"
        restriccion=xsd_digitos.format(digitos_totales)
        self.restricciones.append(restriccion)
        
    def add_digitos_decimales(self, digitos_decimales):
        xsd_digitos="<xsd:fractionDigits value=\"{0}\"/>"
        restriccion=xsd_digitos.format(digitos_decimales)
        self.restricciones.append(restriccion)
        
class TipoSimpleStringConPatron(TipoSimpleConRestriccion):
    def __init__(self, nombre_tipo):
        super().__init__(nombre_tipo, "xsd:string")
    def add_patron(self, patron):
        xsd_patron="<xsd:pattern value=\"{0}\"/>"
        restriccion=xsd_patron.format(patron)
        self.restricciones.append(restriccion)
        
class TipoSimpleStringConEnumeraciones(TipoSimpleConRestriccion):
    def __init__(self, nombre_tipo):
        super().__init__(nombre_tipo, "xsd:string")
    def add_valores(self, lista_valores):
        plantilla_enumeration="<xsd:enumeration value=\"{0}\"/>"
        for valor in lista_valores:
            restriccion=plantilla_enumeration.format(valor)
            self.restricciones.append(restriccion)
        
class TipoAtributo(object):
    def __init__(self, nombre_atributo, nombre_base, obligatorio=False):
        self.esquema=""
        if obligatorio:
            xsd_atributo="<xsd:attribute name=\"{0}\" type=\"{1}\" use=\"required\"/>"
        else:
            xsd_atributo="<xsd:attribute name=\"{0}\" type=\"{1}\"/>"
        self.esquema=xsd_atributo.format(nombre_atributo, nombre_base)
    def get_esquema(self):
        return self.esquema
    
class TipoComplejoConAtributos(object):
    def __init__(self, nombre_tipo, nombre_base, lista_atributos):
        xsd="""
        <xsd:complexType name="{0}">
        <xsd:simpleContent>
            <xsd:extension base="{1}">
                {2}
            </xsd:extension>
        </xsd:simpleContent>
        </xsd:complexType>
        """
        atributos=""
        for a in lista_atributos:
            atributos+=a.get_esquema()
        self.esquema=xsd.format(nombre_tipo, nombre_base, atributos)
    def get_esquema(self):
        return self.esquema
        
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
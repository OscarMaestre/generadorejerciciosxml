#!/usr/bin/env python3
#coding=utf-8

ANY_TYPE="anyType"



def reemplazar_xsd(cadena):
    reemplazos=[ ("<complexType", "<xsd:complexType"), ("</complexType>", "</xsd:complexType>"),
                 ("<simpleType", "<xsd:simpleType"), ("</simpleType>", "</xsd:simpleType>"), 
                 ("<complexContent>", "<xsd:complexContent>"), ("</complexContent>", "</xsd:complexContent>"),
                 ("<simpleContent>", "<xsd:simpleContent>"), ("</simpleContent>", "</xsd:simpleContent>"),
                 ("<attribute", "<xsd:attribute"),
                 ("<extension", "<xsd:extension"), ("</extension>", "</xsd:extension>"),
                 ("<restriction", "<xsd:restriction"), ("</restriction>", "</xsd:restriction>"),
                 ("<enumeration", "<xsd:enumeration"), ("</enumeration>", "</xsd:enumeration>"),
                 ("<fractionDigits", "<xsd:fractionDigits"), ("</fractionDigits>", "</xsd:fractionDigits>"),
                 ("<totalDigits", "<xsd:totalDigits"), ("</totalDigits>", "</xsd:totalDigits>"),
                 ("<minInclusive", "<xsd:minInclusive"), ("</minInclusive>", "</xsd:minInclusive>"),
                 ("<maxInclusive", "<xsd:maxInclusive"), ("</maxInclusive>", "</xsd:maxInclusive>"),
                 ("<pattern", "<xsd:pattern"), ("</pattern>", "</xsd:pattern>"),
                 
                 
                 ]
    
    for r in reemplazos:
        cadena=cadena.replace(r[0], r[1])
    return cadena


def get_esquema_alineado(objeto, separador="  "):
    esquema=objeto.get_esquema().strip()
    trozos=esquema.split(">")
    trozos_con_fin=[(t+">").strip() for t in trozos]
    trozos_esquema=trozos_con_fin[:-1]
    nivel=0
    cadena_esquema=""
    for t in trozos_esquema:
        
        #Si es trozo de cierre
        if t[0:2]=="</":
            nivel=nivel-1
            cadena_esquema+=(separador*nivel) + t +"\n"
            continue
        if t[-2:]=="/>":
            cadena_esquema+=(separador*nivel) + t +"\n"
            continue
        #En el resto de casos es una etiqueta de apertura,POR ESTE ORDEN
        #anadimos e incrementmos
        cadena_esquema+=(separador*nivel) + t +"\n"
        nivel=nivel+1
        
    #Fin del for
        
    return cadena_esquema
    
    
class TipoBasicoW3C(object):
    def get_esquema(self):
        plantilla="<xsd:element name=\"{0}\" type=\"{1}\" />"
        descripcion="{0}".format(self.nombre_tipo_basico, self.nombre_elemento)
        return descripcion
    def get_esquema_alineado(self):
        return get_esquema_alineado(self)
    
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
    
class TipoSimpleNumericoConRestriccion(TipoSimpleConRestriccion):
    def __init__(self, nombre_tipo, nombre_base):
        super().__init__(nombre_tipo, nombre_base)
        
    def add_minInclusive(self, valor):
        self.minimo=valor
        xsd_minimo="<xsd:minInclusive value=\"{0}\"/>"
        restriccion=xsd_minimo.format(self.minimo)
        self.restricciones.append(restriccion)
        
    def add_maxInclusive(self, valor):
        self.maximo=valor
        xsd_maximo="<xsd:maxInclusive value=\"{0}\"/>"
        restriccion=xsd_maximo.format(self.maximo)
        self.restricciones.append(restriccion)
        
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
    def get_esquema_alineado(self):
        return get_esquema_alineado(self)
    
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
    def get_esquema_alineado(self):
        return get_esquema_alineado(self)

class TipoNumericoConRestriccionesMasAtributos(TipoSimpleNumericoConRestriccion):
    def __init__(self, nombre_tipo, nombre_base, lista_atributos):
        nombre_tipo_restringido=nombre_tipo+"Restringido"
        self.tipo_simple_restringido=TipoSimpleNumericoConRestriccion(nombre_tipo_restringido, nombre_base)
        self.tipo_complejo_con_atributos=TipoComplejoConAtributos(
            nombre_tipo, nombre_tipo_restringido, lista_atributos)
    
    def add_minInclusive(self, valor):
        self.tipo_simple_restringido.add_minInclusive(valor)
        
    def add_maxInclusive(self, valor):
        self.maximo=valor
        xsd_maximo="<xsd:maxInclusive value=\"{0}\"/>"
        restriccion=xsd_maximo.format(self.maximo)
        self.restricciones.append(restriccion)
        
    def add_digitos_totales(self, digitos_totales):
        xsd_digitos="<xsd:totalDigits value=\"{0}\"/>"
        restriccion=xsd_digitos.format(digitos_totales)
        self.restricciones.append(restriccion)
        
    def add_digitos_decimales(self, digitos_decimales):
        xsd_digitos="<xsd:fractionDigits value=\"{0}\"/>"
        restriccion=xsd_digitos.format(digitos_decimales)
        self.restricciones.append(restriccion)
        
    def get_esquema(self):
        esquema_simple=self.tipo_simple_restringido.get_esquema()
        esquema_complejo=self.tipo_complejo_con_atributos.get_esquema()
        return esquema_simple + esquema_complejo
    def get_esquema_alineado(self):
        esquema_simple_alineado=get_esquema_alineado(self.tipo_simple_restringido)
        esquema_complejo=get_esquema_alineado(self.tipo_complejo_con_atributos)
        return esquema_simple_alineado + "\n" + esquema_complejo
        
class TipoCadenaConRestriccionesMasAtributos(object):
    TIPO_RESTRICCION_ENUMERACION    = 1
    TIPO_RESTRICCION_PATRON         = TIPO_RESTRICCION_ENUMERACION + 1
    
    def __init__(self, nombre_tipo,  lista_atributos, tipo_restriccion):
        nombre_base="xsd:string"
        nombre_tipo_restringido=nombre_tipo+"Restringido"
        self.tipo_simple_restringido=None
        self.tipo_restriccion = tipo_restriccion
        if tipo_restriccion==TipoCadenaConRestriccionesMasAtributos.TIPO_RESTRICCION_ENUMERACION:
            self.tipo_simple_restringido=TipoSimpleStringConEnumeraciones(nombre_tipo_restringido)
        if tipo_restriccion==TipoCadenaConRestriccionesMasAtributos.TIPO_RESTRICCION_PATRON:
            self.tipo_simple_restringido=TipoSimpleStringConPatron(nombre_tipo_restringido)
            
        self.tipo_complejo_con_atributos=TipoComplejoConAtributos(
            nombre_tipo, nombre_tipo_restringido, lista_atributos)
        
    def get_esquema(self):
        esquema_simple=self.tipo_simple_restringido.get_esquema()
        esquema_complejo=self.tipo_complejo_con_atributos.get_esquema()
        return esquema_simple + esquema_complejo
    def get_esquema_alineado(self):
        esquema_simple_alineado=get_esquema_alineado(self.tipo_simple_restringido)
        esquema_complejo=get_esquema_alineado(self.tipo_complejo_con_atributos)
        return esquema_simple_alineado + "\n" + esquema_complejo
        
    def add_valores(self, lista_valores):
        if self.tipo_restriccion!=TipoCadenaConRestriccionesMasAtributos.TIPO_RESTRICCION_ENUMERACION:
            print("Error, se esta intentando añadir enumeration y al crearlo se dijo que no sería de tipo enumeration")
            raise Exception
        self.tipo_simple_restringido.add_valores(lista_valores)
        
    def add_patron(self, patron):
        if self.tipo_restriccion!=TipoCadenaConRestriccionesMasAtributos.TIPO_RESTRICCION_PATRON:
            print("Error, se esta intentando añadir pattern y al crearlo se dijo que no sería de tipo pattern")
            raise Exception
        self.tipo_simple_restringido.add_patron(patron)
        
class TipoComplejo(object):
    def __init__(self, nombre_tipo, restriccion, lista_atributos):
        plantilla="""
        <xsd:complexType name="{0}">
            <xsd:complexContent>
                <xsd:restriction base="xsd:anyType">
                    {1}
                </xsd:restriction>
                {2}
            </xsd:complexContent>
        </xsd:complexType>
        """
        esquema_restriccion=restriccion.get_esquema()
        lista_esquemas_atributos=[atributo.get_esquema for atributo in lista_atributos]
        esquema_atributos="".join(lista_esquemas_atributos)
        esquema=plantilla.format(nombre_tipo, restriccion, esquema_atributos)
        
        

class RestriccionSecuenciaElementosXML(TipoBasicoW3C):
    def __init__(self, lista_elementos):
        plantilla="<xsd:sequence>{0}</xsd:sequence>"
        elementos="".join(lista_elementos)
        esquema=plantilla.format(elementos)
        
    def get_esquema(self):
        return esquema
    
class RestriccionChoice(TipoBasicoW3C):
    def __init__(self, lista_elementos):
        plantilla="<xsd:choice maxOccurs=\"unbounded\">{0}</xsd:sequence>"
        elementos="".join(lista_elementos)
        esquema=plantilla.format(elementos)
        
    def get_esquema(self):
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
    def get_xml_abreviado(self):
        return "<{0}/>".format(etiqueta, contenido, etiqueta)
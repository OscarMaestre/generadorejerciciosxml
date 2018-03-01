#!/usr/bin/env python3

from ElementoXML import *

prueba_float=TipoSimpleFloatConRestriccion("tipoPeso")
prueba_float.add_digitos_decimales(2)
prueba_float.add_digitos_totales(6)
prueba_float.add_minInclusive(3000)
prueba_float.add_maxInclusive(9000)
print (prueba_float.get_esquema())
print()

prueba_patron=TipoSimpleStringConPatron("tipoCodigo")
prueba_patron.add_patron("[A-Z]{2}")
print(prueba_patron.get_esquema())
print()


prueba_valores=TipoSimpleStringConEnumeraciones("tipoFabricante")
prueba_valores.add_valores(["FAB1", "FAB2", "FAB3"])
print(prueba_valores.get_esquema())
print()

prueba_atributo1=TipoAtributo("sede", "xsd:string")
print(prueba_atributo1.get_esquema())

prueba_atributo2=TipoAtributo("codigo", "xsd:string", True)
print(prueba_atributo2.get_esquema())
lista_atributos=[prueba_atributo1, prueba_atributo2]

prueba_tipocomplejoatributos=TipoComplejoConAtributos("tipoHotel", "xsd:string",lista_atributos)
print(prueba_tipocomplejoatributos.get_esquema())
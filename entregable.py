from enum import Enum

class Ubicacion(Enum):
    ENDOR = 1
    CUMULO_RAMIOS = 2
    NEBULOSA_KALIIDA = 3

class Clase(Enum):
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3

class UnidadCombate():
    def __init__(self, id_combate:str, clave:int):
        self.id_combate = id_combate
        self.clave = clave

class Nave(UnidadCombate):
    def __init__(self, id_combate:str, clave:int, nombre:str, piezas:list[str] = None):
        super().__init__(id_combate, clave)
        self.nombre = nombre
        self.piezas = piezas if piezas else []

class EstacionEspacial(Nave):
    def __init__(self, id_combate:str, clave:int, nombre:str, tripulacion:int, pasaje:int, ubicacion: Ubicacion, piezas:list[str]=None):
        super().__init__(id_combate, clave, nombre, piezas)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion

class NaveEstelar(Nave):
    def __init__(self, id_combate:str, clave:int, nombre:str, tripulacion:int, pasaje:int, clase: Clase, piezas:list[str]=None):
        super().__init__(id_combate, clave, nombre, piezas)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase

class CazaEstelar(Nave):
    def __init__(self, id_combate:str, clave:int, nombre:str, dotacion:int, piezas:list[str]=None):
        super().__init__(id_combate, clave, nombre, piezas)
        self.dotacion = dotacion

class Repuesto:
    def __init__(self, nombre, proveedor, cantidad, precio):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad
        self.precio = precio

class Almacen:

    def __init__(self, nombre:str, id_almacen: int, localizacion:str, catalogo: list[Repuesto] = None):
        self.nombre = nombre
        self.id_almacen = id_almacen
        self.localizacion = localizacion
        self.catalogo = catalogo if catalogo else []

class Usuario:
    def __init__(self, nombre:str, id_usuario:int):
        self.nombre = nombre
        self.id_usuario = id_usuario

class Comandante(Usuario):
    def __init__(self, nombre, id_usuario):
        super().__init__(nombre, id_usuario)

class Operario(Usuario):
    def __init__(self, nombre, id_usuario):
        super().__init__(nombre, id_usuario) 
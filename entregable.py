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

        if not id_combate:
            raise ValueError("El id de combate no puede estar vacío")
        if clave <= 0:
            raise ValueError("La clave debe ser positiva")

        self.id_combate = id_combate
        self.clave = clave

    def __str__(self):
        return f"Id: {self.id_combate} \nClave: {self.clave}"

class Nave(UnidadCombate):
    def __init__(self, id_combate:str, clave:int, nombre:str, piezas:list[str] = None):
        super().__init__(id_combate, clave)

        if not nombre:
            raise ValueError("El nombre de la nave no puede estar vacío")
        
        self.nombre = nombre
        self.piezas = piezas if piezas else []

    def __str__(self):
        return  super().__str__() + f"\nNombre: {self.nombre} \nPiezas: {', '.join(self.piezas)}"

    def añadir_piezas(self, pieza_repuesto):
        if pieza_repuesto in self.piezas:
            raise ValueError("Pieza ya incluida")
        self.piezas.append(pieza_repuesto)

    def quitar_piezas(self, pieza_repuesto):
        if pieza_repuesto not in self.piezas:
            raise ValueError("Pieza no disponible")
        self.piezas.remove(pieza_repuesto)

    def listar_piezas(self):
        print(f"La lista de piezas de la nave {self.nombre} es: {', '.join(self.piezas)}") 

    def tiene_pieza(self, pieza):
        return pieza in self.piezas

    def numero_piezas(self):
        return len(self.piezas)

    def vaciar_piezas(self):
        self.piezas.clear()


class EstacionEspacial(Nave):
    def __init__(self, id_combate:str, clave:int, nombre:str, tripulacion:int, pasaje:int, ubicacion: Ubicacion, piezas:list[str]=None):
        super().__init__(id_combate, clave, nombre, piezas)

        if tripulacion < 0 or pasaje < 0:
            raise ValueError("Capacidad inválida")

        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion

    def __str__(self):
        return super().__str__() + f"\nTripulacion: {self.tripulacion} \nPasaje: {self.pasaje} \nUbicacion: {self.ubicacion}"

    def get_ubicacion(self):
        return self.ubicacion
    
    def set_ubicacion(self, ubicacion : Ubicacion):
        self.ubicacion = ubicacion

    def get_capacidad(self):
        return self.tripulacion + self.pasaje
    
    def añadir_pasajeros(self, cantidad):
        if cantidad <= 0:
            raise ValueError("Cantidad inválida")
        self.pasaje += cantidad

    def quitar_pasajeros(self, cantidad):
        if cantidad <= 0 or cantidad > self.pasaje:
            raise ValueError("Cantidad inválida")
        self.pasaje -= cantidad

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
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

    def __str__(self):
        return  super().__str__() + f", tripulacion: {self.tripulacion}, pasaje: {self.pasaje}, clase: {self.clase}"

    def get_clase(self):
        return self.clase
    
    def set_clase(self, clase : Clase):
        self.clase = clase

    def get_capacidad(self):
        return self.tripulacion + self.pasaje
    

class CazaEstelar(Nave):
    def __init__(self, id_combate:str, clave:int, nombre:str, dotacion:int, piezas:list[str]=None):
        super().__init__(id_combate, clave, nombre, piezas)

        if dotacion <= 0:
            raise ValueError("La dotación debe ser positiva")
        
        self.dotacion = dotacion

    def __str__(self):
        return super().__str__() + f"\nDotacion: {self.dotacion}"
    
    def get_dotacion(self):
        return self.dotacion
    
    def set_dotacion(self, dotacion : int):
        if dotacion <= 0:
            raise ValueError("La dotación debe ser positiva")
        self.dotacion = dotacion

    def aumentar_dotacion(self, cantidad):
        if cantidad <= 0:
            raise ValueError("Cantidad inválida")
        self.dotacion += cantidad

    def reducir_dotacion(self, cantidad):
        if cantidad <= 0 or cantidad > self.dotacion:
            raise ValueError("Cantidad inválida")
        self.dotacion -= cantidad

class Repuesto:
    def __init__(self, nombre, proveedor, cantidad, precio):

        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        if not proveedor:
            raise ValueError("El proveedor no puede estar vacío")
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        if precio <= 0:
            raise ValueError("El precio debe ser positivo")
        
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad
        self.precio = precio
    
    def __str__(self):
        return f'Repuesto: {self.nombre} \nCantidad: {self.__cantidad} \nProveedor: {self.proveedor} \nPrecio: {self.precio}'

    def disminuir_cantidad(self, cantidad):
        if cantidad <= 0:
            raise ValueError("Cantidad inválida")
        if cantidad > self.__cantidad:
            raise ValueError(f"No hay suficiente stock de {self.nombre} (disponibles: {self.__cantidad})")
        self.__cantidad -= cantidad
            
    def aumentar_cantidad(self, cantidad):
        if cantidad <= 0:
            raise ValueError("Cantidad inválida")
        self.__cantidad += cantidad

    def consultar_disponibilidad(self):
        return self.__cantidad > 0

    def get_cantidad(self):
        return self.__cantidad
    
    def get_precio(self):
        return self.precio

    def set_precio(self, precio):
        if precio <= 0:
            raise ValueError("Precio inválido")
        self.precio = precio

    def valor_total_stock(self):
        return self.__cantidad * self.precio

class Almacen:

    def __init__(self, nombre:str, id_almacen: int, localizacion:str, catalogo: list[Repuesto] = None):
        
        if not nombre:
            raise ValueError("El nombre del almacén no puede estar vacío")
        if not localizacion:
            raise ValueError("La localización no puede estar vacía")
        
        self.nombre = nombre
        self.id_almacen = id_almacen
        self.localizacion = localizacion
        self.catalogo = catalogo if catalogo else []

    def __str__(self):
        return f"Almacen {self.nombre} \nLocalizacion: {self.localizacion}"

    def repuesto_en_almacen(self, repuesto):
        return repuesto in self.catalogo
    
    def buscar_repuesto(self, nombre):
        for r in self.catalogo:
            if r.nombre == nombre:
                return r
        return None
    
    def añadir_repuesto(self, repuesto : Repuesto):
        if not isinstance(repuesto, Repuesto):
            raise ValueError('El objeto proporcionado no es un repuesto válido. Debe ser una instancia de la clase Repuesto.')
        if repuesto in self.catalogo:
            raise ValueError(f'El repuesto "{repuesto.nombre}" ya existe en el catálogo.')
        else:
            self.catalogo.append(repuesto)

    def quitar_repuesto(self, repuesto : Repuesto):
        if not isinstance(repuesto, Repuesto):
            raise ValueError('El objeto proporcionado no es un repuesto válido. Debe ser una instancia de la clase Repuesto.')
        if repuesto not in self.catalogo:
            raise ValueError(f'El repuesto "{repuesto.nombre}" no existe en el catálogo.')
        else:
            self.catalogo.remove(repuesto)

    def listar_repuestos(self):
        print(f"La lista de repuestos en el almacén {self.id_almacen} es: {', '.join(r.nombre for r in self.catalogo)}")

class Usuario:
    def __init__(self, nombre:str, id_usuario:int):

        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        if id_usuario <= 0:
            raise ValueError("El id de usuario debe ser positivo")
    
        self.nombre = nombre
        self.id_usuario = id_usuario
        
    def __str__(self):
        return f"Nombre: {self.nombre}"

class Comandante(Usuario):
    
    def __init__(self, nombre, id_usuario):
        super().__init__(nombre, id_usuario)

    def consultar_almacen(self, almacen: Almacen):
        almacen.listar_repuestos()

    def adquirir_repuesto(self, repuesto, cantidad, imperio):
        for almacen in imperio.almacenes:
            if almacen.repuesto_en_almacen(repuesto):
                repuesto.disminuir_cantidad(cantidad)
                return
        raise ValueError("No encontrado en ningún almacén")
    
    def es_comandante(self):
        return True
    
class Operario(Usuario):
    def __init__(self, nombre, id_usuario):
        super().__init__(nombre, id_usuario) 
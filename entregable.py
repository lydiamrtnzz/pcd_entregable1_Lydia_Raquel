from enum import Enum
from abc import ABC, abstractmethod

class Ubicacion(Enum):
    ENDOR = 1
    CUMULO_RAMIOS = 2
    NEBULOSA_KALIIDA = 3

class Clase(Enum):
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3

class UnidadCombate(ABC):
    def __init__(self, id_combate:str, clave:int):

        if not id_combate:
            raise ValueError("El id de combate no puede estar vacío")
        if clave <= 0:
            raise ValueError("La clave debe ser positiva")

        self.id_combate = id_combate
        self.clave = clave

    @abstractmethod
    def __str__(self):
        return f"Id: {self.id_combate} \nClave: {self.clave}"

class Nave(UnidadCombate, ABC):
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


class DatosCapacidad:
    def __init__(self, tripulacion:int, pasaje:int):
        if tripulacion < 0 or pasaje < 0:
            raise ValueError("Capacidad inválida")
        self.tripulacion = tripulacion
        self.pasaje = pasaje

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

class EstacionEspacial(Nave, DatosCapacidad):
    def __init__(self, id_combate:str, clave:int, nombre:str, tripulacion:int, pasaje:int, ubicacion: Ubicacion, piezas:list[str]=None):
        # Llamamos a los dos padres
        Nave.__init__(self, id_combate, clave, nombre, piezas)
        DatosCapacidad.__init__(self, tripulacion, pasaje)
        self.ubicacion = ubicacion

    def __str__(self):
        return Nave.__str__(self) + f"\nTripulacion: {self.tripulacion} \nPasaje: {self.pasaje} \nUbicacion: {self.ubicacion}"

    def get_ubicacion(self):
        return self.ubicacion
    
    def set_ubicacion(self, ubicacion : Ubicacion):
        self.ubicacion = ubicacion
    

class NaveEstelar(Nave, DatosCapacidad):
    def __init__(self, id_combate:str, clave:int, nombre:str, tripulacion:int, pasaje:int, clase: Clase, piezas:list[str]=None):
        Nave.__init__(self, id_combate, clave, nombre, piezas)
        DatosCapacidad.__init__(self, tripulacion, pasaje)
        self.clase = clase
    
    def __str__(self):
        return  Nave.__str__(self) + f", tripulacion: {self.tripulacion}, pasaje: {self.pasaje}, clase: {self.clase}"

    def get_clase(self):
        return self.clase
    
    def set_clase(self, clase : Clase):
        self.clase = clase 

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

    def get_catalogo(self):
        return self.catalogo

    def listar_repuestos(self):
        print(f"La lista de repuestos en el almacén {self.id_almacen} es: {', '.join(r.nombre for r in self.get_catalogo())}")

class Usuario(ABC):
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
    
class Operario(Usuario):
    def __init__(self, nombre, id_usuario):
        super().__init__(nombre, id_usuario)   

    def gestionar_stock(self, almacen:Almacen):
        for elem in almacen.catalogo.copy():  
            # Usamos copy() porque si recorremos directamente almacen.catalogo
            # y eliminamos elementos durante la iteración, la lista puede cambiar
            # de tamaño y provocar errores o saltarse elementos.
            if not elem.consultar_disponibilidad():
                almacen.quitar_repuesto(elem)

    def añadir_repuesto(self, almacen: Almacen, repuesto: Repuesto):
        if almacen.repuesto_en_almacen(repuesto):
            raise ValueError("El repuesto ya existe en el almacén")
        almacen.añadir_repuesto(repuesto)

class MiImperio:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.usuarios = []
        self.unidades_combate = []
        self.almacenes = []

    def alta_usuario(self, usuario: Usuario):
        if not isinstance(usuario, Usuario):
            raise ValueError('El objeto proporcionado no es un Usuario válido. Debe ser una instancia de la clase Usuario.')
        if usuario in self.usuarios:
            raise ValueError(f'El usuario "{usuario.nombre}" ya existe en el imperio.')
        else:
            self.usuarios.append(usuario)

    def alta_unidad_combate(self, unidad_combate):
        if not isinstance(unidad_combate, UnidadCombate):
            raise ValueError('El objeto proporcionado no es una Unidad de Combate válida. Debe ser una instancia de la clase UnidadCombate.')
        if unidad_combate in self.unidades_combate:
            raise ValueError(f'La Unidad de Combate "{unidad_combate.id_combate}" ya existe en el imperio.')
        else:
            self.unidades_combate.append(unidad_combate)

    def alta_almacen(self, almacen: Almacen):
        if not isinstance(almacen, Almacen):
            raise ValueError('El objeto proporcionado no es un almacén válido. Debe ser una instancia de la clase Almacen.')
        if almacen in self.almacenes:
            raise ValueError(f'El almacén "{almacen.nombre}" ya existe en el imperio.')
        else:
            self.almacenes.append(almacen)

    def baja_usuario(self, usuario: Usuario):
        if not isinstance(usuario, Usuario):
            raise ValueError('El objeto proporcionado no es un Usuario válido. Debe ser una instancia de la clase Usuario.')
        if usuario not in self.usuarios:
            raise ValueError(f'El usuario "{usuario.nombre}" no existe en el imperio.')
        else:
            self.usuarios.remove(usuario)

    def baja_unidad_combate(self, unidad_combate):
        if not isinstance(unidad_combate, UnidadCombate):
            raise ValueError('El objeto proporcionado no es una Unidad de Combate válida. Debe ser una instancia de la clase UnidadCombate.')
        if unidad_combate not in self.unidades_combate:
            raise ValueError(f'La Unidad de Combate "{unidad_combate.nombre}" no existe en el imperio.')
        else:
            self.unidades_combate.remove(unidad_combate)

    def baja_almacen(self, almacen: Almacen):
        if not isinstance(almacen, Almacen):
            raise ValueError('El objeto proporcionado no es un almacén válido. Debe ser una instancia de la clase Almacen.')
        if almacen not in self.almacenes:
            raise ValueError(f'El almacén "{almacen.nombre}" no existe en el imperio.')
        else:
            self.almacenes.remove(almacen)

    def listar_usuarios(self):
        print(', '.join(u.nombre for u in self.usuarios))
    
    def listar_unidades_combate(self):
        print(', '.join(u.id_combate for u in self.unidades_combate))

    def listar_almacenes(self):
        print(', '.join(a.nombre for a in self.almacenes))

def demo():
    print("=== DEMO MiImperio ===\n")
    try:
        # Crear imperio
        imperio = MiImperio("Imperio Galáctico")
        print(f"Creado {imperio.nombre}\n")

        # Crear usuarios
        comandante = Comandante("Pepita", 101)
        operario = Operario("Rico", 102)

        # Alta de usuarios
        imperio.alta_usuario(comandante)
        imperio.alta_usuario(operario)
        print("Usuarios dados de alta en el imperio:")
        imperio.listar_usuarios()
        print()

        # Crear repuestos
        repuesto1 = Repuesto("Motor X", "Proveedor1", 5, 1000)
        repuesto2 = Repuesto("Escudo Y", "Proveedor2", 3, 1500)
        repuesto3 = Repuesto("Láser Z", "Proveedor3", 0, 2000)  # Cantidad 0 para probar eliminación

        # Crear almacén y añadir repuestos
        almacen = Almacen("Central", 1, "Endor")
        try:
            operario.añadir_repuesto(almacen, repuesto1)
            operario.añadir_repuesto(almacen, repuesto2)
            operario.añadir_repuesto(almacen, repuesto3)
        except ValueError as e:
            print("Error al añadir repuesto:", e)

        imperio.alta_almacen(almacen)
        print(f"Almacén {almacen.nombre} añadido al imperio\n")

        # Listar repuestos con stock y valor total
        print("Repuestos en el almacén (cantidad y valor total):")
        for r in almacen.catalogo:
            print(f"{r.nombre}: {r.get_cantidad()} unidades, Valor total: {r.valor_total_stock()}")
        print()

        # Crear unidades de combate
        nave1 = NaveEstelar("NC-01", 1, "Eclipse", 10, 20, Clase.ECLIPSE)
        nave2 = CazaEstelar("C-01", 2, "Faucon", 5)
        estacion = EstacionEspacial("ES-01", 3, "Estación Endor", 50, 100, Ubicacion.ENDOR)

        # Alta de unidades en imperio
        imperio.alta_unidad_combate(nave1)
        imperio.alta_unidad_combate(nave2)
        imperio.alta_unidad_combate(estacion)
        print("Unidades de combate en el imperio:")
        imperio.listar_unidades_combate()
        print()

        # Comandante adquiere repuesto
        try:
            comandante.adquirir_repuesto(repuesto1, 2, imperio)
            comandante.adquirir_repuesto(repuesto2, 1, imperio)
        except ValueError as e:
            print("Error al adquirir repuesto:", e)
        print("Stock después de adquisiciones del comandante:")
        for r in almacen.catalogo:
            print(f"{r.nombre}: {r.get_cantidad()} unidades")
        print()

        # Operario gestiona stock (elimina repuesto3 porque cantidad=0)
        operario.gestionar_stock(almacen)
        print("Stock después de gestión de operario:")
        for r in almacen.catalogo:
            print(f"{r.nombre}: {r.get_cantidad()} unidades")
        print()

        # Probar añadir y quitar piezas en nave1
        try:
            nave1.añadir_piezas("Motor X")
            nave1.añadir_piezas("Escudo Y")
            print(f"Piezas de {nave1.nombre} después de añadir:")
            nave1.listar_piezas()
            print(f"Número de piezas: {nave1.numero_piezas()}")
            nave1.quitar_piezas("Motor X")
            print(f"Piezas de {nave1.nombre} después de quitar Motor X:")
            nave1.listar_piezas()
        except ValueError as e:
            print("Error en gestión de piezas:", e)
        print()

        # Cambiar ubicación de estación y añadir/quitar pasajeros
        print(f"Ubicación original de {estacion.nombre}: {estacion.get_ubicacion()}")
        estacion.set_ubicacion(Ubicacion.NEBULOSA_KALIIDA)
        print(f"Ubicación nueva de {estacion.nombre}: {estacion.get_ubicacion()}")
        estacion.añadir_pasajeros(10)
        print(f"Pasaje después de añadir 10 pasajeros: {estacion.pasaje}")
        estacion.quitar_pasajeros(5)
        print(f"Pasaje después de quitar 5 pasajeros: {estacion.pasaje}\n")

        # Probar aumentar/reducir dotación caza estelar
        print(f"Dotación original de {nave2.nombre}: {nave2.dotacion}")
        nave2.aumentar_dotacion(3)
        print(f"Dotación después de aumentar: {nave2.dotacion}")
        nave2.reducir_dotacion(2)
        print(f"Dotación después de reducir: {nave2.dotacion}")

        # Mostrar capacidades
        print(f"Capacidad total de {nave1.nombre}: {nave1.get_capacidad()}")
        print(f"Capacidad total de {estacion.nombre}: {estacion.get_capacidad()}\n")

        # Bajas de usuarios, unidades y almacenes
        imperio.baja_usuario(comandante)
        imperio.baja_unidad_combate(nave2)
        imperio.baja_almacen(almacen)
        print("Después de bajas:")
        print("Usuarios:")
        imperio.listar_usuarios()
        print("Unidades de combate:")
        imperio.listar_unidades_combate()
        print("Almacenes:")
        imperio.listar_almacenes()

    except Exception as e:
        print("Error demo:", e)

if __name__ == "__main__":
    demo()
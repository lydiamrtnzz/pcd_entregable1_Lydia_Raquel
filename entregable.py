from enum import Enum
from abc import ABC

class Ubicacion(Enum):
    ENDOR = 1
    CUMULO_RAMIOS = 2
    NEBULOSA_KALIIDA = 3

class Clase(Enum):
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3

# vamos a crear una nueva clase, para definir el estado de la nave

class Estado(Enum):
    OPERATIVA = 1
    DANADA = 2

# CLASE UNIDAD DE COMBATE 
# Clase abstracta que representa una unidad de combate del imperio.
# Sirve como clase base para todas las naves de combate del imperio

# Decidimos implementarla como abstracta, para forzar a que no se pueda instanciar. 
# Aunque no encontramos métodos comunes en todos los hijos y por ello no definimos métodos abstractos

class UnidadCombate(ABC):
    def __init__(self, id_combate:str, clave:int):

        if not id_combate:
            raise ValueError("El id de combate no puede estar vacío")
        if clave <= 0:
            raise ValueError("La clave debe ser positiva")

        self.id_combate = id_combate # identificador único de la unidad de combate
        self.clave = clave # clave de la unidad
        self.estado = Estado.OPERATIVA # Estado inicial de la unidad (OPERATIVA)

    # vamos a añadir unos metodos, para ver si estas naves están disponibles o no

    def esta_operativa(self):

        # Comprueba si la unidad está operativa. 
        # Donde va a devolver un booleano --> True si la unidad está operativa y False en caso contrario.
        
        return self.estado == Estado.OPERATIVA

    def necesita_reparacion(self):

        # Comprueba si la unidad necesita reparación
        # devuelve un booleano --> True si la unidad está dañada, False si está operativa

        return self.estado == Estado.DANADA

    def reparar(self):

        #  Repara la unidad, cambiando su estado a OPERATIVA.

        self.estado = Estado.OPERATIVA

    def cambiar_estado(self):

        # Cambia el estado de la unidad.
        # - Si está OPERATIVA, pasa a DANADA.
        # - Si está DANADA, se repara y vuelve a OPERATIVA.

        if self.estado == Estado.OPERATIVA:
            self.estado = Estado.DANADA
        else:
            self.reparar()

    def get_estado(self):

        #  Devuelve el estado actual de la unidad como string ('OPERATIVA' o 'DANADA')

        return self.estado.name

    def __str__(self):

        # Representación en cadena de la unidad, mostrando id y clave

        return f"Id: {self.id_combate} \nClave: {self.clave}"
       
# CLASE NAVE 
# Se trata de una clase abstracta que representa una nave del imperio
# Esta clase hereda de UnidadCombate, por lo tanto, al heredar va a tomar sus atributos (nombre y piezas)

# Decidimos implementarla como abstracta, para forzar a que no se pueda instanciar. 
# Aunque no encontramos métodos comunes en todos los hijos y por ello no definimos métodos abstractos

class Nave(UnidadCombate, ABC):

    def __init__(self, id_combate:str, clave:int, nombre:str, piezas:list[str] = None):
       
        super().__init__(id_combate, clave)# Inicializa atributos heredados de UnidadCombate

        if not nombre:
            raise ValueError("El nombre de la nave no puede estar vacío")
        
        self.nombre = nombre # nombre de la nave
        self.piezas = piezas if piezas else [] # lista inicial de piezas de la nave

    def __str__(self):

        # Devuelve la representación en cadena de la nave, incluyendo los datos heredados
        # y su nombre y piezas actuales.

        return  super().__str__() + f"\nNombre: {self.nombre} \nPiezas: {', '.join(self.piezas)}"

    def añadir_piezas(self, pieza_repuesto):

        # este método lo que hace es añadir una pieza a la nave, donde pieza_repuesto es el nombre de la pieza añadida
        # nos va a devolver una excepción si la pieza ya existe en la nave 

        if pieza_repuesto in self.piezas:
            raise ValueError("Pieza ya incluida")
        self.piezas.append(pieza_repuesto)

    def quitar_piezas(self, pieza_repuesto):

        # elimina una pieza de la nave, donde indicamos el nombre de la pieza que queremos quitar,
        # da una excepción si la pieza no está en la nave 

        if pieza_repuesto not in self.piezas:
            raise ValueError("Pieza no disponible")
        self.piezas.remove(pieza_repuesto)

    def listar_piezas(self):

        # Muestra por pantalla todas las piezas de la nave

        print(f"La lista de piezas de la nave {self.nombre} es: {', '.join(self.piezas)}") 

    def tiene_pieza(self, pieza):

        # Comprueba si la nave tiene una pieza determinada y devuelve un  booleano
        # donde ees True si la pieza está en la nave y False si no.

        return pieza in self.piezas

    def numero_piezas(self):

        # Devuelve el número total de piezas que tiene la nave

        return len(self.piezas)

    def vaciar_piezas(self):

        # Elimina todas las piezas de la nave, dejando la lista vacía

        self.piezas.clear()

# CLASE DATOS CAPACIDAD
# Clase que representa la capacidad de una nave o estación espacial.
# Incluye la capacidad de tripulación y de pasajeros, y métodos para gestionar pasajeros.

# La clase DatosCapacidad se implementa para refactorizar el código, 
# ya que tanto EstacionEspacial como NaveEstelar comparten atributos y métodos relacionados con la capacidad de tripulación y pasajeros.
# Esta clase centraliza la gestión de la capacidad, evitando duplicar código en las subclases.
# Proporciona métodos para:
# - Obtener la capacidad total (tripulación + pasaje)
# - Añadir pasajeros de manera controlada
# - Quitar pasajeros de manera controlada, validando que no se exceda el límite

class DatosCapacidad:
    def __init__(self, tripulacion:int, pasaje:int):

        # la excepción es para comprobar que la tripulacion o pasajeros son negativos

        if tripulacion < 0 or pasaje < 0:
            raise ValueError("Capacidad inválida")
        
        self.tripulacion = tripulacion # es el número de plazas para la tripulación
        self.pasaje = pasaje # número de plazas para pasajeros

    def get_capacidad(self):

        # Calcula la capacidad total de la nave o estación.
        # donde devuelve la suma de tripulación y pasajeros

        return self.tripulacion + self.pasaje
    
    def añadir_pasajeros(self, cantidad):

        # se encarga de añadir pasajeros a la nave/estación.
        # donde cantidad es el número de pasajeros a añadir y comprueba que no sea negativo

        if cantidad <= 0:
            raise ValueError("Cantidad inválida")
        self.pasaje += cantidad

    def quitar_pasajeros(self, cantidad):

        # Quita pasajeros de la nave/estación
        # donde cantidad es el número de pasajeros a quitar (debe ser >0 y <= pasaje actual)

        if cantidad <= 0 or cantidad > self.pasaje:
            raise ValueError("Cantidad inválida")
        self.pasaje -= cantidad

# CLASE ESTACION ESPACIAL 
# Clase que representa una estación espacial del imperio.
# La cual Hereda de --> Nave: para poder gestionar piezas y atributos de combate y de 
# DatosCapacidad: para manejar la capacidad de tripulación y pasajeros, se trata de una herencia múltiple 
# que permite combinar funcionalidad de ambas clases, por lo tanrro utiliza herencia múltiple 
# con la gestión de la capacidad de tripulación y pasajeros.
# En el constructor se llaman explícitamente los constructores de ambos padres.
# De igual modo hacemos posteriormente con NaveEstelar

class EstacionEspacial(Nave, DatosCapacidad):

    def __init__(self, id_combate:str, clave:int, nombre:str, tripulacion:int, pasaje:int, ubicacion: Ubicacion, piezas:list[str]=None):
        
        # Llamamos a los dos padres
        Nave.__init__(self, id_combate, clave, nombre, piezas)
        DatosCapacidad.__init__(self, tripulacion, pasaje)

        self.ubicacion = ubicacion # ubicación de la nave 

    def __str__(self):
        return Nave.__str__(self) + f"\nTripulacion: {self.tripulacion} \nPasaje: {self.pasaje} \nUbicacion: {self.ubicacion}"

    def get_ubicacion(self):

        # Devuelve la ubicación de la estación como string (nombre del Enum)

        return self.ubicacion.name
    
    def set_ubicacion(self, ubicacion : Ubicacion):

        # Modifica la ubicación de la estación
        # donde aqui ubicación va a ser la nueva ubicación de la nave 

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

# La relación de composición entre la clase Almacen y la clase Repuesto se representa mediante un atributo en 
# la clase Almacen que almacena una lista de objetos de tipo Repuesto.
# Esta relación implica que los repuestos dependen completamente del almacén: no pueden existir de forma independiente. 
# Por ello, cuando se destruye un objeto de tipo Almacen, también se destruyen los objetos Repuesto que contiene.
# Decidimos que sea composición, ya que no tiene sentido que los repuestos existan de forma independiente.

# Aunque se modela como composición, en Python los objetos pueden seguir existiendo si existen referencias externas 
# a ellos (por ejemplo, variables fuera de la clase).
# Cuando un objeto se elimina de la colección (por ejemplo, al darlo de baja), solo se elimina la referencia que tenía 
# el contenedor, pero el objeto puede seguir existiendo si hay otras referencias apuntándolo.
# La destrucción real del objeto solo ocurre cuando no quedan referencias hacia él.
# En ese momento, el recolector de basura de Python se encarga de eliminarlo automáticamente, 
# sin necesidad de implementar manualmente un método como __del__.
# Por tanto, la composición en este caso se entiende a nivel conceptual (de diseño),
# y no como una restricción estricta impuesta por el lenguaje.
# De igual modo pasará posteriormente, con la implementación de la clase MiImperio.

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

    def disminuir_cantidad_repuesto(self, repuesto: Repuesto, cantidad: int):
        if not isinstance(repuesto, Repuesto):
            raise ValueError('El objeto proporcionado no es un repuesto válido. Debe ser una instancia de la clase Repuesto.')
        repuesto.disminuir_cantidad(cantidad)

    def get_catalogo(self):
        return self.catalogo

    def listar_repuestos(self):
        print(f"La lista de repuestos en el almacén {self.id_almacen} es: {', '.join(r.nombre for r in self.get_catalogo())}")

    def obtencion_repuestos(self):
        for r in self.get_catalogo():
            print(f"{r.nombre}: {r.get_cantidad()} unidades, Valor total: {r.valor_total_stock()}")

# Decidimos implementarla como abstracta, para forzar a que no se pueda instanciar. 
# Aunque no encontramos métodos comunes en todos los hijos y por ello no definimos métodos abstractos
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

    def adquirir_repuesto(self, repuesto: Repuesto, cantidad: int, imperio):
        for almacen in imperio.get_almacenes():
            if almacen.repuesto_en_almacen(repuesto):
                almacen.disminuir_cantidad_repuesto(repuesto, cantidad)
                return
        raise ValueError("No encontrado en ningún almacén")
    
class Operario(Usuario):
    def __init__(self, nombre, id_usuario):
        super().__init__(nombre, id_usuario)   

    def gestionar_stock(self, almacen:Almacen):
        for elem in almacen.get_catalogo().copy():  
            # Usamos copy() porque si recorremos directamente almacen.get_catalogo()
            # y eliminamos elementos durante la iteración, la lista puede cambiar
            # de tamaño y provocar errores o saltarse elementos.
            if not elem.consultar_disponibilidad():
                almacen.quitar_repuesto(elem)

    def gestionar_repuesto(self, almacen: Almacen, repuesto: Repuesto):
        if almacen.repuesto_en_almacen(repuesto):
            raise ValueError("El repuesto ya existe en el almacén")
        almacen.añadir_repuesto(repuesto)

# Se crea la clase MiImperio para representar el imperio y gestionar sus elementos.
# Se implementan métodos para añadir y eliminar elementos, ya que MiImperio mantiene una relación de 
# composición con sus componentes (usuarios, unidades de combate y almacenes).
# Esta composición se representa mediante atributos en la clase que almacenan listas de objetos de las clases 
# con las que se relaciona.
# La composición implica que los elementos dependen del imperio, por lo que no pueden existir de forma independiente.
# Por ello, cuando se destruye un objeto de tipo MiImperio, también se destruyen los usuarios, las unidades de combate 
# y los almacenes que contiene.

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

    def get_almacenes(self):
        return self.almacenes

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
            raise ValueError(f'La Unidad de Combate "{unidad_combate.id_combate}" no existe en el imperio.')
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
            operario.gestionar_repuesto(almacen, repuesto1)
            operario.gestionar_repuesto(almacen, repuesto2)
            operario.gestionar_repuesto(almacen, repuesto3)
        except ValueError as e:
            print("Error al añadir repuesto:", e)

        imperio.alta_almacen(almacen)
        print(f"Almacén {almacen.nombre} añadido al imperio\n")

        # Listar repuestos con stock y valor total
        print("Repuestos en el almacén (cantidad y valor total):")
        almacen.obtencion_repuestos()
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
        almacen.obtencion_repuestos()
        print()

        # Operario gestiona stock (elimina repuesto3 porque cantidad=0)
        operario.gestionar_stock(almacen)
        print("Stock después de gestión de operario:")
        almacen.obtencion_repuestos()
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
        print("Antes de bajas:")
        print("Usuarios:")
        imperio.listar_usuarios()
        print("Unidades de combate:")
        imperio.listar_unidades_combate()
        print("Almacenes:")
        imperio.listar_almacenes()
        print()
        
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
from entregable import *
import pytest

# vamos a crear fixture que es una función que crea un objeto, que vamos a estar 
# empleando en los tests, es para no tener que estar repitiendo el código en cada test

# no creamos objetos ni de UnidadCombate, ni de Nave ni de Usuario porque son clases abstractas que no se pueden instanciar

@pytest.fixture
def nave_estelar():
    # se crea una nave estelar con datos de prueba
    # Nave concreta para probar lógica de UnidadCombate y Nave
    return NaveEstelar("NE-01", 100, "Destructor Estelar", 50, 200, Clase.EJECUTOR)

@pytest.fixture
def caza_estelar():
    return CazaEstelar("C-01", 1, "Faucon", 5)

@pytest.fixture
def repuesto():
    return Repuesto("Motor X", "Kuat Drive Yards", 10, 5000)

@pytest.fixture
def repuesto2():
    return Repuesto("Motor J", "Kuat Drive JSON", 7, 100000000)

@pytest.fixture
def estacion_espacial():
    return EstacionEspacial("ES-01", 1, "Endor Base", 50, 100, Ubicacion.ENDOR)

@pytest.fixture
def almacen():
    return Almacen("Almacén Imperial", 1, "Coruscant")

@pytest.fixture
def operario():
    return Operario("TK-421", 102)

@pytest.fixture
def comandante():
    return Comandante("Thrawn", 101)

@pytest.fixture
def imperio():
    return MiImperio("Imperio Galáctico")


# TEST PARA EstacionEspacial

# creamos el test de estación espacial, el cual se encarga de comprobar que la estación se crea correctamente

def test_estacion_creacion(estacion_espacial):

    assert estacion_espacial.tripulacion == 50
    assert estacion_espacial.pasaje == 100
    assert estacion_espacial.get_ubicacion() == "ENDOR"

# con esto verificamos que se puede cambiar la ubicación sin problema 

def test_cambiar_ubicacion(estacion_espacial):

    estacion_espacial.set_ubicacion(Ubicacion.NEBULOSA_KALIIDA)

    assert estacion_espacial.get_ubicacion() == "NEBULOSA_KALIIDA"

# comprueba que la capacidad total sea tripulación + pasaje 

def test_capacidad_total(estacion_espacial):
    assert estacion_espacial.get_capacidad() == 150

# comprueba que se añaden pasajeros correctamente

def test_añadir_pasajeros(estacion_espacial):

    estacion_espacial.añadir_pasajeros(20)

    assert estacion_espacial.pasaje == 120  

# Comprueba que se eliminan pasajeros correctamente

def test_quitar_pasajeros(estacion_espacial):

    estacion_espacial.quitar_pasajeros(30)

    assert estacion_espacial.pasaje == 70

# CASOS LÍMITE
# Verifica que no se pueden añadir valores negativos

def test_añadir_pasajeros_negativo(estacion_espacial):
    with pytest.raises(ValueError):
        estacion_espacial.añadir_pasajeros(-10)

# No se pueden quitar más pasajeros de los existentes

def test_quitar_pasajeros_mas_que_disponibles(estacion_espacial):
    with pytest.raises(ValueError):
        estacion_espacial.quitar_pasajeros(200)  # más que el pasaje actual

# TEST PARA NaveEstelar
# donde hacemos un test completo de gestión de piezas (añadir, evitar duplicados, eliminar, errores)

def test_nave_estelar_piezas(nave_estelar):
    nave_estelar.añadir_piezas("Motor X")
    assert nave_estelar.numero_piezas() == 1

    with pytest.raises(ValueError): # indico que el codigo de dentro debe lanzas una excepción de tipo ValueError
        nave_estelar.añadir_piezas("Motor X")

    nave_estelar.quitar_piezas("Motor X")
    assert nave_estelar.numero_piezas() == 0
    with pytest.raises(ValueError):
        nave_estelar.quitar_piezas("Motor X")

# se encarga de comprobar el ciclo de estados, es decir operativa --> dañada --> reparada
def test_reparar(nave_estelar):

    assert nave_estelar.get_estado() == "OPERATIVA"
    nave_estelar.cambiar_estado()  # pasa a dañada
    assert nave_estelar.get_estado() == "DANADA"
    assert nave_estelar.necesita_reparacion()
    nave_estelar.reparar()
    assert nave_estelar.esta_operativa()

#Añadir pieza y comprobar existencia

def test_añadir_pieza(nave_estelar):
    nave_estelar.añadir_piezas("Motor X")
    assert nave_estelar.numero_piezas() == 1
    assert nave_estelar.tiene_pieza("Motor X")

def test_quitar_pieza(nave_estelar):
    nave_estelar.añadir_piezas("Motor X")
    nave_estelar.quitar_piezas("Motor X")

    assert nave_estelar.numero_piezas() == 0

# Vaciar lista de piezas

def test_vaciar_piezas(nave_estelar):

    nave_estelar.añadir_piezas("Motor X")
    nave_estelar.añadir_piezas("Escudo Y")

    nave_estelar.vaciar_piezas()

    assert nave_estelar.numero_piezas() == 0

# TEST PARA CazaEstelar 

def test_CazaEstelar_dotacion(caza_estelar):
    caza_estelar.aumentar_dotacion(9)
    assert caza_estelar.get_dotacion() == 14

    with pytest.raises(ValueError): # indico que el codigo de dentro debe lanzas una excepción de tipo ValueError
        caza_estelar.aumentar_dotacion(-3)

    caza_estelar.reducir_dotacion(9)
    assert caza_estelar.get_dotacion() == 5
    with pytest.raises(ValueError):
        caza_estelar.reducir_dotacion(-4)  

    with pytest.raises(ValueError):
        caza_estelar.reducir_dotacion(10)  # dotación inicial = 5

    with pytest.raises(ValueError):
        caza_estelar.aumentar_dotacion(-1)


# TEST PARA REPUESTO 

# va a verificar los valores iniciales
def test_repuesto_crear(repuesto):
    assert repuesto.get_cantidad() == 10
    assert repuesto.consultar_disponibilidad() == True
    assert repuesto.get_precio() == 5000

# Comprueba reducción correcta de stock
def test_disminuir_cantidad(repuesto):
    repuesto.disminuir_cantidad(3)
    assert repuesto.get_cantidad() == 7 # 10 - 3 = 7 

# comprueba los casos invalidos --> más cantidad de la disponible y valores negativos
def test_disminuir_cantidad_error(repuesto):
    with pytest.raises(ValueError): # si trato de disminuir la cantidad un número mayor a la cantidad actual, debe lanzar una excepción
        repuesto.disminuir_cantidad(20)

    with pytest.raises(ValueError): # si trato de disminuir la cantidad un número negativo, debe lanzar una excepción
        repuesto.disminuir_cantidad(-3)

# Aumentar stock
def test_aumentar_cantidad(repuesto):
    repuesto.aumentar_cantidad(5)
    assert repuesto.get_cantidad() == 15


# TEST PARA ALMACEN 

# comprueba los atributos iniciales
def test_almacen_creacion(almacen):

    assert almacen.nombre == "Almacén Imperial"
    assert almacen.localizacion == "Coruscant"
    assert almacen.catalogo == []

# Evita añadir duplicados
def test_repuesto_duplicado(operario, almacen, repuesto):
    operario.gestionar_repuesto(almacen, repuesto)

    with pytest.raises(ValueError):
        operario.gestionar_repuesto(almacen, repuesto)

def test_quitar_repuesto(almacen, repuesto):

    almacen.añadir_repuesto(repuesto)
    almacen.quitar_repuesto(repuesto)

    assert repuesto not in almacen.get_catalogo()

# Buscar repuesto por nombre
def test_buscar_repuesto(almacen, repuesto):

    almacen.añadir_repuesto(repuesto)

    resultado = almacen.buscar_repuesto("Motor X")

    assert resultado == repuesto

# este test se encarga de reducir el stock a 0, que el operario limpie el almacen y verifica la eliminacion 
def test_gestionar_stock_elimina_sin_stock(operario, almacen):
    r = Repuesto("Motor y", "Kuat Drive Polo", 10, 3500)
    operario.gestionar_repuesto(almacen, r)

    r.disminuir_cantidad(10) # quitamos la misma cantidad que tenemos para que no de una excepcion y podamos probar la funcion gestionar_stock

    operario.gestionar_stock(almacen)
    assert r.get_cantidad() == 0

    assert not almacen.repuesto_en_almacen(r) # compruebo que ya no esta en almacen, si no esta entonces pasa el test
    assert r not in almacen.get_catalogo()  # catalogo debe reflejarlo correctamente

# TEST DE OPERARIO

# Añadir repuesto correctamente
def test_operario_añadir_repuesto(operario, almacen, repuesto):
    operario.gestionar_repuesto(almacen, repuesto)
    assert almacen.repuesto_en_almacen(repuesto)

# No elimina repuestos con stock > 0
def test_gestionar_stock_no_elimina_con_stock(operario, almacen, repuesto):
    almacen.añadir_repuesto(repuesto)

    operario.gestionar_stock(almacen)    
    assert almacen.repuesto_en_almacen(repuesto)

# TEST DE COMANDANTE
def test_comandante_adquirir_repuesto(comandante, almacen, repuesto2, imperio):
    imperio.alta_almacen(almacen)
    almacen.añadir_repuesto(repuesto2)
    comandante.adquirir_repuesto(repuesto2, 2, imperio)

    assert repuesto2.get_cantidad() == 5

# TEST MIIMPERIO

# añadir un usuario
def test_alta_usuario(imperio, operario):
    imperio.alta_usuario(operario)

    assert operario in imperio.usuarios

# Añadir almacén
def test_alta_almacen(imperio, almacen):
    imperio.alta_almacen(almacen)

    assert almacen in imperio.almacenes

# Añadir unidad de combate
def test_alta_unidad_combate(imperio, nave_estelar):
    imperio.alta_unidad_combate(nave_estelar)
    assert nave_estelar in imperio.unidades_combate

# Test flujo completo, lo que hace es simular un caso real completo, es decir:
# - crea el sistema (imperio, usuarios, almacén)
# - añade repuestos
# - el operario gestiona el almaceén 
# - el comandante consume stock
# - se va a limpiar el stock vacío

def test_flujo_completo(imperio, almacen, operario, comandante):
    # 1. Alta de almacén y usuarios
    imperio.alta_almacen(almacen)
    imperio.alta_usuario(operario)
    imperio.alta_usuario(comandante)

    # 2. Crear repuestos
    r1 = Repuesto("Motor A", "Kuat", 10, 5000)
    r2 = Repuesto("Motor B", "Kuat", 5, 10000)

    # 3. Operario añade repuestos al almacén
    operario.gestionar_repuesto(almacen, r1)
    operario.gestionar_repuesto(almacen, r2)

    # Comprobamos que están en el almacén
    assert almacen.repuesto_en_almacen(r1)
    assert almacen.repuesto_en_almacen(r2)

    # 4. Comandante adquiere algunos repuestos
    comandante.adquirir_repuesto(r1, 3, imperio)
    assert r1.get_cantidad() == 7  # 10 - 3 = 7

    # 5. Disminuimos a 0 un repuesto y gestionamos stock
    r2.disminuir_cantidad(5)
    operario.gestionar_stock(almacen)

    # Comprobamos que se eliminó correctamente del almacén
    assert not almacen.repuesto_en_almacen(r2)
    assert r2 not in almacen.get_catalogo()
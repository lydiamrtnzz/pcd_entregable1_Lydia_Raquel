from entregable_bueno import *
import pytest

# vamos a crear fixture que es una función que crea un objeto, que vamos a estar 
# empleando en los tests, es para no tener que estar repitiendo el código en cada test

# no creamos objetos ni de UnidadCombate, ni de Nave ni de Usuario porque son clases abstractas que no se pueden instanciar
@pytest.fixture
def nave_estelar():
    # Nave concreta para probar lógica de UnidadCombate y Nave
    return NaveEstelar("NE-01", 100, "Destructor Estelar", 50, 200, Clase.EJECUTOR)

@pytest.fixture
def caza_estelar():
    return CazaEstelar("C-01", 1, "Faucon", 5)

@pytest.fixture
def repuesto():
    return Repuesto("Motor X", "Kuat Drive Yards", 10, 5000)

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

def test_estacion_creacion(estacion_espacial):

    assert estacion_espacial.tripulacion == 50
    assert estacion_espacial.pasaje == 100
    assert estacion_espacial.get_ubicacion() == Ubicacion.ENDOR

def test_cambiar_ubicacion(estacion_espacial):

    estacion_espacial.set_ubicacion(Ubicacion.NEBULOSA_KALIIDA)

    assert estacion_espacial.get_ubicacion() == Ubicacion.NEBULOSA_KALIIDA

def test_capacidad_total(estacion_espacial):
    assert estacion_espacial.get_capacidad() == 150

def test_añadir_pasajeros(estacion_espacial):

    estacion_espacial.añadir_pasajeros(20)

    assert estacion_espacial.pasaje == 120  

def test_quitar_pasajeros(estacion_espacial):

    estacion_espacial.quitar_pasajeros(30)

    assert estacion_espacial.pasaje == 70

# TEST PARA NaveEstelar 

def test_nave_estelar_piezas(nave_estelar):
    nave_estelar.añadir_piezas("Motor X")
    assert nave_estelar.numero_piezas() == 1

    with pytest.raises(ValueError): # indico que el codigo de dentro debe lanzas una excepción de tipo ValueError
        nave_estelar.añadir_piezas("Motor X")

    nave_estelar.quitar_piezas("Motor X")
    assert nave_estelar.numero_piezas() == 0
    with pytest.raises(ValueError):
        nave_estelar.quitar_piezas("Motor X")

def test_reparar(nave_estelar):

    assert nave_estelar.get_estado() == "operativa"
    nave_estelar.cambiar_estado()  # pasa a dañada
    assert nave_estelar.get_estado() == "dañada"
    assert nave_estelar.necesita_reparacion()
    nave_estelar.reparar()
    assert nave_estelar.esta_operativa()

def test_añadir_pieza(nave_estelar):
    nave_estelar.añadir_piezas("Motor X")
    assert nave_estelar.numero_piezas() == 1
    assert nave_estelar.tiene_pieza("Motor X")

def test_quitar_pieza(nave_estelar):
    nave_estelar.añadir_piezas("Motor X")
    nave_estelar.quitar_piezas("Motor X")

    assert nave_estelar.numero_piezas() == 0

def test_vaciar_piezas(nave_estelar):

    nave_estelar.añadir_piezas("Motor X")
    nave_estelar.añadir_piezas("Escudo Y")

    nave_estelar.vaciar_piezas()

    assert nave_estelar.numero_piezas() == 0

# TEST PARA CazaEstelar 

def CazaEstelar_dotacion(caza_estelar):
    caza_estelar.aumentar_dotacion(9)
    assert caza_estelar.get_dotacion() == 14

    with pytest.raises(ValueError): # indico que el codigo de dentro debe lanzas una excepción de tipo ValueError
        caza_estelar.aumentar_dotacion(-3)

    caza_estelar.reducir_dotacion(9)
    assert caza_estelar.get_dotacion() == 5
    with pytest.raises(ValueError):
        caza_estelar.reducir_dotacion(-4)  

'''def test_caza_operativo():
    caza = CazaEstelar("C-01", 1, "Faucon", 5)
    assert caza.es_operativo() == True
    caza.reducir_dotacion(5)
    assert caza.es_operativo() == False'''

# TEST PARA REPUESTO 

def test_repuesto_crear(repuesto):
    assert repuesto.get_cantidad() == 5
    assert repuesto.consultar_disponibilidad() == True
    assert repuesto.get_precio() == 1000

def test_disminuir_cantidad(repuesto):
    repuesto.disminuir_cantidad(3)
    assert repuesto.get_cantidad() == 2

def test_disminuir_cantidad_error(repuesto):
    with pytest.raises(ValueError):
        repuesto.disminuir_cantidad(5)

def test_aumentar_cantidad(repuesto):
    repuesto.aumentar_cantidad(5)
    assert repuesto._Repuesto__cantidad == 15


# TEST PARA ALMACEN 

def test_almacen_creacion(almacen):

    assert almacen.nombre == "Central"
    assert almacen.localizacion == "Endor"
    assert almacen.catalogo == []

def test_operario_añadir_repuesto(operario, almacen, repuesto):
    operario.añadir_repuesto(almacen, repuesto)
    assert almacen.repuesto_en_almacen(repuesto)

def test_repuesto_duplicado(operario, almacen, repuesto):
    operario.añadir_repuesto(almacen, repuesto)

    with pytest.raises(ValueError):
        operario.añadir_repuesto(almacen, repuesto)

def test_quitar_repuesto(almacen, repuesto):

    almacen.añadir_repuesto(repuesto)
    almacen.quitar_repuesto(repuesto)

    assert repuesto not in almacen.get_catalogo()

def test_buscar_repuesto(almacen, repuesto):

    almacen.añadir_repuesto(repuesto)

    resultado = almacen.buscar_repuesto("Motor X")

    assert resultado == repuesto

def test_gestionar_stock_elimina_sin_stock(operario, almacen, repuesto):
    operario.añadir_repuesto(almacen, repuesto)

    repuesto.disminuir_cantidad(1)

    operario.gestionar_stock(almacen)

    assert not almacen.repuesto_en_almacen(repuesto) # compruebo que ya no esta en almacen, si no esta entonces pasa el test


# TEST DE OPERARIO

def test_operario_añadir_repuesto(operario, almacen, repuesto):
    operario.añadir_repuesto(almacen, repuesto)
    assert almacen.repuesto_en_almacen(repuesto)

def test_gestionar_stock(operario, almacen, repuesto):
    almacen.añadir_repuesto(repuesto)

    operario.gestionar_stock(almacen)

    assert not almacen.repuesto_en_almacen(repuesto)

# TEST DE COMANDANTE
def test_comandante_adquirir_repuesto(comandante, operario, almacen, repuesto):
    operario.añadir_repuesto(almacen, repuesto)

    comandante.adquirir_repuesto(repuesto, 2, almacen)

    assert repuesto._Repuesto__cantidad == 8

# TEST MIIMPERIO
def test_alta_usuario(imperio, operario):
    imperio.alta_usuario(operario)

    assert operario.id_usuario in imperio.usuarios

def test_alta_almacen(imperio, almacen):
    imperio.alta_almacen(almacen)

    assert almacen.id_almacen in imperio.almacenes

def test_alta_unidad_combate(imperio):

    imperio.alta_unidad_combate(nave_estelar)

    assert nave_estelar.id_combate in imperio.unidades_combate
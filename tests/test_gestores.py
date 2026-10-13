from mensajeria.modelo import Usuario, Admin, Mensaje
from mensajeria.gestores import GestorDeUsuarios, GestorDeMensajes


# ============ GestorDeUsuarios: inicialización ============

def test_gestor_usuarios_arranca_con_admin_por_defecto():
    g = GestorDeUsuarios()
    admin = g.buscar_por_username("admin")
    assert admin is not None
    assert admin.es_usuario() is False


def test_gestor_usuarios_arranca_con_una_sola_cuenta():
    g = GestorDeUsuarios()
    assert len(g.listar()) == 1


def test_gestor_usuarios_admin_por_defecto_no_es_usuario():
    g = GestorDeUsuarios()
    usuarios = g.listar_usuarios()
    assert usuarios == []


# ============ GestorDeUsuarios: operaciones ============

def test_gestor_usuarios_agregar():
    g = GestorDeUsuarios()
    u = Usuario("ana", "1")
    g.agregar(u)
    assert g.buscar_por_username("ana") == u


def test_gestor_usuarios_buscar_por_username_ok():
    g = GestorDeUsuarios()
    u = Usuario("ana", "1")
    g.agregar(u)
    assert g.buscar_por_username("ana") == u


def test_gestor_usuarios_buscar_por_username_no_existe():
    g = GestorDeUsuarios()
    assert g.buscar_por_username("nadie") is None


def test_gestor_usuarios_eliminar():
    g = GestorDeUsuarios()
    u = Usuario("ana", "1")
    g.agregar(u)
    g.eliminar(u)
    assert g.buscar_por_username("ana") is None


def test_gestor_usuarios_listar_devuelve_copia():
    g = GestorDeUsuarios()
    u = Usuario("ana", "1")
    g.agregar(u)
    lista = g.listar()
    lista.append(Usuario("intruso", "x"))
    # Modificar la lista devuelta no afecta al gestor
    assert g.buscar_por_username("intruso") is None


def test_gestor_usuarios_listar_usuarios_solo_devuelve_usuarios():
    g = GestorDeUsuarios()
    u = Usuario("ana", "1")
    g.agregar(u)
    usuarios = g.listar_usuarios()
    assert u in usuarios
    assert all(c.es_usuario() for c in usuarios)


def test_gestor_usuarios_listar_usuarios_no_incluye_admin_por_defecto():
    g = GestorDeUsuarios()
    usuarios = g.listar_usuarios()
    assert g.buscar_por_username("admin") not in usuarios


def test_gestor_usuarios_agregar_varios_usuarios():
    g = GestorDeUsuarios()
    ana = Usuario("ana", "1")
    beto = Usuario("beto", "2")
    g.agregar(ana)
    g.agregar(beto)
    usuarios = g.listar_usuarios()
    assert ana in usuarios
    assert beto in usuarios
    assert len(usuarios) == 2


# ============ GestorDeMensajes ============

def test_gestor_mensajes_arranca_vacio():
    g = GestorDeMensajes()
    ana = Usuario("ana", "1")
    assert g.mensajes_para(ana) == []
    assert g.mensajes_de(ana) == []


def test_gestor_mensajes_agregar():
    g = GestorDeMensajes()
    ana = Usuario("ana", "1")
    beto = Usuario("beto", "2")
    m = Mensaje(ana, beto, "Hola", "Cuerpo")
    g.agregar_mensaje(m)
    assert m in g.mensajes_para(beto)


def test_gestor_mensajes_mensajes_para_filtra_por_receptor():
    g = GestorDeMensajes()
    ana = Usuario("ana", "1")
    beto = Usuario("beto", "2")
    carla = Usuario("carla", "3")
    m1 = Mensaje(ana, beto, "Hola Beto", "Cuerpo")
    m2 = Mensaje(ana, carla, "Hola Carla", "Cuerpo")
    g.agregar_mensaje(m1)
    g.agregar_mensaje(m2)

    assert g.mensajes_para(beto) == [m1]
    assert g.mensajes_para(carla) == [m2]
    assert g.mensajes_para(ana) == []


def test_gestor_mensajes_mensajes_de_filtra_por_emisor():
    g = GestorDeMensajes()
    ana = Usuario("ana", "1")
    beto = Usuario("beto", "2")
    m1 = Mensaje(ana, beto, "Hola", "Cuerpo")
    m2 = Mensaje(beto, ana, "Respuesta", "Cuerpo")
    g.agregar_mensaje(m1)
    g.agregar_mensaje(m2)

    assert g.mensajes_de(ana) == [m1]
    assert g.mensajes_de(beto) == [m2]


def test_gestor_mensajes_varios_mensajes_mismo_par():
    g = GestorDeMensajes()
    ana = Usuario("ana", "1")
    beto = Usuario("beto", "2")
    m1 = Mensaje(ana, beto, "Primero", "Cuerpo")
    m2 = Mensaje(ana, beto, "Segundo", "Cuerpo")
    g.agregar_mensaje(m1)
    g.agregar_mensaje(m2)

    recibidos = g.mensajes_para(beto)
    assert len(recibidos) == 2
    assert m1 in recibidos
    assert m2 in recibidos
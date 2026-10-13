from datetime import date
from mensajeria.modelo import Usuario, Admin, Mensaje


def test_cuenta_comprobar_usuario_ok():
    u = Usuario("ana", "1234")
    assert u.comprobar_usuario("ana", "1234") is True


def test_cuenta_comprobar_usuario_falla_por_username():
    u = Usuario("ana", "1234")
    assert u.comprobar_usuario("otro", "1234") is False


def test_cuenta_comprobar_usuario_falla_por_contrasenia():
    u = Usuario("ana", "1234")
    assert u.comprobar_usuario("ana", "otra") is False


def test_usuario_es_usuario():
    assert Usuario("ana", "1234").es_usuario() is True


def test_admin_no_es_usuario():
    assert Admin("admin", "admin").es_usuario() is False


def test_cuentas_con_mismo_username_son_iguales():
    assert Usuario("ana", "1234") == Usuario("ana", "otra")


def test_cuentas_con_distinto_username_no_son_iguales():
    assert Usuario("ana", "1234") != Usuario("beto", "1234")


def test_mensaje_arranca_no_leido():
    emisor = Usuario("ana", "1")
    receptor = Usuario("beto", "2")
    m = Mensaje(emisor, receptor, "Hola", "Cuerpo")
    assert m.esta_leido() is False


def test_mensaje_leer_cambia_estado():
    emisor = Usuario("ana", "1")
    receptor = Usuario("beto", "2")
    m = Mensaje(emisor, receptor, "Hola", "Cuerpo")
    m.leer()
    assert m.esta_leido() is True


def test_mensaje_es_para_ok():
    ana = Usuario("ana", "1")
    beto = Usuario("beto", "2")
    m = Mensaje(ana, beto, "Hola", "Cuerpo")
    assert m.es_para(beto) is True


def test_mensaje_es_para_falla():
    ana = Usuario("ana", "1")
    beto = Usuario("beto", "2")
    m = Mensaje(ana, beto, "Hola", "Cuerpo")
    assert m.es_para(ana) is False


def test_mensaje_es_de_ok():
    ana = Usuario("ana", "1")
    beto = Usuario("beto", "2")
    m = Mensaje(ana, beto, "Hola", "Cuerpo")
    assert m.es_de(ana) is True


def test_mensaje_es_de_falla():
    ana = Usuario("ana", "1")
    beto = Usuario("beto", "2")
    m = Mensaje(ana, beto, "Hola", "Cuerpo")
    assert m.es_de(beto) is False


def test_mensaje_fecha_envio_es_hoy():
    ana = Usuario("ana", "1")
    beto = Usuario("beto", "2")
    m = Mensaje(ana, beto, "Hola", "Cuerpo")
    assert str(date.today()) in m.leer()
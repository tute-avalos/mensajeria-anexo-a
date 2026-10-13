from unittest.mock import patch
from mensajeria.sistema import Sistema
from mensajeria.modelo import Usuario, Admin


# ============ Inicialización ============

def test_sistema_se_construye_sin_error():
    s = Sistema()
    assert s is not None


def test_sistema_tiene_gestor_de_usuarios_con_admin():
    s = Sistema()
    # El admin por defecto lo crea el gestor, no el sistema
    admin = s._Sistema__gestor_usuarios.buscar_por_username("admin")
    assert admin is not None
    assert admin.es_usuario() is False


def test_sistema_tiene_gestor_de_mensajes_vacio():
    s = Sistema()
    ana = Usuario("ana", "1")
    assert s._Sistema__gestor_mensajes.mensajes_para(ana) == []


# ============ Inicio de sesión ============

def test_sistema_iniciar_sesion_ok_con_admin():
    s = Sistema()
    with patch("builtins.input", side_effect=["admin", "admin"]):
        cuenta = s._Sistema__iniciar_sesion()
    assert cuenta is not None
    assert str(cuenta) == "admin"


def test_sistema_iniciar_sesion_falla_por_username():
    s = Sistema()
    with patch("builtins.input",
               side_effect=["nadie", "cualquiera"]):
        cuenta = s._Sistema__iniciar_sesion()
    assert cuenta is None


def test_sistema_iniciar_sesion_falla_por_contrasenia():
    s = Sistema()
    with patch("builtins.input",
               side_effect=["admin", "clave-incorrecta"]):
        cuenta = s._Sistema__iniciar_sesion()
    assert cuenta is None


def test_sistema_iniciar_sesion_con_usuario_creado():
    s = Sistema()
    s._Sistema__gestor_usuarios.agregar(Usuario("ana", "1234"))
    with patch("builtins.input", side_effect=["ana", "1234"]):
        cuenta = s._Sistema__iniciar_sesion()
    assert cuenta is not None
    assert str(cuenta) == "ana"


# ============ Operaciones del menú ============

def test_sistema_crear_cuenta_de_usuario():
    s = Sistema()
    with patch("builtins.input",
               side_effect=["ana", "1234"]):
        with patch("mensajeria.ui.EntradaSalida.pedir_entero_entre",
                   return_value=1):
            resultado = s._Sistema__crear_cuenta(None)
    assert resultado is False
    cuenta = s._Sistema__gestor_usuarios.buscar_por_username("ana")
    assert cuenta is not None
    assert cuenta.es_usuario() is True


def test_sistema_crear_cuenta_de_admin():
    s = Sistema()
    with patch("builtins.input",
               side_effect=["root", "root"]):
        with patch("mensajeria.ui.EntradaSalida.pedir_entero_entre",
                   return_value=2):
            s._Sistema__crear_cuenta(None)
    cuenta = s._Sistema__gestor_usuarios.buscar_por_username("root")
    assert cuenta is not None
    assert cuenta.es_usuario() is False


def test_sistema_cerrar_sesion_devuelve_true():
    s = Sistema()
    assert s._Sistema__cerrar_sesion(None) is True


# ============ Envío de mensajes ============

def test_sistema_nuevo_mensaje_guarda_mensaje():
    s = Sistema()
    ana = Usuario("ana", "1")
    beto = Usuario("beto", "2")
    s._Sistema__gestor_usuarios.agregar(ana)
    s._Sistema__gestor_usuarios.agregar(beto)

    # menu devuelve 2 (beto es el segundo usuario de la lista)
    with patch("mensajeria.ui.EntradaSalida.menu", return_value=2):
        with patch("builtins.input",
                   side_effect=["Asunto", "Cuerpo"]):
            resultado = s._Sistema__nuevo_mensaje(ana)

    assert resultado is False
    mensajes = s._Sistema__gestor_mensajes.mensajes_para(beto)
    assert len(mensajes) == 1
    assert mensajes[0].es_de(ana)


def test_sistema_nuevo_mensaje_sin_usuarios_no_hace_nada():
    s = Sistema()
    # Creamos un usuario emisor pero NO lo agregamos al gestor.
    # El gestor solo tiene al admin, que no es Usuario, así que
    # listar_usuarios() devuelve [].
    emisor = Usuario("ana", "1")

    with patch("mensajeria.ui.EntradaSalida.menu") as mock_menu:
        resultado = s._Sistema__nuevo_mensaje(emisor)
        mock_menu.assert_not_called()
    assert resultado is False


# ============ Lectura de mensajes ============

def test_sistema_leer_mensaje_marca_como_leido():
    from mensajeria.modelo import Mensaje
    s = Sistema()
    ana = Usuario("ana", "1")
    beto = Usuario("beto", "2")
    s._Sistema__gestor_usuarios.agregar(ana)
    s._Sistema__gestor_usuarios.agregar(beto)

    m = Mensaje(ana, beto, "Hola", "Cuerpo")
    s._Sistema__gestor_mensajes.agregar_mensaje(m)

    with patch("mensajeria.ui.EntradaSalida.menu", return_value=1):
        s._Sistema__leer_mensaje(beto)

    assert m.esta_leido() is True


def test_sistema_leer_mensaje_sin_mensajes_no_falla():
    s = Sistema()
    beto = Usuario("beto", "2")
    s._Sistema__gestor_usuarios.agregar(beto)

    with patch("mensajeria.ui.EntradaSalida.menu") as mock_menu:
        resultado = s._Sistema__leer_mensaje(beto)
        mock_menu.assert_not_called()
    assert resultado is False


# ============ Ver enviados ============

def test_sistema_ver_enviados_sin_mensajes_no_falla():
    s = Sistema()
    ana = Usuario("ana", "1")
    s._Sistema__gestor_usuarios.agregar(ana)

    with patch("mensajeria.ui.EntradaSalida.listar") as mock_listar:
        resultado = s._Sistema__ver_enviados(ana)
        mock_listar.assert_not_called()
    assert resultado is False


def test_sistema_ver_enviados_con_mensajes_lista():
    from mensajeria.modelo import Mensaje
    s = Sistema()
    ana = Usuario("ana", "1")
    beto = Usuario("beto", "2")
    s._Sistema__gestor_usuarios.agregar(ana)
    s._Sistema__gestor_usuarios.agregar(beto)

    m = Mensaje(ana, beto, "Hola", "Cuerpo")
    s._Sistema__gestor_mensajes.agregar_mensaje(m)

    with patch("mensajeria.ui.EntradaSalida.listar") as mock_listar:
        s._Sistema__ver_enviados(ana)
        mock_listar.assert_called_once()
from typing import Any, Optional
from mensajeria.modelo import Cuenta, Usuario, Admin, Mensaje
from mensajeria.gestores import GestorDeUsuarios, GestorDeMensajes
from mensajeria import constantes as const
from mensajeria.ui import EntradaSalida as io


class Sistema:
    def __init__(self) -> None:
        self.__gestor_usuarios = GestorDeUsuarios()
        self.__gestor_mensajes = GestorDeMensajes()

        self.__acciones: dict[str, Any] = {
            const.CREAR_CUENTA: self.__crear_cuenta,
            const.BORRAR_CUENTA: self.__borrar_cuenta,
            const.NUEVO_MENSAJE: self.__nuevo_mensaje,
            const.LEER_MENSAJE: self.__leer_mensaje,
            const.VER_ENVIADOS: self.__ver_enviados,
            const.SALIR: self.__cerrar_sesion,
        }

    # ====== Bucle principal ======

    def ejecutar(self) -> None:
        cuenta_activa: Optional[Cuenta] = None
        while True:
            if cuenta_activa is None:
                cuenta_activa = self.__iniciar_sesion()
                if cuenta_activa is None:
                    print("Datos incorrectos. Vuelva a intentar.")
            else:
                if self.__menu(cuenta_activa):
                    print(f"Adios, {cuenta_activa}.")
                    cuenta_activa = None

    def __iniciar_sesion(self) -> Optional[Cuenta]:
        username = input("Cuenta: ")
        contrasenia = input("Contraseña: ")
        for c in self.__gestor_usuarios.listar():
            if c.comprobar_usuario(username, contrasenia):
                print("Ingreso exitoso.")
                return c
        return None

    def __menu(self, ca: Cuenta) -> bool:
        opciones = ca.obtener_opciones()
        op = io.menu(opciones, 'Menú principal') - 1
        return self.__acciones[opciones[op]](ca)

    # ====== Operaciones de administración ======

    def __crear_cuenta(self, ua: Cuenta) -> bool:
        username = input("Ingrese nombre: ")
        contrasenia = input("Ingrese contraseña: ")
        print('Ingrese rol:')
        rol = io.menu(['Usuario', 'Admin'])
        if rol == 1:
            self.__gestor_usuarios.agregar(Usuario(username, contrasenia))
        else:
            self.__gestor_usuarios.agregar(Admin(username, contrasenia))
        print(f"Cuenta {username} creada.")
        return False

    def __borrar_cuenta(self, ua: Cuenta) -> bool:
        cuentas = self.__gestor_usuarios.listar()
        nombres = [str(c) for c in cuentas]
        nombres.append("Cancelar")
        op = io.menu(nombres, "Seleccione cuenta a borrar") - 1
        if 0 <= op < len(cuentas):
            c = cuentas[op]
            if c == ua:
                print("No puede borrarse a sí mismo.")
            else:
                self.__gestor_usuarios.eliminar(c)
                print(f"Cuenta {c} eliminada.")
        return False

    # ====== Operaciones de mensajería ======

    def __nuevo_mensaje(self, ua: Cuenta) -> bool:
        assert isinstance(ua, Usuario) # mypy hack
        usuarios = self.__gestor_usuarios.listar_usuarios()
        if not usuarios:
            print("No hay usuarios registrados.")
            return False
        nombres = [str(u) for u in usuarios]
        nombres.append("Cancelar")
        op = io.menu(nombres, "Seleccione usuario destinatario") - 1
        if 0 <= op < len(usuarios):
            receptor = usuarios[op]
            asunto = input("Ingrese asunto: ")
            cuerpo = input("Ingrese mensaje: ")
            m = Mensaje(ua, receptor, asunto, cuerpo)
            self.__gestor_mensajes.agregar_mensaje(m)
            print("Mensaje enviado.")
        return False

    def __leer_mensaje(self, ua: Cuenta) -> bool:
        assert isinstance(ua, Usuario) # mypy hack
        mensajes = self.__gestor_mensajes.mensajes_para(ua)
        if not mensajes:
            print("No tiene mensajes recibidos.")
            return False
        opciones = [str(m) for m in mensajes]
        opciones.append("Cancelar")
        op = io.menu(opciones, "Seleccione mensaje a leer") - 1
        if 0 <= op < len(mensajes):
            print(mensajes[op].leer())
        return False

    def __ver_enviados(self, ua: Cuenta) -> bool:
        assert isinstance(ua, Usuario) # mypy hack
        mensajes = self.__gestor_mensajes.mensajes_de(ua)
        if not mensajes:
            print("No ha enviado mensajes.")
            return False
        io.listar([str(m) for m in mensajes], "Mensajes enviados")
        return False

    # ====== Cierre de sesión ======

    def __cerrar_sesion(self, ua: Cuenta) -> bool:
        return True
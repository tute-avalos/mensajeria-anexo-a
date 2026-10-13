from typing import Optional, cast
from mensajeria.modelo import Cuenta, Usuario, Admin, Mensaje


class GestorDeUsuarios:
    def __init__(self) -> None:
        self.__cuentas: list[Cuenta] = [Admin('admin', 'admin')]

    def agregar(self, cuenta: Cuenta) -> None:
        self.__cuentas.append(cuenta)

    def eliminar(self, cuenta: Cuenta) -> None:
        self.__cuentas.remove(cuenta)

    def buscar_por_username(self, username: str) -> Optional[Cuenta]:
        for c in self.__cuentas:
            if str(c) == username:
                return c
        return None

    def listar(self) -> list[Cuenta]:
        return list(self.__cuentas)

    def listar_usuarios(self) -> list[Usuario]:
        return [cast(Usuario, c) for c in self.__cuentas if c.es_usuario()]


class GestorDeMensajes:
    def __init__(self) -> None:
        self.__mensajes: list[Mensaje] = []

    def agregar_mensaje(self, m: Mensaje) -> None:
        self.__mensajes.append(m)

    def mensajes_para(self, u: Usuario) -> list[Mensaje]:
        return [m for m in self.__mensajes if m.es_para(u)]

    def mensajes_de(self, u: Usuario) -> list[Mensaje]:
        return [m for m in self.__mensajes if m.es_de(u)]
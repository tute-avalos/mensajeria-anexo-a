from abc import ABC, abstractmethod
from datetime import date


class Cuenta(ABC):
    def __init__(self, username: str, contrasenia: str) -> None:
        self.__username = username
        self.__contrasenia = contrasenia

    def comprobar_usuario(self, username: str, contrasenia: str) -> bool:
        return (username == self.__username
                and contrasenia == self.__contrasenia)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cuenta):
            return self.__username == other.__username
        return False

    def __hash__(self) -> int:
        return hash(self.__username)

    def __str__(self) -> str:
        return self.__username

    @abstractmethod
    def obtener_opciones(self) -> list[str]:
        ...

    @abstractmethod
    def es_usuario(self) -> bool:
        ...


class Admin(Cuenta):
    def obtener_opciones(self) -> list[str]:
        from mensajeria import constantes as const
        return [const.CREAR_CUENTA, const.BORRAR_CUENTA, const.SALIR]

    def es_usuario(self) -> bool:
        return False


class Usuario(Cuenta):
    def obtener_opciones(self) -> list[str]:
        from mensajeria import constantes as const
        return [
            const.NUEVO_MENSAJE,
            const.LEER_MENSAJE,
            const.VER_ENVIADOS,
            const.SALIR,
        ]

    def es_usuario(self) -> bool:
        return True


class Mensaje:
    def __init__(self, emisor: Usuario, receptor: Usuario,
                 asunto: str, cuerpo: str) -> None:
        self.__emisor = emisor
        self.__receptor = receptor
        self.__asunto = asunto
        self.__cuerpo = cuerpo
        self.__leido: bool = False
        self.__fecha_envio: date = date.today()

    def leer(self) -> str:
        self.__leido = True
        return (
            "------------------------\n"
            f"De: {self.__emisor}\n"
            f"Para: {self.__receptor}\n"
            f"Fecha: {self.__fecha_envio}\n"
            f"Asunto: {self.__asunto}\n\n"
            "---\n"
            f"{self.__cuerpo}\n"
            "------------------------\n"
        )

    def es_para(self, u: Usuario) -> bool:
        return self.__receptor == u

    def es_de(self, u: Usuario) -> bool:
        return self.__emisor == u

    def esta_leido(self) -> bool:
        return self.__leido

    def __str__(self) -> str:
        marca = "X" if self.__leido else " "
        return (
            f"[{marca}] De: {self.__emisor} | "
            f"Para: {self.__receptor} | "
            f"Fecha: {self.__fecha_envio} | "
            f"Asunto: {self.__asunto}"
        )
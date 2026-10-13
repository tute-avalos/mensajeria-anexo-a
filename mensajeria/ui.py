
from typing import Optional

class EntradaSalida:
    @staticmethod
    def pedir_entero(msj: str) -> int:
        while True:
            try:
                return int(input(msj))
            except ValueError:
                print("Debe ingresar un número entero.")

    @staticmethod
    def pedir_entero_entre(msj: str, vmin: int, vmax: int) -> int:
        if vmin > vmax: vmin, vmax = vmax, vmin
        n = EntradaSalida.pedir_entero(msj)
        while n < vmin or n > vmax:
            n = EntradaSalida.pedir_entero(msj)
        return n

    @staticmethod
    def listar(items: list[str], titulo: Optional[str] = None) -> None:
        if titulo:
            print(f"******** {titulo} ********")
        for i,o in enumerate(items, 1):
            print(f"{i}. {o}")

    @staticmethod
    def menu(opciones: list[str], nombre_menu: Optional[str] = None) -> int:
        EntradaSalida.listar(opciones, nombre_menu)
        return EntradaSalida.pedir_entero_entre("Ingrese una opción: ",1 , len(opciones))

if __name__ == "__main__":
    pass
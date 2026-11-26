import sqlite3
from typing import List, Optional
from db import get_connection


def alta(nombre: str, precio: float, stock: int = 0) -> Optional[int]:
    nombre_limpio = nombre.strip()
    if not nombre_limpio:
        raise ValueError("El nombre no puede estar vacío.")
    try:
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                (nombre_limpio, precio, stock),
            )
            return cur.lastrowid
    except sqlite3.IntegrityError:
        return None


def listar(solo_activos: bool = True) -> List[sqlite3.Row]:
    sql = "SELECT id, nombre, precio, stock, activo FROM productos"
    if solo_activos:
        sql += " WHERE activo = 1"
    sql += " ORDER BY nombre"
    with get_connection() as conn:
        return conn.execute(sql).fetchall()


def modificar(prod_id: int, nombre: str, precio: float, stock: int) -> bool:
    nombre_limpio = nombre.strip()
    if not nombre_limpio:
        raise ValueError("El nombre no puede estar vacío.")
    with get_connection() as conn:
        cur = conn.execute(
            "UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?",
            (nombre_limpio, precio, stock, prod_id),
        )
        return cur.rowcount > 0


def baja_logica(prod_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute(
            "UPDATE productos SET activo = 0 WHERE id = ?",
            (prod_id,),
        )
        return cur.rowcount > 0


if __name__ == "__main__":
    nuevo_id = alta("Coca Cola 500ml", 1800.0, 30)
    if nuevo_id is None:
        print("El producto ya existe, no se duplicó.")
    for fila in listar():
        print(dict(fila))
from pathlib import Path
import sqlite3
from typing import List, Optional

DB_PATH = Path(__file__).resolve().parent / "sistema.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL,
            nombre TEXT NOT NULL UNIQUE,
            precio REAL NOT NULL CHECK (precio >= 0),
            stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
            activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1))
        )
        """
    )
    conn.commit()
    return conn


def insertar_registro(codigo: str, nombre: str, precio: float, stock: int) -> Optional[int]:
    conexion = get_connection()
    try:
        cursor = conexion.cursor()
        query = "INSERT INTO productos (codigo, nombre, precio, stock) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (codigo, nombre, precio, stock))
        conexion.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conexion.close()


def obtener_registros() -> List[sqlite3.Row]:
    conexion = get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id, codigo, nombre, precio, stock FROM productos WHERE activo = 1 ORDER BY id DESC"
        )
        return cursor.fetchall()
    finally:
        conexion.close()


def buscar_registros(texto_busqueda: str) -> List[sqlite3.Row]:
    conexion = get_connection()
    try:
        cursor = conexion.cursor()
        query = """
            SELECT id, codigo, nombre, precio, stock
            FROM productos
            WHERE activo = 1 AND (nombre LIKE ? OR codigo LIKE ?)
            ORDER BY id DESC
        """
        patron = f"%{texto_busqueda.strip()}%"
        cursor.execute(query, (patron, patron))
        return cursor.fetchall()
    finally:
        conexion.close()
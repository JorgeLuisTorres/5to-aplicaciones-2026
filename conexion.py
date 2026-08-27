import sqlite3

# Nombre de la base de datos
DB_NAME = "farmacia.db"


def conectar():
    """Crea y devuelve una conexión a la base de datos"""
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    return conexion


def crear_tabla():
    """Crea la tabla de remedios si no existe"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS remedios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            laboratorio TEXT,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            vencimiento TEXT
        )
    """)
    conexion.commit()
    conexion.close()


# ---------- ALTA ----------
def alta_remedio(nombre, laboratorio, precio, stock, vencimiento):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO remedios (nombre, laboratorio, precio, stock, vencimiento)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, laboratorio, precio, stock, vencimiento))
    conexion.commit()
    conexion.close()
    print("Remedio agregado correctamente.")


# ---------- BAJA ----------
def baja_remedio(id_remedio):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM remedios WHERE id = ?", (id_remedio,))
    conexion.commit()
    conexion.close()
    print("Remedio eliminado correctamente.")


# ---------- MODIFICACIÓN ----------
def modificar_remedio(id_remedio, nombre, laboratorio, precio, stock, vencimiento):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE remedios
        SET nombre = ?, laboratorio = ?, precio = ?, stock = ?, vencimiento = ?
        WHERE id = ?
    """, (nombre, laboratorio, precio, stock, vencimiento, id_remedio))
    conexion.commit()
    conexion.close()
    print("Remedio modificado correctamente.")


# ---------- CONSULTAS ----------
def listar_remedios():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM remedios")
    remedios = cursor.fetchall()
    conexion.close()
    return remedios


def buscar_remedio(id_remedio):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM remedios WHERE id = ?", (id_remedio,))
    remedio = cursor.fetchone()
    conexion.close()
    return remedio


# ---------- EJEMPLO DE USO ----------
if __name__ == "__main__":
    crear_tabla()

    # Ejemplos de alta (podés comentar estas líneas luego de probarlas)
    # alta_remedio("Ibuprofeno 400mg", "Bayer", 1250.50, 100, "2027-05-10")
    # alta_remedio("Paracetamol 500mg", "Genérico", 890.00, 50, "2026-12-01")

    print("Remedios cargados:")
    for r in listar_remedios():
        print(dict(r)) 
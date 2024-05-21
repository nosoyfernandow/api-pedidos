import psycopg2

# Conectar a la base de datos postgres por defecto para comprobar si la base de datos 'orden' existe
default_conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="bdproyecto",  # Tu contraseña de postgres
    host="database-2.c7w6ds5r8lrc.us-east-1.rds.amazonaws.com"
)
default_conn.autocommit = True  # Necesario para crear una base de datos fuera de una transacción
default_cursor = default_conn.cursor()

# Comprobar si la base de datos 'orden' existe
default_cursor.execute("SELECT 1 FROM pg_database WHERE datname='orden'")
db_exists = default_cursor.fetchone()

# Crear la base de datos 'orden' si no existe
if not db_exists:
    default_cursor.execute("CREATE DATABASE orden")

# Cerrar la conexión inicial
default_cursor.close()
default_conn.close()

# Conectar a la base de datos 'orden'
conn = psycopg2.connect(
    dbname="orden",
    user="postgres",
    password="bdproyecto",  # Tu contraseña de postgres
    host="database-2.c7w6ds5r8lrc.us-east-1.rds.amazonaws.com"
)

cursor = conn.cursor()

# Comprobar si la tabla 'orders' existe
cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'orders')")
table_exists = cursor.fetchone()[0]

# Crear la tabla 'orders' si no existe
if not table_exists:
    sql_query = """
        CREATE TABLE orders (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            order_date DATE NOT NULL
        )
    """
    cursor.execute(sql_query)
    conn.commit()

def commit():
    conn.commit()

# Ahora sigue con la definición de la API y las operaciones CRUD para los pedidos
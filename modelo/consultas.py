import pymysql

def mostrar_tablas(query):
    # Configuración de conexión
    conn = pymysql.connect(
        host="tu-endpoint-rds",
        user="tu_usuario",
        password="tu_password",
        database="tu_basedatos",
        port=3306
    )

    try:
        cursor = conn.cursor()
        
        # Consulta para listar tablas
        cursor.execute(query)
        
        tablas = cursor.fetchall()
        
        return tablas
    finally:
        cursor.close()
        conn.close()
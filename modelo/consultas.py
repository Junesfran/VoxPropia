import pymysql

def mostrar_tablas(query):
    # Configuración de conexión
    conn = pymysql.connect(
        host="voxpropia-db.cxgeswuswcvs.us-east-1.rds.amazonaws.com",
        user="admin",
        password="12345678",
        database="voxpropia_db",
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


def insertar_datos(params):
    # Configuración de conexión
    conn = pymysql.connect(
        host="voxpropia-db.cxgeswuswcvs.us-east-1.rds.amazonaws.com",
        user="admin",
        password="12345678",
        database="voxpropia_db",
        port=3306
    )

    try:
        cursor = conn.cursor()

        # Consulta para listar tablas
        query="INSERT INTO chat_history (query_text, chat_id) VALUES (%s, %s)"
        cursor.execute(query, params)


        conn.commit()

        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

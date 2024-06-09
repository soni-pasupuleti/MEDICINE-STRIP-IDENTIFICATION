import mysql.connector


def connect_to_database():
    return mysql.connector.connect(
       host="localhost",
        user="root",
        password="Buha@2097",
        database="medovision"
    )


def execute_query(query, values=None, fetchall=False):
    connection = connect_to_database()
    cursor = connection.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    if fetchall:
        result = cursor.fetchall()
    else:
        result = cursor.fetchone()
    connection.commit()
    connection.close()
    return result

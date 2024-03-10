#Importamos las clases necesarias para el proyecto
from flask import Flask, request, jsonify

import pymysql.cursors
import pymysql

def connection_mysql():
            connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='actividad3',
                            cursorclass=pymysql.cursors.DictCursor)
            return connection
     


app= Flask(__name__)

# Ruta para crear un usuario
@app.route('/usuarios', methods=['POST'])
def create():

    data = request.get_json()
    connection = connection_mysql()

    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO usuarios (correo, contraseña) VALUES (%s, %s)"
            cursor.execute(sql, (data['correo'], data['contraseña']))
        connection.commit()

    return jsonify({
        'message': 'Se ha creado el usuario con éxito.'
    }), 201


# Ruta para llamar los datos de todos los usuarios
@app.route('/usuarios', methods=['GET'])
def list():
    connection = connection_mysql()

    with connection.cursor() as cursor:
        sql = "SELECT id, correo, contraseña FROM usuarios"
        cursor.execute(sql)
        result = cursor.fetchall()

    return jsonify({
        'data': result
    }), 200

# Ruta para actualizar un usuario por su ID
@app.route('/usuarios/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    connection = connection_mysql()

    with connection.cursor() as cursor:
        sql = "UPDATE usuarios SET correo = %s, contraseña = %s WHERE id = %s"
        cursor.execute(sql, (data['correo'], data['contraseña'], id))

    connection.commit()

    return jsonify({
        'message': 'Usuario actualizado con éxito.'
    }), 200

# Ruta para eliminar un usuario por su ID
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete(id):
    connection = connection_mysql()

    with connection.cursor() as cursor:
        sql = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id,))

    connection.commit()

    return jsonify({
        'message': 'Usuario eliminado con éxito.'
    }), 200

if __name__ == '__main__':
     app.run(debug=True)
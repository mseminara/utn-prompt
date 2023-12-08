# Instalar con pip install Flask
from flask import Flask, request, jsonify

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

from datetime import datetime, timedelta

import random
import string

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 


class Codigo:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.create_database()

    def create_database(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = self.connection.cursor()

            # Crear la base de datos si no existe
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database} CHARACTER SET utf8 COLLATE utf8_general_ci")
            cursor.execute(f"USE {self.database}")

            # Crear la tabla clientes si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(40) NOT NULL,
                    dni VARCHAR(8) NOT NULL,
                    instagram_user VARCHAR(30),
                    fecha_nac DATETIME NOT NULL
                ) CHARACTER SET utf8 COLLATE utf8_general_ci
            """)

            # Crear la tabla codigos si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS codigos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha_generacion DATETIME NOT NULL,
                    codigo VARCHAR(10) NOT NULL,
                    fecha_vencimiento DATETIME NOT NULL,
                    fecha_utilizado DATETIME,
                    fk_cliente INT NOT NULL,
                    FOREIGN KEY (fk_cliente) REFERENCES clientes(id)
                ) CHARACTER SET utf8 COLLATE utf8_general_ci
            """)

            # Insertar datos en la tabla clientes y tabla codigos
            cursor.execute("""
                INSERT INTO clientes (id, nombre, dni, instagram_user, fecha_nac) VALUES
                    (1, 'Juan Pérez', '12345678', 'juancito23', '1997-05-20 00:00:00'),
                    (2, 'María García', '23456789', 'maria_g', '2001-08-10 00:00:00'),
                    (3, 'Pedro Martinez', '34567890', 'pedrito_m', '2000-11-15 00:00:00'),
                    (4, 'Lucía Rodríguez', '45678901', 'lucy_22', '2002-03-25 00:00:00'),
                    (5, 'Santiago López', '56789012', 'santi_l', '2003-07-18 00:00:00'),
                    (6, 'Valentina Fernández', '67890123', 'vale_fdez', '2002-09-05 00:00:00'),
                    (7, 'Mateo González', '78901234', 'mateo.g', '2001-12-30 00:00:00'),
                    (8, 'Camila Silva', '89012345', 'camila.s', '2000-04-12 00:00:00'),
                    (9, 'Lucas Pérez', '90123456', 'lucas_25', '2003-01-08 00:00:00'),
                    (10, 'Martina Díaz', '01234567', 'marti.d', '2002-06-29 00:00:00')
                """)

            cursor.execute("""INSERT INTO codigos (id, fecha_generacion, codigo, fecha_vencimiento, fk_cliente) VALUES
                    (1, '2023-11-20 09:30:00', 'A1B2C3D4E5', '2023-11-27 09:30:00', 5),
                    (2, '2023-11-25 15:45:00', 'X9Y8Z7W6V5', '2023-12-02 15:45:00', 3),
                    (3, '2023-11-30 11:20:00', 'M3N7O1P5Q9', '2023-12-07 11:20:00', 9),
                    (4, '2023-12-01 08:10:00', 'R6S2T8U4V0', '2023-12-08 08:10:00', 6),
                    (5, '2023-12-03 13:55:00', 'F1G3H5I7J9', '2023-12-10 13:55:00', 1),
                    (6, '2023-12-05 10:00:00', 'K2L4M6N8O0', '2023-12-12 10:00:00', 8),
                    (7, '2023-12-07 14:20:00', 'P9Q1R3S5T7', '2023-12-14 14:20:00', 10),
                    (8, '2023-11-17 12:45:00', 'W5X7Y9Z1A3', '2023-11-24 12:45:00', 4),
                    (9, '2023-11-21 16:00:00', 'B2C4D6E8F0', '2023-11-28 16:00:00', 7),
                    (10, '2023-11-29 17:30:00', 'G3H5I7J9K1', '2023-12-06 17:30:00', 2),
                    (11, '2023-11-22 18:10:00', 'N8O0P2Q4R6', '2023-11-29 18:10:00', 5),
                    (12, '2023-11-24 19:45:00', 'S5T7U9V1W3', '2023-12-01 19:45:00', 1),
                    (13, '2023-11-27 21:20:00', 'X2Y4Z6A8B0', '2023-12-04 21:20:00', 9),
                    (14, '2023-11-28 22:00:00', 'C1D3E5F7G9', '2023-12-05 22:00:00', 10),
                    (15, '2023-12-03 23:30:00', 'H4I6J8K0L2', '2023-12-10 23:30:00', 6);
            """)
            self.connection.commit()
            cursor.close()
            self.connection.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def generar_codigo(self, nombre, dni, instagram_user, fecha_nac):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = self.connection.cursor()

            # Verificar si el DNI existe en la tabla clientes
            cursor.execute("SELECT id FROM clientes WHERE dni = %s", (dni,))
            cliente = cursor.fetchone()

            if cliente:
                # Si el DNI existe en clientes, buscar un código generado en los últimos siete días
                seven_days_ago = datetime.now() - timedelta(days=7)
                cursor.execute("SELECT id FROM codigos WHERE fk_cliente = %s AND fecha_generacion > %s", (cliente[0], seven_days_ago))
                codigo_existente = cursor.fetchone()

                if codigo_existente:
                    return False, False  # Si existe un código generado en los últimos siete días, retornar False, False

                # Si no existe un código generado en los últimos siete días, insertar en la tabla codigos
                fecha_generacion = datetime.now()
                #codigo = "xxx"
                codigo = self.crear_codigo_aleatorio()  # Aquí deberías generar el código real
                fecha_vencimiento = fecha_generacion + timedelta(days=7)

                cursor.execute("""
                    INSERT INTO codigos (fecha_generacion, codigo, fecha_vencimiento, fk_cliente)
                    VALUES (%s, %s, %s, %s)
                """, (fecha_generacion, codigo, fecha_vencimiento, cliente[0]))

                self.connection.commit()
                cursor.close()
                self.connection.close()

                return codigo, fecha_vencimiento

            else:
                # Si el DNI no existe en clientes, insertarlo y luego insertar en la tabla codigos
                fecha_generacion = datetime.now()
                cursor.execute("""
                    INSERT INTO clientes (nombre, dni, instagram_user, fecha_nac)
                    VALUES (%s, %s, %s, %s)
                """, (nombre, dni, instagram_user, fecha_nac))

                cliente_id = cursor.lastrowid
                # codigo = "xxx"
                codigo = self.crear_codigo_aleatorio()
                fecha_vencimiento = fecha_generacion + timedelta(days=7)

                cursor.execute("""
                    INSERT INTO codigos (fecha_generacion, codigo, fecha_vencimiento, fk_cliente)
                    VALUES (%s, %s, %s, %s)
                """, (fecha_generacion, codigo, fecha_vencimiento, cliente_id))

                self.connection.commit()
                cursor.close()
                self.connection.close()

                return codigo, fecha_vencimiento

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def verificar_existencia(self, codigo):
        try:
            cursor = self.connection.cursor()

            cursor.execute("SELECT id FROM codigos WHERE codigo = %s", (codigo,))
            codigo_existente = cursor.fetchone()
            codigo_existente = False
            return bool(codigo_existente)  # Retorna True si el código existe, False si no existe

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False  # En caso de error, se devuelve False por defecto

    def crear_codigo_aleatorio(self):
        codigo = ''.join(random.choices(string.ascii_letters + string.digits, k=10)).upper()

        while self.verificar_existencia(codigo):
            # Generar un nuevo código si el actual ya existe en la tabla codigos
            codigo = ''.join(random.choices(string.ascii_letters + string.digits, k=10)).upper()

        return codigo  # Devolver el código generado

# Instanciar el objeto:
codigo = Codigo('localhost', 'root', '', 'cerveceria')


@app.route('/generar_codigo', methods=['POST'])
def generar_codigo():
    nombre = request.form.get('nombre')
    dni = request.form.get('dni')
    instagram_user = request.form.get('instagram_user')
    fecha_nac = request.form.get('fecha_nac')

    codigo_generado, fecha_vencimiento = codigo.generar_codigo(nombre, dni, instagram_user, fecha_nac)
    if codigo_generado and fecha_vencimiento:
        return jsonify({'codigo': codigo_generado, 'fecha_vencimiento': fecha_vencimiento}), 200
    else:
        return "No puede generar otro código en este momento", 400

if __name__ == '__main__':
    app.run(debug=True)

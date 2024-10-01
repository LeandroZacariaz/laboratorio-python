"""
Desafío 1: Sistema de Gestión de Productos
Objetivo: Desarrollar un sistema para manejar productos en un inventario.

Requisitos:

Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
Implementar operaciones CRUD para gestionar productos del inventario.
Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
Persistir los datos en archivo JSON.
"""
import mysql.connector
from mysql.connector import Error
from decouple import config


class Producto:
    def __init__(self, idproducto, nombre, descripcion, precio, cantidad):
<<<<<<< HEAD:laboratorio.py
        self.__idproducto=self.validar_id(idproducto)
=======
        self.__idproducto=idproducto
>>>>>>> 5ff16bddf98dba16f585c2408fb418297159e9d3:laboratorio1_python/laboratorio.py
        self.__nombre=nombre
        self.__descripcion=descripcion
        self.__precio=self.validar_precio(precio)
        self.__cantidad=self.validar_cantidad(cantidad)

    @property
    def idproducto(self):
        return self.__idproducto
    
    @idproducto.setter
    def idproducto(self, nuevo_id):
        self._idproducto = self.validar_id(nuevo_id)
<<<<<<< HEAD:laboratorio.py
    
    def validar_id(self, id):
        try:
            id_num=int(id)
            if id_num <=0:
                raise ValueError("El ID debe ser un número positivo.")
            return id_num
        except ValueError:
            raise ValueError("El ID debe ser numérico.")
=======

>>>>>>> 5ff16bddf98dba16f585c2408fb418297159e9d3:laboratorio1_python/laboratorio.py

    @property
    def nombre(self):
        return self.__nombre.capitalize()
    
    @property
    def descripcion(self):
        return self.__descripcion.capitalize()
    
    @property
    def precio(self):
        return self.__precio
    
    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)
    
    def validar_precio(self, precio):
        try:
            precio_num=float(precio)
            if precio_num <=0:
                raise ValueError("El precio debe ser un número positivo.")
            return precio_num
        except ValueError:
            raise ValueError("El precio debe ser numérico.")

    @property
    def cantidad(self):
        return self.__cantidad
    
    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        self.__cantidad = self.validar_cantidad(nueva_cantidad)
        
    def validar_cantidad(self, cantidad):
        try:
            cantidad_num=int(cantidad)
            if cantidad_num <=0:
                raise ValueError("La cantidad debe ser un número positivo.")
            return cantidad_num
        except ValueError:
            raise ValueError("La cantidad debe ser numérico.")
        
    def to_dict(self):
        return {
            "idproducto": self.idproducto,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "cantidad": self.cantidad
        }


class ProductoElectronico(Producto):
    def __init__(self, idproducto, nombre, descripcion, precio, cantidad, garantia):
        super().__init__(idproducto, nombre, descripcion, precio, cantidad)
        self.__garantia= self.validar_garantia(garantia)

    @property
    def garantia(self):
        return self.__garantia
    
    @garantia.setter
    def garantia(self, nueva_garantia):
        self.__garantia = self.validar_garantia(nueva_garantia)
    
    def validar_garantia(self, garantia):
        try:
            garantia_num=int(garantia)
            if garantia_num <=0:
                raise ValueError("La garantia debe ser un número positivo.")
            return garantia_num
        except ValueError:
            raise ValueError("La garantia debe ser numérico.")
            
    def to_dict(self):
        data = super().to_dict()
        data["garantia"]=self.garantia
        return data


class ProductoVestimenta(Producto):
    def __init__(self, idproducto, nombre, descripcion, precio, cantidad, marca, color, genero):
        super().__init__(idproducto, nombre, descripcion, precio, cantidad)
        self.__marca=marca
        self.__color=color
        self.__genero=self.validar_genero(genero)
    
    @property
    def marca(self):
        return self.__marca
    
    @property
    def color(self):
        return self.__color

    @property
    def genero(self):
        return self.__genero    
    
    @genero.setter
    def genero(self, nuevo_genero):
        self.__genero = self.validar_genero(nuevo_genero)
    
    def validar_genero(self, genero):
        try:
            if genero not in ["H", "M", "U"]:
                raise ValueError("El género debe ser H (Hombre), M (Mujer) o U (Unisex).")
            return genero
        except ValueError:
            raise ValueError("El género ingresado no es el correcto.")    

    def to_dict(self):
        data = super().to_dict()
        data["marca"]=self.marca
        data["color"] = self.color
        data["genero"] = self.genero
        return data
    
class GestionProductos:
    def __init__(self):
        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.port = config('DB_PORT')

    def connect(self):
        '''Establecer una conexion con la base de datos'''
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )

            if connection.is_connected():
                return connection
        
        except Error as e:
            print(f'Error al conectar a la base de datos: {e}')
            return None

    def crear_producto(self, producto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT idproducto FROM producto WHERE idproducto=%s',(producto.idproducto,))
                    if cursor.fetchone():
                        print(f'Error: Ya existe un producto con ID {producto.idproducto}')
                        return
                    
                    if isinstance(producto, ProductoElectronico):
                        query = '''
                        INSERT INTO producto (idproducto, nombre, descripcion, precio, cantidad)
                        VALUES (%s,%s,%s,%s,%s)
                        '''
                        cursor.execute(query, (producto.idproducto, producto.nombre, producto.descripcion, 
                                               producto.precio, producto.cantidad))
                        
                        query='''
                        INSERT INTO productoelectronico (idproducto, garantia)
                        VALUES (%s,%s)
                        '''
                        cursor.execute(query, (producto.idproducto, producto.garantia))
                    
                    elif isinstance(producto, ProductoVestimenta):
                        query = '''
                        INSERT INTO producto (idproducto, nombre, descripcion, precio, cantidad)
                        VALUES (%s,%s,%s,%s,%s)
                        '''
                        cursor.execute(query, (producto.idproducto, producto.nombre, producto.descripcion, 
                                               producto.precio, producto.cantidad))
                        
                        query='''
                        INSERT INTO productovestimenta (idproducto, marca, color, genero)
                        VALUES (%s, %s, %s, %s)
                        '''
                        cursor.execute(query, (producto.idproducto, producto.marca, producto.color, producto.genero))
                    
                    connection.commit()
                    print(f'Producto {producto.nombre} con ID {producto.idproducto} creado correctamente.')
        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')

    def leer_producto(self, idproducto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor: 
                    cursor.execute('SELECT * FROM producto WHERE idproducto= %s', (idproducto,))
                    producto_data=cursor.fetchone()

                    if producto_data:
                        cursor.execute('SELECT garantia FROM productoelectronico WHERE idproducto = %s', (idproducto,))
                        garantia=cursor.fetchone()

                        if garantia:
                            producto_data['garantia']=garantia['garantia']
                            producto = ProductoElectronico(**producto_data)
                        else: 
                            cursor.execute('SELECT marca,color,genero FROM productovestimenta WHERE idproducto =%s',(idproducto,))
                            marca=cursor.fetchone()
                            if marca:
                                producto_data['marca'] = marca['marca']
                                producto_data['color'] = marca['color']
                                producto_data['genero'] = marca['genero']
                                producto=ProductoVestimenta(**producto_data)
                            else:
                                producto = Producto(**producto_data)
                        
                        print (f'Producto encontrado: {producto.nombre} ')
                    
                    else:
                        print(f'No se encontró el producto con ID {idproducto}')

        except Error as e:
            print(f'Error al leer producto: {e}')
        finally:
            if connection.is_connected():
                connection.close()


    def actualizar_producto(self, idproducto, nuevo_precio):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM producto WHERE idproducto = %s', (idproducto,))
                    if not cursor.fetchone():
                        print(f'No se encontró al producto con ID {idproducto}.')
                        return
                    
                    cursor.execute('UPDATE producto SET precio = %s WHERE idproducto = %s', (nuevo_precio, idproducto))

                    if cursor.rowcount>0:
                        connection.commit()
                        print(f'Precio actualizado para el producto con ID {idproducto}.')
                    else:
                        print(f'No se encontró al producto con ID {idproducto}.')

        except Exception as e:
            print(f'Error al actualizar el producto: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def eliminar_producto(self, idproducto):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM producto WHERE idproducto = %s', (idproducto,))
                    if not cursor.fetchone():
                        print (f'No se encontró al producto con ID {idproducto}.')
                        return
                    
                    cursor.execute('DELETE FROM productoelectronico WHERE idproducto = %s', (idproducto,))
                    cursor.execute('DELETE FROM productovestimenta WHERE idproducto = %s', (idproducto,))
                    cursor.execute('DELETE FROM producto WHERE idproducto = %s', (idproducto,))
                    if cursor.rowcount>0:
                        connection.commit()
                        print(f'Producto con ID: {idproducto} eliminado correctamente ')
                    else:
                        print(f'No se encontró producto con ID {idproducto}.')

        except Exception as e:
            print(f'Error al eliminar el producto: {e}')
        finally:
            if connection.is_connected():
                connection.close()

    def leer_todos_los_productos(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM producto')
                    productos_data=cursor.fetchall()

                    productos=[]

                    for producto_data in productos_data:
                        idproducto=producto_data['idproducto']

                        cursor.execute('SELECT garantia FROM productoelectronico WHERE idproducto = %s', (idproducto,))
                        garantia=cursor.fetchone()

                        if garantia:
                            producto_data['garantia']=garantia['garantia']
                            producto=ProductoElectronico(**producto_data)
                        else:
                            cursor.execute('SELECT marca,color,genero FROM productovestimenta WHERE idproducto=%s', (idproducto,))
                            marca = cursor.fetchone()
                            producto_data['marca']=marca['marca']
                            producto_data['color'] = marca['color']
                            producto_data['genero'] = marca['genero']
                            producto=ProductoVestimenta(**producto_data)

                        productos.append(producto)

        except Exception as e:
            print(f'Error al mostrar los productos: {e}')
        else:
            return productos
        finally:
            if connection.is_connected():
                connection.close()

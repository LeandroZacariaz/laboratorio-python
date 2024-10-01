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
import json

class Producto:
    def __init__(self, idproducto, nombre, descripcion, precio, cantidad):
        self.__idproducto=idproducto
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
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crear_producto(self, producto):
        try:
            datos = self.leer_datos()
            idproducto = producto.idproducto
            if not str(idproducto) in datos.keys():
                datos[idproducto] = producto.to_dict()
                self.guardar_datos(datos)
                print(f"Producto {producto.idproducto} {producto.nombre} creado correctamente.")
            else:
                print(f"Ya existe producto con id '{idproducto}'.")
        except Exception as error:
            print(f'Error inesperado al crear producto: {error}')

    def leer_producto(self, idproducto):
        try:
            datos = self.leer_datos()
            if idproducto in datos:
                producto_data = datos[idproducto]
                if 'garantia' in producto_data:
                    producto = ProductoElectronico(                    
                    nombre=producto_data['nombre'],
                    descripcion=producto_data['descripcion'],
                    precio=producto_data['precio'],
                    cantidad=producto_data['cantidad'],
                    garantia=producto_data['garantia'])
                else:
                    producto = ProductoVestimenta(                    
                    nombre=producto_data['nombre'],
                    descripcion=producto_data['descripcion'],
                    precio=producto_data['precio'],
                    cantidad=producto_data['cantidad'],
                    marca=producto_data['marca'],
                    color=producto_data['color'],
                    genero=producto_data['genero'])
                producto.idproducto = producto_data['idproducto']
                print(f'Producto encontrado con ID {idproducto} - Nombre: {producto.nombre} - Precio: {producto.precio}. ')
            else:
                print(f'No se encontró el producto con ID {idproducto}')

        except Exception as e:
            print(f'Error al leer producto: {e}')


    def actualizar_producto(self, idproducto, nuevo_precio):
        try:
            datos = self.leer_datos()
            if str(idproducto) in datos.keys():
                 datos[idproducto]['precio'] = nuevo_precio
                 self.guardar_datos(datos)
                 print(f'Precio actualizado para el producto ID: {idproducto}')
            else:
                print(f'No se encontró producto con ID: {idproducto}')
        except Exception as e:
            print(f'Error al actualizar el producto: {e}')

    def eliminar_producto(self, idproducto):
        try:
            datos = self.leer_datos()
            if str(idproducto) in datos.keys():
                 del datos[idproducto]
                 self.guardar_datos(datos)
                 print(f'Producto:{idproducto} eliminado correctamente')
            else:
                print(f'No se encontró producto ID:{idproducto}')
        except Exception as e:
            print(f'Error al eliminar el producto: {e}')
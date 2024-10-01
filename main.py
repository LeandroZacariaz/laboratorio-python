import os
import platform

from laboratorio import (
    ProductoVestimenta,ProductoElectronico, GestionProductos
)

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') # Para Linux/Unix/MacOs

def mostrar_menu():
    print("╔══════════════════════════════════════════╗")
    print("║       Menú de Gestión de Productos       ║")
    print("╠══════════════════════════════════════════╣")
    print("║ 1. Agregar Producto Electrónico          ║")
    print("║ 2. Agregar Producto de Vestimenta        ║")
    print("║ 3. Buscar Producto por ID                ║")
    print("║ 4. Actualizar Producto                   ║")
    print("║ 5. Eliminar Producto por ID              ║")
    print("║ 6. Mostrar Todos los Productos           ║")
    print("║ 7. Salir                                 ║")
    print("╚══════════════════════════════════════════╝")

def agregar_producto(gestion, tipo_producto):
    try:
        idproducto = input ('Ingrese el id del producto: ')
        nombre = input('Ingrese nombre del producto: ')
        descripcion = input('Ingrese descripcion del producto: ')
        precio = float(input('Ingrese precio del producto: '))
        cantidad = int(input('Ingrese cantidad de stock del producto: '))

        if tipo_producto == '1':
            garantia = int(input('Ingrese garantia en meses: '))
            producto = ProductoElectronico(idproducto, nombre, descripcion, precio, cantidad, garantia)
        elif tipo_producto == '2':
            marca = input('Ingrese la marca del producto: ')
            color = input ('Ingrese el color del producto: ')
            genero = input ('Ingrese el género del producto H (Hombre), M (Mujer) o U (Unisex): ')
            producto = ProductoVestimenta(idproducto, nombre, descripcion, precio, cantidad, marca, color, genero)
        else:
            print('Opción inválida')
            return

        gestion.crear_producto(producto)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_producto_por_id(gestion):
    idproducto = input('Ingrese el ID del producto a buscar: ')
    gestion.leer_producto(idproducto)
    input('Presione enter para continuar...')

def actualizar_precio_producto(gestion):
    idproducto = input('Ingrese el ID del producto para actualizar precio: ')
    precio = float(input('Ingrese el precio del producto: '))
    gestion.actualizar_producto(idproducto, precio)
    input('Presione enter para continuar...')

def eliminar_producto_por_id(gestion):
    idproducto = input('Ingrese el ID del producto a eliminar: ')
    gestion.eliminar_producto(idproducto)
    input('Presione enter para continuar...')

def mostrar_todos_los_productos(gestion):
    print("╔═══════════════════════════════════════════════════════════════")
    print("║               Listado completo de los Productos               ")
    print("╠═══════════════════════════════════════════════════════════════")
    try:
        productos=gestion.leer_todos_los_productos()
        for producto in productos:
            if isinstance(producto, ProductoElectronico):
                print(f'║ ID: {producto.idproducto} NOMBRE: {producto.nombre} PRECIO: {producto.precio} GARANTIA: {producto.garantia}')
            elif isinstance(producto, ProductoVestimenta):
                print(f'║ ID: {producto.idproducto} NOMBRE: {producto.nombre} PRECIO: {producto.precio} MARCA: {producto.marca}')
    except Exception as e:
        print(f'Error al mostrar los productos {e}')
    print("╚═══════════════════════════════════════════════════════════════")
    input('Presione enter para continuar...')

if __name__ == "__main__":
    gestion = GestionProductos()

    while True:
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_producto(gestion, opcion)
        
        elif opcion == '3':
            buscar_producto_por_id(gestion)

        elif opcion == '4':
            actualizar_precio_producto(gestion)

        elif opcion == '5':
            eliminar_producto_por_id(gestion)

        elif opcion == '6':
            mostrar_todos_los_productos(gestion)

        elif opcion == '7':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-7)')
        

# Escribimos una serie de funciones para crear una pequeña app que
# maneje un arreglo que contenga datos de productos.
# Cada producto tiene un código numérico entero, una descripción
# alfabética, una cantidad en stock y un precio de venta.
# Nuestro producto también incluye una imagen y un proveedor.
# Nuestras funciones harán lo siguiente:
#
# - Agregar un producto al arreglo
# - Consultar un producto a partir de su código
# - Modificar los datos de un producto a partir de su código
# - Obtener un listado de los productos que existen en el arreglo.
# - Eliminar un producto del arreglo
# -------------------------------------------------------------------
# Definimos una lista para almacenar los productos.
# Es una lista de diccionarios.


import mysql.connector

print("\033[H\033[J") # Limpiar la consola

class Catalogo:
    productos = [] 
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            codigo INT,
            descripcion VARCHAR(255) NOT NULL,
            cantidad INT NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            imagen_url VARCHAR(255),
            proveedor INT)''')
        self.conn.commit()


    # -------------------------------------------------------------------
    # Agregar productos
    # -------------------------------------------------------------------
    def agregar_productos(self, cod, des, can, pre, ima, pro):
        self.cursor.execute(f"SELECT * FROM productos WHERE codigo = {cod}")
        producto_exist = self.cursor.fetchone()
        if producto_exist:
            return False

        sql = f"INSERT INTO productos \
            (codigo, descripcion, cantidad, precio, imagen_url, proveedor) \
            VALUES \
            ({cod}, '{des}', {can}, {pre}, '{ima}', {pro})"
        self.cursor.execute(sql)
        self.conn.commit()
        return True

    #-------------------------------------------------------------------
    # Listar productos
    #------------------------------------------------------------------
    def listar_productos(self):
        print("-"*30)
        for producto in self.productos:
            print(f"Codigo.....: {producto['codigo']}" )
            print(f"Producto...: {producto['descripcion']}" )
            print(f"Stock......: {producto['cantidad']}" )
            print(f"Valor......: {producto['precio']}" )
            print(f"Imagen.....: {producto['imagen']}" )
            print(f"Id Prov....: {producto['proveedor']}" )
            print("-"*30)


    # -------------------------------------------------------------------
    # Consultar productos
    # ------------------------------------------------------------------
    def consultar_producto(self, cod):
        self.cursor.execute(f"SELECT * FROM productos WHERE codigo = {cod}")
        producto_exist = self.cursor.fetchone()
        if producto_exist:
            return producto_exist

    # -------------------------------------------------------------------
    # Eliminar producto
    # ------------------------------------------------------------------
    def eliminar_producto(self, cod):
        self.cursor.execute(f"DELETE FROM productos WHERE codigo = {cod}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    # -------------------------------------------------------------------
    # Modificar producto
    # ------------------------------------------------------------------
    def modificar_producto(self, cod, des, can, pre, ima, pro):
        sql = f"UPDATE productos SET \
                descripcion = '{des}',\
                cantidad = {can},\
                precio = {pre},\
                imagen_url = '{ima}',\
                proveedor = {pro}\
                WHERE codigo = {cod}"
        self.cursor.execute(sql)
        self.conn.commit()
        return True

# # -------------------------------------------------------------------
mi_lista_de_productos = Catalogo(host='localhost', user='root', password='', database='miapp')

#print(mi_lista_de_productos.agregar_productos(1, "Teclado USB", 45, 8700, "teclado.jpg", 4))
#print(mi_lista_de_productos.agregar_productos(2, "Mouse USB", 415, 700, "mpouse.jpg", 4))
# mi_lista_de_productos.listar_productos()
#print(mi_lista_de_productos.modificar_producto(2, "TELE 50", 5, 7, "tv50.jpg", 3))
print(mi_lista_de_productos.eliminar_producto(2))
print(mi_lista_de_productos.consultar_producto(2))

"""#-------------------------------------------------------------------
mi_lista_de_productos = Catalogo (localhost, root, '', miapp)

mi_lista_de_productos.agregar_productos
mi_lista_de_productos.listar_productos
agregar_productos(1, "conejito con zanahoria", 10, 800, ima, pro)
agregar_productos(2, "Pokemon snorlax", 15, 2300, ima, pro)
agregar_productos(3, "pokemon pikachu", 18, 800, ima, pro)
agregar_productos(4, "llavero corazon", 10, 800, ima, pro)
agregar_productos(5, "baby yoda", 10, 800, ima, pro)
agregar_productos(6, "stitch", 10, 800, ima, pro)
agregar_productos(7, "heladitos", 4, 1200, ima, pro)
agregar_productos(8, "sirenita", 3, 1500, ima, pro)
agregar_productos(9, "gallinita", 5, 1850, ima, pro)
agregar_productos(10, "alpaca chica", 7, 1350, ima, pro)"""

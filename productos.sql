CREATE DATABASE productos;
USE productos;

CREATE TABLE Producto (
    idproducto INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    cantidad INT
);

CREATE TABLE ProductoElectronico (
    idproducto INT PRIMARY KEY,
    garantia INT NOT NULL,
    FOREIGN KEY (idproducto) REFERENCES Producto(idproducto)
);

CREATE TABLE ProductoVestimenta (
    idproducto INT PRIMARY KEY,
    marca VARCHAR(100) NOT NULL,
    color VARCHAR(50) NOT NULL,
    genero CHAR(1) NOT NULL,
    FOREIGN KEY (idproducto) REFERENCES Producto(idproducto)
);

SELECT * FROM producto;


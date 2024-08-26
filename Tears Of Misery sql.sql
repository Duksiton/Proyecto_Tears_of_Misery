
create database tearsOfMisery;
use tearsOfMisery;


create table roles (
idRol int primary key auto_increment NOT NULL unique,
nombreRol varchar (20) NOT NULL unique
);

CREATE TABLE usuario (
    idUsuario INT PRIMARY KEY AUTO_INCREMENT NOT NULL UNIQUE,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(40) NOT NULL UNIQUE,
    contraseña VARCHAR(30) NOT NULL,
    direccion VARCHAR(40) NOT NULL DEFAULT '',
    telefono VARCHAR(10) NOT NULL DEFAULT '',
    nombreRol VARCHAR(20) NOT NULL DEFAULT 'Usuario',
    FOREIGN KEY (nombreRol) REFERENCES roles(nombreRol)
);

CREATE TABLE categoria (
    idCat INT PRIMARY KEY AUTO_INCREMENT NOT NULL UNIQUE,
    nombre VARCHAR(50) UNIQUE NOT NULL
);


CREATE TABLE producto (
    idProducto INT PRIMARY KEY AUTO_INCREMENT NOT NULL UNIQUE,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    talla ENUM('S', 'M', 'L', 'XL'),
    precio FLOAT NOT NULL,
    stock INT NOT NULL, 
    imagen VARCHAR(255) NOT NULL,
    idCat INT NOT NULL,
    FOREIGN KEY (idCat) REFERENCES categoria(idCat)
);


create table pedido (
idPedido int primary key auto_increment NOT NULL unique,
fechaPedido date NOT NULL,
totalPedido float NOT NULL,
estado varchar (40) NOT NULL,
idUsuario int NOT NULL, 
foreign key (idUsuario) references usuario (idUsuario)
);

create table detallePedido (
idDetalle int primary key auto_increment NOT NULL unique,
cantidad int NOT NULL,
precio float NOT NULL,
idProducto int NOT NULL,
foreign key (idProducto) references producto (idProducto),
idPedido int NOT NULL,
foreign key (idPedido) references pedido (idPedido)
);

insert into roles (nombreRol) values ('Administrador');
insert into roles (nombreRol) values ('Usuario');

insert into usuario (nombre, email, contraseña, direccion, telefono, nombreRol) values
('Usuario 1', 'user1@gmail.com','miContraseña','Calle 37 A Bis Sur','3227467685', 'Usuario');

insert into usuario (nombre, email, contraseña, direccion, telefono, nombreRol) values
('Administrador', 'admin@gmail.com','admin1234','Calle 5 A 5 B Sur','3008155607', 'Administrador');

insert into categoria (nombre) values ('Camisas');
insert into categoria (nombre) values ('Discos');
insert into categoria (nombre) values ('Sacos');


SELECT p.*, c.nombre AS categoriaNombre
FROM producto p
LEFT JOIN categoria c ON p.idCat = c.idCat;

select * from producto;


select * from pedido;
select * from usuario;
select * from categoria;
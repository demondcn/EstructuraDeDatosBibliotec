# Portada

**Titulo del trabajo:** Prototipo funcional de un sistema de gestion de biblioteca usando estructuras de datos lineales

**Asignatura:** Estructura de Datos

**Estudiante:** [Cristian Stiven Guerrero Andrade]

**Docente:** [Jorje Ruis]

**Institucion:** [Iberoamericana]

**Fecha:** [4/5/2026]

## Introduccion

Este documento presenta el desarrollo de un prototipo funcional para la gestion de una biblioteca, orientado a la aplicacion de estructuras de datos lineales en un problema del mundo real. El sistema fue implementado en Python y permite registrar libros y usuarios, realizar prestamos y devoluciones, controlar reservas y consultar la informacion almacenada mediante una interfaz de consola.

## Desarrollo del tema

### Analisis de requisitos

El sistema debia almacenar informacion de libros y usuarios, permitir operaciones de consulta y administrar el flujo de prestamos. A partir de estos requisitos se seleccionaron estructuras de datos lineales que responden a la naturaleza de cada proceso.

### Seleccion de estructuras de datos

- **Listas:** se utilizaron para almacenar libros, usuarios y prestamos, ya que permiten recorridos secuenciales y gestion dinamica del tamano.
- **Cola:** se uso para gestionar las reservas de libros sin disponibilidad, respetando el principio FIFO.
- **Pila:** se implemento para conservar un historial reciente de acciones del sistema.
- **Arreglo:** se empleo para mantener un conjunto fijo de categorias base de la biblioteca.

### Parametros de los datos almacenados

Los libros almacenan `isbn`, `titulo`, `autor`, `categoria`, `ejemplares_totales`, `ejemplares_disponibles` y `tamano_cola_reserva`.

Los usuarios almacenan `id_usuario`, `nombre` y `correo`.

Los prestamos almacenan `isbn_libro`, `id_usuario`, `fecha_prestamo` y `estado_devolucion`.

### Relacion entre conceptos y solucion

La implementacion evidencia la aplicacion practica de estructuras lineales. Las listas permiten concentrar el inventario y los registros. La cola organiza reservas en orden de llegada. La pila permite seguimiento de operaciones recientes. El arreglo fija categorias iniciales y ejemplifica el uso de una estructura de tamano constante.

### Interfaz de usuario

Se construyo una interfaz de consola basada en menu numerico. Esta interfaz facilita el acceso a las operaciones principales del sistema y permite validar el comportamiento del prototipo en un entorno sencillo y entendible.

### Pruebas realizadas

Se desarrollaron pruebas unitarias para validar:

- registro de libros
- registro de usuarios
- busqueda de libros
- prestamos con disponibilidad
- ingreso a cola de reserva
- asignacion automatica del libro al primer usuario en espera

## Conclusiones

El prototipo demuestra que las estructuras de datos lineales permiten resolver de forma organizada y eficiente necesidades reales de administracion de informacion. La seleccion adecuada de cada estructura mejora la claridad del diseno, facilita la implementacion y fortalece la comprension de los conceptos estudiados en la unidad.

## Referencias

Ayala San Martin, G. (2020). *Algoritmos y programacion: mejores practicas*. Fundacion Universidad de las Americas Puebla.

Fritelli, V., Guzman, A., & Tymoschuk, J. (2020). *Algoritmos y estructuras de datos* (2.a ed.). Jorge Sarmiento Editor - Universitas.

Ruiz Rodriguez, R. (2009). *Fundamentos de la programacion orientada a objetos: una aplicacion a las estructuras de datos en Java*. El Cid Editor.

Zohonero Martinez, I., & Joyanes Aguilar, L. (2008). *Estructuras de datos en Java*. McGraw-Hill.

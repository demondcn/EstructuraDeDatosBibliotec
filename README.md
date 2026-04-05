# IberoBibliopyStructureDates

Prototipo academico en Python para administrar libros, usuarios, prestamos y reservas usando estructuras de datos lineales y una interfaz grafica en Tkinter inspirada en Koha.

## Estructuras usadas

- `list`: almacenamiento principal de libros, usuarios y prestamos.
- `deque`: cola de reservas por libro.
- `list` como pila: historial de acciones recientes.
- `list` de tamano fijo: categorias base de la biblioteca.

## Funcionalidades

- Registrar libros y usuarios.
- Buscar libros por titulo, autor o ISBN.
- Registrar prestamos y devoluciones.
- Administrar reservas en cola.
- Consultar historial de acciones.
- Mostrar catalogo, usuarios y prestamos activos.

## Interfaz

- Barra superior y barra de circulacion inspiradas en Koha.
- Panel lateral con ficha del usuario seleccionado.
- Vista central con prestamos, catalogo, usuarios e historial.
- Formularios emergentes para registrar libros y usuarios.
- Paleta visual en negro, amarillo y tonos miel.

## Ejecucion

```bash
python main.py
```

## Pruebas

```bash
python -m unittest discover -s tests
```

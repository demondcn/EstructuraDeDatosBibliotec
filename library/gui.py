from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from library.system import LibrarySystem


class LibraryApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.system = LibrarySystem()
        self.selected_user_id: str | None = None
        self.selected_book_isbn: str | None = None

        self.title("IberoBibliopyStructureDates")
        self.geometry("1400x840")
        self.minsize(1180, 760)
        self.configure(bg="#f6f0df")

        self.colors = {
            "dark": "#171411",
            "primary": "#d6a419",
            "primary_light": "#f0c44c",
            "honey": "#b7791f",
            "surface": "#ffffff",
            "surface_alt": "#f6f0df",
            "panel": "#e8d7a4",
            "panel_alt": "#f7eed2",
            "border": "#d8bb68",
            "text": "#1c1814",
            "muted": "#68563b",
            "accent": "#f3c64d",
        }

        self._build_styles()
        self._build_layout()
        self.refresh_all_views()

    def run(self) -> None:
        self.mainloop()

    def _build_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "App.Treeview",
            background=self.colors["surface"],
            fieldbackground=self.colors["surface"],
            foreground=self.colors["text"],
            rowheight=30,
            bordercolor=self.colors["border"],
            borderwidth=1,
        )
        style.configure(
            "App.Treeview.Heading",
            background=self.colors["panel_alt"],
            foreground=self.colors["text"],
            relief="flat",
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "App.Treeview",
            background=[("selected", "#f1d88a")],
            foreground=[("selected", self.colors["text"])],
        )

    def _build_layout(self) -> None:
        self._build_top_navigation()
        self._build_search_bar()

        body = tk.Frame(self, bg=self.colors["surface_alt"])
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        self.sidebar = tk.Frame(body, bg=self.colors["panel"], width=310)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        self.content = tk.Frame(body, bg=self.colors["surface_alt"])
        self.content.grid(row=0, column=1, sticky="nsew", padx=24, pady=20)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(2, weight=1)

        self._build_sidebar()
        self._build_content()

    def _build_top_navigation(self) -> None:
        nav = tk.Frame(self, bg=self.colors["dark"], height=40)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        logo = tk.Label(nav, text="IB", bg=self.colors["dark"], fg=self.colors["accent"], font=("Segoe UI", 13, "bold"))
        logo.pack(side="left", padx=(14, 8))

        tk.Label(
            nav,
            text="IberoBibliopyStructureDates",
            bg=self.colors["dark"],
            fg="white",
            font=("Georgia", 16, "bold"),
        ).pack(side="left", padx=(0, 24))

        for item in ("Circulacion", "Usuarios", "Busqueda", "Catalogo"):
            tk.Label(nav, text=item, bg=self.colors["dark"], fg="white", font=("Segoe UI", 11)).pack(side="left", padx=14)

        tk.Label(
            nav,
            text="Biblioteca Central",
            bg=self.colors["dark"],
            fg="white",
            font=("Segoe UI", 11, "bold"),
        ).pack(side="right", padx=16)

    def _build_search_bar(self) -> None:
        bar = tk.Frame(self, bg=self.colors["primary"], height=58)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(
            bar,
            text="Prestamo",
            bg=self.colors["primary"],
            fg=self.colors["text"],
            font=("Segoe UI", 12, "bold"),
        ).pack(side="left", padx=(18, 18))

        self.user_search_var = tk.StringVar()
        self.user_search_entry = PlaceholderEntry(
            bar,
            placeholder="Ingrese el ID, nombre o correo del usuario",
            textvariable=self.user_search_var,
            relief="flat",
            font=("Segoe UI", 12),
            width=45,
        )
        self.user_search_entry.pack(side="left", padx=(0, 0), ipady=8, pady=10)
        self.user_search_entry.bind("<Return>", lambda _event: self.search_user())

        tk.Button(
            bar,
            text="Ir",
            command=self.search_user,
            bg=self.colors["dark"],
            fg=self.colors["accent"],
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            activebackground="#2b241f",
            activeforeground=self.colors["accent"],
            padx=16,
            pady=6,
        ).pack(side="left", padx=(0, 18))

        for text, command in (
            ("Prestar", self.checkout_selected),
            ("Devolver", self.return_selected),
            ("Buscar catalogo", self.search_catalog),
        ):
            tk.Button(
                bar,
                text=text,
                command=command,
                bg=self.colors["primary"],
                fg=self.colors["text"],
                relief="flat",
                font=("Segoe UI", 11, "underline"),
                activebackground=self.colors["primary"],
                activeforeground=self.colors["text"],
                cursor="hand2",
            ).pack(side="left", padx=12)

    def _build_sidebar(self) -> None:
        self.user_card = tk.Frame(self.sidebar, bg=self.colors["panel_alt"], padx=16, pady=16)
        self.user_card.pack(fill="x", padx=0, pady=(32, 0))

        self.user_name_label = tk.Label(
            self.user_card,
            text="Sin usuario seleccionado",
            bg=self.colors["panel_alt"],
            fg=self.colors["text"],
            font=("Segoe UI", 15, "bold"),
        )
        self.user_name_label.pack(anchor="w")

        self.user_details_label = tk.Label(
            self.user_card,
            text="Busca por ID, nombre o correo para cargar el patron.",
            bg=self.colors["panel_alt"],
            fg=self.colors["muted"],
            font=("Segoe UI", 11),
            justify="left",
        )
        self.user_details_label.pack(anchor="w", pady=(10, 0))

        menu = tk.Frame(self.sidebar, bg=self.colors["panel_alt"])
        menu.pack(fill="x", pady=(18, 0))

        for text, callback in (
            ("Prestamos", lambda: self.notebook.select(self.loan_tab)),
            ("Detalles", lambda: self.notebook.select(self.user_tab)),
            ("Catalogo", lambda: self.notebook.select(self.catalog_tab)),
            ("Historial", lambda: self.notebook.select(self.history_tab)),
        ):
            button = tk.Button(
                menu,
                text=text,
                command=callback,
                anchor="w",
                bg=self.colors["panel_alt"],
                fg=self.colors["text"],
                relief="flat",
                font=("Segoe UI", 12, "bold" if text == "Prestamos" else "normal"),
                padx=16,
                pady=10,
                activebackground="#e9d08a",
            )
            button.pack(fill="x")

    def _build_content(self) -> None:
        actions = tk.Frame(self.content, bg=self.colors["surface_alt"])
        actions.grid(row=0, column=0, sticky="ew")
        actions.grid_columnconfigure(1, weight=1)

        tk.Label(
            actions,
            text="Prestamos",
            bg=self.colors["surface_alt"],
            fg=self.colors["dark"],
            font=("Segoe UI", 25, "bold"),
        ).grid(row=0, column=0, sticky="w")

        quick = tk.Frame(actions, bg=self.colors["surface_alt"])
        quick.grid(row=0, column=1, sticky="e")

        for text, command in (
            ("+ Agregar usuario", self.open_register_user_dialog),
            ("+ Agregar libro", self.open_register_book_dialog),
            ("Buscar reserva", self.search_catalog),
        ):
            tk.Button(
                quick,
                text=text,
                command=command,
                relief="flat",
                bg=self.colors["surface_alt"],
                fg=self.colors["muted"],
                font=("Segoe UI", 11),
                cursor="hand2",
            ).pack(side="left", padx=8)

        checkout_panel = tk.Frame(
            self.content,
            bg=self.colors["surface"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=14,
            pady=14,
        )
        checkout_panel.grid(row=1, column=0, sticky="ew", pady=(14, 16))
        checkout_panel.grid_columnconfigure(0, weight=1)

        tk.Label(
            checkout_panel,
            text="Registrar prestamo para el usuario seleccionado",
            bg=self.colors["surface"],
            fg=self.colors["text"],
            font=("Segoe UI", 15, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        entry_wrap = tk.Frame(checkout_panel, bg=self.colors["surface"])
        entry_wrap.grid(row=1, column=0, sticky="w")

        self.checkout_var = tk.StringVar()
        self.checkout_entry = PlaceholderEntry(
            entry_wrap,
            placeholder="Ingrese o seleccione el ISBN del libro",
            textvariable=self.checkout_var,
            width=44,
            font=("Segoe UI", 12),
            highlightthickness=2,
            highlightbackground=self.colors["honey"],
            highlightcolor=self.colors["honey"],
            relief="flat",
        )
        self.checkout_entry.pack(side="left", ipady=8)
        self.checkout_entry.bind("<Return>", lambda _event: self.checkout_selected())

        tk.Button(
            entry_wrap,
            text="Prestar",
            command=self.checkout_selected,
            bg=self.colors["accent"],
            fg=self.colors["text"],
            relief="flat",
            font=("Segoe UI", 11),
            padx=18,
            pady=8,
        ).pack(side="left", padx=12)

        self.notebook = ttk.Notebook(self.content)
        self.notebook.grid(row=2, column=0, sticky="nsew")

        self.loan_tab = tk.Frame(self.notebook, bg=self.colors["surface_alt"])
        self.catalog_tab = tk.Frame(self.notebook, bg=self.colors["surface_alt"])
        self.user_tab = tk.Frame(self.notebook, bg=self.colors["surface_alt"])
        self.history_tab = tk.Frame(self.notebook, bg=self.colors["surface_alt"])

        self.notebook.add(self.loan_tab, text="Prestamos")
        self.notebook.add(self.catalog_tab, text="Catalogo")
        self.notebook.add(self.user_tab, text="Usuarios")
        self.notebook.add(self.history_tab, text="Historial")

        self._build_loans_tab()
        self._build_catalog_tab()
        self._build_users_tab()
        self._build_history_tab()

    def _build_loans_tab(self) -> None:
        top = tk.Frame(self.loan_tab, bg=self.colors["surface_alt"])
        top.pack(fill="x", pady=(8, 10))

        self.checkout_status = tk.Label(
            top,
            text="No hay prestamos registrados.",
            bg=self.colors["surface_alt"],
            fg=self.colors["muted"],
            font=("Segoe UI", 12),
        )
        self.checkout_status.pack(anchor="w")

        cols = ("isbn", "user", "date", "title")
        self.loans_tree = ttk.Treeview(self.loan_tab, columns=cols, show="headings", style="App.Treeview", height=14)
        for column, title, width in (
            ("isbn", "ISBN", 130),
            ("user", "Usuario", 120),
            ("date", "Fecha", 120),
            ("title", "Titulo", 400),
        ):
            self.loans_tree.heading(column, text=title)
            self.loans_tree.column(column, width=width, anchor="w")
        self.loans_tree.pack(fill="both", expand=True)

        button_row = tk.Frame(self.loan_tab, bg=self.colors["surface_alt"])
        button_row.pack(fill="x", pady=12)
        tk.Button(
            button_row,
            text="Registrar devolucion",
            command=self.return_selected,
            bg=self.colors["primary"],
            fg="white",
            relief="flat",
            padx=12,
            pady=8,
        ).pack(side="left")

    def _build_catalog_tab(self) -> None:
        toolbar = tk.Frame(self.catalog_tab, bg=self.colors["surface_alt"])
        toolbar.pack(fill="x", pady=(8, 10))

        self.catalog_search_var = tk.StringVar()
        self.catalog_entry = PlaceholderEntry(
            toolbar,
            placeholder="Buscar por ISBN, titulo o autor",
            textvariable=self.catalog_search_var,
            font=("Segoe UI", 11),
            width=42,
        )
        self.catalog_entry.pack(side="left", ipady=6)
        self.catalog_entry.bind("<Return>", lambda _event: self.search_catalog())

        tk.Button(
            toolbar,
            text="Buscar en el catalogo",
            command=self.search_catalog,
            bg=self.colors["primary"],
            fg="white",
            relief="flat",
            padx=12,
            pady=6,
        ).pack(side="left", padx=10)

        cols = ("isbn", "title", "author", "category", "availability", "queue")
        self.catalog_tree = ttk.Treeview(self.catalog_tab, columns=cols, show="headings", style="App.Treeview", height=16)
        for column, title, width in (
            ("isbn", "ISBN", 120),
            ("title", "Titulo", 300),
            ("author", "Autor", 180),
            ("category", "Categoria", 120),
            ("availability", "Disponibles", 110),
            ("queue", "Reservas", 90),
        ):
            self.catalog_tree.heading(column, text=title)
            self.catalog_tree.column(column, width=width, anchor="w")
        self.catalog_tree.pack(fill="both", expand=True)
        self.catalog_tree.bind("<<TreeviewSelect>>", self._on_catalog_select)

    def _build_users_tab(self) -> None:
        toolbar = tk.Frame(self.user_tab, bg=self.colors["surface_alt"])
        toolbar.pack(fill="x", pady=(8, 10))

        self.user_filter_var = tk.StringVar()
        self.user_filter_entry = PlaceholderEntry(
            toolbar,
            placeholder="Buscar por ID, nombre o correo",
            textvariable=self.user_filter_var,
            font=("Segoe UI", 11),
            width=42,
        )
        self.user_filter_entry.pack(side="left", ipady=6)
        self.user_filter_entry.bind("<Return>", lambda _event: self.search_user(from_panel=True))

        tk.Button(
            toolbar,
            text="Buscar usuarios",
            command=lambda: self.search_user(from_panel=True),
            bg=self.colors["primary"],
            fg="white",
            relief="flat",
            padx=12,
            pady=6,
        ).pack(side="left", padx=10)

        cols = ("id", "name", "email", "loans")
        self.users_tree = ttk.Treeview(self.user_tab, columns=cols, show="headings", style="App.Treeview", height=16)
        for column, title, width in (
            ("id", "ID", 120),
            ("name", "Nombre", 220),
            ("email", "Correo", 240),
            ("loans", "Prestamos activos", 140),
        ):
            self.users_tree.heading(column, text=title)
            self.users_tree.column(column, width=width, anchor="w")
        self.users_tree.pack(fill="both", expand=True)
        self.users_tree.bind("<<TreeviewSelect>>", self._on_user_select)

    def _build_history_tab(self) -> None:
        self.history_list = tk.Listbox(
            self.history_tab,
            font=("Segoe UI", 11),
            bg=self.colors["surface"],
            fg=self.colors["text"],
            selectbackground="#f1d88a",
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.colors["border"],
        )
        self.history_list.pack(fill="both", expand=True, pady=(8, 0))

    def refresh_all_views(self) -> None:
        self.refresh_catalog()
        self.refresh_users()
        self.refresh_loans()
        self.refresh_history()
        self.refresh_sidebar()

    def refresh_catalog(self, books: list | None = None) -> None:
        self.catalog_tree.delete(*self.catalog_tree.get_children())
        books = self.system.books if books is None else books
        for book in books:
            self.catalog_tree.insert(
                "",
                "end",
                iid=book.isbn,
                values=(
                    book.isbn,
                    book.title,
                    book.author,
                    book.category,
                    f"{book.available_copies}/{book.total_copies}",
                    book.waitlist_size,
                ),
            )

    def refresh_users(self, users: list | None = None) -> None:
        self.users_tree.delete(*self.users_tree.get_children())
        users = self.system.users if users is None else users
        for user in users:
            self.users_tree.insert(
                "",
                "end",
                iid=user.user_id,
                values=(
                    user.user_id,
                    user.name,
                    user.email,
                    len(self.system.list_user_active_loans(user.user_id)),
                ),
            )

    def refresh_loans(self) -> None:
        self.loans_tree.delete(*self.loans_tree.get_children())
        if self.selected_user_id:
            loans = self.system.list_user_active_loans(self.selected_user_id)
            self.checkout_status.config(
                text="El usuario no tiene prestamos activos." if not loans else f"Prestamos activos del usuario: {len(loans)}"
            )
        else:
            loans = self.system.list_active_loans()
            self.checkout_status.config(text=f"Prestamos activos generales: {len(loans)}")

        for loan in loans:
            book = self.system.find_book_by_isbn(loan.book_isbn)
            title = book.title if book else "Libro no disponible"
            self.loans_tree.insert(
                "",
                "end",
                values=(loan.book_isbn, loan.user_id, loan.loan_date.isoformat(), title),
            )

    def refresh_history(self) -> None:
        self.history_list.delete(0, tk.END)
        for item in self.system.get_recent_history():
            self.history_list.insert(tk.END, item)

    def refresh_sidebar(self) -> None:
        if not self.selected_user_id:
            self.user_name_label.config(text="Sin usuario seleccionado")
            self.user_details_label.config(text="Busca por ID, nombre o correo para cargar el patron.")
            return

        user = self.system.find_user_by_id(self.selected_user_id)
        if user is None:
            self.selected_user_id = None
            self.refresh_sidebar()
            return

        loans = self.system.list_user_active_loans(user.user_id)
        details = [
            f"ID: {user.user_id}",
            f"Correo: {user.email}",
            "Categoria: Usuario activo",
            f"Prestamos activos: {len(loans)}",
        ]
        self.user_name_label.config(text=f"{user.name} ({user.user_id})")
        self.user_details_label.config(text="\n".join(details))

    def search_user(self, from_panel: bool = False) -> None:
        query = self.user_filter_entry.get_value() if from_panel else self.user_search_entry.get_value()
        if not query:
            self.refresh_users()
            return

        users = self.system.search_users(query)
        self.refresh_users(users)
        if not users:
            messagebox.showinfo("Busqueda de usuarios", "No se encontraron usuarios.")
            return

        first_user = users[0]
        self.selected_user_id = first_user.user_id
        self.refresh_sidebar()
        self.refresh_loans()
        self.users_tree.selection_set(first_user.user_id)
        self.users_tree.focus(first_user.user_id)
        self.notebook.select(self.user_tab if from_panel else self.loan_tab)

    def search_catalog(self) -> None:
        query = self.catalog_entry.get_value()
        books = self.system.search_books(query) if query else self.system.books
        self.refresh_catalog(books)
        self.notebook.select(self.catalog_tab)
        if not books:
            messagebox.showinfo("Catalogo", "No se encontraron libros.")

    def checkout_selected(self) -> None:
        if not self.selected_user_id:
            messagebox.showwarning("Prestamo", "Selecciona un usuario antes de registrar un prestamo.")
            return

        isbn = self.checkout_entry.get_value() or self.selected_book_isbn
        if not isbn:
            messagebox.showwarning("Prestamo", "Ingresa o selecciona un ISBN.")
            return

        message = self.system.lend_book(isbn, self.selected_user_id)
        self.checkout_var.set("")
        self.refresh_all_views()
        messagebox.showinfo("Prestamo", message)

    def return_selected(self) -> None:
        selected = self.loans_tree.selection()
        if not selected:
            messagebox.showwarning("Devolucion", "Selecciona un prestamo en la tabla.")
            return

        values = self.loans_tree.item(selected[0], "values")
        isbn, user_id = values[0], values[1]
        message = self.system.return_book(isbn, user_id)
        self.refresh_all_views()
        messagebox.showinfo("Devolucion", message)

    def open_register_user_dialog(self) -> None:
        dialog = _FormDialog(self, "Registrar usuario", ("ID", "Nombre", "Correo"))
        self.wait_window(dialog)
        if not dialog.result:
            return
        user_id, name, email = dialog.result
        message = self.system.register_user(user_id, name, email)
        self.refresh_all_views()
        messagebox.showinfo("Usuarios", message)

    def open_register_book_dialog(self) -> None:
        dialog = _FormDialog(self, "Registrar libro", ("ISBN", "Titulo", "Autor", "Categoria", "Ejemplares"))
        self.wait_window(dialog)
        if not dialog.result:
            return
        isbn, title, author, category, copies_raw = dialog.result
        if not copies_raw.isdigit():
            messagebox.showwarning("Catalogo", "Ejemplares debe ser un numero entero positivo.")
            return
        message = self.system.register_book(isbn, title, author, category, int(copies_raw))
        self.refresh_all_views()
        messagebox.showinfo("Catalogo", message)

    def _on_user_select(self, _event: object) -> None:
        selected = self.users_tree.selection()
        if not selected:
            return
        self.selected_user_id = selected[0]
        self.refresh_sidebar()
        self.refresh_loans()

    def _on_catalog_select(self, _event: object) -> None:
        selected = self.catalog_tree.selection()
        if not selected:
            return
        self.selected_book_isbn = selected[0]
        self.checkout_var.set(self.selected_book_isbn)


class _FormDialog(tk.Toplevel):
    def __init__(self, parent: tk.Misc, title: str, fields: tuple[str, ...]) -> None:
        super().__init__(parent)
        self.result: tuple[str, ...] | None = None

        self.title(title)
        self.configure(bg="#ffffff")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

        container = tk.Frame(self, bg="#ffffff", padx=18, pady=18)
        container.pack(fill="both", expand=True)

        self.entries: list[tk.Entry] = []
        for row, field in enumerate(fields):
            tk.Label(container, text=field, bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=row, column=0, sticky="w", pady=6)
            entry = tk.Entry(container, font=("Segoe UI", 11), width=36)
            entry.grid(row=row, column=1, pady=6, padx=(14, 0))
            self.entries.append(entry)

        buttons = tk.Frame(container, bg="#ffffff")
        buttons.grid(row=len(fields), column=0, columnspan=2, sticky="e", pady=(14, 0))

        tk.Button(buttons, text="Cancelar", command=self.destroy, relief="flat", padx=12, pady=6).pack(side="left", padx=6)
        tk.Button(
            buttons,
            text="Guardar",
            command=self._submit,
            bg="#d6a419",
            fg="white",
            relief="flat",
            padx=14,
            pady=6,
        ).pack(side="left")

        if self.entries:
            self.entries[0].focus_set()

    def _submit(self) -> None:
        values = tuple(entry.get().strip() for entry in self.entries)
        if any(not value for value in values):
            messagebox.showwarning("Formulario", "Todos los campos son obligatorios.", parent=self)
            return
        self.result = values
        self.destroy()


class PlaceholderEntry(tk.Entry):
    def __init__(self, master: tk.Misc, placeholder: str, textvariable: tk.StringVar, **kwargs) -> None:
        self.placeholder = placeholder
        self.textvariable = textvariable
        self.default_fg = kwargs.get("fg", "#1c1814")
        self.placeholder_fg = "#9f947b"
        super().__init__(master, textvariable=textvariable, **kwargs)

        self._showing_placeholder = False
        self.bind("<FocusIn>", self._handle_focus_in)
        self.bind("<FocusOut>", self._handle_focus_out)
        self._apply_placeholder_if_needed()

    def get_value(self) -> str:
        return "" if self._showing_placeholder else self.textvariable.get().strip()

    def _handle_focus_in(self, _event: object) -> None:
        if self._showing_placeholder:
            self._showing_placeholder = False
            self.textvariable.set("")
            self.config(fg=self.default_fg)

    def _handle_focus_out(self, _event: object) -> None:
        self._apply_placeholder_if_needed()

    def _apply_placeholder_if_needed(self) -> None:
        if self.textvariable.get().strip():
            self._showing_placeholder = False
            self.config(fg=self.default_fg)
            return
        self._showing_placeholder = True
        self.textvariable.set(self.placeholder)
        self.config(fg=self.placeholder_fg)

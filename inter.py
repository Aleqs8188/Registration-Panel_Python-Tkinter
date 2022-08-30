import tkinter as tk
from PIL import ImageTk, Image
import sqlite3
from tkinter import LEFT, ttk, PhotoImage
import tkinter.messagebox as mb

# from requests import head

# --------------------------------------------------------------------------------------------------------
try:  # connect with sqlite3
    with sqlite3.connect("bzdz.db") as db:
        cursor = db.cursor()
    if cursor.execute("SELECT * FROM nameSurname,pocztaPasswordNumer,peoples"):
        print("")
    else:
        print("")
    print("succesfully connected...")
    print("#" * 20)

except:  # if Error
    cursor.execute(
        """CREATE TABLE "nameSurname" ( "id" INTEGER, "name" text NOT NULL, "surname" text NOT NULL, PRIMARY KEY("id"));"""
    )
    cursor.execute(
        """CREATE TABLE "pocztaPasswordNumer" ( "id" INTEGER, "poczta"	text NOT NULL, "password"	text NOT NULL, "numer"	integer, PRIMARY KEY("id"));"""
    )
    cursor.execute(
        """CREATE TABLE "peoples" ( "id" INTEGER, "name" text NOT NULL, "surname" text NOT NULL, "poczta" text NOT NULL, "password" text NOT NULL, "numer"	integer, PRIMARY KEY("id"));"""
    )
    print("Таблицы созданы")
    # mb.showerror("Error...", ex)


# --------------------------------------------------------------------------------------------------------
def save_to_bd():
    if var.get() == 1:  # dla podtwiedzenia / prowerka na flag
        value = name.get()
        value1 = familia.get()
        value2 = poczta.get()
        value3 = password.get()
        value4 = str(combo_numer.get()) + " " + str(numer.get())
        cursor.execute(
            """INSERT OR IGNORE INTO nameSurname(name, surname) VALUES(?, ?)""",
            (value, value1),
        )
        cursor.execute(
            """INSERT OR IGNORE INTO pocztaPasswordNumer(poczta, password, numer) VALUES(?, ?, ?)""",
            (value2, value3, value4),
        )
        cursor.execute(
            """INSERT OR IGNORE INTO peoples(name, surname, poczta, password, numer) VALUES(?, ?, ?, ?, ?)""",
            (value, value1, value2, value3, value4),
        )
        db.commit()
        delete()
    else:  # okno s Error...
        msg = "Podtwiedz 'Apply \"Add\"'"
        mb.showerror("Podtwiedzenie", msg)
        print("Ooops...")


# --------------------------------------------------------------------------------------------------------
def createWindowToLogin(root):  # new window to login
    loginWindow = tk.Toplevel(root)

    frameCnt = 12
    frames = [
        PhotoImage(file="2.gif", format="gif -index %i" % (i)) for i in range(frameCnt)
    ]

    def update(ind):
        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        label.configure(image=frame)
        loginWindow.after(100, update, ind)

    label = tk.Label(loginWindow)
    label.pack()
    loginWindow.after(0, update, 0)
    loginWindow.config(bg="black")
    photo1 = tk.PhotoImage(file="adminico.png")  # iconka
    loginWindow.iconphoto(False, photo1)
    loginWindow.geometry(f"300x200+550+250")  # rozmiar
    loginWindow.title("Admin login")
    loginWindow.resizable(False, False)
    # --------------------------------------------------------------------------------------------------------
    admin = tk.Label(
        loginWindow,
        text="login: admin",
        fg="red",
        bg="black",
        bd=2,
        font=("Arial", 10, "bold"),
    )
    admin.place(x=10, y=140)
    admin = tk.Label(
        loginWindow,
        text="Password: admin",
        fg="red",
        bg="black",
        bd=2,
        font=("Arial", 10, "bold"),
    )
    admin.place(x=10, y=160)
    log = tk.Label(
        loginWindow,
        text="Login:",
        bg="black",
        bd=2,
        fg="white",
        font=("Arial", 10, "bold"),
    )
    log.place(x=2, y=40)
    pasw = tk.Label(
        loginWindow,
        text="Password:",
        bg="black",
        bd=2,
        fg="White",
        font=("Arial", 10, "bold"),
    )
    pasw.place(x=2, y=70)

    log = tk.Entry(loginWindow, bd=2)
    log.place(x=80, y=40)
    pasw = tk.Entry(loginWindow, show="*", bd=2)
    pasw.place(x=80, y=70)

    def clicked():
        username = log.get()
        password1 = pasw.get()
        if username == "admin" and password1 == "admin":
            panel = tk.Toplevel()

            def on_close():
                response = mb.askyesno("Exit", "Are you sure you want to exit?")
                if response:
                    panel.destroy()
                    loginWindow.destroy()

            panel.protocol("WM_DELETE_WINDOW", on_close)
            # ----------------------------------------------------------------------------
            # scrollbar = tk.Scrollbar(panel)
            # scrollbar.pack(side="right", fill="y")
            frameCnt = 12
            frames = [
                PhotoImage(file="kosmo.gif", format="gif -index %i" % (i))
                for i in range(frameCnt)
            ]

            def update(ind):
                frame = frames[ind]
                ind += 1
                if ind == frameCnt:
                    ind = 0
                label.configure(image=frame)
                panel.after(100, update, ind)

            # -----------------------------------
            def newPocztaTable():
                pocztaPanel = tk.Toplevel()

                class pocztaTable(tk.Frame):
                    # mb.showinfo('Good',"Succesfully Enter...")
                    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
                        super().__init__(parent)
                        table = ttk.Treeview(self, show="headings", selectmode="browse")
                        table["columns"] = headings
                        table["displaycolumns"] = headings
                        for head in headings:
                            table.heading(head, text=head, anchor=tk.CENTER)
                            table.column(head, anchor=tk.CENTER)
                        for row in rows:
                            table.insert("", tk.END, values=tuple(row))
                        scrolltable = tk.Scrollbar(self, command=table.yview)
                        table.configure(yscrollcommand=scrolltable.set)
                        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
                        table.pack(expand=tk.YES, fill=tk.BOTH)

                data = ()
                cursor.execute("SELECT * FROM pocztaPasswordNumer")
                data = (row for row in cursor.fetchall())
                table = pocztaTable(
                    pocztaPanel,
                    headings=("id", "E-mail", "Password", "Number"),
                    rows=data,
                )
                table.pack(expand=tk.YES, fill=tk.BOTH)
                pocztaPanel.title("Panel poczty/hasła/numera")
                photo1 = tk.PhotoImage(file="i.png")  # iconka
                pocztaPanel.iconphoto(False, photo1)

                loginWindow.destroy()

            def newNamesTable():
                namesPanel = tk.Toplevel()

                class namesTable(tk.Frame):
                    # mb.showinfo('Good',"Succesfully Enter...")
                    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
                        super().__init__(parent)
                        table = ttk.Treeview(self, show="headings", selectmode="browse")
                        table["columns"] = headings
                        table["displaycolumns"] = headings
                        for head in headings:
                            table.heading(head, text=head, anchor=tk.CENTER)
                            table.column(head, anchor=tk.CENTER)
                        for row in rows:
                            table.insert("", tk.END, values=tuple(row))
                        scrolltable = tk.Scrollbar(self, command=table.yview)
                        table.configure(yscrollcommand=scrolltable.set)
                        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
                        table.pack(expand=tk.YES, fill=tk.BOTH)

                data = ()
                cursor.execute("SELECT * FROM nameSurname")
                data = (row for row in cursor.fetchall())
                table = namesTable(
                    namesPanel, headings=("id", "Name", "Surname"), rows=data
                )
                table.pack(expand=tk.YES, fill=tk.BOTH)
                namesPanel.title("Panel with names/surnames")
                photo1 = tk.PhotoImage(file="i.png")  # iconka
                namesPanel.iconphoto(False, photo1)
                loginWindow.destroy()

            def peopleTable():

                peoplePanel = tk.Toplevel()

                class peopleTable(tk.Frame):
                    # mb.showinfo('Good',"Succesfully Enter...")
                    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
                        super().__init__(parent)

                        self.tree = ttk.Treeview(
                            peoplePanel, show="headings", selectmode="browse"
                        )

                        self.entry_search_id = tk.Entry(self, bd=5, width=20)
                        self.entry_search_id.pack()

                        delbtn = tk.Button(
                            self,
                            text="Delete chosed column",
                            command=self.del_acc,
                            fg="white",
                            bg="#8B0000",
                            bd=5,
                            font=("Arial", 9, "bold"),
                            activebackground="red",
                            width=25,
                            height=1,
                        )
                        delbtn.place(x=920, y=5)

                        tk.Label(
                            self,
                            text="Enter what are you want and search by buttons...",
                            bd=3,
                            bg="Yellow",
                            fg="black",
                            font=(
                                "Arial",
                                11,
                            ),
                        ).place(x=190, y=2)
                        searchButton = tk.Button(
                            self,
                            text="Search by ID",
                            command=self.search_id,
                            fg="white",
                            bg="#8B0000",
                            bd=5,
                            font=("Arial", 9, "bold"),
                            activebackground="red",
                            width=15,
                            height=1,
                        )
                        searchButton.bind(
                            "<Button-1>",
                            lambda event: self.search_id(self.entry_search_id.get()),
                        )
                        searchButton.pack(side=LEFT)

                        searchButton = tk.Button(
                            self,
                            text="Search by Name",
                            command=self.search_name,
                            fg="white",
                            bg="#8B0000",
                            bd=5,
                            font=("Arial", 9, "bold"),
                            activebackground="red",
                            width=15,
                            height=1,
                        )
                        searchButton.bind(
                            "<Button-1>",
                            lambda event: self.search_name(self.entry_search_id.get()),
                        )
                        searchButton.pack(side=LEFT)

                        searchButton = tk.Button(
                            self,
                            text="Search by Surname",
                            command=self.search_surname,
                            fg="white",
                            bg="#8B0000",
                            bd=5,
                            font=("Arial", 9, "bold"),
                            activebackground="red",
                            width=20,
                            height=1,
                        )
                        searchButton.bind(
                            "<Button-1>",
                            lambda event: self.search_surname(
                                self.entry_search_id.get()
                            ),
                        )
                        searchButton.pack(side=LEFT)

                        searchButton = tk.Button(
                            self,
                            text="Search by E-mail",
                            command=self.search_poczta,
                            fg="white",
                            bg="#8B0000",
                            bd=5,
                            font=("Arial", 9, "bold"),
                            activebackground="red",
                            width=15,
                            height=1,
                        )
                        searchButton.bind(
                            "<Button-1>",
                            lambda event: self.search_poczta(
                                self.entry_search_id.get()
                            ),
                        )
                        searchButton.pack(side=LEFT)

                        searchButton = tk.Button(
                            self,
                            text="Search by Password",
                            command=self.search_password,
                            fg="white",
                            bg="#8B0000",
                            bd=5,
                            font=("Arial", 9, "bold"),
                            activebackground="red",
                            width=20,
                            height=1,
                        )
                        searchButton.bind(
                            "<Button-1>",
                            lambda event: self.search_password(
                                self.entry_search_id.get()
                            ),
                        )
                        searchButton.pack(side=LEFT)

                        searchButton = tk.Button(
                            self,
                            text="Search by Number phone",
                            command=self.search_number,
                            fg="white",
                            bg="#8B0000",
                            bd=5,
                            font=("Arial", 9, "bold"),
                            activebackground="red",
                            width=20,
                            height=1,
                        )
                        searchButton.bind(
                            "<Button-1>",
                            lambda event: self.search_number(
                                self.entry_search_id.get()
                            ),
                        )
                        searchButton.pack(side=LEFT)

                        self.tree["columns"] = headings
                        self.tree["displaycolumns"] = headings
                        for head in headings:
                            self.tree.heading(head, text=head, anchor=tk.CENTER)
                            self.tree.column(head, anchor=tk.CENTER)
                        for row in rows:
                            self.tree.insert("", tk.END, values=tuple(row))
                        scrolltable = tk.Scrollbar(peoplePanel, command=self.tree.yview)
                        self.tree.configure(yscrollcommand=scrolltable.set)
                        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
                        self.tree.pack(expand=tk.YES, fill=tk.BOTH)

                    def search_id(self, id):
                        id = ("%" + id + "%",)
                        cursor.execute("""SELECT * FROM peoples WHERE id LIKE ?""", id)
                        [self.tree.delete(i) for i in self.tree.get_children()]
                        [
                            self.tree.insert("", "end", values=row)
                            for row in cursor.fetchall()
                        ]

                    def search_name(self, imie):
                        imie = ("%" + imie + "%",)
                        cursor.execute(
                            """SELECT * FROM peoples WHERE name LIKE ?""", imie
                        )
                        [self.tree.delete(i) for i in self.tree.get_children()]
                        [
                            self.tree.insert("", "end", values=row)
                            for row in cursor.fetchall()
                        ]

                    def search_surname(self, surname):
                        surname = ("%" + surname + "%",)
                        cursor.execute(
                            """SELECT * FROM peoples WHERE surname LIKE ?""", surname
                        )
                        [self.tree.delete(i) for i in self.tree.get_children()]
                        [
                            self.tree.insert("", "end", values=row)
                            for row in cursor.fetchall()
                        ]

                    def search_poczta(self, poczta):
                        poczta = ("%" + poczta + "%",)
                        cursor.execute(
                            """SELECT * FROM peoples WHERE poczta LIKE ?""", poczta
                        )
                        [self.tree.delete(i) for i in self.tree.get_children()]
                        [
                            self.tree.insert("", "end", values=row)
                            for row in cursor.fetchall()
                        ]

                    def search_password(self, password):
                        password = ("%" + password + "%",)
                        cursor.execute(
                            """SELECT * FROM peoples WHERE password LIKE ?""", password
                        )
                        [self.tree.delete(i) for i in self.tree.get_children()]
                        [
                            self.tree.insert("", "end", values=row)
                            for row in cursor.fetchall()
                        ]

                    def search_number(self, number):
                        number = ("%" + number + "%",)
                        cursor.execute(
                            """SELECT * FROM peoples WHERE numer LIKE ?""", number
                        )
                        [self.tree.delete(i) for i in self.tree.get_children()]
                        [
                            self.tree.insert("", "end", values=row)
                            for row in cursor.fetchall()
                        ]

                    def del_acc(self):
                        pk = self.tree.set(self.tree.selection()[0], ["id"])
                        cursor.execute("DELETE FROM peoples WHERE id=?", (pk,))
                        cursor.execute("DELETE FROM nameSurname WHERE id=?", (pk,))
                        cursor.execute(
                            "DELETE FROM pocztaPasswordNumer WHERE id=?", (pk,)
                        )
                        db.commit()
                        self.view_records()

                    def view_records(self):
                        cursor.execute("SELECT * FROM peoples")
                        [self.tree.delete(i) for i in self.tree.get_children()]
                        [
                            self.tree.insert("", "end", values=row)
                            for row in cursor.fetchall()
                        ]

                data = ()
                cursor.execute("SELECT * FROM peoples")
                data = (row for row in cursor.fetchall())
                peopleTable(
                    peoplePanel,
                    headings=("id", "Name", "Surname", "E-mail", "Password", "Number"),
                    rows=data,
                ).pack(expand=tk.YES, fill=tk.BOTH)
                peoplePanel.title("Panel wszystkich tablic")
                peoplePanel.geometry("1200x550")
                photo1 = tk.PhotoImage(file="i.png")  # iconka
                peoplePanel.iconphoto(False, photo1)

                loginWindow.destroy()

            def nameTable():
                namePanel = tk.Toplevel()

                class namesTable(tk.Frame):
                    # mb.showinfo('Good',"Succesfully Enter...")
                    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
                        super().__init__(parent)
                        table = ttk.Treeview(self, show="headings", selectmode="browse")
                        table["columns"] = headings
                        table["displaycolumns"] = headings
                        for head in headings:
                            table.heading(head, text=head, anchor=tk.CENTER)
                            table.column(head, anchor=tk.CENTER)
                        for row in rows:
                            table.insert("", tk.END, values=tuple(row))
                        scrolltable = tk.Scrollbar(self, command=table.yview)
                        table.configure(yscrollcommand=scrolltable.set)
                        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
                        table.pack(expand=tk.YES, fill=tk.BOTH)

                data = ()
                cursor.execute("SELECT id,name FROM peoples")
                data = (row for row in cursor.fetchall())
                table = namesTable(namePanel, headings=("id", "Name"), rows=data)
                table.pack(expand=tk.YES, fill=tk.BOTH)
                namePanel.title("Panel with names")
                photo1 = tk.PhotoImage(file="i.png")  # iconka
                namePanel.iconphoto(False, photo1)
                loginWindow.destroy()

            def surNameTable():
                surnamePanel = tk.Toplevel()

                class surNamesTable(tk.Frame):
                    # mb.showinfo('Good',"Succesfully Enter...")
                    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
                        super().__init__(parent)
                        table = ttk.Treeview(self, show="headings", selectmode="browse")
                        table["columns"] = headings
                        table["displaycolumns"] = headings
                        for head in headings:
                            table.heading(head, text=head, anchor=tk.CENTER)
                            table.column(head, anchor=tk.CENTER)
                        for row in rows:
                            table.insert("", tk.END, values=tuple(row))
                        scrolltable = tk.Scrollbar(self, command=table.yview)
                        table.configure(yscrollcommand=scrolltable.set)
                        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
                        table.pack(expand=tk.YES, fill=tk.BOTH)

                data = ()
                cursor.execute("SELECT id,surname FROM peoples")
                data = (row for row in cursor.fetchall())
                table = surNamesTable(
                    surnamePanel, headings=("id", "Surname"), rows=data
                )
                table.pack(expand=tk.YES, fill=tk.BOTH)
                surnamePanel.title("Panel with surnames")
                photo1 = tk.PhotoImage(file="i.png")  # iconka
                surnamePanel.iconphoto(False, photo1)
                loginWindow.destroy()

            def emailTable():
                emailPanel = tk.Toplevel()

                class emailesTable(tk.Frame):
                    # mb.showinfo('Good',"Succesfully Enter...")
                    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
                        super().__init__(parent)
                        table = ttk.Treeview(self, show="headings", selectmode="browse")
                        table["columns"] = headings
                        table["displaycolumns"] = headings
                        for head in headings:
                            table.heading(head, text=head, anchor=tk.CENTER)
                            table.column(head, anchor=tk.CENTER)
                        for row in rows:
                            table.insert("", tk.END, values=tuple(row))
                        scrolltable = tk.Scrollbar(self, command=table.yview)
                        table.configure(yscrollcommand=scrolltable.set)
                        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
                        table.pack(expand=tk.YES, fill=tk.BOTH)

                data = ()
                cursor.execute("SELECT id,poczta FROM peoples")
                data = (row for row in cursor.fetchall())
                table = emailesTable(emailPanel, headings=("id", "E-mail"), rows=data)
                table.pack(expand=tk.YES, fill=tk.BOTH)
                emailPanel.title("Panel with E-mails")
                photo1 = tk.PhotoImage(file="i.png")  # iconka
                emailPanel.iconphoto(False, photo1)
                loginWindow.destroy()

            def passwordTable():
                passwordPanel = tk.Toplevel()

                class passwordsTable(tk.Frame):
                    # mb.showinfo('Good',"Succesfully Enter...")
                    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
                        super().__init__(parent)
                        table = ttk.Treeview(self, show="headings", selectmode="browse")
                        table["columns"] = headings
                        table["displaycolumns"] = headings
                        for head in headings:
                            table.heading(head, text=head, anchor=tk.CENTER)
                            table.column(head, anchor=tk.CENTER)
                        for row in rows:
                            table.insert("", tk.END, values=tuple(row))
                        scrolltable = tk.Scrollbar(self, command=table.yview)
                        table.configure(yscrollcommand=scrolltable.set)
                        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
                        table.pack(expand=tk.YES, fill=tk.BOTH)

                data = ()
                cursor.execute("SELECT id,password FROM peoples")
                data = (row for row in cursor.fetchall())
                table = passwordsTable(
                    passwordPanel, headings=("id", "Password"), rows=data
                )
                table.pack(expand=tk.YES, fill=tk.BOTH)
                passwordPanel.title("Panel with passwords")
                photo1 = tk.PhotoImage(file="i.png")  # iconka
                passwordPanel.iconphoto(False, photo1)
                loginWindow.destroy()

            def numberTable():
                numberPanel = tk.Toplevel()

                class numbersTable(tk.Frame):
                    # mb.showinfo('Good',"Succesfully Enter...")
                    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
                        super().__init__(parent)
                        table = ttk.Treeview(self, show="headings", selectmode="browse")
                        table["columns"] = headings
                        table["displaycolumns"] = headings
                        for head in headings:
                            table.heading(head, text=head, anchor=tk.CENTER)
                            table.column(head, anchor=tk.CENTER)
                        for row in rows:
                            table.insert("", tk.END, values=tuple(row))
                        scrolltable = tk.Scrollbar(self, command=table.yview)
                        table.configure(yscrollcommand=scrolltable.set)
                        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
                        table.pack(expand=tk.YES, fill=tk.BOTH)

                data = ()
                cursor.execute("SELECT id,numer FROM peoples")
                data = (row for row in cursor.fetchall())
                table = numbersTable(numberPanel, headings=("id", "Number"), rows=data)
                table.pack(expand=tk.YES, fill=tk.BOTH)
                numberPanel.title("Panel wszystkich tablic")
                photo1 = tk.PhotoImage(file="i.png")  # iconka
                numberPanel.iconphoto(False, photo1)
                loginWindow.destroy()

            label = tk.Label(panel)
            label.pack()
            panel.after(0, update, 0)
            panel.config(bg="black")
            photo1 = tk.PhotoImage(file="adminico.png")  # iconka
            panel.iconphoto(False, photo1)
            panel.geometry(f"300x300+550+200")  # rozmiar
            panel.title("Select Table")
            panel.resizable(False, False)

            newtable = tk.Button(
                panel,
                text="📥Open table with names",
                command=lambda: nameTable(),
                bg="black",
                fg="white",
                bd=2,
                activebackground="red",
            )
            newtable.place(x=1, y=15)
            newtable = tk.Button(
                panel,
                text="📥Open table with surnames",
                command=lambda: surNameTable(),
                bg="black",
                fg="white",
                bd=2,
                activebackground="red",
            )
            newtable.place(x=1, y=50)
            newtable = tk.Button(
                panel,
                text="📥Open table with e-mails",
                command=lambda: emailTable(),
                bg="black",
                fg="white",
                bd=2,
                activebackground="red",
            )
            newtable.place(x=1, y=85)
            newtable = tk.Button(
                panel,
                text="📥Open table with passwords",
                command=lambda: passwordTable(),
                bg="black",
                fg="white",
                bd=2,
                activebackground="red",
            )
            newtable.place(x=1, y=120)
            newtable = tk.Button(
                panel,
                text="📥Open table with numbers",
                command=lambda: numberTable(),
                bg="black",
                fg="white",
                bd=2,
                activebackground="red",
            )
            newtable.place(x=1, y=155)
            newtable = tk.Button(
                panel,
                text="📥Open table with names/surnames",
                command=lambda: newNamesTable(),
                bg="black",
                fg="white",
                bd=2,
                activebackground="red",
            )
            newtable.place(x=1, y=190)
            newtable = tk.Button(
                panel,
                text="📥Open table with e-mails/passwords/numbers",
                command=lambda: newPocztaTable(),
                bg="black",
                fg="white",
                bd=2,
                activebackground="red",
            )
            newtable.place(x=1, y=225)
            newtable = tk.Button(
                panel,
                text="📥Open all tables with searching...",
                command=lambda: peopleTable(),
                bg="black",
                fg="red",
                bd=2,
                activebackground="red",
            )
            newtable.place(x=1, y=260)
        else:
            mb.showerror("Error...", "Not correct login/password")
            createWindowToLogin(root)

    enter = tk.Button(
        loginWindow,
        command=lambda: clicked(),
        bg="black",
        fg="white",
        text="Enter",
        bd=2,
        activebackground="red",
        width=10,
    )
    enter.place(x=105, y=100)


# --------------------------------------------------------------------------------------------------------
root = tk.Tk()
frameCnt = 12
frames = [
    PhotoImage(file="2.gif", format="gif -index %i" % (i)) for i in range(frameCnt)
]


def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(100, update, ind)


label = tk.Label(root)
label.pack()
root.after(0, update, 0)
# canvas = tk.Canvas(root, width=500, height=400)
# image = ImageTk.PhotoImage(Image.open('Fun.png'))
# canvas.create_image(0, 0, anchor=tk.NW, image=image)
# canvas.pack()
# --------------------------------------------------------------------------------------------------------
all = 0
all1 = tk.END


def delete_name_entry():
    name.delete(all, all1)


def delete_familia_entry():
    familia.delete(all, all1)


def delete_poczta_entry():
    poczta.delete(all, all1)


def delete_password_entry():
    password.delete(all, all1)


def delete_numer_entry():
    numer.delete(all, all1)


def delete():  # clear pola
    name.delete(all, all1)
    familia.delete(all, all1)
    poczta.delete(all, all1)
    password.delete(all, all1)
    numer.delete(all, all1)


# --------------------------------------------------------------------------------------------------------
def submit():  # hide/show password
    if password.cget("show") == "":
        password.config(show="*"), sub.config(text="Show")
    else:
        password.config(show=""), sub.config(text="Hide")


# --------------------------------------------------------------------------------------------------------
root.config(bg="grey")  # Fon
photo = tk.PhotoImage(file="Fun.png")  # iconka
root.iconphoto(False, photo)
root.title("Registration programe by Oleksii Bulhak")  # title
root.geometry(f"500x400+450+150")  # rozmiar
root.resizable(False, False)
# --------------------------------------------------------------------------------------------------------
tk.Label(
    root,
    text="✔Registration Panel",
    bg="#1a162a",
    bd=2,
    fg="White",
    font=("Arial", 16, "bold"),
    padx=1,
    pady=1,
).place(
    x=150, y=1
)  # Nadpis Hello
tk.Label(
    root, text="Name:", bg="#1a162a", bd=2, fg="white", font=("Arial", 10, "bold")
).place(x=2, y=70)
tk.Label(
    root, text="Surname:", bg="#1a162a", bd=2, fg="white", font=("Arial", 10, "bold")
).place(x=2, y=110)
tk.Label(
    root, text="E-mail:", bg="#1a162a", bd=2, fg="white", font=("Arial", 10, "bold")
).place(x=2, y=150)
tk.Label(
    root, text="Password:", bg="#1a162a", fg="white", bd=2, font=("Arial", 10, "bold")
).place(x=2, y=190)
tk.Label(
    root, text="Number:", bg="#1a162a", fg="white", bd=2, font=("Arial", 10, "bold")
).place(x=2, y=230)
# --------------------------------------------------------------------------------------------------------
name = tk.Entry(root, bd=2)
name.place(x=90, y=70)  # Wwod imeni
familia = tk.Entry(root, bd=2)
familia.place(x=90, y=110)  # Wwod familii
poczta = tk.Entry(root, bd=2)
poczta.place(x=90, y=150)  # Wwod poczty
password = tk.Entry(root, show="*", bd=2)
password.place(x=90, y=190)  # Wwod parola
numer = tk.Entry(
    root,
    bd=2,
    width=12,
)
numer.place(x=140, y=230)  # Wwod parola
# --------------------------------------------------------------------------------------------------------
delete1 = tk.Button(
    root,
    text="Clear",
    command=delete_name_entry,
    fg="white",
    bg="#8B0000",
    bd=5,
    font=("Arial", 9, "bold"),
    activebackground="blue",
    width=7,
    height=1,
)
delete1.place(x=240, y=65)  # Clear imie
delete2 = tk.Button(
    root,
    text="Clear",
    command=delete_familia_entry,
    fg="white",
    bg="#8B0000",
    bd=5,
    font=("Arial", 9, "bold"),
    activebackground="blue",
    width=7,
    height=1,
)
delete2.place(x=240, y=105)  # Clear Nazwisko
delete3 = tk.Button(
    root,
    text="Clear",
    command=delete_poczta_entry,
    fg="white",
    bg="#8B0000",
    bd=5,
    font=("Arial", 9, "bold"),
    activebackground="blue",
    width=7,
    height=1,
)
delete3.place(x=240, y=145)  # Clear Poczta
delete4 = tk.Button(
    root,
    text="Clear",
    command=delete_password_entry,
    fg="white",
    bg="#8B0000",
    bd=5,
    font=("Arial", 9, "bold"),
    activebackground="blue",
    width=7,
    height=1,
)
delete4.place(x=240, y=185)  # Clear Parol
delete5 = tk.Button(
    root,
    text="Clear",
    command=delete_numer_entry,
    fg="white",
    bg="#8B0000",
    bd=5,
    font=("Arial", 9, "bold"),
    activebackground="blue",
    width=7,
    height=1,
)
delete5.place(x=240, y=225)  # Clear numer
sub = tk.Button(
    root,
    text="Submit",
    command=submit,
    bd=5,
    bg="#DAA520",
    font=("Arial", 9, "bold"),
    activebackground="blue",
    width=7,
    height=1,
)
sub.place(x=330, y=185)  # Pokaz Parola
addbzd = tk.Button(
    root,
    text="Add",
    fg="white",
    bd=2,
    bg="#1a162a",
    command=save_to_bd,
    font=("Arial", 10, "bold"),
    activebackground="blue",
    width=15,
    height=1,
)
addbzd.place(x=190, y=349)  # dobawlenie w Bazu

buttonExample = tk.Button(
    root,
    text="Admin Panel",
    activebackground="black",
    font=("Arial", 10, "bold"),
    fg="red",
    bd=2,
    bg="#1a162a",
    command=lambda: createWindowToLogin(root),
    width=12,
    height=1,
)
buttonExample.place(x=360, y=348)  # dla wchoda
# --------------------------------------------------------------------------------------------------------
combo_numer = ttk.Combobox(root, values=["+48", "+380"], width=4, state="disabled")
combo_numer.current(0)
combo_numer.place(x=94, y=230)  # skrol numerow
# --------------------------------------------------------------------------------------------------------
var = tk.IntVar()
chkBtn = tk.Checkbutton(
    root,
    text='Apply "Add"',
    fg="green",
    bg="#1a162a",
    bd=2,
    activebackground="yellow",
    variable=var,
    onvalue=1,
    offvalue=0,
    font=("Arial", 10, "bold"),
    width=10,
    height=1,
)
chkBtn.place(x=50, y=350)  # podtwierdzenie
# --------------------------------------------------------------------------------------------------------
root.mainloop()

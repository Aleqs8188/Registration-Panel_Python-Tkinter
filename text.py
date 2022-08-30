#import sqlite3
#import tkinter as tk
#import tkinter.ttk as ttk
#
#
#class Table(tk.Frame):
#   def __init__(self, parent=None, headings=tuple(), rows=tuple()):
#      super().__init__(parent)
#
#      table = ttk.Treeview(self, show="headings", selectmode="browse")
#      table["columns"] = headings
#      table["displaycolumns"] = headings
#
#      for head in headings:
#         table.heading(head, text=head, anchor=tk.CENTER)
#         table.column(head, anchor=tk.CENTER)
#
#      for row in rows:
#         table.insert('', tk.END, values=tuple(row))
#
#      scrolltable = tk.Scrollbar(self, command=table.yview)
#      table.configure(yscrollcommand=scrolltable.set)
#      scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
#      table.pack(expand=tk.YES, fill=tk.BOTH)
#
#
#data = ()
#with sqlite3.connect('test.db') as connection:
#   cursor = connection.cursor()
#   
#   cursor.execute("""CREATE TABLE IF NOT EXISTS people(name text NOT NULL, surname text NOT NULL, poczta text NOT NULL, password text NOT NULL, numer integer);""") 
#   
#   cursor.execute("""INSERT OR IGNORE INTO people(name, surname, poczta, password, numer) VALUES(?, ?, ?, ?, ?)""",('Oleg', 'value1', 'value2', 'value3', 22222))
#   cursor.execute("SELECT * FROM people")
#   data = (row for row in cursor.fetchall())
#
#root = tk.Tk()
#table = Table(root, headings=('Фамилия', 'Имя', 'Отчество'), rows=data)
#table.pack(expand=tk.YES, fill=tk.BOTH)
#root.mainloop()
#
#def view():
#               conn=sqlite3.connect("bzdz.db")
#               cur=conn.cursor()
#               cur.execute("SELECT * FROM peoples")
#               rows=cur.fetchall()
#               conn.close()
#               return rows
#            def delete_many(id_list):
#               placeholders = ', '.join('?'*len(id_list))
#               sql = f"DELETE FROM peoples WHERE id IN ({placeholders})"
#               print(sql, id_list)
#            
#            
#            def delete_records():
#               if selected_id_list:
#                  delete_many(selected_id_list)
#                  for item in list1.curselection()[::-1]:
#                     list1.delete(item)
#            
#            def get_selectd_row(event):
#               global selected_id_list
#               selected_id_list = [list1.get(index)[0] for index in list1.curselection()]
#               print(selected_id_list)
#            list1 = tk.Listbox(peoplePanel, width=100,height=100, selectmode=tk.EXTENDED)
#            list1.grid(row=5,column=0,rowspan=7,columnspan=2)
#            list1.bind("<<ListboxSelect>>", get_selectd_row)                                   #Setup listbox location
#            
#            sb1=tk.Scrollbar(peoplePanel)                               #Create a vertical scrollbar for the listbox
#            sb1.grid(row=6,column=2,rowspan=4,sticky="NS")      #Setup the scrollbar's location and size - extends from top to bottom
#            
#            list1.configure(yscrollcommand=sb1.set)             #Attach the vertical scrollbar to the listbox
#            sb1.configure(command=list1.yview)                  #Setup scrollbar for vertical scrolling
#
#            sb2=tk.Scrollbar(peoplePanel, orient='horizontal')          #Create a horizontal scrollbar for the listbox
#            sb2.grid(row=11,column=0,columnspan=2,sticky="WE")  #Setup the scrollbar's location and size - extends from left to right
#
#            list1.configure(xscrollcommand=sb2.set)             #Attach the horizontal scrollbar to the listbox
#            sb2.configure(command=list1.xview)
#            data = ()
#            cursor.execute("SELECT * FROM peoples")
#            data = (row for row in cursor.fetchall())
#            for data in range(0, tk.END):
#               list1.insert(data)                  #Setup scrollbar for horizontal scrolling
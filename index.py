"""
	PRACTICA GUIADA
Autor: Codaya007
"""
from tkinter import*
import tkinter.ttk as ttk
import sqlite3
from tkinter import messagebox

global lista_de_registros
lista_de_registros = []
#--------------------------FUNCIONES PARA COMBOBOX---------------------------------------
def listar_registros():
	conexion = sqlite3.connect("Usuarios")
	cursor = conexion.cursor()
	try:
		cursor.execute("SELECT ID FROM USUARIOS")
		registros = cursor.fetchall()
		lista_de_registros.clear() #Vaciando la lista para q no se repitan los valores
		for i in registros:
			lista_de_registros.append(str(i[0]))		
		lista_desp["values"] = lista_de_registros
		
	except sqlite3.OperationalError:
		lista_desp["values"] = ["No hay registros"]

	cursor.close()

#-------------------CONSTRUYENDO LAS FUNCIONES DEL MENU CRUD-------------------------------
#SUBMENU 1
def crear_bbdd():
	conexion = sqlite3.connect("Usuarios")
	cursor = conexion.cursor()
	
	try:
		cursor.execute('''
			CREATE TABLE USUARIOS 
			(ID INTEGER PRIMARY KEY AUTOINCREMENT,
			NOMBRE VARCHAR(25) NOT NULL, APELLIDO VARCHAR(25), 
			PASSWORD VARCHAR(25) NOT NULL, DIRECCION VARCHAR(25),
			COMENTARIO VARCHAR(50))''')
		messagebox.showinfo("BBDD", "¡La Base de datos ha sido creada exitosamente!")
		borrar_campos()
	except:
		messagebox.showwarning("BBDD", "¡Ya se ha creado la BBDD!")

def salir(root):
	salir = messagebox.askquestion("Salir", "¿Desea salir de la apliación?")
	if salir == "yes":
		root.destroy()

#SUBMENU 2......................................
def borrar_campos():
	ID.set("")
	nombre.set("")
	apellido.set("")
	password.set("")
	direccion.set("")
	textoComentario.delete(0.1, END) #Para setear un text y dejar el cursor al incio (I guess)

#SUBMENU 3......................................
#CONSULTAS PARAMETRIZADAS -> Revisar para mejorar la funcion crear_registro(), en el curso de PHP/MySQL del video 47 al 53 de pildorasinformaticas

def crear_registro():
	conexion = sqlite3.connect("Usuarios")
	cursor = conexion.cursor()
	
	try:
		if(nombre.get().lstrip() != "" and password.get().lstrip() != ""):
			
			#CONSULTO LA INSTRUCCION PARA REEMPLAZARLA POR UNA CONSULTA PARAMETRIZADA QUE ES MAS SEGURA Y PREVIENE SQL INJECTIONS
			# cursor.execute("INSERT INTO USUARIOS VALUES(NULL ,'"+ (nombre.get()).strip() + "','" + (apellido.get()).strip() + "','"+ (password.get()).strip() + "','"+ (direccion.get()).strip() +"' ,'" + (textoComentario.get("0.1", END)).strip() +"');")
			
			datos = (nombre.get()).strip(), (apellido.get()).strip(), (password.get()).strip() ,(direccion.get()).strip(), (textoComentario.get("0.1", END)).strip()

			cursor.execute("INSERT INTO USUARIOS VALUES(NULL, ?, ?, ?, ?, ?)",  (datos))

			conexion.commit()
			messagebox.showinfo("EXITO", "Registro ingresado con éxito en la BBDD")
			borrar_campos()
		else:
			messagebox.showwarning("ADVERTENCIA", "El campo NOMBRE y/o CONTRASEÑA no puede quedar vacío.")
	except sqlite3.OperationalError:
		messagebox.showwarning("ERROR", "La BBDD aún no ha sido creada. Puede crearla en el menu BBDD opcion conectar. ")
	
	cursor.close()

def leer_registro():
	conexion = sqlite3.connect("Usuarios")
	cursor = conexion.cursor()
	print(ID.get())
	try:
		cursor.execute("SELECT * FROM USUARIOS WHERE ID = "+ID.get()+";")
		datos = cursor.fetchall()
		print(datos)
		nombre.set(datos[0][1])
		apellido.set(datos[0][2])
		password.set(datos[0][3])
		direccion.set(datos[0][4])
		textoComentario.insert("0.1", datos[0][5]) #Para insertar un texto en un TEXT de tkinter

	except sqlite3.OperationalError:
		messagebox.showwarning("ERROR", "La BBDD aún no ha sido creada. Puede crearla en el menu BBDD opcion conectar. ")	
	except:
		messagebox.showwarning("ERROR AL LEER REGISTRO", "¡Aún no se encuentran registros o ese registro no existe!")
	cursor.close()
	

def actualizar_registro():
	conexion = sqlite3.connect("Usuarios")
	cursor = conexion.cursor()
	
	try:
		# Tambien usare consultas parametrizadas por lo que comentare el codigo que estaba antes
		# cursor.execute("UPDATE USUARIOS SET NOMBRE = '"+ nombre.get() +"', APELLIDO = '"+ apellido.get()+"', PASSWORD = '" + password.get() +"', DIRECCION = '" + direccion.get() + "', COMENTARIO = '" + textoComentario.get("1.0", END) +"' WHERE ID = " + ID.get())
		datos = (nombre.get()).strip(), (apellido.get()).strip(), (password.get()).strip() ,(direccion.get()).strip(), (textoComentario.get("0.1", END)).strip(), (ID.get()).strip()

		cursor.execute("UPDATE USUARIOS SET NOMBRE = ?, APELLIDO = ?, PASSWORD = ?, DIRECCION = ?, COMENTARIO = ? WHERE ID = ?", (datos))

		conexion.commit()
		messagebox.showinfo("UPDATE", "¡Registro actualizado exitosamente!")
		borrar_campos()
	except sqlite3.OperationalError:
		messagebox.showwarning("ERROR", "La BBDD aún no ha sido creada. Puede crearla en el menu BBDD opcion conectar. ")
	except:
		messagebox.showwarning("ERROR AL LEER REGISTRO", "¡Aún no se encuentran registros o ese registro no existe!")

	cursor.close()
	
def eliminar_registro():
	conexion = sqlite3.connect("Usuarios")
	cursor = conexion.cursor()
	try:
		cursor.execute("DELETE FROM USUARIOS WHERE ID = " + ID.get())
		conexion.commit()
		messagebox.showinfo("DELETED", "¡Registro eliminado exitosamente!")
		borrar_campos()
	except sqlite3.OperationalError:
		messagebox.showwarning("ERROR", "La BBDD aún no ha sido creada. Puede crearla en el menu BBDD opcion conectar. ")
	except:
		messagebox.showwarning("ERROR AL ELIMINAR REGISTRO", "¡Aún no se encuentran registros o ese registro no existe!")

	cursor.close()
#------------------------------------------------------------------------------------------


root = Tk()
root.title("BBDD")

#------------------------------------------CONSTRUYENDO EL MENU---------------------------
barraMenu = Menu(root)
root.config(menu = barraMenu, bg = "skyblue")

BBDD = Menu(barraMenu, tearoff = 0)
BBDD.add_command(label = "Conectar", command = crear_bbdd)
BBDD.add_command(label = "Salir", command = lambda:salir(root))

Borrar = Menu(barraMenu, tearoff = 0)
Borrar.add_command(label= "Borrar campos", command = borrar_campos)

CRUD = Menu(barraMenu, tearoff = 0)
CRUD.add_command(label = "Crear registro", command = crear_registro)
CRUD.add_command(label = "Leer registro", command = leer_registro)
CRUD.add_command(label = "Actualizar registro", command = actualizar_registro)
CRUD.add_command(label = "Eliminar registro", command = eliminar_registro)

ayuda = Menu(barraMenu, tearoff = 0)
ayuda.add_command(label = "Licencia")
ayuda.add_command(label = "Acerca de")

#AÑADIENDO CADA SUBMENU A BARAMENU 
barraMenu.add_cascade(label = "BBDD", menu = BBDD)
barraMenu.add_cascade(label = "Borrar", menu = Borrar)
barraMenu.add_cascade(label = "CRUD", menu = CRUD)
barraMenu.add_cascade(label = "Ayuda", menu = ayuda)

#-------------------------CONSTRUYENDO FRAME-----------------------------------------------
frame = Frame(root, width = 350, height = 350, bg = "skyblue")
frame.pack(padx = 10, pady = 10)


#------------------------CONSTRUYENDO LAS ENTRYS Y LABELS DEL FRAME------------------------
ID = StringVar() 


lista_desp = ttk.Combobox(frame, state = "readonly", textvariable = ID, postcommand = listar_registros)
lista_desp.grid(row=0, column=1, padx = 10, pady = 10)
listar_registros()

Label(frame, text = 'ID: ', bg = "skyblue").grid(row=0, column=0, padx = 10, pady = 10)

nombre = StringVar()
Entry(frame, textvariable=nombre, width=30).grid(row=1, column=1, padx = 10, pady = 10)
Label(frame, text = 'Nombre: ', bg = "skyblue").grid(row=1, column=0, padx = 10, pady = 10)

apellido = StringVar()
Entry(frame, textvariable=apellido, width=30).grid(row=2, column=1, padx = 10, pady = 10)
Label(frame, text = 'Apellido: ', bg = "skyblue").grid(row=2, column=0, padx = 10, pady = 10)

password = StringVar()
Entry(frame, show = "*", textvariable=password, width=30).grid(row=3, column=1, padx = 10, pady = 10)
Label(frame, text = 'Password: ', bg = "skyblue").grid(row=3, column=0, padx = 10, pady = 10)

direccion = StringVar()
Entry(frame, textvariable=direccion, width=30).grid(row=4, column=1, padx = 10, pady = 10)
Label(frame, text = 'Dirección: ', bg = "skyblue").grid(row=4, column=0, padx = 10, pady = 10)

#, textvariable = comentario
#COMENTARIO Y SCROLLBAR
textoComentario = Text(frame, width = 25, height = 5)
textoComentario.grid(row = 5, column = 1)

barraDesplazamiento = Scrollbar(frame, command = textoComentario.yview)
barraDesplazamiento.grid(row = 5, column = 2, sticky = "nsew")

textoComentario.config(yscroll =barraDesplazamiento.set)

Label(frame, text = "Comentario: ", bg = "skyblue", padx = 10, pady = 10).grid(row= 5, column = 0, padx = 10, pady = 10)

#-----------------------CONSTRUYENDO LOS BOTONES CRUD---------------------------------------------
#He creado otro frame pq no se ubicaban bonito en el frame principal :c
frame2 = Frame(root, width = 350, height = 50, bg = "skyblue")
frame2.pack(padx = 10, pady = 10)

btnCreate = Button(frame2, text = "Create", width = 7, command = lambda:[crear_registro(), actualizar_registro])
btnCreate.grid(row = 1, column = 0, padx = 10, pady = 15)

btnRead = Button(frame2,text = "Read", width = 7, command = leer_registro)
btnRead.grid(row = 1, column = 1, padx = 10, pady = 15)

btnUpdate = Button(frame2, text = "Update", width = 7, command = actualizar_registro)
btnUpdate.grid(row = 1, column = 2, padx = 10, pady = 15)

btnDelete = Button(frame2, text = "Delete", width = 7, command = lambda:[eliminar_registro(), actualizar_registro])
btnDelete.grid(row = 1, column = 3, padx = 10, pady = 15)

root.mainloop()
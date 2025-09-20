import tkinter as tk
from tkinter import messagebox
import os

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("400x500")
        self.tareas = []

        self.titulo = tk.Label(root, text="Mis Tareas", font=("Arial", 18))
        self.titulo.pack(pady=10)

        self.entrada_tarea = tk.Entry(root, width=30, font=("Arial", 14))
        self.entrada_tarea.pack(pady=10)

        self.boton_agregar = tk.Button(root, text="Agregar Tarea", command=self.agregar_tarea)
        self.boton_agregar.pack(pady=5)

        self.lista_tareas = tk.Listbox(root, width=40, height=15, font=("Arial", 12))
        self.lista_tareas.pack(pady=10)

        self.boton_eliminar = tk.Button(root, text="Eliminar Tarea Seleccionada", command=self.eliminar_tarea)
        self.boton_eliminar.pack(pady=5)

        self.boton_guardar = tk.Button(root, text="Guardar Tareas", command=self.guardar_tareas)
        self.boton_guardar.pack(pady=5)

        self.boton_cargar = tk.Button(root, text="Cargar Tareas", command=self.cargar_tareas)
        self.boton_cargar.pack(pady=5)

        self.cargar_tareas()

    def agregar_tarea(self):
        tarea = self.entrada_tarea.get()
        if tarea:
            self.lista_tareas.insert(tk.END, tarea)
            self.entrada_tarea.delete(0, tk.END)
        else:
            messagebox.showwarning("Atención", "Escribe una tarea antes de agregar.")

    def eliminar_tarea(self):
        seleccion = self.lista_tareas.curselection()
        if seleccion:
            self.lista_tareas.delete(seleccion)
        else:
            messagebox.showwarning("Atención", "Selecciona una tarea para eliminar.")

    def guardar_tareas(self):
        with open("tareas.txt", "w", encoding="utf-8") as archivo:
            for i in range(self.lista_tareas.size()):
                archivo.write(self.lista_tareas.get(i) + "\n")
        messagebox.showinfo("Guardado", "Tareas guardadas correctamente.")

    def cargar_tareas(self):
        if os.path.exists("tareas.txt"):
            with open("tareas.txt", "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    self.lista_tareas.insert(tk.END, linea.strip())

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
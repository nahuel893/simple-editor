import tkinter as tk
from tkinter import ttk

import sys
sys.path.append('/home/nahuel/Estudios/MisProyectos/simplepyeditor')
from modules.tkinter.editor import TabsContainer
from config.configs import main_color, active_color, settings

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('875x762')
        self.title('Text Editor')
        style = ttk.Style()
        style.theme_create("my_style", parent='alt', settings=settings)
        style.theme_use('my_style')
        self.tabs = TabsContainer(self)
        self.tabs.new_tab_blank()
        self._crear_menu()
        self.grid_columnconfigure(0, weight=1)
    def _exit(self):
        global finish
        finish = False
        self.destroy()
    def _crear_menu(self):
        # Creamos el menu de la App
        menu_app = tk.Menu(self, bg=main_color, fg='white',
                           activebackground=active_color)
        self.config(menu=menu_app)
        # Agregamos las opciones a nuestro menu
        # Agregamos menu archivo
        menu_archivo = tk.Menu(
            menu_app, tearoff=False, bg=main_color, fg='white', activebackground=active_color)
        menu_app.add_cascade(label='Archivo', menu=menu_archivo)
        menu_archivo.add_command(
            label='Abrir', command=self.tabs.new_tab_file)
        
        menu_archivo.add_command(label='Salir', command=self._exit)
        
        menu_archivo.add_command(label='Guardar', command=self.tabs.save_current_tab)
        menu_archivo.add_command(label='Guardar como...',
                                  command=self.tabs.save_as_current_tab)
        menu_archivo.add_command(label='Nueva Pestaña', command=self.tabs.new_tab_blank)
        menu_archivo.add_separator()
        menu_archivo.add_command(label='Salir', command=self.quit)

if __name__ == '__main__':
    window = Window()
    window.mainloop()

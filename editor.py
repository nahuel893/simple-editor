from time import sleep
from tkinter.filedialog import askopenfile, asksaveasfilename
from tkinter import Scrollbar, ttk
import tkinter as tk
import threading

main_color = '#3a3c42'
active_color = '#83868f'
second_color = '#373737'
text_color = 'white'

class EditorTab(tk.Frame):

    def __init__(self, container):
        super().__init__(container)
        # Configuraciones del frame
        self.grid(row=0, column=0)
        self.grid_columnconfigure(1, weight=1)
        #self.grid_columnconfigure(0, weight=1)
        self.config(background=main_color)

        # self.config(width=900, height=900)
        # Utilizaremos un atributo para darle un nombre a la pestaña
        self.name = ''
        # Guardamos una referencia al contenedor en donde esta el obj EditorTab
        self.container = container
        self.saved = False

        # Atributo de archivo
        self.archivo = False

        # Atributo para saber si ya se abrio un archivo anteriormente
        self.archivo_abierto = False

        # Atributo de campo de texto
        self.text_box = tk.Text(
            self, 
            wrap=tk.WORD,
            font=('Jetbrains Mono Medium', 10),
            width=90,
            height=40,
        )
        self.text_box.grid(row=0, column=1, sticky='NSEW')
        self.text_box.config(bg=main_color, fg=text_color)

        
        # Creamos una scroll bar para el campo de texto
        # scrool vertical
        # referencia para entender el scroll vertical: https://stackoverflow.com/questions/32038701/python-tkinter-making-two-text-widgets-scrolling-synchronize


        self._vscrollbar = Scrollbar(self, orient='vertical')
        self._vscrollbar.config(command=self.text_box.yview,
                          background=main_color)

        self._vscrollbar.grid(row=0, column=3, sticky='NSE')
        self.text_box.config(yscrollcommand=self._vscrollbar.set)

        # scrool horizontal
        self._hscrollbar = Scrollbar(self, orient='horizontal')
        self._hscrollbar.config(command=self.text_box.xview,
                          background=main_color)
        self._hscrollbar.grid(row=3, column=1, sticky='EW')
        self.text_box.config(xscrollcommand=self._hscrollbar.set)



    def _set_name(self):
        self.name = self.archivo.name.split('/')[-1]
        if self.container.isHere(self):
            self.container.set_text(self, self.name)

    def isSaved(self):
        pass

    def open_file(self):
        # Abrimos el archivo para edicion (lectura-escritura) usando tkinter.
        self.archivo_abierto = askopenfile(mode='r+')
        print(self.archivo_abierto)
        # Revisamos si hay un archivo abierto
        if not self.archivo_abierto:
            return False# simplemente cortamos la ejecucion del metodo
        # Eliminamos el texto existente en el Text
        self.text_box.delete(1.0, tk.END)
        # Abrimos un archivo en modo lectura/escritura, utilizando la funciones incluidas en python.
        with open(self.archivo_abierto.name, 'r+') as self.archivo:
            # Leemos el contenido del archivo
            texto = self.archivo.read()
            # Insertamos todo este contenido en el campo de texto
            self.text_box.insert(1.0, texto)
            self._set_name()
            return True

    def save(self):
        # Si ya se abrio previamente un archivo lo sobreescribimos
        if self.archivo_abierto:
            # Guardamos el archivo (lo abrimos en modo escritura)
            with open(self.archivo_abierto.name, 'w') as self.archivo:
                # Leemos el contenido de la caja de texto
                texto = self.text_box.get(1.0, tk.END)
                # Escribimos el contenido al mismo archivo
                self.archivo.write(texto)
                # Cambiamos el nombre del titulo del app
                self._set_name()
        else:
            self.save_as()

    def save_as(self):
        # Salvamos el archivo actual como un nuevo archivo
        self.archivo = asksaveasfilename(
            defaultextension='txt',
            filetypes=[('Archivos de Texto', '*.txt'), ('Todos los archivos', '*.*')])
        # Si no esta abierto un archivo
        if not self.archivo:
            return False
        # Abrimos el archivo en modo escritura
        with open(self.archivo, 'w') as self.archivo:
            # Leemos el contenido de la caja de texto
            texto = self.text_box.get(1.0, tk.END)
            # Escribimos el contenido al nuevo archivo
            self.archivo.write(texto)
            # Cambiamos el titulo de la tab
            self._set_name()
            #  Indicamos que ya hemos abierto un archivo
            self.archivo_abierto = self.archivo
            return True


class TabsContainer(ttk.Notebook):
    def __init__(self, rootwindow):
        super().__init__(rootwindow)
        self.grid(sticky='nsew')
        self.tabs_list = []
        style = ttk.Style()
        settings = {
            "TNotebook": {"configure": {"background": main_color}
                          },
            "TNotebook.Tab": {"configure": {"padding": [5, 1],
                                            "background": main_color,
                                            "foreground": 'white'
                                            },
                              "map": {"background": [("selected", active_color),
                                                     ("active", active_color)],
                                      "foreground": [("selected", 'white'),
                                                     ("active", 'white')]

                                      }
                              }
        }

        style.theme_create("mi_estilo", parent="alt", settings=settings)
        style.theme_use("mi_estilo")
        self.rootwindow = rootwindow
    def _get_current_tab(self):
        return self.tabs_list[self.index(self.select())]
    def isHere(self, tab):
        return tab in self.tabs_list

    def save_current_tab(self):
        current_tab = self._get_current_tab()
        current_tab.save()
    
    def save_as_current_tab(self):
        current_tab = self._get_current_tab()
        current_tab.save_as()
 
    def open_in_current_tab(self):
        current_tab = self._get_current_tab()
        current_tab.open_file()

    def new_tab_blank(self):
        tab = EditorTab(self)
        self.tabs_list.append(tab) 
        self.add(tab, text='New File')
        return tab
    # corregido error al clickear opcion abrir pero no seleccionar ningun archivo.
    # se abria una pestaña en blanco sin titulo
    def new_tab_file(self):
        tab = EditorTab(self)
        res = tab.open_file()
        if res:
            self.tabs_list.append(tab) 
            self.add(tab, text=tab.name)
            self.select(tab)
        else:
            tab.destroy()

    def set_text(self, tab, string):
        self.tab(tab, text=string)


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('875x762')
       
        self.title('Text Editor')
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

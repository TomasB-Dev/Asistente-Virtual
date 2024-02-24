import speech_recognition as sr
import pyttsx3
import pywhatkit
import subprocess as sub
import wikipedia, datetime, keyboard, os
from pygame import mixer
from tkinter import *
from PIL import Image, ImageTk


Raiz = Tk()
Raiz.title('Asistente Valentina')
Raiz.geometry("800x400")
Raiz.resizable(0,0)
Raiz.config(bg='#8f94fb')

Label_Tittle = Label(Raiz, text="Asistente Valentina", bg="#8f94fb", fg='#4e54c8', font=('Arial',30, 'bold'))
Label_Tittle.pack(pady=10)

Valentina_Image = ImageTk.PhotoImage(Image.open("assets/imagenes/robot.jpg"))
win_photo = Label(Raiz, image=Valentina_Image)
win_photo.pack(pady=5)

comandos = """
        Comandos para usar:


        COMANDOS PARA UTILIZAR
        - Reproducir.. (cancion)
        - Busca... (algo)
        - Abrir... (pagina web o app)
        - Archivo... (nombre)
        - Termina (apagar)
        - Busca en google(algo)
        - Despertador(horario)
        - Escribí (texto)



"""
Canvas_comandos = Canvas(bg="purple", height=170,width=200)
Canvas_comandos.place(x=0,y=1)
Canvas_comandos.create_text(90,80, text=comandos, fill="white", font='Arial 10')

text_info = Text(Raiz, bg="#881cba",fg="#111111")
text_info.place(x=0, y=175, height=250, width=205)



name = "man"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)


sites=dict()
files=dict()
programs=dict()

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    rec = ""  # Inicializar rec antes del bloque try
    try:
        with sr.Microphone() as source:
            print('escuchando...')
            pc = listener.listen(source, timeout=5)  # Establecer un tiempo de espera para la escucha
            print('Grabación completada. Procesando...')
            rec = listener.recognize_google(pc, language='es-ES')
            print('Texto reconocido:', rec)
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
    except sr.UnknownValueError:
        print("Error en la función listen: No se pudo entender el audio.")
    except sr.RequestError as e:
        print(f"Error en la función listen: Error de solicitud a la API de reconocimiento - {e}")
    except Exception as e:
        print(f"Error en la función listen: {type(e).__name__} - {e}")
    return rec

def run_man():
    talk(f'hey! Hola!! Soy valentina, en que puedo ayudarte?')
    while True:
        rec = listen()
        if 'reproducir' in rec:
            musica = rec.replace('reproducir', '')
            print("reproduciendo" + musica)
            talk("reproduciendo" + musica)
            pywhatkit.playonyt(musica)
        elif 'busca en google' in rec:
            busqueda = rec.replace('busca en google','')
            talk("buscando" + busqueda)
            pywhatkit.search(busqueda)
        elif 'busca' in rec:
            search = rec.replace('busca','')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            talk(wiki)
        elif 'despertador' in rec:
            hora = rec.replace("despertador",'')
            hora.strip()
            talk("alarma activada a las" + hora + "horas")
            while True:
                if datetime.datetime.now().strftime('%H:%M') == hora:
                    print ("Despierta!")
                    mixer.init()
                    mixer.music.load("assets/audio/despertador.mp3")
                    mixer.music.play()
                    if keyboard.read_key() == "S":
                        mixer.music.stop()
                        break
        elif 'abrir' in rec:
            for site in sites:
                if site in rec:
                    sub.call(['start', 'chrome.exe', sites[site]], shell=True)
                    talk(f'Abriendo {site}')
            for app in programs:
                if app in rec:
                    talk(f'abriendo{app}')
                    os.startfile(programs[app])
        elif 'archivo' in rec:
            for file in files:
                if file in rec:
                    sub.Popen([files[file]], shell=True)
                    talk(f'abriendo {file}')
        elif 'escribí' in rec:
            try:
                with open("nota.txt",'a') as f:
                    write(f)
            except FileNotFoundError as e:
                file = open ("nota.txt", 'w')
                write(file)
        elif 'termina' in rec:
            talk('no me siento bien...')
            talk('no se que esta pasando')
            talk('No... no me quiero ir señor stark')
            talk("lo... lo.. lo... siento")
            break
def write(f):
    talk('que quieres que escriba?')
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo! ¿quieres revisarlo?")
    rec_decision = listen()
    if 'sí' in rec_decision:
        sub.Popen("nota.txt", shell=True)
    elif 'no' in rec_decision:
        talk("Esta bien, el archivo se guardo dentro de la carpeta!")
#funciones para cambiar la voz        
def latino():
    change_voice(3)
    talk("Cambiaste mi idioma a español latino")
def españa():
    change_voice(0)
    talk("Cambiaste mi idioma a español españa")
def english():
    change_voice(1)
    talk("You changed my language to English")
def change_voice(id):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[id].id)
#funciones para leer texto dado
def leeryhablar():
    texti = text_info.get('1.0','end')
    talk(texti)  
#funciones para agregar diccionarios y cosas
def open_w_files():
    windows_files = Toplevel()
    windows_files.title("agregar archivos")
    windows_files.config(bg="#8f94fb")
    windows_files.geometry("300x200")
    windows_files.resizable(0,0)
    Raiz.eval(f"tk::PlaceWindow {str(windows_files)} center")
    title_Label = Label(windows_files,text="agrega el archivo", fg="#111111",bg="#8f94fb",font=("Arial", 12, "bold"))
    title_Label.pack(pady=3)
    name_Label = Label(windows_files,text="Nombre del archivo", fg="#111111",bg="#8f94fb",font=("Arial", 10, "bold"))
    name_Label.pack(pady=2)

    nameFileEntry = Entry(windows_files)
    nameFileEntry.pack(pady=1)

    path_Label = Label(windows_files,text="Ruta del archivo", fg="#111111",bg="#8f94fb",font=("Arial", 10, "bold"))
    path_Label.pack(pady=2)
    pathFileEntry = Entry(windows_files, width=35)
    pathFileEntry.pack(pady=1) 

    save_btn = Button(windows_files,text="guardar", bg="white", fg="#111111")
    save_btn.pack(pady=4)
def open_w_apps():
        windows_apps = Toplevel()
        windows_apps.title("agregar archivos")
        windows_apps.config(bg="#8f94fb")
        windows_apps.geometry("300x200")
        windows_apps.resizable(0,0)
        Raiz.eval(f"tk::PlaceWindow {str(windows_apps)} center")
        title_Label = Label(windows_apps,text="agrega app", fg="#111111",bg="#8f94fb",font=("Arial", 12, "bold"))
        title_Label.pack(pady=3)
        name_Label = Label(windows_apps,text="Nombre de la app", fg="#111111",bg="#8f94fb",font=("Arial", 10, "bold"))
        name_Label.pack(pady=2)

        nameFileEntry = Entry(windows_apps)
        nameFileEntry.pack(pady=1)

        path_Label = Label(windows_apps,text="Ruta de la app", fg="#111111",bg="#8f94fb",font=("Arial", 10, "bold"))
        path_Label.pack(pady=2)
        pathFileEntry = Entry(windows_apps, width=35)
        pathFileEntry.pack(pady=1) 

        save_btn = Button(windows_apps,text="guardar", bg="white", fg="#111111")
        save_btn.pack(pady=4)
def open_w_pages():
        windows_pages = Toplevel()
        windows_pages.title("agregar archivos")
        windows_pages.config(bg="#8f94fb")
        windows_pages.geometry("300x200")
        windows_pages.resizable(0,0)
        Raiz.eval(f"tk::PlaceWindow {str(windows_pages)} center")
        title_Label = Label(windows_pages,text="Agrega una pagina", fg="#111111",bg="#8f94fb",font=("Arial", 12, "bold"))
        title_Label.pack(pady=3)
        name_Label = Label(windows_pages,text="Nombre de la pagina", fg="#111111",bg="#8f94fb",font=("Arial", 10, "bold"))
        name_Label.pack(pady=2)

        nameFileEntry = Entry(windows_pages)
        nameFileEntry.pack(pady=1)

        path_Label = Label(windows_pages,text="Ruta de la pagina", fg="#111111",bg="#8f94fb",font=("Arial", 10, "bold"))
        path_Label.pack(pady=2)
        pathFileEntry = Entry(windows_pages, width=35)
        pathFileEntry.pack(pady=1) 

        save_btn = Button(windows_pages,text="guardar", bg="white", fg="#111111")
        save_btn.pack(pady=4)
    
#botones de las voces#
Button_voice_mx = Button(Raiz,text="Voz Español Latino",fg="white", bg="Green", font=("Arial", 10, "bold"),command=latino)
Button_voice_mx.place(x=600,y=80 , width=170, height=30)
Button_voice_es = Button(Raiz,text="Voz Español España",fg="white", bg="#f5af19", font=("Arial", 10, "bold"),command=españa)
Button_voice_es.place(x=600,y=115 , width=170, height=30)
Button_voice_en = Button(Raiz,text="Voice English USA",fg="white", bg="#000046", font=("Arial", 10, "bold"),command=english)
Button_voice_en.place(x=600,y=155 , width=170, height=30)
#boton para hablar
Button_Listen = Button(Raiz,text="Escuchar",fg="white", bg="blue", font=("Arial", 10, "bold"),command=run_man)
Button_Listen.place(x=600,y=300 , width=170, height=30)
#boton para leer
Button_Leer = Button(Raiz,text="Leer",fg="white", bg="blue", font=("Arial", 10, "bold"),command=leeryhablar)
Button_Leer.place(x=600,y=250 , width=170, height=30)
#botones para agregar cosas
Button_add_files = Button(Raiz,text="Agregar archivos",fg="white", bg="blue", font=("Arial", 7, "bold"),command=open_w_files)
Button_add_files.place(x=600,y=195 , width=85, height=25)
Button_add_apps = Button(Raiz,text="agregar apps",fg="white", bg="blue", font=("Arial", 7, "bold"),command=open_w_apps)
Button_add_apps.place(x=690,y=195 , width=85, height=25)
Button_add_pages = Button(Raiz,text="Agregar paginas",fg="white", bg="blue", font=("Arial", 7, "bold"),command=open_w_pages)
Button_add_pages.place(x=645,y=220 , width=85, height=25)
Raiz.mainloop()
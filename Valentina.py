import speech_recognition as sr
import pyttsx3
import pywhatkit
import subprocess as sub
import wikipedia, datetime, keyboard, os
from pygame import mixer


name = "man"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

sites={
            'google':'google.com',
            'youtube':'youtube.com',
            'github':'github.com',
            'lucho':'twitch.tv/skalaiven'
}
files={
        'texto' :'texto.txt'
}
programs={
    'steam': r"C:\Program Files (x86)\Steam\steam.exe",
    'riot': r"C:\Riot Games\Riot Client\RiotClientServices.exe",
    'discord': r"C:\Users\Tomas\AppData\Local\Discord\Update.exe --processStart Discord.exe"

}
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
            print(search +":"+wiki)
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
        

if __name__ == '__main__':
    run_man()
    
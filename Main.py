from pytubefix import YouTube
import requests
import os
import flet
import time
import requests
from pathlib import Path
import uuid

from flet import(
    Container,
    Column,
    TextField,
    Row,
    IconButton,
    icons,
    ElevatedButton,
    Dropdown,
    dropdown,
    ListView,
    Text,
    Image,
    ImageFit,
    BoxShadow,
    Offset,
    ShadowBlurStyle,
    FontWeight,
    AlertDialog,
    TextButton,
    MainAxisAlignment,
    ProgressBar,
    Icon,
    BottomSheet,
    Audio,
    Window
)

# clase de la cancion, recive un atributo que es el link
class Cancion:


    def __init__(self, link):

        self.link = link
        self.author = ""
        self.end_time = ""
        self.title = ""
        self.miniatura_path = ""
        self.conexion_wifi = True
        self.exist_file = True
        self.error = False

        # funcion para descargar el audio
    def download_song_only_audio(self):
       
        yt = YouTube(self.link)
        # obtener la mejor resolucion
        audio = yt.streams.get_audio_only()

        # ruta donde se guardara la cancion
        file_path = os.path.expanduser("~\\Music")
        try:
            # descargar la cancion 
            audio.download(output_path=file_path, mp3=True)
        except:
            self.error = True

    # funcion para descargar el video con audio
    def download_video(self):

        yt = YouTube(self.link)

        try:
            # obtenemos el video con audio
            video = yt.streams.filter(progressive=True).first()

            # ruta para guardar el video
            file_path = os.path.expanduser("~\\Videos")

            # descargar el video y guardar en la anteriro ruta
            video.download(output_path=file_path)
            # se extrae el nombre del archivo con el que se descargo

            """
            esto lo hago porque en la funcion de informacion del video, se obtiene el titulo del video como se muestra en youtube, pero
            cuando se descarga se eliminan los puntos, por lo tanto cuando se hacee la condicion de verificar 
            si el archivo existe devolvera false y se descargara el video no importa si ya esta descargado,
            lo que hice fue renombrar el archivo de la cancion y darle el titulo que se muestra en youtube.
            """

            file_name = video.default_filename
            if os.path.exists(os.path.expanduser("~\\Videos\\"+file_name)):
                os.rename(os.path.expanduser("~\\Videos\\"+file_name), os.path.expanduser("~\\Videos\\"+self.title+".mp4"))
        except:
            self.error = True
        
    # esta funcioon extrae toda la informacion de la cancion antes de descargar el audio
    def song_info(self):

        yt = YouTube(self.link)

        try:
            # titulo
            self.title = str(yt.title).replace("?", "")

            # si existe el archivo no cambia la variable exist_file y la deja en true
            if os.path.exists(os.path.expanduser("~\\Music\\"+self.title+".mp3")):
                pass
            # si no existe el archivo se extrae la infomacion 
            elif not os.path.exists(os.path.expanduser("~\\Music\\"+self.title+".mp3")):

                # auto 
                self.author = yt.author

                # duracion de la cancion
                time = yt.length
                self.time_song_video(time)

                # miniatura
                miniatura = yt.thumbnail_url

                # obtener la miniatura
                download = requests.get(miniatura)

                # ruta de descargas
                download_foulder = os.path.expanduser("~\\Downloads\\Download_images")

                # os.mkdir(download_foulder)
                if not os.path.exists(download_foulder):

                    os.mkdir(download_foulder)
                    # ruta final para guardar se une con el nombre de la cancion
                    self.miniatura_path = os.path.join(download_foulder, f"{self.title}.png")
                    # crear el archivo de la imagen
                    with open(self.miniatura_path, 'wb') as file:
                        file.write(download.content)

                if os.path.exists(download_foulder):

                    # ruta final para guardar se une con el nombre de la cancion
                    self.miniatura_path = os.path.join(download_foulder, f"{self.title}.png")
                    # crear el archivo de la imagen
                    with open(str(self.miniatura_path), 'wb') as file:
                        file.write(download.content)

                # cambiar el valor de la variable a False para que agregue el contenido a la pantalla y luuego se descargue
                self.exist_file = False
                self.error = False
        except:
            self.error = True
        
     # esta funcioon extrae toda la informacion de la cancion antes de descargar el video
    def video_info(self):

        yt = YouTube(self.link)
        try:

            # titulo
            self.title = str(yt.title)
            # si existe el archivo no cambia la variable exist_file y la deja en true
            if os.path.exists(os.path.expanduser("~\\Videos\\"+self.title+".mp4")):
                pass

            # si no existe el archivo se extrae la infomacion 
            elif not os.path.exists(os.path.expanduser("~\\Videos\\"+self.title+".mp4")):
                # auto 
                self.author = yt.author
                # audio = yt.streams.get_audio_only()

                # duracion de la cancion
                time = yt.length
                self.time_song_video(time)

                # miniatura
                miniatura = yt.thumbnail_url

                # obtener la miniatura
                download = requests.get(miniatura)

                # ruta de descargas
                download_foulder = os.path.expanduser("~\\Downloads\\Download_images")
                # os.mkdir(download_foulder)
                if not os.path.exists(download_foulder):
                    os.mkdir(download_foulder)
                    # ruta final para guardar se une con el nombre de la cancion
                    self.miniatura_path = os.path.join(download_foulder, f"{self.title}.png")

                    # crear el archivo de la imagen
                    with open(self.miniatura_path, 'wb') as file:
                        file.write(download.content)
                if os.path.exists(download_foulder):
                    # ruta final para guardar se une con el nombre de la cancion
                    self.miniatura_path = os.path.join(download_foulder, f"{self.title}.png")

                    # crear el archivo de la imagen
                    with open(self.miniatura_path, 'wb') as file:
                        file.write(download.content)
                self.exist_file = False
                self.error = False
        except:
            self.error = True

    # funcion para verificar la conexion de wifi
    def check_wifi(self):

        try:
            url = "https://www.google.com"
            requests.get(url, timeout=5)
            self.conexion_wifi = True
        except:
            self.conexion_wifi = False

    # funcion para la duracion de la cancion o video
    def time_song_video(self, seg):

        # esta condicion es para cuando los segundos son menores a una hora y facilitar el proceso
        if seg <= 3600:
            minutos = seg//60
            segundos = seg%60
            self.end_time = f"{minutos:02d}:{segundos:02d}"
        
        # si los segundos son amyores a una hora se hace la operacion con horas minutos y segundos
        elif seg > 3600:
            horas = seg//3600
            minutos_2 = int(seg%3600)//60
            segundos_2 = int(seg%3600)%60
            self.end_time = f"{horas:02d}:{minutos_2:02d}:{segundos_2:02d}"

# esta es la case donde esta la interfaz grafica
class Dowloader_app:

    def __init__(self, page):
        self.page = page
        self.path_audio = " "
        self.ident_container = int
        self.list_container = []
        self.audio = ""


        # este es el tamaño inicial del programa
        self.page.window.width = 1094
        self.page.window.height = 640

        # icono de la ventana
        self.page.window.icon = r"C:\Users\divar\Desktop\mis_proyectos\Music_Downloader\assets\musica.ico"
        self.page.title = "Music Downloader"

        # la ventana se mostrara en el centro de la pantalla
        self.page.window.center()
        self.page.update()

        # entrada del link
        self.input_text = TextField(
                                    label="Paste link",
                                    bgcolor="white",
                                    multiline=False,
                                    border_radius=18,
                                    expand=True,
                                    
        )

        # boton para actualizar el boton de descargar, es para si el boton de descargar se desactiva.
        self.button_update = IconButton(
            icon=icons.UPDATE_ROUNDED,
            icon_color="#8e9c8e",
            icon_size=38,
            on_click=self.page_update
        )

        # lista donde se mostraran todas las canciones
        self.songs_list = ListView(
            spacing=20,
            expand=True,
            reverse=True,
            auto_scroll=True,
        )

        # boton para descargar el contenido
        self.Download_button = ElevatedButton(
                                            "Download",
                                            icon=icons.DOWNLOAD_ROUNDED,
                                            width=240,
                                            height=50,
                                            icon_color="#0B440A",
                                            color="#107D0E",
                                            bgcolor="white",
                                            on_click=self.download_song_UI,
                                            tooltip="Download song"
        )

        # icono de check
        self.icon_dwlad_check = Icon(
            name=icons.CHECK_CIRCLE_ROUNDED,
            size=200,
            color="#5BDC44",
            # disabled=True
        )

        # esto es una cascada de opciones para escoger audio o video
        self.file_type = Dropdown(
            label="File type",
            width=110,
            height=50,
            border_color="#107D0E",
            bgcolor="white",
            tooltip="Download song",
            border_radius=15,
            options=[
                dropdown.Option("Audio"),
                dropdown.Option("Video"),
            ]
        )

        # esta es la cascada de opciones para escoger la calidad del video, aun sin funcionalidad
        self.resolution = Dropdown(
            label="Resolution",
            width=121,
            height=50,
            border_color="#107D0E",
            bgcolor="white",
            border_radius=15,
            tooltip="Download song",
            options=[
                dropdown.Option("high"),
                dropdown.Option("Middle"),
                dropdown.Option("Low"),
            ]
        )

        # fila donde estan los componentes de entrada tipo de archivo y resolucion
        self.row_widgets_1 =Row(
                    controls=[
                    Column(width=120,),
                    self.input_text,
                    self.file_type,
                    self.resolution,
                    Column(width=90)
                ],
                alignment=flet.MainAxisAlignment.CENTER
            )

        # container para la fila anterior        
        self.container_3 = Container(
            margin=15,
            content=self.row_widgets_1
        )

        # fila para el boton de descarga 
        self.row_download_button = Row(
            controls=[
                self.Download_button
            ],
            alignment=flet.MainAxisAlignment.CENTER
        )

        self.container_update = Container(
            content=Row(controls=[
                self.button_update
                ],
                alignment=flet.MainAxisAlignment.END
            ),
        )

        self.container_song_list = Container(
            margin=flet.margin.only(bottom=30),
            expand=True,
            content=self.songs_list,
        )

        # container para todos los widgets 
        self.container_2 = Container(
            content=Column(
                spacing=5,
                controls=[
                    self.container_update,
                    self.container_3,
                    self.row_download_button,
                    self.container_song_list
                ],
                alignment=flet.MainAxisAlignment.START
            ),
            margin=5,
        )

        # container para el container anterior, este es el container principal de fondo, se empaquetan en diferentes containers
        # para manejar mejor los espacios y ubicacion de cada conponente
        self.container_1 = Container(
            bgcolor="transparent",
            expand=True,
            margin=-10,
            height=self.page.height,
            content=self.container_2
        )

        self.container_bground = Container(
            content=self.container_1,
            image_src=r"C:\Users\divar\Desktop\mis_proyectos\Music_Downloader\assets\bground_lofi.jpg",
            image_fit="FILL",
            expand=True,
            height=self.page.height,
            margin=-10
        )

        # alerta de error
        self.dlg_modal = AlertDialog(
            # modal=True,
            title=Text("!Upss", weight=FontWeight.W_600, size=24),
            content=Text("Link provied error :(", weight=FontWeight.W_500, size=20),
            actions=[
                TextButton("OK", on_click=self.close_dialog)
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        self.icon_check_dialog = AlertDialog(
            modal=True,
            content=self.icon_dwlad_check,
            bgcolor="transparent"
        )

        self.check_wifi_banner = BottomSheet(
            content=Row(
                spacing=20,
                controls=[
                    Icon(name=icons.SIGNAL_WIFI_OFF_SHARP, color="#BD0014" ,size=30),
                    Container(
                        padding=10,
                    border_radius=15,
                    content=Text("Connection error", weight=FontWeight.W_500, size=35)
                    ),
                ],
                alignment=flet.MainAxisAlignment.CENTER
            )
        )

        """
        la clase cancion se intancia dos veces esta instancia es para poder usarla fuera 
        de la funcion de descargar el video o audio
        ya que si hago una sola instancia para todo no me retorna los valores necesarios
        """
        self.downloader_2 = Cancion(self.input_text.value)

    """
    def play_song(self):
        print("### Funcion play_song ###")
        data = self.ident_container
        for i in self.list_container:
            print("  -- Ingresando al bucle")
            print(f"  variable data {data}")
            print("  imprimiendo i: ", i)
            if i[0] == data:
                self.path_audio = i[1]
                print(f"  valor de: path {self.path_audio}")

                print("  -- Antes de la variable audio")
                self.audio = Audio(
                        src=Path(self.path_audio),
                        autoplay=False
                    )
                print("  -- Antes de agregar audio a page en play ")
                self.page.overlay.append(self.audio)
                self.page.update()
                print("  -- widget audio agregado")
                print("  -- reproduciendo en play...")
                self.audio.play()
                self.page.update()
                print("  -- saliendo de reproduccion en play <-")
                self.ident_container = int
                self.path_audio = " "
            else:
                print("-- no esta la cancion en lista")
    """
    
    def pause(self, e):
        # self.audio.autoplay = False
        self.audio.pause()
        self.page.update()
        print(self.audio.autoplay)
        print("-- saliendo de pause")

    def page_update(self, e):
        self.Download_button.disabled = False
        self.page.update()

    # funcion para abrir el dialogo
    def open_dialog(self):
        self.page.overlay.append(self.dlg_modal)
        self.dlg_modal.open = True
        self.page.update()

    # funcion para cerrar el dialogo
    def close_dialog(self, e):
        self.dlg_modal.open = False
        self.page.update()

    # esta funcion muestra la alerta cuando se inicia el programa, si no 
    # hay conexion a internet, se ejecutara en unbucle hasta que se conecte.
    # el boton de descarga estara bloqueado hasta que se conecte al wifi
    def dialog_check_wifi_initial(self):

        while True:
            self.downloader_2.check_wifi()
            if not self.downloader_2.conexion_wifi:
                self.Download_button.disabled = True
                self.page.update()
                self.page.open(self.check_wifi_banner)
                time.sleep(3)
                self.page.close(self.check_wifi_banner)
                self.page.update()
            elif self.downloader_2.conexion_wifi:
                self.check_wifi_banner.content = Row(
                                                    spacing=20,
                                                    controls=[
                                                        Icon(name=icons.SIGNAL_WIFI_STATUSBAR_4_BAR, color="#27E127" ,size=30),
                                                        Container(
                                                            padding=10,
                                                        # width=410,
                                                        # height=50,
                                                        border_radius=15,
                                                        content=Text("Connection established", weight=FontWeight.W_500, size=35)
                                                        ),
                ],
                alignment=flet.MainAxisAlignment.CENTER
                )
                self.page.open(self.check_wifi_banner)
                time.sleep(2)
                self.page.close(self.check_wifi_banner)
                # aqui se activa dde nuevo el boton de descrga
                self.Download_button.disabled = False
                self.page.update()
                break
            time.sleep(2)

    # esta funcion es igual que la anterior pero se llamara cuando se oprima el boton de descarga, ya que si no hay 
    # conexion se pueda informar al usuario que no tiene conexion.
    def dialog_check_wifi_in_progress(self):
        # se llama la funcion que erifica la conexion
        self.downloader_2.check_wifi()
        if not self.downloader_2.conexion_wifi:

            self.check_wifi_banner.content = Row(
                                                spacing=20,
                                                controls=[
                                                    Icon(name=icons.SIGNAL_WIFI_OFF_SHARP, color="#BD0014" ,size=30),
                                                    Container(
                                                        padding=10,
                                                    border_radius=15,
                                                    content=Text("Connection error", weight=FontWeight.W_500, size=35)
                                                    ),
                ],
                alignment=flet.MainAxisAlignment.CENTER
                )
            self.page.open(self.check_wifi_banner)
            time.sleep(3)
            self.page.close(self.check_wifi_banner)
            self.page.update()
        if self.downloader_2.conexion_wifi:
            self.check_wifi_banner.content = Row(
                                                    spacing=20,
                                                    controls=[
                                                        Icon(name=icons.SIGNAL_WIFI_STATUSBAR_4_BAR, color="#27E127" ,size=30),
                                                        Container(
                                                            padding=10,
                                                        border_radius=15,
                                                        content=Text("Connection established", weight=FontWeight.W_500, size=35)
                                                        ),
                ],
                alignment=flet.MainAxisAlignment.CENTER
                )
            self.page.open(self.check_wifi_banner)
            time.sleep(2)
            self.page.close(self.check_wifi_banner)
            self.page.update()

                

    # funcion para mostrar la cancion en pantalla y descargar el contenido
    def download_song_UI(self, e):
        code = uuid.uuid4()
        self.Download_button.disabled = True
        self.page.update()

        # esta instancia es la que se usa dentro de la funcion de descargar 
        downloader = Cancion(self.input_text.value)
        progressbar = ProgressBar(width=300)
        progressbar.visible = False
        progressbar.value = 0
        ruta = " "

         # numero de progreso de descarga
        num_progress = Text(
            selectable=True,
            weight=FontWeight.W_500,
            color="black",
            size=14
        )
        """
        def get_identificator(e):
            print("  ### Funcion identificator ###")
            print(f"    -- identificador: {self.ident_container}")
            if self.ident_container:
                print(f"    -- valor de e {e}")
                self.ident_container = e
                print(f"    -- identificador: {self.ident_container}")
                print(f"    -- lista: {self.list_container}")
                print("    -- saliendo de get _identificator")
                self.play_song()
            else:
                print("    -- no ocurrio nada")
        """

        # esta funcion muestra un check cuando termina la descarga
        def open_icon_check_audio():

            self.page.overlay.append(self.icon_check_dialog)
            self.icon_check_dialog.open = True
            self.page.update()

            # cuando se muestra el check de descarga se inicia la descarga y en medio de eso
            #  descargara el audio, cuando termine la descarga desaparece el check
            downloader.download_song_only_audio()
            self.icon_check_dialog.open = False
            self.page.update()

        # este es el check de descarga del video
        def open_icon_check_video():

            self.page.overlay.append(self.icon_check_dialog)
            self.icon_check_dialog.open = True
            self.page.update()
            # cuando se muestra el check de descarga se inicia la descarga y en medio de eso
            # descargara el video, cuando termine la descarga desaparece el check
            downloader.download_video()
            self.icon_check_dialog.open = False
            self.page.update()

        # esta funcion se crea con todo el container para darle interactividad a la bara de progreso
        def progress():
            progressbar.visible = True

            for i in range(0, 101):
                progressbar.value = i*0.01
                num_progress.value = f"{i}%"
                time.sleep(0.01)
                self.page.update()

        # button_play = IconButton(icons.PLAY_CIRCLE_OUTLINE, on_click=play_music)
        # button_pause = IconButton(icons.PAUSE_CIRCLE_OUTLINE_ROUNDED, on_click=pause_music)

        # condicional para confirmar que si se introdujo el link el tipo de archivo y resolucion
        if not self.input_text.value or not self.file_type.value or not self.resolution.value:

            # se muestra la alerta si no se introdujo nada en los campos
            self.dlg_modal.content = Text("Incompleted Spaces", weight=FontWeight.W_500, size=20)
            self.open_dialog()
            self.page.update()

        # si estan completos los inputs pasa aqui
        elif self.input_text.value and self.file_type.value and self.resolution.value:

            # si el input de tipo de archivo es Audio y si hay conexioon a internet procede a descargar el audio
            if self.file_type.value == "Audio" and downloader.conexion_wifi:

                try:

                    # extraer la informacion de la cancion
                    downloader.song_info()

                    title_join = downloader.title+".mp3"
                    path_join = os.path.expanduser("~\\Music\\")
                    ruta = os.path.join(path_join, title_join)
                    print(f"-- ruta final en dounloader: {ruta}")

                    if not downloader.error:

                        if downloader.exist_file:

                            self.dlg_modal.content = Text("Existing file :(", weight=FontWeight.W_500, size=20)
                            self.open_dialog()
                            self.page.update()
                        elif not downloader.exist_file:
                            print("-- Ingresando a crear el container")

                            # se extrae la ruta para la miniatura del video
                            path = downloader.miniatura_path

                            # se arregla la ruta quitado la C: y las barras inclinadas hacia el otro lado,
                            #  la barra \ se pone doble para que la tome como string
                            new_path = path.replace("\\", "/").replace("C:", "")


                            """
                            se agregan los widgets a la lista donde se ponen las canciones descargadas, 
                            se crean nuevos widgets cada que se descarga una cancion ya que si se crean 
                            como variables cambia el valor de todas las descargaas que se muestran en pantalla
                            simepre que se descargue una canion
                            """
                            self.songs_list.controls.append(
                                Container(
                                    height=110,
                                    margin=flet.margin.only(left=85, right=85),
                                    padding=-7,
                                        content=Container(
                                        margin=10,
                                        content=Row(
                                        controls=[
                                            Container(
                                            bgcolor="white",
                                            width=155,
                                            height=95,
                                            content=Image(
                                                        src=new_path,
                                                        fit=ImageFit.FILL,
                                                        width=200,
                                                        height=110
                                                    ),
                                            border_radius=15
                                        ),
                                        Column(
                                            controls=[
                                            Container(
                                                width=600,
                                                content=Text(
                                                        # se acceden a los atributos de la clase cancion desde la intancia 
                                                        # que se hizo antriormente, eneste caso es el titulo
                                                        value=downloader.title,
                                                        selectable=True,
                                                        weight=FontWeight.W_700,
                                                        color="black",
                                                        size=23

                                                ),
                                            ),
                                            Row(
                                                spacing=10,
                                                controls=[
                                                        Text(
                                                            # se acceden a los atributos de la clase cancion desde la intancia 
                                                            # que se hizo antriormente, eneste caso es el autor
                                                            value=downloader.author,
                                                            selectable=True,
                                                            weight=FontWeight.W_600,
                                                            color="black",
                                                            size=17
                                                        ),
                                                        Text(
                                                            # se acceden a los atributos de la clase cancion desde la intancia 
                                                            # que se hizo antriormente, eneste caso es el tiempo de diracion la cancion
                                                            value=downloader.end_time,
                                                            selectable=True,
                                                            weight=FontWeight.W_500,
                                                            color="black",
                                                            size=14
                                                        ),
                                                        # barra de progreso y numero de progreso
                                                        progressbar,
                                                        num_progress
                                                    ],
                                                )
                                        ]
                                        ),
                                        Container(
                                            expand=True,
                                            content=Row(
                                                controls=[
                                                    
                                                        IconButton(
                                                                icon=icons.PLAY_CIRCLE_OUTLINE,
                                                                # on_click=lambda x: get_identificator(x.control.data),
                                                                tooltip="In proces",
                                                                data=code
                                                                ),
                                                        IconButton(
                                                                icon=icons.PAUSE_CIRCLE_OUTLINE_ROUNDED,
                                                                data=code,
                                                                tooltip="In proces",
                                                                on_click=self.pause
                                                                ),
                                                        Column(width=10),
                                                        ],
                                                        alignment=flet.MainAxisAlignment.END
                                                        )
                                                    )
                                                ],
                                                )
                                            ),
                                        bgcolor="white",
                                        border_radius=15,
                                        shadow=BoxShadow(
                                                spread_radius=1,
                                                blur_radius=3,
                                                offset=Offset(-2, 2),
                                                blur_style=ShadowBlurStyle.NORMAL,
                                                color="#b21aab"
                                                ),
                                )
                            )
                            self.page.update()
                            print("-- Despues de crear el container")
                            # se llama la funcion de barra de progrso 
                            progress()
                            self.page.update()
                            # se confirma la informacion extraida de la cancion 
                            if downloader.title and downloader.author and downloader.end_time:
                                try:
                                    # se descarga la cancion
                                    # cuando se llama esta fucion se muestra el check de descarga luego inicia la descarga y cuuando termina 
                                    # desaparece el check de descarga
                                    open_icon_check_audio()
                                    self.input_text.value = ""
                                    self.Download_button.disabled = False
                                    print("-- despues de descargar")
                                    self.page.update()
                                except TypeError:
                                    # si ocurre algun error me muestra la alerta
                                    self.dlg_modal.content(Text("Downloaded not completed"))
                                    self.open_dialog()
                                    self.page.update()
                    elif downloader.error:
                        self.dialog_check_wifi_in_progress()
                except:

                    try:
                        requests.get(downloader.link)
                        # confirm = True
                    except requests.exceptions.MissingSchema:
                        self.dlg_modal.content = Text("Link error", weight=FontWeight.W_500, size=20)
                        self.open_dialog()
                    except requests.ConnectionError:
                        self.dialog_check_wifi_in_progress()
                self.page.update()

                """
                aqui se confira cuando es la eleccion del usuario es video, la funcionalidad es la misma que con la cancion, 
                solo cambia la funcion para descargar el video 
                """
            elif self.file_type.value == "Video" and downloader.conexion_wifi:
                try:

                    downloader.video_info()
                    if not downloader.error:

                        if downloader.exist_file:

                            self.dlg_modal.content = Text("Existing file :(", weight=FontWeight.W_500, size=20)
                            self.open_dialog()
                            self.page.update()

                        elif not downloader.exist_file:
                            path = downloader.miniatura_path
                            new_path = path.replace("\\", "/").replace("C:", "")

                            self.songs_list.controls.append(
                                Container(
                                    height=110,
                                    margin=flet.margin.only(left=85, right=85),
                                    padding=-7,
                                        content=Container(
                                        margin=10,
                                        content=Row(
                                        controls=[
                                            Container(
                                            bgcolor="red",
                                            width=155,
                                            height=95,
                                            content=Image(
                                                        src=new_path,
                                                        fit=ImageFit.FILL,
                                                        width=200,
                                                        height=110
                                                    ),
                                            border_radius=15
                                        ),
                                        Column(
                                            controls=[
                                            Container(
                                                width=600,
                                                content=Text(
                                                        value=downloader.title,
                                                        selectable=True,
                                                        weight=FontWeight.W_700,
                                                        color="black",
                                                        size=23

                                                ),
                                            ),
                                            Row(
                                                spacing=10,
                                                controls=[
                                                        Text(
                                                            value=downloader.author,
                                                            selectable=True,
                                                            weight=FontWeight.W_600,
                                                            color="black",
                                                            size=17
                                                        ),
                                                        Text(
                                                            value=downloader.end_time,
                                                            selectable=True,
                                                            weight=FontWeight.W_500,
                                                            color="black",
                                                            size=14
                                                        ),
                                                        progressbar,
                                                        num_progress
                                                    ],
                                                )
                                        ]
                                        ),
                                        Container(
                                            expand=True,
                                            content=Row(
                                            controls=[
                                                        IconButton(
                                                                icon=icons.PLAY_CIRCLE_OUTLINE,
                                                                # on_click=lambda x: get_identificator(x.control.data),
                                                                tooltip="In proces",
                                                                data=code
                                                                ),
                                                        IconButton(
                                                                icon=icons.PAUSE_CIRCLE_OUTLINE_ROUNDED,
                                                                data=code,
                                                                tooltip="In proces",
                                                                # on_click=self.pause
                                                                ),
                                                        Column(width=10),
                                                    ],
                                                    alignment=flet.MainAxisAlignment.END
                                                        )
                                                    )
                                                ],
                                                )
                                            ),
                                        bgcolor="white",
                                        border_radius=15,
                                        shadow=BoxShadow(
                                                spread_radius=1,
                                                blur_radius=3,
                                                offset=Offset(-4, 4),
                                                blur_style=ShadowBlurStyle.NORMAL,
                                                color="#4a235a"
                                                )
                                )
                            )
                            progress()
                            self.page.update()
                            if downloader.title and downloader.author and downloader.end_time:
                                try:
                                    # esta es la funcion para descargar el video
                                    open_icon_check_video()
                                    self.input_text.value = ""
                                    self.Download_button.disabled = False
                                    self.page.update()
                                except TypeError:
                                    self.dlg_modal.content(Text("Downloaded not completed"))
                    elif downloader.error:
                        self.dlg_modal.content = Text("Link error", weight=FontWeight.W_500, size=20)
                        self.open_dialog()
                except :

                    try:
                        requests.get(downloader.link)
                        # confirm = True
                    except requests.exceptions.MissingSchema:
                        self.dlg_modal.content = Text("Link error", weight=FontWeight.W_500, size=20)
                        self.open_dialog()
                    except requests.ConnectionError:
                        self.dialog_check_wifi_in_progress()

                self.page.update()
            elif not downloader.conexion_wifi:
                self.dialog_check_wifi_in_progress()
        self.list_container.append((code, ruta))
        print(f"-- lista: {self.list_container}")
        self.Download_button.disabled = False
        self.page.update()


    # metodo para iniciar el programa
    def start(self):

        # se verifica el wifi con el metodo de la clase cancion si  
        self.downloader_2.check_wifi()

        # si esta en True me inicia el programa
        if self.downloader_2.conexion_wifi:
            self.page.add(self.container_bground)
            """
            si esta en False se iniciara el programa igualmente pero con la funcion que muestra la alerta de conexion de wifi.
            lo separe en un condicional ya que si inicio el programa directamente y luego pogo la funcion de alerta de coneccion
            me mostrara la alerta de coneccion etablecida y la idea es que no me muestre nada si ya esta la coneccion
            """
        else:
            self.page.add(self.container_bground)
            self.dialog_check_wifi_initial()
        self.page.update()


# funcion para arracar el programa
def inicio(page):
    app = Dowloader_app(page)
    app.start()
    page.update()

flet.app(target=inicio)
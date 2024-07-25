import urllib.request
from pytubefix import YouTube
import requests
import os
import flet
import time
import requests

from flet import(
    Container,
    LinearGradient,
    alignment,
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
    TextStyle,
    FontWeight,
    AlertDialog,
    TextButton,
    MainAxisAlignment,
    ButtonStyle,
    ProgressBar,
    Icon,
    BottomSheet,
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

        # funcion para descargar el audio
    def download_song_only_audio(self):
        print("-- funcion descargar audio")
        
        yt = YouTube(self.link)
        print("-- despues de Yuotube")
        # obtener la mejor resolucion
        audio = yt.streams.get_audio_only()
        print("-- despues de get audio")

        # ruta donde se guardara la cancion
        file_path = os.path.expanduser("~\\Music")

        # descargar la cancion 
        print("-- antes de descargar")
        audio.download(output_path=file_path, mp3=True)
        print("-- despues de descargar")
        # exit()

    # funcion para descargar el video con audio
    def download_video(self):

        yt = YouTube(self.link)

        # obtenemos el video con audio
        video = yt.streams.filter(progressive=True).first()

        # ruta para guardar el video
        file_path = os.path.expanduser("~\\Videos")

        # descargar el video y guardar en la anteriro ruta
        video.download(output_path=file_path)
        
    # esta funcioon extrae toda la informacion de la cancion antes de descargar el video o el audio
    def song_info(self):

        yt = YouTube(self.link)

        # titulo
        self.title = yt.title

        # auto 
        self.author = yt.author
        # audio = yt.streams.get_audio_only()

        # duracion de la cancion
        time = yt.length
        hours = time//60
        minutes = int(hours%60)
        seconds = minutes%60
        self.end_time = f"{hours}:{minutes}:{seconds}"

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

    def check_wifi(self):

        try:
            url = "https://www.google.com"
            requests.get(url, timeout=7)
            self.conexion_wifi = True
        except:
            self.conexion_wifi = False

# esta es la case donde esta la interfaz grafica
class Dowloader_app:

    def __init__(self, page):
        self.page = page

        # entrada del link
        self.input_text = TextField(
                                    label="Paste link",
                                    bgcolor="white",
                                    multiline=False,
                                    border_radius=18,
                                    expand=True,
                                    
        )

        # lista donde se mostraran todas las canciones
        self.songs_list = ListView(
            spacing=-15,
            expand=True,
            reverse=True,
            auto_scroll=True
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
                                            on_click=self.download_song_UI
        )

        # este es el tamaño inicial del programa
        self.page.window.width = 900
        self.page.window.height = 600

        # la ventana se mostrara en el centro de la pantalla
        self.page.window.center()
        self.page.update()

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

        # container para todos los widgets 
        self.container_2 = Container(
            content=Column(
                controls=[
                    self.container_3,
                    self.row_download_button,
                    self.songs_list,
                ],
                alignment=flet.MainAxisAlignment.START
            ),
            margin=15,
        )

        # container para el container anterior, este es el container principal de fondo, se empaquetan en diferentes containers
        # para manejar mejor los espacios y ubicacion de cada conponente
        self.container_1 = Container(
            # bgcolor="red",
            gradient=LinearGradient(
                begin=alignment.center_right,
                end=alignment.top_left,
                colors=["#0B440A", "#107D0E", "#129B0F",]
            ),
            expand=True,
            margin=-10,
            height=self.page.height,
            content=self.container_2
        )

        # alerta de error
        self.dlg_modal = AlertDialog(
            modal=True,
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
                    # width=410,
                    # height=50,
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

    # funcion para abrir el dialogo
    def open_dialog(self):
        self.page.overlay.append(self.dlg_modal)
        self.dlg_modal.open = True
        self.page.update()

    # funcion para cerrar el dialogo
    def close_dialog(self, e):
        self.dlg_modal.open = False
        self.page.update()

    # esta funcion muestra un check cuando termina la descarga
    def open_icon_check(self):

        self.page.overlay.append(self.icon_check_dialog)
        self.icon_check_dialog.open = True
        # self.page.update()
        print("-- antees de descargar dentro de check")
        self.downloader_2.download_song_only_audio()
        print("-- despues de descargar dentro de check")
        self.icon_check_dialog.open = False
        self.page.update()

    def dialog_check_wifi_initial(self):

        while True:
            self.downloader_2.check_wifi()
            if not self.downloader_2.conexion_wifi:
                self.Download_button.disabled = True
                self.page.update()
                self.page.open(self.check_wifi_banner)
                time.sleep(3)
                self.page.close(self.check_wifi_banner)
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
                self.Download_button.disabled = False
                self.page.update()
                break
            time.sleep(2)

    def dialog_check_wifi_in_progress(self):
        print("ingreso a verificar en progres")
        self.downloader_2.check_wifi()
        if not self.downloader_2.conexion_wifi:
            # self.Download_button.disabled = True
            self.check_wifi_banner.content = Row(
                                                spacing=20,
                                                controls=[
                                                    Icon(name=icons.SIGNAL_WIFI_OFF_SHARP, color="#BD0014" ,size=30),
                                                    Container(
                                                        padding=10,
                                                    # width=410,
                                                    # height=50,
                                                    border_radius=15,
                                                    content=Text("Connection error", weight=FontWeight.W_500, size=35)
                                                    ),
                ],
                alignment=flet.MainAxisAlignment.CENTER
                )
            self.page.open(self.check_wifi_banner)
            time.sleep(3)
            self.page.close(self.check_wifi_banner)
        if self.downloader_2.conexion_wifi:
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
            # self.Download_button.disabled = False

                

    # funcion para mostrar la cancion en pantalla y descargar el contenido
    def download_song_UI(self, e):
        self.Download_button.disabled = True
        self.page.update()

        # esta instancia es la que se usa dentro de la funcion de descargar 
        downloader = Cancion(self.input_text.value)
        progressbar = ProgressBar(width=300)
        progressbar.visible = False
        progressbar.value = 0

        # esta funcion muestra un check cuando termina la descarga
        def open_icon_check():

            self.page.overlay.append(self.icon_check_dialog)
            self.icon_check_dialog.open = True
            self.page.update()
            print("-- antees de descargar dentro de check")
            downloader.download_song_only_audio()
            print("-- despues de descargar dentro de check")
            self.icon_check_dialog.open = False
            self.page.update()

        # numero de progreso de descarga
        num_progress = Text(
            selectable=True,
            weight=FontWeight.W_500,
            color="black",
            size=14
        )

        # esta funcion se crea con todo el container para darle interactividad a la bara de progreso
        def progress():
            progressbar.visible = True

            for i in range(0, 101):
                progressbar.value = i*0.01
                num_progress.value = f"{i}%"
                time.sleep(0.01)
                self.page.update()

        # condicional para confirmar que si se introdujo el link el tipo de archivo y resolucion
        if not self.input_text.value or not self.file_type.value or not self.resolution.value:

            # se muestra la alerta si no se introdujo nada en los campos
            self.dlg_modal.content = Text("incompleted Spaces", weight=FontWeight.W_500, size=20)
            print("en if no")
            self.open_dialog()

        # si estan completos los inputs pasa aqui
        elif self.input_text.value and self.file_type.value and self.resolution.value:

            print("en else")
            # si el input de tipo de archivo es Audio y si hay conexioon a internet procede a descargar el audio
            if self.file_type.value == "Audio" and downloader.conexion_wifi:

                try:

                    # extraer la informacion de la cancion
                    downloader.song_info()

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
                            margin=10,
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
                                                # boton para reproducir la cancion o video, aun sin funcionalidad
                                                IconButton(icons.PLAY_CIRCLE_OUTLINE),
                                                Column(width=10)
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
                                        offset=Offset(-6, 8),
                                        blur_style=ShadowBlurStyle.NORMAL,
                                        color="#084107"
                                        )
                        
                        )
                    )

                    # se llama la funcion de barra de progrso 
                    progress()

                    # se confirma la informacion extraida de la cancion 
                    if downloader.title and downloader.author and downloader.end_time:
                        try:
                            # se descarga la cancion
                            print("antes de descargar y el icono")
                            open_icon_check()
                            # self.icon_check_dialog.open = False
                            print("-- despues de descargar y mostrar check")
                            # self.downloader.download_song_only_audio()
                            # print("despues de descargar y el icono")
                        except TypeError:
                            # si ocurre algun error me muestra la alerta
                            self.dlg_modal.content(Text("Downloaded not completed"))
                            self.open_dialog()
                except:

                    try:
                        requests.get(downloader.link)
                        # confirm = True
                    except requests.exceptions.MissingSchema:
                        print("tipo de error 1", TypeError)
                        self.dlg_modal.content = Text("Link error", weight=FontWeight.W_500, size=20)
                        self.open_dialog()
                    except requests.ConnectionError:
                        print("tipo de error 2", type)
                        self.dialog_check_wifi_in_progress()
                        print("despues de el check icon ")
                    finally:
                        self.page.update()
                self.page.update()

                """
                aqui se confira cuando es video, la funcionalidad es la misma que con la cancion, 
                solo cambia la funcion para descargar el video 
                """

            elif self.file_type.value == "Video" and downloader.conexion_wifi:

                try:
                    downloader.song_info()
                    path = downloader.miniatura_path
                    new_path = path.replace("\\", "/").replace("C:", "")

                    self.songs_list.controls.append(
                        Container(
                            height=110,
                            margin=10,
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
                                                IconButton(icons.PLAY_CIRCLE_OUTLINE),
                                                Column(width=10)
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
                                        offset=Offset(-6, 8),
                                        blur_style=ShadowBlurStyle.NORMAL,
                                        color="#084107"
                                        )
                        )
                    )
                    progress()
                    if downloader.title and downloader.author and downloader.end_time:
                        try:
                            # esta es la funcion para descargar el video
                            open_icon_check()
                            # downloader.download_video()
                        except TypeError:
                            self.dlg_modal.content(Text("Downloaded not completed"))
                except :

                    try:
                        requests.get(downloader.link)
                        # confirm = True
                    except requests.exceptions.MissingSchema:
                        print("tipo de error 1", TypeError)
                        self.dlg_modal.content = Text("Link error", weight=FontWeight.W_500, size=20)
                        self.open_dialog()
                    except requests.ConnectionError:
                        print("tipo de error 2", type)
                        self.dialog_check_wifi_in_progress()
                        print("despues de el check icon ")
                    finally:
                        self.page.update()
                self.page.update()
            elif not downloader.conexion_wifi:
                self.dialog_check_wifi_in_progress()
        self.Download_button.disabled = False
        self.page.update()


    # metodo para iniciar el programa
    def start(self):

        # se verifica el wifi con el metodo de la clase cancion si  
        self.downloader_2.check_wifi()

        # si esta en True me inicia el programa
        if self.downloader_2.conexion_wifi:
            self.page.add(self.container_1)

            """
            si esta en False se iniciara el programa igualmente pero con la funcion que muestra la alerta de conexion de wifi.
            lo separe en un condicional ya que si inicio el programa directamente y luego pogo la funcion de alerta de coneccion
            me mostrara la alerta de coneccion etablecida y la idea es que no me muestre nada si ya esta la coneccion
            """
        else:
            self.page.add(self.container_1)
            self.dialog_check_wifi_initial()
        self.page.update()


# funcion para arracar el programa
def inicio(page):
    app = Dowloader_app(page)
    app.start()
    page.update()

flet.app(target=inicio)



"""
para poder reproducir la musica sera necesario convertir la musica descargada mp3 a WAV, 
luego guardarla en el ordenador, esa ruta de la cacnion co WAV se reproduce con pygame.
pero ademas se tendra que eliminar el archivo mp3 para liberar espacio y que no quede duplicada la cancio
"""
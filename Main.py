from pytubefix import YouTube
import requests
import os
import flet
import time

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
    ProgressBar
)

class Cancion:


    def __init__(self, link):

        self.link = link
        self.author = ""
        self.end_time = ""
        self.title = ""
        self.miniatura_path = ""
        self.register_progress = int()
        self.confirm_download = False

    def download_song_only_audio(self):
        
        yt = YouTube(self.link, on_progress_callback=self.progres)
        print(f"- antes download: {self.register_progress}")

        audio = yt.streams.get_audio_only()
        file_path = os.path.expanduser("~\\Music")
        print(file_path)
        audio.download(output_path=file_path)
        # bar.value = self.register_progress
        # print(f"despues del download: {self.register_progress}")


    def progres(self, stream, chunk, bytes_remaining):

        total_size = stream.filesize
        print(f"- tamaño total: {total_size}")
        bytes_downloades = total_size - bytes_remaining
        print(f"- bytes restantes: {bytes_downloades}")
        self.register_progress = bytes_downloades / total_size * 100
        print(f"- progreso: {self.register_progress}")

    def download_video(self):

        yt = YouTube(self.link)
        
        video = yt.streams.filter(progressive=True).first()
        file_path = os.path.expanduser("~\\Videos")
        print("-- path video", file_path)
        video.download(output_path=file_path)
            


    def song_info(self):

        yt = YouTube(self.link)
        self.title = yt.title
        print(f"titulo: {yt.title}")

        self.author = yt.author
        print(f"autor: {self.author}")
        audio = yt.streams.get_audio_only()

        time = yt.length
        hours = time//60
        print
        minutes = int(hours%60)
        seconds = minutes%60
        self.end_time = f"{hours}:{minutes}:{seconds}"
        print(f"tiempo: {self.end_time}")

        miniatura = yt.thumbnail_url
        download = requests.get(miniatura)
        download_foulder = os.path.expanduser("~\\Downloads")
        self.miniatura_path = os.path.join(download_foulder, f"{self.title}.png")

        with open(self.miniatura_path, 'wb') as file:
            file.write(download.content)
        pass


class Dowloader_app:

    def __init__(self, page):
        self.page = page
        self.message = ""

        self.input_text = TextField(
                                    label="Paste link",
                                    bgcolor="white",
                                    multiline=False,
                                    border_radius=18,
                                    expand=True,
                                    
        )


        self.songs_list = ListView(
            spacing=-15,
            expand=True,
            reverse=True,
            auto_scroll=True
        )

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

        self.page.window.width = 900
        self.page.window.height = 600

        self.page.window.center()
        self.page.update()

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
        
        self.container_3 = Container(
            margin=15,
            content=self.row_widgets_1
        )
        
        self.row_download_button = Row(
            controls=[
                self.Download_button
            ],
            alignment=flet.MainAxisAlignment.CENTER
        )

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

        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("!Upss", weight=FontWeight.W_600, size=24),
            content=Text("Link provied error :(", weight=FontWeight.W_500, size=20),
            actions=[
                TextButton("OK", on_click=self.close_dialog)
            ],
            actions_alignment=MainAxisAlignment.END,
        )

    def open_dialog(self):
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()
    
    def close_dialog(self, e):
        self.dlg_modal.open = False
        self.page.update()

    # funtions
    def download_song_UI(self, e):
        downloader = Cancion(self.input_text.value)
        print("ingresando a la funcion")

        progressbar = ProgressBar(width=300)
        progressbar.visible = False
        progressbar.value = 0

        num_progress = Text(
            selectable=True,
            weight=FontWeight.W_500,
            color="black",
            size=14
        )

        def progress():
            print("- Ingresando a progressbar")
            # num_1 = int(num)
            progressbar.visible = True

            for i in range(0, 101):
                # print(f"bucle dentro de progres {i}")
                progressbar.value = i*0.01
                num_progress.value = f"{i}%"
                time.sleep(0.01)
                self.page.update()




        if not self.input_text.value and self.file_type and self.resolution.value:
            print("espacios vacios ingrese un  link")

        else:
            print("ingresando al else")


            if self.file_type.value == "Audio":

                try:

                    print("ingresando a if del else")
                    print("ingresando al try")
                    downloader.song_info()
                    path = downloader.miniatura_path
                    new_path = path.replace("\\", "/").replace("C:", "")

                    print(new_path)
                    print(downloader.link)

                    self.songs_list.controls.append(
                        Container(
                            height=110,
                            margin=10,
                            padding=-7,
                                content=Container(
                                # bgcolor="red",
                                margin=10,
                                content=Row(
                                controls=[
                                    Container(
                                    # height=160,
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
                                    # width=500,
                                    # height=100,
                                    controls=[
                                    Container(
                                        # bgcolor="red",
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
                                    # bgcolor="black",
                                    # width=100,
                                    # margin=10,
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
                                bgcolor="white", # #1CBF1A
                                border_radius=15,
                                shadow=BoxShadow(
                                        spread_radius=1,
                                        blur_radius=3,
                                        offset=Offset(-5, 8),
                                        blur_style=ShadowBlurStyle.NORMAL,
                                        color="#084107"
                                        )
                        
                        )
                    )
                    progress()
                    if downloader.title and downloader.author and downloader.end_time:
                        try:
                            downloader.download_song_only_audio()
                        except TypeError:
                            print(TypeError)
                            self.dlg_modal.content(Text("Downloaded not completed"))
                except :
                    self.open_dialog()
                self.page.update()

            elif self.file_type.value == "Video":

                try:

                    print("ingresando a if del else")
                    print("ingresando al try")
                    downloader.song_info()
                    path = downloader.miniatura_path
                    new_path = path.replace("\\", "/").replace("C:", "")

                    print(new_path)
                    print(downloader.link)

                    self.songs_list.controls.append(
                        Container(
                            height=110,
                            margin=10,
                            padding=-7,
                                content=Container(
                                # bgcolor="red",
                                margin=10,
                                content=Row(
                                controls=[
                                    Container(
                                    # height=160,
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
                                    # width=500,
                                    # height=100,
                                    controls=[
                                    Container(
                                        # bgcolor="red",
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
                                    # bgcolor="black",
                                    # width=100,
                                    # margin=10,
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
                                bgcolor="white", # #1CBF1A
                                border_radius=15,
                                shadow=BoxShadow(
                                        spread_radius=1,
                                        blur_radius=3,
                                        offset=Offset(-5, 8),
                                        blur_style=ShadowBlurStyle.NORMAL,
                                        color="#084107"
                                        )
                        
                        )
                    )
                    progress()
                    if downloader.title and downloader.author and downloader.end_time:
                        try:
                            downloader.download_video()
                        except TypeError:
                            print(TypeError)
                            self.dlg_modal.content(Text("Downloaded not completed"))
                except :
                    self.open_dialog()
                self.page.update()

    def start(self):
        self.page.add(self.container_1)
        self.page.update()

def inicio(page):
    app = Dowloader_app(page)
    app.start()
    page.update()

flet.app(target=inicio)
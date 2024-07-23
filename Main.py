from pytubefix import YouTube
import requests
import os
import flet

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
    ButtonStyle
)

class Cancion:


    def __init__(self, link):
        self.link = link
        self.author = ""
        self.end_time = ""
        self.title = ""
        self.miniatura_path = ""

    def download_song_only_audio(self):
        
        yt = YouTube(self.link)
        tittle = yt.title

        audio = yt.streams.get_audio_only()
        file_path = os.path.expanduser("~\\Music")
        print(file_path)
        final_path = os.path.join(file_path)
        print(final_path)
        audio.download(output_path=final_path)

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
        dowload = requests.get(miniatura)
        download_foulder = os.path.expanduser("~\\Downloads")
        self.miniatura_path = os.path.join(download_foulder, f"{self.title}.png")

        with open(self.miniatura_path, 'wb') as file:
            file.write(dowload.content)
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

        self.Dowload_button = ElevatedButton(
                                            "Download",
                                            icon=icons.DOWNLOAD_ROUNDED,
                                            width=240,
                                            height=50,
                                            icon_color="#0B440A",
                                            color="#107D0E",
                                            bgcolor="white",
                                            on_click=self.download_song
        )

        self.page.window.width = 900
        self.page.window.height = 600

        self.page.window_center()
        self.page.update()

        self.file_type = Dropdown(
            label="File type",
            width=110,
            height=50,
            border_color="#107D0E",
            bgcolor="white",
            border_radius=15,
            options=[
                dropdown.Option("audio"),
                dropdown.Option("video"),


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
        
        self.row_dowload_button = Row(
            controls=[
                self.Dowload_button
            ],
            alignment=flet.MainAxisAlignment.CENTER
        )

        self.container_2 = Container(
            content=Column(
                controls=[
                    self.container_3,
                    self.row_dowload_button,
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
    def download_song(self, e):
        print("ingresando a la funcion")

        if not self.input_text.value and self.file_type and self.resolution.value:
            print("espacios vacios ingrese un  link")

        else:
            print("ingresando al else")


            if self.file_type.value == "audio":

                try:

                    print("ingresando a if del else")
                    print("ingresando al try")
                    dowloader = Cancion(self.input_text.value)
                    dowloader.song_info()
                    path = dowloader.miniatura_path
                    new_path = path.replace("\\", "/").replace("C:", "")

                    print(new_path)
                    print(dowloader.link)

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
                                                value=dowloader.title,
                                                selectable=True,
                                                weight=FontWeight.W_700,
                                                color="black",
                                                size=23

                                        ),
                                    ),
                                    Row(
                                        controls=[
                                                Text(
                                                    value=dowloader.author,
                                                    selectable=True,
                                                    weight=FontWeight.W_600,
                                                    color="black",
                                                    size=17
                                                ),
                                                Text(
                                                    value=dowloader.end_time,
                                                    selectable=True,
                                                    weight=FontWeight.W_500,
                                                    color="black",
                                                    size=14
                                                )
                                            ]
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
                                                IconButton(icons.PLAY_CIRCLE_OUTLINE)
                                            ],
                                            alignment=flet.MainAxisAlignment.END
                                                )
                                            )
                                        ],
                                    # alignment=flet.MainAxisAlignment.SPACE_AROUND
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
                    if dowloader.title and dowloader.author and dowloader.end_time:
                        try:
                            dowloader.download_song_only_audio()
                        except TypeError:
                            print(TypeError)
                            # self.open_dialog("Link provied error")
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
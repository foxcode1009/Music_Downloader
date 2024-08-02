"""
botones para reproducir la musica
Container(
        expand=True,
        content=Row(
            controls=[
                
                    IconButton(
                            icon=icons.PLAY_CIRCLE_OUTLINE,
                            on_click=lambda x: get_identificator(x.control.data),
                            data=code
                            ),
                    IconButton(
                            icon=icons.PAUSE_CIRCLE_OUTLINE_ROUNDED,
                            data=code,
                            on_click=self.pause
                            ),
                    Column(width=10),
                    ],
                    alignment=flet.MainAxisAlignment.END
                    )
                )

funcion para obtener el identificador del contenedor

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

funciones para reproducir musica

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
    
    def pause(self, e):
        # self.audio.autoplay = False
        self.audio.pause()
        self.page.update()
        print(self.audio.autoplay)
        print("-- saliendo de pause")
"""
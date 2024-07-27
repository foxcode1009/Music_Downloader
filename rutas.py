import os
rutas_check = False
tittle = "Anuel - Ayer ft Dj Nelson [Official Video].mp4"
print(tittle)
if os.path.exists(os.path.expanduser("~\\Videos\\"+tittle)):
    print("1", os.path.expanduser("~\\Videos\\"+tittle))
    print("-- archivo existente")
    print(rutas_check)
    rutas_check = True
    print(rutas_check)
else:
    print("-- no existe")

print(f"saliendo: {rutas_check}")
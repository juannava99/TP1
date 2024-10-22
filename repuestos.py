from url import conexion
from pymongo import MongoClient

mongo_url = conexion
print(conexion)

cliente = MongoClient(host=[mongo_url])

#print(cliente.list_database_names())

db = cliente["repuestos_tp1"]

colleccion = db["repuestos"]

#documento = {"nombre": "Juan", "edad": 30, "ciudad": "Buenos Aires", "lista" : [1,5,"no",True]}
#documento = {"nombre": "Juan", "edad": 30, "ciudad": "Buenos Aires", "lista" : [1.5,5,"no",True]}
#resultado = colleccion.insert_one(documento)
#print(f"Documento insertado con ID: {resultado.inserted_id}")

filtro = {"lista" : 1.5}
documentos = colleccion.find(filtro)

for documento in documentos:
    print(documento)


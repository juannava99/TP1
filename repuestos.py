from datos import conexion,base_datos,coleccion
from pymongo import MongoClient


#documento = {"nombre": "Juan", "edad": 30, "ciudad": "Buenos Aires", "lista" : [1,5,"no",True]}
#documento = {"nombre": "Juan", "edad": 30, "ciudad": "Buenos Aires", "lista" : [1.5,5,"no",True]}
#resultado = colleccion.insert_one(documento)
#print(f"Documento insertado con ID: {resultado.inserted_id}")

#filtro = {"lista" : 1.5}

#documentos = colleccion.find(filtro)

#for documento in documentos:
    #print(documento)

datos_repuesto = ("Precio","SKU","Nombre","Marca","Compatible")

def existe_sku(repuesto):
    es_valido = False
    if repuesto is None:
            es_valido = True
    else:
        print("El SKU ingresado ya existe, porfavor ingrese otro.")
    return es_valido

def no_existe_sku(repuesto):
    es_valido = False
    if repuesto is not None:
            es_valido = True
    else:
        print("El SKU ingresado no existe, porfavor ingrese otro.")
    return es_valido


def validar_sku(coleccion_repuestos,func):
    es_valido = False
    while not es_valido:
        sku_valido = False
        while not sku_valido:
            sku = input("Ingresar el ´SKU´ del repuesto: ")
            if len(sku) == 8:
                sku_valido = True
            else:
                print("El sku ingresado es invalido, debe de tener 8 caracteres")
        filtro = {datos_repuesto[1] : sku}
        repuesto = coleccion_repuestos.find_one(filtro)
        es_valido = func(repuesto)
    return sku

    

def validar_precio():
    precio_valido = False
    while not precio_valido:
        precio = validar_numero("Ingresar el precio del repuesto: ")
        if 0 < precio:
            precio_valido = True
        else:
            print("La opcion ingresada no es valida, tiene que ser mayor a 0")
    return precio

def validar_numero(mensaje):
    no_es_valido = True
    while no_es_valido:
        try:
            numero = float(input(mensaje))
            no_es_valido = False 

        except:
            print("Error en el ingreso de datos, debe de ingresar un numero")
    return numero

def validar_respuesta(mensaje):
    continuar = True
    seguir = True
    respuesta = input(f"{mensaje}, Presione ´S´ para continuar , ´N´ para no continuar: ")
    while continuar:
        if respuesta.upper() == "S":
            continuar = False
        elif respuesta.upper() == "N": 
            continuar = False
            seguir = False
        else:
            respuesta = input(f"La respuesta ingresa es invalida, Debe ingresar ´S´ para continuar , ´N´ para no continuar: ")
    return seguir

def lista_modelos_compatibles(modelos_compatibles):
    actualizar_mas = True
    if  not modelos_compatibles:
        while actualizar_mas:
             modelos_compatible = input("Ingrese un modelo compatible con el repuesto ingresado: ")
             modelos_compatibles.append(modelos_compatible)
             actualizar_mas = validar_respuesta("Quiere ingresar mas modelos compatibles ?")
    else:
        while actualizar_mas:
            imprimir_menu_modificar_modelo(modelos_compatibles)
            opcion = validar_opciones(imprimir_menu_modificar_repuesto,1,2)
            if opcion == 1:
                modelos_compatible = input("Ingrese un modelo compatible con el repuesto ingresado: ")
                modelos_compatibles.append(modelos_compatible)
            else:
                print("Que modelo quiere eliminar")
                modelo_seleccionado = validar_opciones(imprimir_menu_modificar_modelo,0,len(modelos_compatibles),modelos_compatibles)
                del modelos_compatibles[int(modelo_seleccionado)]
            actualizar_mas = validar_respuesta("Quiere modifcar algun modelo compatibles ?")
            

    return modelos_compatibles


def ingresar_accesorio(coleccion_repuestos):
    
    precio = validar_precio()
    sku= validar_sku(coleccion_repuestos,existe_sku)
    nombre = input("Ingresar el nombre del repuesto: ")
    marca = input("Ingresar la marca del repuesto: ")
    compatible = lista_modelos_compatibles([])
    repuesto = {datos_repuesto[0]:precio,datos_repuesto[1]:sku,datos_repuesto[2]:nombre,datos_repuesto[3]:marca,datos_repuesto[4]:compatible}
    coleccion_repuestos.insert_one(repuesto)

def modificar_accesorios(coleccion_respuestos):
    print("Opcion Modificar Repuesto")
    sku = validar_sku(coleccion_respuestos,no_existe_sku)
    print("Que especificacion del repuesto desea modificar:")
    opcion = validar_opciones(imprimir_menu_modificar,0,5)
    filtro = {datos_repuesto[1] : sku}
    if opcion == 0:
        acualizacion = {"$set": {datos_repuesto[0]: validar_precio()}}
    elif opcion == 1:
        sku_modificar = validar_sku(coleccion_respuestos,existe_sku)
        acualizacion = {"$set": {datos_repuesto[1]: sku_modificar}}
    elif opcion == 2:
        acualizacion = {"$set": {datos_repuesto[2]: input("Ingresar el nombre del repuesto: ")}}
    elif opcion == 3:
        acualizacion = {"$set": {datos_repuesto[3]: input("Ingresar la marca del repuesto: ")}}
    elif opcion == 4:
        repuesto = coleccion_respuestos.find_one(filtro)
        acualizacion = {"$set": {datos_repuesto[4]: lista_modelos_compatibles(repuesto.get(datos_repuesto[4],[]))}}
    if opcion != 5 : 
        coleccion_respuestos.update_one(filtro,acualizacion)
        print("El repuesto se ha modificado con exito")

def eliminar_accesorio(coleccion_repuestos):
    print("Opcion Eliminar Repuesto")
    sku = validar_sku(coleccion_repuestos,no_existe_sku)
    continuar = True
    respuesta = validar_respuesta(f"Desea eliminar el repuesto con el siguiente ´SKU´: {sku},")
    if respuesta:
        filtro = {datos_repuesto[1] : sku}
        coleccion_repuestos.delete_one(filtro)
        print(f"Se elimino el repuesto ´SKU´: {sku} correctamente")
        
    else:
        print(f"No elimino el repuesto ´SKU´: {sku}")

def consultar_accesorios(coleccion_repuestos ):
    repuestos = coleccion_repuestos.find()
    valor = " "
    print("Lista de accesorios")
    print(f"\n{datos_repuesto[0]}{valor.rjust(10)} {datos_repuesto[1]}{valor.rjust(12)} {datos_repuesto[2]}{valor.rjust(14)} {datos_repuesto[3]} {valor.rjust(10)} {datos_repuesto[4]} {valor.rjust(10)}")
    for dato in repuestos:
        compatible_str = ', '.join(dato[datos_repuesto[4]]) if isinstance(dato[datos_repuesto[4]], list) else dato[datos_repuesto[4]]
        print(f"{str(dato[datos_repuesto[0]]).ljust(10)}{(dato[datos_repuesto[1]]).center(20)}{(dato[datos_repuesto[2]]).center(12)}{(dato[datos_repuesto[3]]).rjust(16)} {compatible_str.center(32)}")
    
def consultar_accesorio_especifico(coleccion_respuestos):
    sku = validar_sku(coleccion_respuestos,no_existe_sku)
    filtro = {datos_repuesto[1] : sku}
    repuesto = coleccion_respuestos.find_one(filtro)
    valor = " "
    print("\nAcesorio especifico encontrado:\n")
    print(f"{datos_repuesto[0]}{valor.rjust(10)} {datos_repuesto[1]}{valor.rjust(12)} {datos_repuesto[2]}{valor.rjust(14)} {datos_repuesto[3]} {valor.rjust(10)} {datos_repuesto[4]}{valor.rjust(10)} ")
    compatible_str = ', '.join(repuesto[datos_repuesto[4]]) if isinstance(repuesto[datos_repuesto[4]], list) else repuesto[datos_repuesto[4]]
    print(f"{str(repuesto[datos_repuesto[0]]).ljust(10)}{(repuesto[datos_repuesto[1]]).center(20)}{(repuesto[datos_repuesto[2]]).center(12)}{(repuesto[datos_repuesto[3]]).rjust(16)} {compatible_str.center(32)}")

def imprimir_menu_modificar():
    for i in range(len(datos_repuesto)):
        print(f"Opcion {i} {datos_repuesto[i]} ")
    print("Opcion 5 Salir")

def imprimir_menu_modificar_repuesto():
    print("1: Agregar \n2: Eliminar ")

def imprimir_menu_modificar_modelo(modelos_compatibles):
    print("Modelos compatibles registrados")
    for i,modelo in enumerate(modelos_compatibles): 
        print(f"#{i} Modelo: {modelo}  ")

def validar_opciones(menu_imprimir,numero_menor,numero_mayor,*args):
    opcion_valida = False
    while not opcion_valida:
        menu_imprimir(*args)
        opcion = validar_numero("Ingresar una opcion: ")
        if numero_menor - 1 < opcion < numero_mayor + 1:
            opcion_valida = True
        else:
            print(f"La opcion ingresada no es valida, tiene que ser entre {numero_menor} y {numero_mayor}")
    return opcion

def imprimir_menu():
    print("\nMenu")
    print("1 Ingresar nuevos accesorios.")
    print("2 Modificar accesorios.")
    print("3 Eliminar accesorios.")
    print("4 Consultar todos los accesorios")
    print("5 Consultar por un accesorio determinado. (sku)")
    print("6 Salir\n")


def main():
    mongo_url = conexion
    cliente = MongoClient(host=[mongo_url])
    db = cliente[base_datos]
    coleccion_repuestos = db[coleccion]
    continuar = True
    while continuar:
        opcion = validar_opciones(imprimir_menu,1,6)
        cant_repuestos = coleccion_repuestos.count_documents({})
        if opcion == 1: ingresar_accesorio(coleccion_repuestos)
        elif coleccion_repuestos.count_documents({}) > 0 and opcion != 6:
            if opcion == 2: modificar_accesorios(coleccion_repuestos)
            elif opcion == 3: eliminar_accesorio(coleccion_repuestos)
            elif opcion == 4: consultar_accesorios(coleccion_repuestos)
            elif opcion == 5: consultar_accesorio_especifico(coleccion_repuestos)
        elif coleccion_repuestos.count_documents({}) == 0 and opcion != 6: 
            print(f"\nNo se encuentra registrado ningun repuesto")        
        else: continuar = False

if __name__ == "__main__":
    main()
from flask import Flask, render_template, request, redirect, url_for                    #LIBRERIAS
import os                                           #importacón de librería os
import pymongo          #libreria para la conexion con mongo
import json
from werkzeug.security import generate_password_hash, check_password_hash       #libreria para encriptar y desencriptar

MONGO_HOST="localhost"          #servidor local para la conexion
MONGO_PUERTO="27017"            #puerto para la conexion
MONGO_TIEMPO_FUERA=1000

MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"          #concatenacion para la conexcion del mongo

MONGO_BASEDATOS="Escuela"           #nombre de la base de datos
MONGO_COLLECTION="Personas"           #nombre de la coleccion para la validacion
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
baseDatos=cliente[MONGO_BASEDATOS]          #asigna el nombre de la bdd a una variable
ColeccionPersonas=baseDatos[MONGO_COLLECTION]      #asigna el nombre de la coleccion a una variable    
#return a list of all collections in your database
#print(baseDatos.list_collection_names())

# Inicializar la aplicacion
app = Flask(__name__, template_folder='templates')              #indica la carpte de los templates
app._static_folder = os.path.abspath("templates/static/")                       #Carpeta static de los templates


@app.route('/', methods=['GET','POST'])         # Ruta principal 
def home():
    return render_template("layouts/home.html")


@app.route('/loginAdmin', methods=['GET','POST'])        
def loginAdmin():
    if(request.method == "POST"):
        user = request.form['Usuario']          #obtencion de correo
        contrase = request.form['password']         #obtencion de contraseña
        try:
            if(ColeccionPersonas.find_one({'Usuario':user, 'Contraseña': contrase, 'Rol':"Admin"})):        #compara los datos ingresados con el registro     
                return redirect(url_for('administrador'))  
            else:
                return redirect(url_for('loginAdmin'))            #si no esta registrado redirecciona a la pagina principal
        except:
            return redirect(url_for('loginAdmin'))             #en caso de error redirecciona a la pagina principal

    return render_template("layouts/loginAdmin.html")

@app.route('/administrador', methods=['GET','POST'])       
def administrador():  
    if(request.method == "POST"):
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['email']
        contraseña = request.form['contraseña']
        rol = request.form['DocenteRol']
        encripta=generate_password_hash(contraseña)
        dato = {"nombre": nombre, "apellido":  apellido, "correo": correo, "contraseña": encripta, "Rol": rol}
        ColeccionPersonas.insert_one(dato)

    Docentes = baseDatos['Personas']
    DocentesReceived = Docentes.find()

    Usuarios = baseDatos['Personas']
    UsuariosReceived = Usuarios.find()

    Roles = baseDatos['Roles']
    RolesReceived = Roles.find()

    Cursos = baseDatos['Cursos']
    CursosReceived = Cursos.find()

    CursosMuestra = baseDatos['Cursos']
    CursosMuestraReceived = CursosMuestra.find()

    Estudiantes = baseDatos['Estudiantes']
    EstudiantesReceived = Estudiantes.find()

    return render_template("layouts/administrador.html", Docentes = DocentesReceived, Roles = RolesReceived, Usuarios = UsuariosReceived,
    Curso = CursosReceived, CursosMuestra=CursosMuestraReceived, Estudiantes = EstudiantesReceived) 


@app.route('/EliminarDocente', methods=['GET','POST'])  
def EliminarDocente():  
    if(request.method == "POST"):
        try:
            correo = request.form['email']
            print(correo)
            ColeccionPersonas.delete_one({"correo": correo})
        except:
            return redirect(url_for('administrador'))
    return redirect(url_for('administrador'))


@app.route('/loginDocentes', methods=['GET','POST'])         
def loginDocentes():
    if(request.method == "POST"):
        correo = request.form['email']          #obtencion de correo
        contrase = request.form['password']         #obtencion de contraseña   
        try:
            dato = ColeccionPersonas.find_one({'correo': correo})
            if check_password_hash(dato["contraseña"], contrase ):
                return redirect(url_for('Niño')) 
            else:
                return redirect(url_for('loginDocentes'))
        except:
            return redirect(url_for('loginDocentes'))
    return render_template("layouts/loginDocente.html")


@app.route('/CrearCurso', methods=['GET','POST'])       
def CrearCurso():  
    if(request.method == "POST"):
        nombreCurso = request.form['nombre']          #obtencion de correo
        nombreDocente = request.form['NombreDocente']         #obtencion de contraseña   

        MONGO_COLLECTION="Cursos"           #nombre de la coleccion para la validacion
        cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
        baseDatos=cliente[MONGO_BASEDATOS]          #asigna el nombre de la bdd a una variable
        ColeccionCursos=baseDatos[MONGO_COLLECTION] 

        dato = {"Curso": nombreCurso, "Docente":  nombreDocente}
        ColeccionCursos.insert_one(dato)
        return redirect(url_for('loginDocentes'))

    return render_template("layouts/administrador.html" ) 


@app.route('/RegistrarNiño', methods=['GET','POST'])       
def RegistrarNiño():  
    if(request.method == "POST"):
        nombre = request.form['Nombre']          #obtencion de correo
        apellido = request.form['Apellido']         #obtencion de contraseña  
        fecha = request.form['Fecha'] 

        MONGO_COLLECTION="Estudiantes"           #nombre de la coleccion para la validacion
        cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
        baseDatos=cliente[MONGO_BASEDATOS]          #asigna el nombre de la bdd a una variable
        ColeccionEstudiantes=baseDatos[MONGO_COLLECTION] 

        dato = {"Nombre": nombre, "Apellido":  apellido, "Fecha_Nacimiento": fecha, "Rol": "Estudiante"}
        ColeccionEstudiantes.insert_one(dato)
        return redirect(url_for('administrador'))

    return render_template("layouts/administrador.html" ) 


@app.route('/EliminarNiño', methods=['GET','POST'])  
def EliminarNiño():  
    if(request.method == "POST"):
        try:
            nombre = request.form['nombre']
            MONGO_COLLECTION="Estudiantes"           #nombre de la coleccion para la validacion
            cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
            baseDatos=cliente[MONGO_BASEDATOS]          #asigna el nombre de la bdd a una variable
            ColeccionEstudiantes=baseDatos[MONGO_COLLECTION] 
            ColeccionEstudiantes.delete_one({"Nombre": nombre})
        except:
            return redirect(url_for('administrador'))
    return redirect(url_for('administrador'))


@app.route('/Niño' , methods=['GET','POST'])        #ruta de la pagina niño, tiene entrada de datos por medio del metodo post
def Niño():     #funcion que renderiza el archivo niño.html
    if(request.method == "POST"):        #si detecta ingreso de datos por el metodo post   
        juan = request.form['juan1']     
        sofia = request.form['sofia1']
        try:   
            print(juan)
            print(sofia)
            return redirect(url_for('Juego'))
        except:
            return redirect(url_for('Niño'))
    return render_template("layouts/Niño.html")   #renderiza el template


@app.route('/NiñosB' )        #ruta de la pagina niño de otro curso,
def NiñosB():  #funcion que renderiza el archivo niñosb.html
    return render_template("layouts/NiñosB.html")       #renderiza el template



@app.route('/Juego')        #ruta de la pagina para el juego, 
def Juego():    #funcion que renderiza el archivo juegos.html
    return render_template("layouts/Juego.html")     #renderiza el template


#funcion que recive el puntaje del archivo javascript
@app.route('/Resultado', methods=['POST'])      #tiene entrada de datos por medio del metodo post
def test():
    output = request.get_json()
    result = json.loads(output)     #convierte de json a diccionario de python
    print(result) # imprime el puntaje
    return result


#main del programa
if __name__ == '__main__':
    app.run(debug=True) # Ejecuta la aplicacion




#DATOS ADMIN PAGINA
'''
dato = {"Usuario": "@Admin", "Contraseña": "@Admin", "Rol":"Admin"}
ColeccionPersonas.insert_one(dato)    
'''

#DATOS ROLES
'''
MONGO_COLLECTION="Roles"           #nombre de la coleccion para la validacion
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
baseDatos=cliente[MONGO_BASEDATOS]          #asigna el nombre de la bdd a una variable
ColeccionRoles=baseDatos[MONGO_COLLECTION] 

dato = {"Rol": "Admin"}
dato1 = {"Rol": "Estudiante"}
dato2 = {"Rol": "Docente"}
ColeccionRoles.insert_one(dato)   
ColeccionRoles.insert_one(dato1)   
ColeccionRoles.insert_one(dato2)   
'''

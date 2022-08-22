from flask import Flask, render_template, request, redirect, url_for                    #LIBRERIAS
import os                                           #importacón de librería os
import pymongo          #libreria para la conexion con mongo
import json

MONGO_HOST="localhost"          #servidor local para la conexion
MONGO_PUERTO="27017"            #puerto para la conexion
MONGO_TIEMPO_FUERA=1000

MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"          #concatenacion para la conexcion del mongo

MONGO_BASEDATOS="Escuela"           #nombre de la base de datos
MONGO_COLLECTION="Profesores"           #nombre de la coleccion para la validacion
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
baseDatos=cliente[MONGO_BASEDATOS]          #asigna el nombre de la bdd a una variable
coleccionProfesor=baseDatos[MONGO_COLLECTION]      #asigna el nombre de la coleccion a una variable    
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
        correo = request.form['email']          #obtencion de correo
        contrase = request.form['password']         #obtencion de contraseña
        try:
            if(coleccionProfesor.find_one({'Correo':correo, 'Contraseña': contrase})):        #compara los datos ingresados con el registro     
                return redirect(url_for('administrador'))  
            else:
                return redirect(url_for('loginAdmin'))            #si no esta registrado redirecciona a la pagina principal
        except:
            return redirect(url_for('loginAdmin'))             #en caso de error redirecciona a la pagina principal

    return render_template("layouts/loginAdmin.html")

@app.route('/administrador' )       
def administrador():  
    return render_template("layouts/administrador.html")    


@app.route('/loginDocentes', methods=['GET','POST'])         
def loginDocentes():

    if(request.method == "POST"):
        correo = request.form['email']          #obtencion de correo
        contrase = request.form['password']         #obtencion de contraseña
        try:
            preesccolar =request.form['preescolar']   #obtencion del preescolar
        except:
            return redirect(url_for('loginDocentes'))     
                  
        try:
            if(coleccionProfesor.find_one({'Correo':correo, 'Contraseña': contrase, 'Preescolar': preesccolar })):        #compara los datos ingresados con el registro
                    if(preesccolar=="Preescolar 1"):        #si el preescolar es el curso 1:
                        return redirect(url_for('Niño'))        #ingresa a la pagina niños
                    else:
                        return redirect(url_for('NiñosB'))  #si no al otro curso
            else:
                return redirect(url_for('loginDocentes'))            #si no esta registrado el profesor redirecciona a la pagina principal
        except:
            return redirect(url_for('loginDocentes'))             #en caso de error redirecciona a la pagina principal

    return render_template("layouts/loginDocente.html")


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



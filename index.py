from flask import Flask, render_template, request, redirect, url_for                    #LIBRERIAS
import os                                           #importacón de librería os
import pymongo
import json

MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000

MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

MONGO_BASEDATOS="Escuela"
MONGO_COLLECTION="Profesores"
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
baseDatos=cliente[MONGO_BASEDATOS]
coleccionProfesor=baseDatos[MONGO_COLLECTION]
#return a list of all collections in your database
#print(baseDatos.list_collection_names())

# Inicializar la aplicacion
app = Flask(__name__, template_folder='templates')
app._static_folder = os.path.abspath("templates/static/")                       #Carpeta static de los templates


@app.route('/', methods=['GET','POST'])         # Ruta principal 
def home():

    if(request.method == "POST"):
        correo = request.form['email']          #obtencion de correo
        contrase = request.form['password']         #obtencion de contraseña
        preesccolar =request.form['preescolar'] 
        try:
            if(coleccionProfesor.find_one({'Correo':correo, 'Contraseña': contrase, 'Preescolar': preesccolar })):        #compara los datos ingresados con el registro
                if(preesccolar=="Preescolar 1"):
                    return redirect(url_for('Niño')) 
                else:
                    return redirect(url_for('NiñosB')) 
            else:
                return redirect(url_for('home'))   
        except:
            return redirect(url_for('home'))

    return render_template("layouts/loginDocente.html")


@app.route('/Niño' , methods=['GET','POST'])        
def Niño(): 
    if(request.method == "POST"):
        juan = request.form['juan1']     #obtencion de correo
        sofia = request.form['sofia1']
        try:   
            print(juan)
            print(sofia)
            return redirect(url_for('Juego'))
        except:
            return redirect(url_for('Niño'))
    return render_template("layouts/Niño.html")


@app.route('/NiñosB' )        
def NiñosB(): 
    return render_template("layouts/NiñosB.html")



@app.route('/Juego')        
def Juego(): 
    return render_template("layouts/Juego.html")



@app.route('/Resultado', methods=['POST'])
def test():
    output = request.get_json()
    result = json.loads(output) #this converts the json output to a python dictionary
    print(result) # Printing the new dictionary
    return result




if __name__ == '__main__':
    app.run(debug=True) # Ejecuta la aplicacion



const cuadro = document.querySelectorAll(".cuadro"); //Constante que seleciona los cuadros creados en el HTML
const tiempoFaltante = document.querySelector("#tiempo"); //Constante que toma tiempo ingresado en el HTML
let puntaje = document.getElementById("puntaje"); //Variable que toma el tiempo ingresado en el HTML

let resultado = 0; //el resultado final empieza en 0, para ir incrementando
let tiempoActual = tiempoFaltante.textContent; //variable que actualiza el tiempo 


/*Función que mueve el topo por los diferemtes cuadros de manera que
aleratoria, con la funicion Math.random se calcula un numero aleratorio */
function cuadroAzar() {
    cuadro.forEach((nombreDeClase) => {
        nombreDeClase.classList.remove("topo");
    });
    let posicionAlAzar = cuadro[Math.floor(Math.random() * 16)]; //calcula un numero aleratorio
    posicionAlAzar.classList.add("topo");

    posicionTopo = posicionAlAzar.id; //actualiza la posicion segun el numero al azar
}

/*Aumeta el punataje del juego segun encuentre el topo en los cuadros 
del HTML*/
cuadro.forEach((identificador) => {
    identificador.addEventListener("click", () => { //evento que controla los clicks sobre el topo y aumenta el puntaje
        if (identificador.id === posicionTopo) {
            resultado = resultado + 1; //aumenta el puntaje de 1 en 1
            puntaje.textContent = resultado;
            posicionTopo = null;
        }
    });
});

/*Funcion que mueve el topo por los cuadros cada 2 segundos*/
function moverTopo() {
    tiempoTopo = setInterval(cuadroAzar, 2000); //2000 milisegundos = 2 segundos
}

moverTopo(); //llama a la funcion moverTopo

function actualizar() { location.reload(true); } //funicion para recargar la pagina de manera automatia

/*FUNCION para la disminucion del tiempo segun los segundos ingresados en el HTML*/
function cuentaRegresiva() {
    tiempoActual--; //el tiempo disminuye
    tiempoFaltante.textContent = tiempoActual; //se actualiza el tiempo

    if (tiempoActual === 0) {
        clearInterval(idTiempo);
        clearInterval(tiempoTopo);
        /*alert("¡El tiempo ha terminado Atrapaste " + resultado + " topos!");*/

        if (resultado > 3) { //si el resultado obtentido ejecuta la siguiente instruccion 
            const music = new Audio('templates/static/audio/niños.wav'); //carga archivo de audio
            music.play(); //reproduce audio
            //ALERTA DE 6 ESTRELLAS si se completan mas de 3 puntos
            Swal.fire({
                imageUrl: 'https://static.vecteezy.com/system/resources/previews/003/795/482/non_2x/collection-of-emoticon-icon-of-cute-star-cartoon-free-vector.jpg',
                imageWidth: 400, //ancho de imagen
                imageHeight: 300, //alto de imagen
                timer: 4000, //asiganacion de tiempo para que cerrar alerta
                showConfirmButton: false, //quita la confirmacion en la alerta
            });
            music.pause(); //detiene el audio
        } else {
            //si se completan menos de 3 putos solo obtiene 3 estrellas
            Swal.fire({
                imageUrl: 'https://img.freepik.com/vector-premium/estrella-dibujos-animados-color-amarillo-brillante-forma-redondeada-estilo-gris-ilustracion-botones-interfaz-usuario-coleccion-estrellas-premio_505956-270.jpg?w=2000',
                imageWidth: 400, //ancho de imagen
                imageHeight: 300, //alto de imagen
                timer: 4000, //asiganacion de tiempo para que cerrar alerta
                showConfirmButton: false, //quita la confirmacion en la alerta
            });
        }

        const dict_values = {
                resultado
            }
            //envia el resultado obtenido hacia python por medio de ajax
        const s = JSON.stringify(dict_values);
        $.ajax({
            url: "/Resultado", //envia a la funcion resultado
            type: "POST", //envia por medio del metodo post
            contentType: "application/json",
            data: JSON.stringify(s) //envia como tipo json
        });
    }
    //Función para actualizar cada n segundos(n milisegundos)
    setInterval("actualizar()", 40000);
}

let idTiempo = setInterval(cuentaRegresiva, 500);
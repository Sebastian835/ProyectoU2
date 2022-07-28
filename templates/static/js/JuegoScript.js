const cuadro = document.querySelectorAll(".cuadro");
const tiempoFaltante = document.querySelector("#tiempo");
let puntaje = document.getElementById("puntaje");

let resultado = 0;
let tiempoActual = tiempoFaltante.textContent;

function cuadroAzar() {
    cuadro.forEach((nombreDeClase) => {
        nombreDeClase.classList.remove("topo");
    });
    let posicionAlAzar = cuadro[Math.floor(Math.random() * 16)];
    posicionAlAzar.classList.add("topo");

    posicionTopo = posicionAlAzar.id;
}

cuadro.forEach((identificador) => {
    identificador.addEventListener("click", () => {
        if (identificador.id === posicionTopo) {
            resultado = resultado + 1;
            puntaje.textContent = resultado;
            posicionTopo = null;
        }
    });
});

function moverTopo() {
    tiempoTopo = setInterval(cuadroAzar, 2000);
}

moverTopo();

function actualizar() { location.reload(true); }

function cuentaRegresiva() {
    tiempoActual--;
    tiempoFaltante.textContent = tiempoActual;

    if (tiempoActual === 0) {
        clearInterval(idTiempo);
        clearInterval(tiempoTopo);
        /*alert("¡El tiempo ha terminado Atrapaste " + resultado + " topos!");*/

        if (resultado > 3) {
            const music = new Audio('templates/static/audio/niños.wav');
            music.play();
            music.loop = true;
            music.playbackRate = 2;
            Swal.fire({
                imageUrl: 'https://static.vecteezy.com/system/resources/previews/003/795/482/non_2x/collection-of-emoticon-icon-of-cute-star-cartoon-free-vector.jpg',
                imageWidth: 400,
                imageHeight: 300,
                timer: 4000,
                showConfirmButton: false,
            });
            music.pause();
        } else {
            Swal.fire({
                imageUrl: 'https://img.freepik.com/vector-premium/estrella-dibujos-animados-color-amarillo-brillante-forma-redondeada-estilo-gris-ilustracion-botones-interfaz-usuario-coleccion-estrellas-premio_505956-270.jpg?w=2000',
                imageWidth: 400,
                imageHeight: 300,
                timer: 4000,
                showConfirmButton: false,
            });
        }

        const dict_values = {
            resultado
        }
        const s = JSON.stringify(dict_values);
        $.ajax({
            url: "/Resultado",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(s)
        });
    }


    //Función para actualizar cada n segundos(n milisegundos)
    setInterval("actualizar()", 40000);
}

let idTiempo = setInterval(cuentaRegresiva, 500);
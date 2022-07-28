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

function cuentaRegresiva() {
    tiempoActual--;
    tiempoFaltante.textContent = tiempoActual;

    if (tiempoActual === 0) {
        clearInterval(idTiempo);
        clearInterval(tiempoTopo);
        alert("¡El tiempo ha terminado Atrapaste " + resultado + " topos!");
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
}

let idTiempo = setInterval(cuentaRegresiva, 500);
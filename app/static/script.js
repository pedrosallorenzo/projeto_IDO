const usuarioSelect = document.getElementById("usuario");
const salaSelect = document.getElementById("sala");

const listaSalas = document.getElementById("lista-salas");
const listaReservas = document.getElementById("lista-reservas");

const formulario = document.getElementById("form-reserva");
const mensagem = document.getElementById("mensagem");


async function carregarUsuarios() {
    const resposta = await fetch("/usuarios");
    const usuarios = await resposta.json();

    usuarioSelect.innerHTML = "";

    usuarios.forEach(usuario => {
        const option = document.createElement("option");

        option.value = usuario.id;
        option.textContent = usuario.nome;

        usuarioSelect.appendChild(option);
    });
}


async function carregarSalas() {
    const resposta = await fetch("/salas");
    const salas = await resposta.json();

    salaSelect.innerHTML = "";
    listaSalas.innerHTML = "";

    salas.forEach(sala => {

        const option = document.createElement("option");

        option.value = sala.id;
        option.textContent =
            `${sala.nome} - ${sala.localizacao}`;

        salaSelect.appendChild(option);


        const item = document.createElement("div");

        item.className = "sala";

        item.innerHTML = `
            <strong>${sala.nome}</strong><br>
            Local: ${sala.localizacao}<br>
            Capacidade: ${sala.capacidade} pessoas
        `;

        listaSalas.appendChild(item);
    });
}


async function carregarReservas() {
    const resposta = await fetch("/reservas");
    const reservas = await resposta.json();

    listaReservas.innerHTML = "";

    if (reservas.length === 0) {
        listaReservas.innerHTML =
            "<p>Nenhuma reserva cadastrada.</p>";

        return;
    }

    reservas.forEach(reserva => {

        const item = document.createElement("div");

        item.className = "reserva";

        const inicio = new Date(reserva.inicio);
        const fim = new Date(reserva.fim);

        item.innerHTML = `
            <strong>${reserva.titulo}</strong><br>

            Início:
            ${inicio.toLocaleString("pt-BR")}
            <br>

            Fim:
            ${fim.toLocaleString("pt-BR")}
            <br>

            Sala ID:
            ${reserva.sala_id}

            <br>

            <button
                class="cancelar"
                onclick="cancelarReserva(${reserva.id})"
            >
                Cancelar reserva
            </button>
        `;

        listaReservas.appendChild(item);
    });
}


formulario.addEventListener("submit", async (evento) => {

    evento.preventDefault();

    mensagem.textContent = "";
    mensagem.className = "";

    const reserva = {
        titulo: document.getElementById("titulo").value,

        usuario_id:
            Number(usuarioSelect.value),

        sala_id:
            Number(salaSelect.value),

        inicio:
            document.getElementById("inicio").value,

        fim:
            document.getElementById("fim").value
    };


    const resposta = await fetch("/reservas", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(reserva)

    });


    const dados = await resposta.json();


    if (!resposta.ok) {

        mensagem.textContent =
            dados.detail || "Não foi possível realizar a reserva.";

        mensagem.className = "erro";

        return;
    }


    mensagem.textContent =
        "Reserva criada com sucesso!";

    mensagem.className = "sucesso";


    formulario.reset();

    await carregarReservas();
});


async function cancelarReserva(id) {

    const resposta = await fetch(`/reservas/${id}`, {
        method: "DELETE"
    });


    const dados = await resposta.json();


    if (!resposta.ok) {

        mensagem.textContent =
            dados.detail || "Não foi possível cancelar a reserva.";

        mensagem.className = "erro";

        return;
    }


    mensagem.textContent = dados.message;
    mensagem.className = "sucesso";

    await carregarReservas();
}


async function iniciarPagina() {

    await carregarUsuarios();
    await carregarSalas();
    await carregarReservas();

}


iniciarPagina();
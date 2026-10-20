const menu = document.querySelector('.menu');
const alternarMenu = document.querySelector('[data-menu-toggle]');

if (menu && alternarMenu) {
    alternarMenu.addEventListener('click', () => {
        const aberto = menu.classList.toggle('aberto');
        alternarMenu.setAttribute('aria-expanded', String(aberto));
        alternarMenu.setAttribute('aria-label', aberto ? 'Fechar menu' : 'Abrir menu');
    });

    window.matchMedia('(min-width: 761px)').addEventListener('change', (evento) => {
        if (evento.matches) {
            menu.classList.remove('aberto');
            alternarMenu.setAttribute('aria-expanded', 'false');
            alternarMenu.setAttribute('aria-label', 'Abrir menu');
        }
    });
}

const dialogo = document.querySelector('#dialogo-confirmacao');
const tituloDialogo = document.querySelector('#dialogo-titulo');
const mensagemDialogo = document.querySelector('#dialogo-mensagem');
let formularioPendente = null;

if (dialogo && tituloDialogo && mensagemDialogo) {
    document.querySelectorAll('[data-confirmar]').forEach((formulario) => {
        formulario.addEventListener('submit', (evento) => {
            if (formulario.dataset.confirmado === 'true') {
                delete formulario.dataset.confirmado;
                return;
            }

            evento.preventDefault();
            formularioPendente = formulario;
            tituloDialogo.textContent = formulario.dataset.confirmarTitulo || 'Confirmar ação';
            mensagemDialogo.textContent = formulario.dataset.confirmar;
            dialogo.showModal();
        });
    });

    document.querySelector('[data-dialogo-cancelar]').addEventListener('click', () => {
        formularioPendente = null;
        dialogo.close();
    });

    document.querySelector('[data-dialogo-confirmar]').addEventListener('click', () => {
        if (formularioPendente) {
            const formulario = formularioPendente;
            formularioPendente = null;
            formulario.dataset.confirmado = 'true';
            dialogo.close();
            formulario.requestSubmit();
        }
    });

    dialogo.addEventListener('cancel', () => {
        formularioPendente = null;
    });
}

const fecharMensagem = (mensagem) => {
    if (!mensagem) {
        return;
    }
    mensagem.classList.add('saindo');
    window.setTimeout(() => mensagem.remove(), 180);
};

document.querySelectorAll('.mensagem').forEach((mensagem) => {
    mensagem.querySelector('[data-fechar-mensagem]')?.addEventListener('click', () => fecharMensagem(mensagem));
    window.setTimeout(() => fecharMensagem(mensagem), 6500);
});

document.querySelectorAll('[data-envio-unico]').forEach((formulario) => {
    formulario.addEventListener('submit', () => {
        const botao = formulario.querySelector('button[type="submit"]');
        if (botao) {
            botao.disabled = true;
            botao.textContent = 'Registrando...';
        }
    });
});
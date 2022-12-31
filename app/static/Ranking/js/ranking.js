function detalhes(){
    var ticker = prompt("Digite o ticker: ")
    window.location.href = `/detalhes?ticker=${ticker} `
}

function Deslogar() {
    const botaoSair = document.getElementById('sair');

    botaoSair.addEventListener('click', (e) => {
        e.preventDefault();
        
        axios.post('/validar', { action: 'logout'})
        .then( (succes) => {window.location.href = "/login";})
        .catch( (err) => {window.location.href = "/login";})

    })
}

Deslogar()
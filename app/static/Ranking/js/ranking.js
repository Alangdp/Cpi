function detalhes(){
    var ticker = prompt("Digite o ticker: ")
    
    axios.post('/validar', { 
        action: 'validaTicker',
        ticker,
    })
        .then( (succes) => {window.href = `/detalhes?=${ticker}`})
        .catch( (err) => alert("Ticker inválido"))
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

function cleanCookie(nome) {
    document.cookie = `${nome}=John Smith; expires=Thu, 18 Dec 2013 12:00:00 UTC; path=/`;
}
Deslogar()
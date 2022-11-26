function detalhes(){
    var ticker = prompt("Digite o ticker: ")
    if(!ticker ){
        alert('Ticker inválido');
    }if(ticker.length > 6){
        alert('Ticker inválido');
    }if(ticker.length < 5){
        alert('Ticker inválido')
    }else{
        alert('Ticker válido')
        location.href = `/detalhes?ticker=${ticker}`;
    }
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
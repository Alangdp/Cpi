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


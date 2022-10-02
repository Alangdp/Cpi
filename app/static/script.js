function httpGet(ticker)
{
    url = "/valid?ticker=" + ticker;
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url, false ); 
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function getTicker(){
    var ticker = prompt("Digite o ticker: ")
    if(!ticker ){
        alert('Ticker inválido');
    }if(ticker.length > 6){
        alert('Ticker inválido');
    }if(ticker.length < 5){
        alert('Ticker inválido')
    }else{
        alert('Ticker válido')
        location.href = 'https://statusinvest.com.br/acoes/{{ticker}}';
    }

}

//////////////////////////////////////////////////

const content = document.querySelector('#content');
content.style.transformOrigin = 'top left';

window.addEventListener('resize', recalculateScale);

function recalculateScale() {
  const windowHeight = window.innerHeight;
  content.style.transform = `scale(${windowHeight / content.offsetHeight})`;
}

/////////////////////

function Search(){
    const Evento = document.getElementById('search').value;

}
function httpGet(ticker)
{
    url = "/detalhes?ticker=$" + ticker;
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
    }

    httpGet(ticker);

}

///////////////////////////////////////////////////////

function httpGetL(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function getTickerL(){
    var ticker = prompt("Digite o ticker: ")
    if(!ticker ){
        alert('Ticker inválido');
    }if(ticker.length > 6){
        alert('Ticker inválido');
    }if(ticker.length < 5){
        alert('Ticker inválido')
    }else{
        alert('Ticker válido')
    }

    url = "/detalhes?ticker=" + ticker;
    httpGetL(url);

}

//////////////////////////////////////////////////

const content = document.querySelector('#content');
content.style.transformOrigin = 'top left';

window.addEventListener('resize', recalculateScale);

function recalculateScale() {
  const windowHeight = window.innerHeight;
  content.style.transform = `scale(${windowHeight / content.offsetHeight})`;
}

recalculateScale();
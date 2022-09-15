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
}



// $.ajax({
//     url: '/',
//     method: 'post',
//     data: ticker_data,
//     processData: false,
//     contentType: false,
//     sucess: function(resposta_ticker){
//         alert(resposta_ticker)
//     }
// }).done(function(resposta){
//     alert(resposta)
// })

// function sendData(event){
//     data = ticker_data;
//     let httpRequest = new XMLHttpRequest();
//     httpRequest.setRequestHeader("X-Content-Type-Options", "multipart/form-data")
//     httpRequest.send(data);
//     httpRequest.onreadystatechange = response;
// }


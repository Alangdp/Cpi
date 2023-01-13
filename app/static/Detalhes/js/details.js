// alert('ESTA PÁGINA ESTA EM DESENVOLVIMENTO')
// alert('AINDA NÃO HÁ ATUALIZAÇÃO DINÂMICA')
// alert('SE TRATA DE UM EXEMPLO FUTURO')

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
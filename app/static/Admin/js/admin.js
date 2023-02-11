
class ValidaRegistro{
    constructor () {
        this.formulario = document.querySelector(".column")
        this.events();
    }

    events() {
        const registrar = this.formulario.querySelector('.registrar')
        registrar.addEventListener('click', (e) => {
            this.handleSubmit(e); 
        })
    }
    handleSubmit(e) {
        const senha  = this.formulario.querySelector('.Senha').value;
        const email = this.formulario.querySelector('.Email').value.toLowerCase();
        this.postJSON(email,senha)
        
    }

    postJSON(email, senha){
        axios.post('/admin', { 
            email : email,
            senha : senha,
            action: 'admin'
        }).then( (succes) => {
            alert('Login concluido')
            window.location.href = '/admin'
            return true;
        }).catch( (err) => {
            alert('Senha ou Email, Invalidos!')
            return false;
        })
    }
}

const valida = new ValidaRegistro();


// ADMIN PAGE


function Deslogar() {
    axios.post('/admin', { action: 'logoutAdmin'})
    .then( (succes) => window.location.href = '/admin')
    .catch( (err) => true)
}

function cleanCookie(nome) {
    document.cookie = `${nome}=John Smith; expires=Thu, 18 Dec 2013 12:00:00 UTC; path=/`;
}



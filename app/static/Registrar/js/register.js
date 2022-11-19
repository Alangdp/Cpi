function setCookie(nome, valor) { 
    document.cookie = nome + "=" + (valor || '') + "; expires=Fri, 31 Dec 9999 23:59:59 GMT" + "; path=/ invisible";
}

class ValidaRegistro{
    constructor () {

        this.formulario = document.querySelector(".formulario")
        this.events();
    }

    events() {
        this.formulario.addEventListener('submit', (e) => {
            this.handleSubmit(e);
            
        })
    }

    handleSubmit(e) {
        e.preventDefault();

        const camposvalidos = this.validaFormulario();
        const senhasValidas = this.isValidPassword();

        if(camposvalidos && senhasValidas) {

            const usuario = this.formulario.querySelector('.Usuario').value;
            const senha  = this.formulario.querySelector('.Senha').value;
            const email = this.formulario.querySelector('.Email').value;
            const cpf = this.formulario.querySelector('.CPF').value;


            this.cleanCookie('senha');
            this.cleanCookie('email')

            setCookie('senha', senha);
            setCookie('email', email);


            this.postJSON(usuario,email,senha,cpf)
            
        }
    }

    postJSON(usuario, email, senha, cpf){
        axios.post('/validar', { 
            usuario : usuario,
            email : email,
            senha : senha,
            cpf : cpf,
            action: 'registro'
        }).then( (succes) => {
            alert('Registro concluido')
            window.location.href = "/login";
            return true;
        }).catch( (err) => {
            alert('Impossível concluir o registro, tente mais tarde')
            return false;
        })
    }

    getCookie(nome) {
        var cookieName = nome + "=";
        var ca = document.cookie.split(';');
        for(var i=0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) ==' ') c = c.substring(1,c.length);
            if (c.indexOf(cookieName) == 0) return c.substring(cookieName.length, c.length);

        }

        return null;
    }

    cleanCookie(nome) {
        document.cookie = nome +'=; path=/ Expires=Thu, 01 Jan 1970 00:00:00 GMT; ';
    }

    validaFormulario() {
        let valid = true;

        for(const erro of this.formulario.querySelectorAll('.error-text')) {
            erro.remove();
        }

        for(const campo of this.formulario.querySelectorAll('.input')){
            const labelName = campo.classList[0];
            if(!campo.value){
                this.createError(campo, `${labelName} não pode ficar vazio`);
                valid = false;
            }

            if(campo.classList.contains('CPF')) {
                if(!this.validaCPF(campo)) valid = false;
            }

            if(campo.classList.contains('Usuario')){
                if(!this.validaUsuario(campo)) valid = false;
            }

        }

        return valid;
    }

    isValidPassword(){
        let valid = true;
        const senha = this.formulario.querySelector('.Senha');
        const repetirSenha = this.formulario.querySelector('.Senha-Repetida');

        console.log()
        if(senha.value !== repetirSenha.value) {
            this.createError(senha, 'Campos repetir senha e senha precisam ser iguais');
            valid = false;
        }

        if(senha.value.length < 6 || senha.value.length > 12) {
            this.createError(senha, 'Senha precisa estar entre 6 e 12 caracteres');
            valid = false;
        }

        return valid;

    }

    validaUsuario(campo) {
        const usuario = campo.value;
        let valid = true;
        if(usuario.length > 12 || usuario.length < 3) {
            this.createError(campo, 'Usuário precisa ter entre 3 e 12 caracteres')
            valid = false;
        }

        if(!usuario.match(/[a-zA-Z0-9]+$/g)){
            this.createError(campo, 'Nome de usuário precisa conter apenas letras e números')
            valid = false;
        }
        return valid;
    }

    validaCPF(campo) {
        let valid = true;
        const cpf = new ValidaCPF(campo.value)

        if(!cpf.VerificaCPF()) {
            this.createError(campo, 'CPF inválido')
            valid = false;
        }

        return valid;
    }

    createError(campo, msg) {
        const div = document.createElement('div');
        div.innerHTML = msg;
        div.classList.add('error-text');
        campo.insertAdjacentElement('afterend', div);
    }
}

const valida = new ValidaRegistro();


function setCookie(nome, valor) { 
    document.cookie = nome + "=" + (valor || '') + "; expires=Fri, 31 Dec 9999 23:59:59 GMT" + "; path=/";
}

class ValidaRegistro{
    constructor () {

        this.chargeInputs();
        this.formulario = document.querySelector(".formulario");
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

            const senha  = this.formulario.querySelector('.Senha').value;
            const email = this.formulario.querySelector('.Email').value;

            this.cleanCookie('senha');
            this.cleanCookie('email')

            setCookie('senha', senha);
            setCookie('email', email);


            this.formulario.submit();
        }
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
        document.cookie = nome +'=; path=/ Expires=Thu, 01 Jan 1970 00:00:00 GMT;';
    }

    chargeInputs() {
        const senha = document.getElementById('senha');
        const email = document.getElementById('email');

        senha.value = this.getCookie('senha');
        email.value = this.getCookie('email');
    }

    validaFormulario() {
        let valid = true;

        for(const erro of this.formulario.querySelectorAll('.error-text')) {
            erro.remove();
        }
        for(const campo of this.formulario.querySelectorAll('.input')){
            const labelName = campo.classList[0];
            if(!campo.value) {
                this.createError(campo, `${labelName} não pode ficar vazio`)
                valid = false;
            }
        }


        return valid;
    }

    isValidPassword(){
        let valid = true;
        const senha = this.formulario.querySelector('.Senha');
        const regex = /^(?=.*\d)(?=.*[!@#$%^&*(){}])(?=.*[a-z])(?=.*[A-Z]).{8,12}$/;

        if(senha.value.length < 6 || senha.value.length > 12) {
            this.createError(senha, 'Senha precisa estar entre 6 e 12 caracteres');
            valid = false;
        }
        
        if(!senha.value.match(regex)){
            this.createError(senha, 'Senha inválida')
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
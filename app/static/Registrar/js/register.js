function setCookie(nome, valor) { 
    document.cookie = nome + "=" + (valor || '') + "; expires=Fri, 31 Dec 9999 23:59:59 GMT" + "; path=/ invisible";
}

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
        const senhasValidas = this.isValidPassword();
        const camposvalidos = this.validaFormulario();
        console.log(senhasValidas, camposvalidos)

        if(camposvalidos && senhasValidas) {

            const usuario = this.formulario.querySelector('.Usuario').value;
            const senha  = this.formulario.querySelector('.Senha').value;
            const email = this.formulario.querySelector('.Email').value.toLowerCase();
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
        
        for(const campo of this.formulario.querySelectorAll('input')){
            let validField = true;
            
            const labelName = campo.classList[0];
            if(!campo.value){
                valid = false, validField = false;
                this.createError(campo)

            }

            if(campo.classList.contains('CPF')) {
                if(!this.validaCPF(campo)) 
                valid = false, validField = false;
                this.createError(campo)

            }
            if(campo.classList.contains('Usuario')){
                if(!this.validaUsuario(campo)) 
                valid = false, validField = false;
                this.createError(campo)

            }

            if(campo.classList.contains('Email')){
                if(!this.validaEmail(campo)){
                    valid = false, validField = false;
                    this
                }
            }

            if(validField) {
                this.removeError(campo)
            }
        }

        return valid;
    }

    validaEmail(campo) {
        let valid = true;
        const email = campo.value;
        const regex = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}/
        if(!regex.test(email)) {
            this.createError(campo)
            valid = false;
        } else {
            this.removeError(campo)
        }
        return valid;

    }

    isValidPassword(){
        let valid = true;
        const senha = this.formulario.querySelector('.Senha');
        const senhaRepetida = this.formulario.querySelector('.Senha-Repetida');
        const regex = /^(?=.*\d)(?=.*[!@#$%^&*(){}])(?=.*[a-z])(?=.*[A-Z]).{8,12}$/;

        if(senha.value.length < 6 || senha.value.length > 12) {
            this.createError(senha), this.createError(senhaRepetida);
            valid = false;
        }
        
        if(senha.value !== senhaRepetida.value) {
            this.createError(senha), this.createError(senhaRepetida);
            valid = false;

        }

        if(!senha.value.match(regex)){
            this.createError(senha), this.createError(senhaRepetida);
            valid = false;
        }

        if(valid) {
            this.removeError(senha);
            this.removeError(senhaRepetida);
        }
        return valid;

    }

    validaUsuario(campo) {
        const usuario = campo.value;
        let valid = true;
        if(usuario.length > 12 || usuario.length < 4) {
            valid = false;
        }

        if(!usuario.match(/[a-zA-Z0-9]+$/g)){
            valid = false;
        }
        return valid;
    }

    validaCPF(campo) {
        let valid = true;
        const cpf = new ValidaCPF(campo.value)

        if(!cpf.VerificaCPF()) {
            valid = false;
        }

        return valid;
    }

    createError(campo) {
        const valid = campo.nextElementSibling.querySelector('.bx-chevron-down')
        valid.style.color = 'Red';
        valid.style.opacity = '1';
    }

    removeError(campo) {
        const valid = campo.nextElementSibling.querySelector('.bx-chevron-down')
        valid.style.color = 'Green';
        valid.style.opacity = '1';

        
    }
}

const valida = new ValidaRegistro();


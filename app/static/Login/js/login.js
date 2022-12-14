
class ValidaRegistro{
    constructor () {

        this.formulario = document.querySelector(".column")
        this.events();
    }

    events() {
        const registrar = this.formulario.querySelector('.registrar')
        document.addEventListener('keydown', (e) => {
            if(e.key == `Enter`) {
                this.handleSubmit()
            }
        })

        registrar.addEventListener('click', (e) => {
            this.handleSubmit(e);
        })
    }

    handleSubmit(e) {
        const senhasValidas = this.isValidPassword();
        const camposvalidos = this.validaFormulario();
        console.log(senhasValidas, camposvalidos)

        if(camposvalidos && senhasValidas) {

            const senha  = this.formulario.querySelector('.Senha').value;
            const email = this.formulario.querySelector('.Email').value.toLowerCase();
            this.postJSON(email,senha);
        } else {
            alert(`Alguma informacao inválida`);
        }
    }

    postJSON(email, senha){
        axios.post('/validar', { 
            email : email,
            senha : senha,
            action: 'login'
        }).then( (succes) => {
            alert('Login concluido')
            window.location.href = "/ranking";
            return true;
        }).catch( (err) => {
            alert('Senha ou Email, Invalidos!')
            return false;
        })
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
        const regex = /^(?=.*\d)(?=.*[!@#$%^&*(){}])(?=.*[a-z])(?=.*[A-Z]).{8,12}$/;

        if(senha.value.length < 6 || senha.value.length > 12) {
            this.createError(senha);
            valid = false;
        }

        if(!senha.value.match(regex)){
            this.createError(senha);
            valid = false;
        }

        if(valid) this.removeError(senha);
        
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

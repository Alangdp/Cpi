

// function siteCPF() {
//     const cpfCampo = document.querySelector('.cpf');
//     const cpfLabel = document.querySelector('.cpf_warning');

//     cpfCampo.addEventListener('keyup', function(){
//         let cpf = new ValidaCPF(cpfCampo.value);
//         if (cpf.cpf == '') cpfLabel.innerText = '';
//         if (cpf.validaCPF()) {cpfLabel.innerText = 'CPF VÁLIDO'; return true;}
//         else cpfLabel.innerText = 'CPF INVÁLIDO';
//     });
// };

// function siteSenha(){
//     const senha = document.querySelector('.password');
//     const senhaLabel = document.querySelector('.password_warning');
//     const regex = /^(?=.*\d)(?=.*[!@#$%^&*(){}])(?=.*[a-z])(?=.*[A-Z]).{8,}$/;

//     senha.addEventListener('keyup', function(e){
//         if (regex.test(senha.value)){
//             senhaLabel.innerText = 'SENHA VÁLIDA';
//             return true;
//         } else {
//             senhaLabel.innerText = 'SENHA INVÁLIDA';
//         } if(senha.value === ''){
//             senhaLabel.innerText = ''
//         }
//     })
// }

// function siteEmail(){
//     const email = document.querySelector('.email')
//     const emailLabel = document.querySelector('.email_warning')
//     const regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
//     email.addEventListener('keyup', function(e) {
//         if (regex.test(email.value)){
//             emailLabel.innerText = 'EMAIL VÁLIDO';
//             return true;
//         } else {
//             emailLabel.innerText = 'EMAIL INVÁLIDO';
//         } if(email.value === ''){
//             emailLabel.innerText = '';
//         }
//     })
// }

// function siteUserName(){
//     const username = document.querySelector('.username');
//     username.addEventListener('keyup', function(e){
//         if( username.value !== '') return true;
//         else return false;
//     })
// }

// function registrar(){
//     const registrar = document.querySelector('.submit')
    

//     registrar.addEventListener('click', function(e){
//         console.log(siteCPF() && siteEmail() && siteSenha() && siteUserName())

//         if(siteCPF() && siteEmail() && siteSenha() && siteUserName()){
//             console.log('valido')
//         } else {
//             console.log('invalido')
//         }
//     })
// }

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
            alert('Formulário enviado');
            this.formulario.submit();
        }
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
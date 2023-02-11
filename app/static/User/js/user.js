const id = document.querySelector('#userId').value;

function genError(form ,message) {
    const div = document.createElement("div");
    div.className = "alerts alert-danger alert-server";

    const h5 = document.createElement("h5");
    h5.className = "text-alert";
    h5.textContent = message;

    div.appendChild(h5);
    form.appendChild(div);
}

function removeErrors(form) {
    for(const error of form.querySelectorAll('.alert-server')){
        error.remove();
    }
}

function valida(event) {
    const action = event.target.id;
    const actionForm = event.target.parentNode;

    event.preventDefault();
    removeErrors(actionForm)
    
    if(action === 'buttonEmail'){
        
        const actualEmail = document.getElementById('inputEmailA');
        const newEmail = document.getElementById('inputEmailN');
        const confirmNewEmail = document.getElementById('inputEmailC');

        if(newEmail.value === '' || confirmNewEmail.value === '' || actualEmail === '') {
            genError(actionForm, 'Algum dos campos está vazio.');
            return
        }
        if(!newEmail.value === confirmNewEmail.value) {
            genError(actionForm, 'Os emails não correspondem.')
            return
        }
        if(actualEmail.value === newEmail.value && actualEmail.value !== ''){
            genError(actionForm, 'Email atual igual novo email.');
            return
        }

        actionForm.submit()
    }

    if(action === 'buttonPassword'){

        const actualPassword = document.getElementById('inputPasswordA');
        const newPassword = document.getElementById('inputPasswordN');
        const confirmPassword = document.getElementById('inputPasswordC');

        if(newPassword.value === '' || confirmPassword.value === '' || actualPassword.value === '') {
            genError(actionForm, 'Algum dos campos está vazio.');
            return
        }
        if(!newPassword.value === confirmPassword.value) {
            genError(actionForm, 'As senhas não correspondem.');
            return
        }
        if( actualPassword.value === newPassword.value && actualPassword.value !== '') {
            genError(actionForm, 'Senha atual igual nova senha.');
            return
        }

        actionForm.submit()

    }

}
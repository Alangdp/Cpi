class ValidaCPF {

    constructor (cpf) {
        this.cpf = cpf.toString().replace(/\D+/g , '');
        this.cpfArray = Array.from(this.cpf);
        this.cpfLimpo = this.cpfArray.splice(0,9);
        
    }
    
    esequencia() {
        return this.cpf[0].repeat(this.cpf.length) === this.cpf;
    }

    valida() {
        if(typeof(this.cpf) !== 'string') return false;
        if(this.cpf.length !== 11) return false;
        if(this.esequencia()) return false;
        return true;
    }

    primeiroDigito() {
        if(this.valida()){
            let mult = 10;
            const multiplicado = this.cpfLimpo.reduce( (ac, val) => {
                ac += Number(val) * Number(mult);
                mult--;
                return ac;
            },0)
    
            const prDigito = 11 - (multiplicado % 11);
            if(prDigito > 9) return 0;
            return prDigito;       
        } else {
            return 0;
        }
        
    }

    segundoDigito() {
        if(this.valida()) {
            const arrayConjunto = Array.from(`${this.cpfLimpo.join('')}${this.primeiroDigito()}`)
            let mult = 11;
            const multiplicado = arrayConjunto.reduce( (ac, val) => {
                ac += Number(val) * Number(mult);
                mult--;
                return ac;
            },0)

            const seDigito = 11 - (multiplicado % 11);
            if(seDigito > 9) return 0;
            return seDigito;
        } else {
            return 0;
        }
        
    } 

    VerificaCPF() {
        const cpfnovo = `${this.cpfLimpo.join('')}${this.primeiroDigito()}${this.segundoDigito()}`
        if (cpfnovo !== this.cpf) return false;
        return true;
    }
}
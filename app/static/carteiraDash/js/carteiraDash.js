
const grafico = (moment) => {

    function botoes(meses , semana, anos) {
        document.addEventListener('click', e => {
            const botao = e.target.textContent;
            console.log(e.target)
            console.log(botao)
            if(botao === "Anos") {
                select = anos.reverse();
            }

            if(botao === "Mês") {
                meses = semana.reverse()
                select = meses;
            }

            if(botao === "Semana") {
                semana = semana.reverse()
                select = semana;
            }

            const chart = document.querySelector("#lineChart");
            const canvaClone = chart.cloneNode(true);
            const divPai = document.querySelector('.chartjs-size-monitor')
            divPai.appendChild(canvaClone)

            renderizaGrafico()
        })
    }

    function ehBissexto(ano) {
        return (ano % 4 === 0 && ano % 100 !== 0) || ano % 400 === 0;
    }
        

    var dataAtual = moment.format("DD/MM/YYYY");
    var dataInicial = moment

    console.log(dataInicial)

    var datasSemana = [];
    for (var i = -7; i <= 0; i++) {
        datasSemana.push(moment.subtract(i, 'days').format('DD/MM/YYYY'));
    }

    var datasMes = []; 
    for (var i = 0; i <= 30; i++) {
        datasMes.push(moment.subtract(i, 'days').format('DD/MM/YYYY'));
    }

    var datasAno = [];
    var numDias = ehBissexto(moment.year()) ? 366 : 365; 
    for (var i = 0; i < numDias; i++) {
        datasAno.push(dataInicial.format("DD/MM/YYYY"));
        dataInicial.subtract(1, 'day');
    }

    function renderizaGrafico(select = datasMes, data = []) {
        const ctxL = document.getElementById("lineChart").getContext('2d');
        const myLineChart = new Chart(ctxL, {
            type: 'line',
            data: {
                labels: select,
                datasets: [{
                    label: "Carteira",
                    data: [60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 65, 60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 65, 60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 65, 60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 65, 60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 65, 60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 65, 60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 65, 60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 65, 60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 65],
                    backgroundColor: ['transparent'],
                    pointBackgroundColor: 'rgb(253,180,92',
                    borderColor: ['rgb(253,180,92)'],
                    borderWidth: 2
                }, {
                    label: "Ibovespa",
                    data: [28, 48, 40, 19, 86, 27, 28, 48, 40, 19, 86, 27],
                    backgroundColor: ['transparent'],
                    pointBackgroundColor: 'rgb(255, 8, 0)',
                    borderColor: ['rgb(255, 8, 0)'],
                    borderWidth: 2
                }, {
                    label: "Selic",
                    data: [28, 48, 40, 19, 86, 27, 28, 78, 40, 12, 98, 99],
                    backgroundColor: ['transparent'],
                    pointBackgroundColor: 'rgb(0, 153, 255)',
                    borderColor: ['rgb(0, 153, 255)'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                tooltips: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(tooltipItem, data) {
                            const label = data.labels[tooltipItem.index];
                            label.display = true;
                            return label;
                        }
                    }
                },
                hover: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    xAxes: [{
                        ticks: {
                            display: true
                        }
                    }]
                }
            }
        });
    }
    
    let select = datasMes

    renderizaGrafico(select)
    botoes(mes = datasMes, semana = datasSemana, ano = datasAno)
        
}
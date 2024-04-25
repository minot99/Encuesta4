const labelsPie = ['Certificados (CELT-P /TKT)', 'Capacitados Local', 'Capacitados Extranjeros (US / CAN)', 'Aprobados Curso'];
const colorsPie = ['rgb(28, 202, 184)', 'rgb(42, 118, 244)', 'rgb(241,69,134)', 'rgb(244,183,54)'];
const dataValuesPie = [30, 20, 25, 25];

const graphPie = document.querySelector("#grafica");

const dataPie = {
    labels: labelsPie,
    datasets: [{
        data: dataValuesPie,
        backgroundColor: colorsPie
    }]
};

const configPie = {
    type: 'pie',
    data: dataPie,
    options: {
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.label || '';
                        let value = context.parsed || 0;
                        return label;
                    }
                }
            }
        }
    }
};

// Añadir porcentaje a las etiquetas
labelsPie.forEach((label, index) => {
    labelsPie[index] += ': ' + dataValuesPie[index] + '%';
});

new Chart(graphPie, configPie);

var options = {
    series: [44, 55, 13, 43, 22],
    chart: {
        width: 380,
        type: 'pie',
    },
    labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
    responsive: [{
        breakpoint: 480,
        options: {
            chart: {
                width: 200
            },
            legend: {
                position: 'bottom'
            }
        }
    }]
};

var chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();

// Gráfico de barras

const labelsBar = ['Horas de Inglés / Semana', 'Horas Laboratorio / Semana', 'Horas de Science / Semana', 'Horas Otras Asignaturas Inglés / Semana'];
const dataValuesBar1 = [11, 2, 2, 1]; // Valores para la primera barra de cada elemento
const dataValuesBar2 = [8, 6, 0, 3]; // Valores para la segunda barra de cada elemento
const colorsBar1 = ['rgb(28, 202, 184)', 'rgba(28, 202, 184, 0.5)', 'rgb(28, 202, 184)', 'rgba(28, 202, 184, 0.5)'];
const colorsBar2 = ['rgb(42, 118, 244)', 'rgba(42, 118, 244, 0.5)', 'rgb(42, 118, 244)', 'rgba(42, 118, 244, 0.5)'];

const graphBar = document.querySelector("#graficaBar");

const dataBar = {
    labels: labelsBar,
    datasets: [{
        label: 'KIDS (Primaria)',
        data: dataValuesBar1,
        backgroundColor: colorsBar1,
        borderWidth: 1
    }, {
        label: 'AFTER SCHOOL (Media y Premedia)',
        data: dataValuesBar2,
        backgroundColor: colorsBar2,
        borderWidth: 1
    }]
};

const configBar = {
    type: 'bar',
    data: dataBar,
    options: {
        indexAxis: 'y', // Cambiar para agrupar las barras en el eje Y
        plugins: {
            legend: {
                position: 'top',
            }
        },
        scales: {
            x: {
                stacked: false,
            },
            y: {
                stacked: false
            }
        }
    }
};

new Chart(graphBar, configBar);

// SEGUNDA BARRA

const labelsBarHorizontal = ['Horas de Capacitación Docente No Certificados', 'Horas de Capacitación Docente Certificados'];
const dataValuesBarHorizontal1 = [45, 35]; // Valores para la primera barra horizontal
const dataValuesBarHorizontal2 = [55, 45]; // Valores para la segunda barra horizontal

const colorsBarHorizontal1 = ['rgb(28, 202, 184)', 'rgba(28, 202, 184, 0.5)']; // Colores para la primera barra
const colorsBarHorizontal2 = ['rgb(42, 118, 244)', 'rgba(42, 118, 244, 0.5)']; // Colores para la segunda barra

const graphBarHorizontal = document.querySelector("#graficaBarHorizontal");

const dataBarHorizontal = {
    labels: labelsBarHorizontal,
    datasets: [{
        label: 'KIDS (Primaria)',
        data: dataValuesBarHorizontal1,
        backgroundColor: colorsBarHorizontal1,
        borderWidth: 1
    }, {
        label: 'AFTER SCHOOL (Media y Premedia)',
        data: dataValuesBarHorizontal2,
        backgroundColor: colorsBarHorizontal2,
        borderWidth: 1
    }]
};

const configBarHorizontal = {
    type: 'bar', // Cambiar el tipo a barra
    data: dataBarHorizontal,
    options: {
        indexAxis: 'x', // Mantener el eje vertical
        plugins: {
            legend: {
                position: 'top',
                maxWidth: 200, // Establecer un ancho máximo para la leyenda
                labels: {
                    padding: 10, // Ajustar el espacio entre las etiquetas de la leyenda
                }
            }
        },
        scales: {
            x: {
                stacked: false,
                maxBarThickness: 50, // Ajustar el grosor máximo de las barras
            },
            y: {
                stacked: false, // Desactivar la agrupación de barras vertical
                categoryPercentage: 0.5, // Ajustar el ancho de las barras relativo al espacio disponible
            }
        }
    }
};

new Chart(graphBarHorizontal, configBarHorizontal);
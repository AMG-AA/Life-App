// ! Option 1
// fetch('/get_growth_data')
//     .then(response => response.json())
//     .then(response => {
//         console.log(response); // Verificar la respuesta en la consola
//         const { has_data, data } = response;

//         if (has_data) {
//             // Convertir las fechas de "YYYY-MM" a objetos Date
//             const labels = data.map(item => {
//                 const year = item.year;
//                 const month = item.month;
//                 // Crear una nueva fecha con el primer día de cada mes
//                 return new Date(year, month - 1); // Los meses en JavaScript empiezan desde 0
//             });

//             // Obtener las alturas para la gráfica
//             const growth = data.map(item => item.growth_cm);

//             const ctx = document.getElementById('growth-chart').getContext('2d');
//             new Chart(ctx, {
//                 type: 'line',
//                 data: {
//                     labels: labels,
//                     datasets: [{
//                         label: 'Baby Growth (cm)',
//                         data: growth,
//                         borderColor: 'rgba(75, 192, 192, 1)', // Ajustar color de la línea
//                         backgroundColor: 'rgba(75, 192, 192, 0.2)', // Ajustar color de fondo
//                         pointBackgroundColor: 'rgba(75, 192, 192, 1)', // Ajustar color de los puntos
//                         pointBorderColor: 'rgba(75, 192, 192, 1)', // Ajustar color del borde de los puntos
//                     }]
//                 },
//                 options: {
//                     responsive: true,
//                     plugins: {
//                         legend: { display: true },
//                         tooltip: {
//                             callbacks: {
//                                 // Agregar la diferencia antes del label principal
//                                 label: function(tooltipItem) {
//                                     const currentHeight = tooltipItem.raw;
//                                     const currentDate = labels[tooltipItem.dataIndex].toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
//                                     return `${currentDate}: Height: ${currentHeight.toFixed(2)} cm`;
//                                 },
//                                 afterLabel: function(tooltipItem) {
//                                     const index = tooltipItem.dataIndex;
//                                     const currentHeight = tooltipItem.raw;
//                                     let beforeLabel = ''; 

//                                     // Si no es el primer registro, calcular la diferencia
//                                     if (index > 0) {
//                                         const previousHeight = growth[index - 1];
//                                         const growthDifference = currentHeight - previousHeight;
//                                         const previousDate = labels[index - 1].toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
//                                         // Agregar la diferencia como contenido adicional
//                                         beforeLabel = `${previousDate}: ${growthDifference.toFixed(2)} cm`;
//                                     }
//                                     return beforeLabel;
//                                 }
//                             }
//                         }
//                     },
//                     scales: {
//                         x: {
//                             type: 'time', // Especificar que estamos usando fechas en el eje X
//                             title: {
//                                 display: true,
//                                 text: 'Date'
//                             },
//                             time: {
//                                 unit: 'month', // Mostrar por meses
//                                 tooltipFormat: 'yyyy-MM',
//                                 displayFormats: {
//                                     month: 'MMM yyyy' // Formato de fecha para mostrar en el gráfico
//                                 }
//                             }
//                         },
//                         y: {
//                             beginAtZero: true,
//                             title: {
//                                 display: true,
//                                 text: 'Baby Growth (cm)'
//                             }
//                         }
//                     }
//                 }
//             });
//         } else {
//             document.getElementById('growth-chart').style.display = 'none';
//             document.getElementById('no-data-message').style.display = 'block';
//         }
//     });


// ! Option 2
// fetch('/get_growth_data')
//     .then(response => response.json())
//     .then(response => {
//         console.log(response); // Verificar la respuesta en la consola
//         const { has_data, data } = response;

//         if (has_data) {
//             // Convertir las fechas de "YYYY-MM" a objetos Date
//             const labels = data.map(item => {
//                 const year = item.year;
//                 const month = item.month;
//                 // Crear una nueva fecha con el primer día de cada mes
//                 return new Date(year, month - 1); // Los meses en JavaScript empiezan desde 0
//             });

//             // Obtener las alturas para la gráfica
//             const growth = data.map(item => item.growth_cm);

//             const ctx = document.getElementById('growth-chart').getContext('2d');
//             new Chart(ctx, {
//                 type: 'line',
//                 data: {
//                     labels: labels,
//                     datasets: [{
//                         label: 'Baby Growth (cm)',
//                         data: growth,
//                         borderColor: 'rgba(75, 192, 192, 1)', // Ajustar color de la línea
//                         backgroundColor: 'rgba(75, 192, 192, 0.2)', // Ajustar color de fondo
//                         pointBackgroundColor: 'rgba(75, 192, 192, 1)', // Ajustar color de los puntos
//                         pointBorderColor: 'rgba(75, 192, 192, 1)', // Ajustar color del borde de los puntos
//                     }]
//                 },
//                 options: {
//                     responsive: true,
//                     plugins: {
//                         legend: { display: true },
//                         tooltip: {
//                             callbacks: {
//                                 // Personalizar el contenido del tooltip
//                                 label: function(tooltipItem) {
//                                     const index = tooltipItem.dataIndex;
//                                     const currentHeight = tooltipItem.raw;
//                                     const currentDate = tooltipItem.label;
//                                     let tooltipText = `${currentDate}: Growth: ${currentHeight.toFixed(2)} cm`;

//                                     // Si no es el primer registro, calcular la diferencia
//                                     if (index > 0) {
//                                         const previousHeight = growth[index - 1];
//                                         const growthDifference = currentHeight - previousHeight;
//                                         // Añadir salto de línea para la diferencia
//                                         tooltipText += `\n(Dif: ${growthDifference.toFixed(2)} cm)`;
//                                     }

//                                     return tooltipText;
//                                 }
//                             }
//                         }
//                     },
//                     scales: {
//                         x: {
//                             type: 'time', // Especificar que estamos usando fechas en el eje X
//                             title: {
//                                 display: true,
//                                 text: 'Date'
//                             },
//                             time: {
//                                 unit: 'month', // Mostrar por meses
//                                 tooltipFormat: 'yyyy-MM',
//                                 displayFormats: {
//                                     month: 'MMM yyyy' // Formato de fecha para mostrar en el gráfico
//                                 }
//                             }
//                         },
//                         y: {
//                             beginAtZero: true,
//                             title: {
//                                 display: true,
//                                 text: 'Baby Growth (cm)'
//                             }
//                         }
//                     }
//                 }
//             });
//         } else {
//             document.getElementById('growth-chart').style.display = 'none';
//             document.getElementById('no-data-message').style.display = 'block';
//         }
//     });

// ! Option 3
fetch('/get_growth_data')
    .then(response => response.json())
    .then(response => {
        console.log(response); // Verificar la respuesta en la consola
        const { has_data, data } = response;

        if (has_data) {
            // Convertir las fechas de "YYYY-MM" a objetos Date
            const labels = data.map(item => {
                const year = item.year;
                const month = item.month;
                // Crear una nueva fecha con el primer día de cada mes
                return new Date(year, month - 1); // Los meses en JavaScript empiezan desde 0
            });

            // Obtener las alturas para la gráfica
            const growth = data.map(item => item.growth_cm);

            const ctx = document.getElementById('growth-chart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Baby Growth (cm)',
                        data: growth,
                        borderColor: 'rgba(75, 192, 192, 1)', // Ajustar color de la línea
                        backgroundColor: 'rgba(75, 192, 192, 0.2)', // Ajustar color de fondo
                        pointBackgroundColor: 'rgba(75, 192, 192, 1)', // Ajustar color de los puntos
                        pointBorderColor: 'rgba(75, 192, 192, 1)', // Ajustar color del borde de los puntos
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: true },
                        tooltip: {
                            callbacks: {
                                
                                label: function(tooltipItem) {
                                    const currentHeight = tooltipItem.raw;
                                    const currentDate = tooltipItem.label;
                                    return `${currentDate}: ${currentHeight.toFixed(2)} cm`;
                                },
                                afterLabel: function(tooltipItem) {
                                    const index = tooltipItem.dataIndex;
                                    const currentHeight = tooltipItem.raw;
                                    let beforeLabel = ''; 

                                    // Si no es el primer registro, calcular la diferencia
                                    if (index > 0) {
                                        const previousHeight = growth[index - 1];
                                        const growthDifference = currentHeight - previousHeight;
                                        const previousDate = labels[index - 1].toLocaleDateString('en-US', { year: 'numeric', month: 'short' });

                                        // Determinar si la diferencia es positiva o negativa y agregar el símbolo correspondiente
                                        const differenceSign = growthDifference >= 0 ? '+' : '';  // Si es positivo, agregar el '+'
                                        
                                        // Agregar la diferencia como contenido adicional
                                        //// beforeLabel = `${previousDate}: ${differenceSign}${growthDifference.toFixed(2)} cm`;
                                        beforeLabel = `Growth: ${differenceSign} ${growthDifference.toFixed(2)} cm`;
                                    }
                                    return beforeLabel;
                                },
                                
                            }
                        }
                    },
                    scales: {
                        x: {
                            type: 'time', // Especificar que estamos usando fechas en el eje X
                            title: {
                                display: true,
                                text: 'Date'
                            },
                            time: {
                                unit: 'month', // Mostrar por meses
                                tooltipFormat: 'yyyy-MM',
                                displayFormats: {
                                    month: 'MMM yyyy' // Formato de fecha para mostrar en el gráfico
                                }
                            }
                        },
                        y: {
                            beginAtZero: false, // Iniciar el eje Y desde el valor más bajo
                            title: {
                                display: true,
                                text: 'Baby Growth (cm)'
                            }
                        }
                    }
                }
            });
        } else {
            document.getElementById('growth-chart').style.display = 'none';
            document.getElementById('no-data-message').style.display = 'block';
        }
    });


const phrases = [
    "Track your baby's growth with ease!",
    "Set and achieve your parenting and baby goals!",
    "Stay updated with the latest insights for your baby's development!",
    "Get personalized recommendations for your baby's health and wellness!",
    "Get AI advice on parenting and baby care!",
    "Get the best baby care tips and tricks!",
];

let index = 0;
setInterval(() => {
    document.getElementById('rotating-banner').textContent = phrases[index];
    index = (index + 1) % phrases.length;
}, 5000);

document.addEventListener("DOMContentLoaded", function() {
    const babyNameElement = document.getElementById('baby-name');
    const gender = "{{ baby.gender }}"; // Asumiendo que tienes esta variable disponible

    // Colores pastel para niño
    const colorsBoy = [
        '#BAE1FF', // pastel blue
        '#BAFFC9', // pastel green
        '#FFFFBA', // pastel yellow
        '#E1BAFF', // pastel purple
        '#A0E7E5', // pastel cyan
        '#B4F8C8', // pastel mint
        '#FFAEBC', // pastel pink
        '#FBE7C6', // pastel peach
        '#C1C8E4', // pastel lavender
        '#D4A5A5'  // pastel rose
    ];

    // Colores pastel para niña
    const colorsGirl = [
        '#FFB3BA', // pastel pink
        '#FFDFBA', // pastel orange
        // '#FFFFBA', // pastel yellow
        '#F7B5D4', // pastel pink
        '#FFAEBC', // pastel pink
        '#FFC3A0', // pastel peach
        '#FFB7B2', // pastel coral
        '#FFDAC1', // pastel apricot
        // '#E2F0CB', // pastel lime
        '#C1C8E4'  // pastel lavender
    ];

    const colors = gender === 'boy' ? colorsBoy : colorsGirl;
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    babyNameElement.style.color = randomColor;
});
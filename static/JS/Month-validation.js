document.addEventListener('DOMContentLoaded', function() {
    // Parsear el JSON correctamente
    const rangesByDate = JSON.parse(document.getElementById('ranges-json-data').value);
    const birthDate = new Date(document.getElementById('birth_date').value);
    const birthYear = birthDate.getFullYear();
    const birthMonth = birthDate.getMonth() + 1; // Meses en JS son 0-11

    const yearSelect = document.getElementById('year');
    const monthSelect = document.getElementById('month');
    const weightSelect = document.getElementById('weight');
    const heightSelect = document.getElementById('height');
    const currentYear = new Date().getFullYear();
    const currentMonth = new Date().getMonth() + 1;

    function updateMonths() {
        const selectedYear = parseInt(yearSelect.value);
        for (let i = 1; i <= 12; i++) {
            const option = monthSelect.querySelector(`option[value="${i}"]`);
            if (option) {
                if (selectedYear === birthYear && i < birthMonth) {
                    option.style.display = 'none'; // Ocultar meses antes del nacimiento
                } else if (selectedYear === currentYear && i > currentMonth) {
                    option.style.display = 'none'; // Ocultar meses futuros
                } else {
                    option.style.display = ''; // Mostrar meses válidos
                }
            }
        }
        updateRanges();
    }

    function updateRanges() {
        const selectedYear = parseInt(yearSelect.value);
        const selectedMonth = parseInt(monthSelect.value);
        if (selectedYear && selectedMonth) {
            const key = `${selectedYear}-${selectedMonth}`;
            const ranges = rangesByDate[key];
            if (ranges) {
                weightSelect.innerHTML = '<option value="" disabled selected>Select a weight</option>';
                ranges.weight_range.forEach(weight => {
                    const option = document.createElement('option');
                    option.value = weight;
                    option.textContent = weight + ' kg';
                    weightSelect.appendChild(option);
                });

                heightSelect.innerHTML = '<option value="" disabled selected>Select a height</option>';
                ranges.height_range.forEach(height => {
                    const option = document.createElement('option');
                    option.value = height;
                    option.textContent = height + ' cm';
                    heightSelect.appendChild(option);
                });
            }
        }
    }

    yearSelect.addEventListener('change', updateMonths);
    monthSelect.addEventListener('change', updateRanges);

    // Inicializar al cargar la página
    if (yearSelect.value) updateMonths();
});
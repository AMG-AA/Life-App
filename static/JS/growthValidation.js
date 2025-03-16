// Cargar los archivos JSON con los percentiles de peso y altura
async function loadPercentiles() {
    const boysWeightData = await fetch('/assets/boys_weight_for_age.json').then(res => res.json());
    const girlsWeightData = await fetch('/assets/girls_weight_for_age.json').then(res => res.json());
    const boysHeightData = await fetch('/assets/boys_height_for_age.json').then(res => res.json());
    const girlsHeightData = await fetch('/assets/girls_height_for_age.json').then(res => res.json());

    return { boysWeightData, girlsWeightData, boysHeightData, girlsHeightData };
}

// Calcular la edad en meses basándose en la fecha de nacimiento
function calculateAgeInMonths(birthDate) {
    const birth = new Date(birthDate);
    const today = new Date();
    const ageInMonths = (today.getFullYear() - birth.getFullYear()) * 12 + (today.getMonth() - birth.getMonth());
    return ageInMonths;
}

// Obtener los percentiles de peso o altura según el género y la edad
function getPercentileData(gender, type, ageInMonths, percentilesData) {
    const data = type === 'weight' ? (gender === 'Boy' ? percentilesData.boysWeightData : percentilesData.girlsWeightData) :
                                    (gender === 'Boy' ? percentilesData.boysHeightData : percentilesData.girlsHeightData);

    return data.find(entry => entry.Month === ageInMonths);  // Buscar por edad
}

// Validar los datos de crecimiento (peso y altura)
async function validateGrowthData(event, babyData) {
    event.preventDefault();  // Prevenir el envío del formulario por defecto

    const percentiles = await loadPercentiles();  // Cargar los percentiles
    const form = event.target;
    const weightInput = document.getElementById("weight");
    const heightInput = document.getElementById("height");
    const weightError = document.getElementById("weight-error");
    const heightError = document.getElementById("height-error");

    const weight = parseFloat(weightInput.value);
    const height = parseFloat(heightInput.value);
    const gender = babyData.gender;  // Género del bebé
    const birthDate = babyData.birth_date;  // Fecha de nacimiento del bebé
    
    const ageInMonths = calculateAgeInMonths(birthDate);  // Calcular la edad en meses

    // Obtener los percentiles de peso y altura para el bebé
    const weightPercentiles = getPercentileData(gender, 'weight', ageInMonths, percentiles);
    const heightPercentiles = getPercentileData(gender, 'height', ageInMonths, percentiles);

    // Validar peso
    if (weightPercentiles && (weight < weightPercentiles.P5 || weight > weightPercentiles.P95)) {
        weightError.textContent = `Weight is outside the normal percentiles (P5 to P95).`;
    } else {
        weightError.textContent = '';  // Limpiar el error si es válido
    }

    // Validar altura
    if (heightPercentiles && (height < heightPercentiles.P5 || height > heightPercentiles.P95)) {
        heightError.textContent = `Height is outside the normal percentiles (P5 to P95).`;
    } else {
        heightError.textContent = '';  // Limpiar el error si es válido
    }
    
    // Si no hay errores, enviar el formulario
    if (!weightError.textContent && !heightError.textContent) {
        form.submit();
    }
}

// Validar el formulario de crecimiento
function validateForm(event) {
    const form = event.target;
    const weightInput = document.getElementById("weight");
    const heightInput = document.getElementById("height");
    const weightError = document.getElementById("weight-error");
    const heightError = document.getElementById("height-error");

    let valid = true;

    weightError.textContent = "";
    heightError.textContent = "";

    if (isNaN(weightInput.value) || weightInput.value <= 0 || weightInput.value > 80) {
        weightError.textContent = "Weight must be a number between 0.01 and 80.";
        valid = false;
    }

    if (isNaN(heightInput.value) || heightInput.value <= 0 || heightInput.value > 200) {
        heightError.textContent = "Height must be a number between 0.01 and 200.";
        valid = false;
    }

    if (!valid) {
        event.preventDefault();
    }
}

// Limitar la longitud de entrada
function limitInputLength(inputElement, maxLength) {
    inputElement.addEventListener("input", function() {
        if (inputElement.value.length > maxLength) {
            inputElement.value = inputElement.value.slice(0, maxLength);
        }
    });
}

// Conectar todo y validar cuando el formulario se envíe
document.addEventListener("DOMContentLoaded", async function() {
    const babyId = 1;  // Ejemplo de ID del bebé
    const babyData = await fetchBabyData(babyId);  // Obtener los datos del bebé

    const form = document.querySelector("#growth-form");
    form.addEventListener("submit", (event) => validateGrowthData(event, babyData));  // Validar datos al enviar

    const yearSelect = document.getElementById('year');
    const monthSelect = document.getElementById('month');
    const weightSelect = document.getElementById('weight');
    const heightSelect = document.getElementById('height');
    const birthDate = new Date(document.getElementById('birth_date').value);

    yearSelect.addEventListener('change', () => {
        if (validateYear(yearSelect)) {
            updateMonthOptions(yearSelect, monthSelect);
        }
    });
    monthSelect.addEventListener('change', () => updateGrowthOptions(yearSelect, monthSelect, weightSelect, heightSelect, birthDate));

    if (yearSelect.value) {
        updateMonthOptions(yearSelect, monthSelect);
    }

    form.addEventListener("submit", validateForm);

    limitInputLength(document.getElementById("weight"), 4);
    limitInputLength(document.getElementById("height"), 4);
});

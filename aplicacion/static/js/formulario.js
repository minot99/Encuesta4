const totalPasos = document.querySelectorAll('.step').length;
const steps = document.querySelectorAll(".stp");
const circleSteps = document.querySelectorAll(".step");
const formInputs = document.querySelectorAll(".step-1 form input");
let currentStep = 1;
let currentCircle = 0;

steps.forEach((step) => {
  const nextBtn = step.querySelector(".next-stp");
  const prevBtn = step.querySelector(".prev-stp");
  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      document.querySelector(`.step-${currentStep}`).style.display = "none";
      currentStep--;
      document.querySelector(`.step-${currentStep}`).style.display = "flex";
      circleSteps[currentCircle].classList.remove("active");
      currentCircle--;
      actualizarBarraDeProgreso(currentStep);
    });
  }
  nextBtn.addEventListener("click", () => {
    document.querySelector(`.step-${currentStep}`).style.display = "none";
    if (currentStep < 6 && validateForm()) {
      currentStep++;
      currentCircle++;
    }
    document.querySelector(`.step-${currentStep}`).style.display = "flex";
    circleSteps[currentCircle].classList.add("active");
    actualizarBarraDeProgreso(currentStep);
  });
});

function validateForm() {
  let valid = true;
  formInputs.forEach(input => {
    if (!input.value) {
      valid = false;
      input.classList.add("err");
      findLabel(input).nextElementSibling.style.display = "flex";
    } else {
      input.classList.remove("err");
      findLabel(input).nextElementSibling.style.display = "none";
    }
  });
  return valid;
}

function findLabel(el) {
  const idVal = el.id;
  const labels = document.getElementsByTagName("label");
  for (let i = 0; i < labels.length; i++) {
    if (labels[i].htmlFor === idVal) return labels[i];
  }
}

function actualizarBarraDeProgreso(pasoActual) {
    const progreso = (pasoActual / totalPasos) * 100;
    const barraDeProgreso = document.getElementById('barra-porcentaje');
    barraDeProgreso.style.width = `${progreso}%`;
    barraDeProgreso.innerText = `${progreso.toFixed(2)}%`;

    // Cambiar color de fondo según el progreso
    if (progreso <= (100 / 3)) {
      barraDeProgreso.style.backgroundColor = 'red'; // Menor o igual a 1/3
    } else if (progreso > (100 / 3) && progreso <= (200 / 3)) {
        barraDeProgreso.style.backgroundColor = 'orange'; // Mayor a 1/3 y menor o igual a 2/3
    } else {
        barraDeProgreso.style.backgroundColor = 'green'; // Mayor a 2/3
    }
}
actualizarBarraDeProgreso(currentStep);
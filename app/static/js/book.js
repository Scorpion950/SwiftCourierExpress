document.addEventListener('DOMContentLoaded', function () {
  const weightInput = document.getElementById('weight_kg');
  const serviceInput = document.getElementById('service_type');
  const chargeInput = document.getElementById('charge');

  function calculateCharge() {
    if (!weightInput || !serviceInput || !chargeInput) return;
    const weight = Number(weightInput.value || 0);
    const service = serviceInput.value || 'Standard';
    let charge = 100 + weight * 50;
    if (service === 'Express') charge *= 1.5;
    if (service === 'International') charge *= 3;
    chargeInput.value = charge.toFixed(2);
  }

  if (weightInput) {
    weightInput.addEventListener('input', calculateCharge);
  }
  if (serviceInput) {
    serviceInput.addEventListener('change', calculateCharge);
  }

  if (chargeInput && !chargeInput.value) {
    calculateCharge();
  }
});

document.addEventListener("DOMContentLoaded", async function () {
  const stateSelect = document.getElementById("state_of_origin");
  const lgaSelect = document.getElementById("local_department");
  if (!stateSelect || !lgaSelect) return;

  stateSelect.innerHTML = '<option value="">Select State</option>';
  lgaSelect.innerHTML = '<option value="">Select LGA</option>';

  try {
    const response = await fetch('/static/js/states.json');
    const stateInfo = await response.json();

    stateInfo.forEach((item) => {
      stateSelect.add(new Option(item.state, item.state));
    });

    stateSelect.addEventListener("change", function () {
      lgaSelect.length = 1;
      const selected = stateInfo.find((item) => item.state === this.value);
      if (!selected) return;
      selected.local.forEach((lga) => {
        lgaSelect.add(new Option(lga, lga));
      });
    });
  } catch (error) {
    console.error('Failed to load state data:', error);
  }
});

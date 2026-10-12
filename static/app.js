document.querySelectorAll("form[data-validate]").forEach(function (form) {
  form.addEventListener("submit", function (e) {
    var bad = false;
    form.querySelectorAll(".err").forEach(function (x) { x.textContent = ""; });
    form.querySelectorAll("input[data-required]").forEach(function (input) {
      var err = form.querySelector('.err[data-for="' + input.name + '"]');
      var value = input.type === "password" ? input.value : input.value.trim();
      var msg = "";
      if (!value) msg = input.dataset.required;
      else if (input.dataset.match && value !== form.elements[input.dataset.match].value) msg = input.dataset.mismatch;
      else if (input.dataset.max && value.length > Number(input.dataset.max)) msg = input.dataset.toolong;
      if (msg) { err.textContent = msg; bad = true; }
    });
    if (bad) e.preventDefault();
  });
});

document.querySelectorAll("form[data-confirm]").forEach(function (form) {
  form.addEventListener("submit", function (e) {
    if (!confirm(form.dataset.confirm)) e.preventDefault();
  });
});

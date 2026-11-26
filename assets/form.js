// Turns a form's answers into an email draft. Nothing is sent or stored by this site:
// the visitor's own email app opens with the answers filled in, and they press send.
// Without JavaScript the form still works: its action is a mailto: link.
(function () {
  var form = document.querySelector("form[data-mailto]");
  if (!form) return;
  var result = document.getElementById("form-result");
  var output = document.getElementById("form-output");
  var copy = document.getElementById("form-copy");
  var copied = document.getElementById("form-copied");

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var lines = [];
    form.querySelectorAll("[data-q]").forEach(function (group) {
      var answers = [];
      group.querySelectorAll("input, textarea").forEach(function (el) {
        if (el.type === "radio" || el.type === "checkbox") {
          if (el.checked) answers.push(el.value);
        } else if (el.value.trim()) {
          answers.push(el.value.trim());
        }
      });
      lines.push(group.getAttribute("data-q") + "\n" + (answers.length ? answers.join("\n") : "(no answer)"));
    });
    var body = lines.join("\n\n");

    output.value = body;
    copied.textContent = "";
    result.hidden = false;
    result.focus();

    window.location.href = "mailto:" + form.getAttribute("data-mailto") +
      "?subject=" + encodeURIComponent(form.getAttribute("data-subject")) +
      "&body=" + encodeURIComponent(body);
  });

  copy.addEventListener("click", function () {
    output.select();
    var done = function () { copied.textContent = "Copied."; };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(output.value).then(done, function () { document.execCommand("copy"); done(); });
    } else {
      document.execCommand("copy"); done();
    }
  });
})();

// ==UserScript==
// @match *://*/*
// ==/UserScript==

let passwordFields = null;

document.addEventListener("keydown", (event) => {
  if (
    event.ctrlKey &&
    event.shiftKey &&
    (event.key === "s" || event.key === "S")
  ) {
    if (passwordFields === null) {
      passwordFields = document.querySelectorAll("input[type=password]");
      for (const passwordField of passwordFields) {
        passwordField.type = "text";
      }
    } else {
      for (const passwordField of passwordFields) {
        passwordField.type = "password";
      }
      passwordFields = null;
    }
  }
});

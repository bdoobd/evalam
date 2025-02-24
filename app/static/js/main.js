const nav = document.querySelector("nav");

nav.addEventListener("click", (event) => {
  event.preventDefault();
  if (
    event.target.hasAttribute("href") &&
    event.target.getAttribute("href") !== "#"
  ) {
    console.dir("point found");
  }
});

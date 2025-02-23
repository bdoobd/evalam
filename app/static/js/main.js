const loginSubmit = document.getElementById("submit");
const alertBlock = document.querySelector(".alert");
loginSubmit.addEventListener("click", login);

async function login(event) {
  event.preventDefault();

  const loginForm = document.getElementById("loginForm");
  const loginFormData = new FormData(loginForm);
  const loginData = Object.fromEntries(loginFormData.entries());

  console.log(JSON.stringify(loginData));
  try {
    const response = await fetch("/user/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(loginData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail);
    }

    const result = await response.json();

    console.log("result", result);
    // if (result.access_token) {
    //   window.location.href = "/";
    // }
  } catch (error) {
    loginForm.reset();
    // TODO: Вывести ошибку на страницу
    const alertBlock = document.querySelector(".alert");
    alertBlock.textContent = error.message;
    alertBlock.classList.remove("hide-element");
    // window.location.href = "/login";
    console.error("Error:", error);
  }
}

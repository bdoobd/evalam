const addUserButton = document.getElementById("add-user");
const modalWindowBlock = document.getElementById("modal-window");
const userForm = document.querySelector("table");

addUserButton.addEventListener("click", (e) => {
  e.preventDefault();
  modalWindowBlock.insertAdjacentHTML("afterbegin", userModalWindow());
  // TODO: Добавить функцию создания динамического списка для ролей
  createSelectOptions();
});

modalWindowBlock.addEventListener("click", (e) => {
  if (e.target.classList.contains("btn-close")) {
    modalWindowBlock.innerHTML = "";
  }
});

const userModalWindow = function (data = { action: "create" }) {
  return `
  <div class="modal-base">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="staticBackdropLabel">${
                  data.title ?? "Add new"
                } category</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
             <form id="userForm" onsubmit="processForm(event)">
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" class="form-control" id="username" name="username" value="${
                      data.username ?? ""
                    }">
                </div>
                <div class="mb-3">
                    <label for="role" class="form-label">Role</label>
                    <select class="form-select" aria-label="Default select" name="role" id="role">
                      <!-- <option selected>Open this select menu</option> -->
                    </select>
                </div>
                <div class="form-check mb-2">
                    <input class="form-check-input" type="checkbox" value="true" name="disabled" id="disabled">
                    <label class="form-check-label" for="disabled">
                    Disabled
                    </label>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password" name="password" value="">
                </div>
                <div class="mb-3">
                    <label for="confirm_password" class="form-label">Confirm password</label>
                    <input type="password" class="form-control" id="confirm_password" name="confirm_password" value="">
                </div>
                <input type="hidden" name="id" value="${data.id ?? ""}">
                <input type="hidden" name="action" value="${
                  data.action ?? "create"
                }">
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
            </div>
        </div>
    </div>
</div>`;
};

const userDeleteWindow = function (data) {
  console.log("DeleteUserWindow");
};

async function processForm(e, data) {
  e.preventDefault();

  const userForm = document.getElementById("userForm");
  const userFormData = new FormData(userForm);
  const userData = Object.fromEntries(userFormData);
  let actionURL = "/user/register";
  let actionMethod = "POST";

  if (userData.action === "update") {
    let actionURL = `/user/${userData.id}`;
    let actionMethod = "PUT";
  }

  try {
    const response = await fetch(actionURL, {
      method: actionMethod,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail);
    }

    const result = await response.json();

    console.log(result);
    userForm.reset();
    modalWindowBlock.innerHTML = "";
    window.location.href = "/admin";
  } catch (error) {
    console.error(error);
  }
}

async function getRoles() {
  try {
    const response = await fetch("/user/roles");
    const result = await response.json();

    return result;
  } catch (error) {
    console.error(error);
  }
}
async function createSelectOptions() {
  const selectList = document.getElementById("role");

  const rolesData = await getRoles();
  for (let key in await rolesData) {
    let optionItem = document.createElement("option");
    optionItem.value = key;
    optionItem.textContent = rolesData[key];

    if (key === "user") {
      optionItem.selected = true;
    }

    selectList.appendChild(optionItem);
  }
}

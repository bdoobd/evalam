const addUserButton = document.getElementById("add-user");
const modalWindowBlock = document.getElementById("modal-window");
const userTable = document.querySelector("table");

addUserButton.addEventListener("click", (e) => {
  e.preventDefault();
  modalWindowBlock.insertAdjacentHTML("afterbegin", userModalWindow());
  createSelectOptions();
});

modalWindowBlock.addEventListener("click", (e) => {
  if (e.target.classList.contains("btn-close")) {
    modalWindowBlock.innerHTML = "";
  }
});

userTable.addEventListener("click", (e) => {
  const element = e.target;
  if (element.nodeName !== "IMG") {
    return;
  }

  const itemId = element.dataset.itemId;
  const itemAction = element.dataset.itemAction;

  if (itemAction && doAction[itemAction]) {
    doAction[itemAction](itemId);
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
                } user data</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
             <form id="userForm" onsubmit="processForm(event)">
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" class="form-control" id="username" name="username" value="${
                      data.username ?? ""
                    }" ${data.action === "update" ? "disabled" : ""}>
                </div>
                <div class="mb-3">
                    <label for="role" class="form-label">Role</label>
                    <select class="form-select" aria-label="Default select" name="role" id="role">
                      <!-- <option selected>Open this select menu</option> -->
                    </select>
                </div>
                <div class="form-check mb-2">
                    <input class="form-check-input" type="checkbox" value="true" name="disabled" id="disabled" ${
                      data.disabled ? `checked` : ``
                    }>
                    <label class="form-check-label" for="disabled">
                    Disabled
                    </label>
                </div>
                ${
                  data.action === "create"
                    ? `
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password" name="password" value="">
                </div>
                <div class="mb-3">
                    <label for="confirm_password" class="form-label">Confirm password</label>
                    <input type="password" class="form-control" id="confirm_password" name="confirm_password" value="">
                </div>`
                    : ``
                }
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

const userDeleteModalWindow = function (data) {
  return `
  <div class="modal-base">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="staticBackdropLabel">${"Delete user"} category</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
             <form id="deleteForm" onsubmit="deleteUser(event)">
                <h6>Do you really need to delete user from DB?</h6>
                <p><small>Name - ${data.username},</small></p>
                <p><small>Role - ${data.role},</small></p>
                <input type="hidden" name="id" value="${data.id}">
                <button type="submit" class="btn btn-danger">Delete</button>
              </form>
            </div>
        </div>
    </div>
</div>`;
};

// const userDeleteWindow = function (data) {
//   console.log("DeleteUserWindow");
// };

async function processForm(e, data) {
  e.preventDefault();

  const userForm = document.getElementById("userForm");
  const userFormData = new FormData(userForm);
  const userData = Object.fromEntries(userFormData);
  let actionURL = "/user/register";
  let actionMethod = "POST";

  if (userData.action === "update") {
    actionURL = `/user/${userData.id}`;
    actionMethod = "PUT";
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

    userForm.reset();
    modalWindowBlock.innerHTML = "";
    window.location.href = "/admin";
  } catch (error) {
    console.error(error);
  }
}

async function deleteUser(e) {
  e.preventDefault();

  const deleteForm = document.getElementById("deleteForm");
  const deleteFormData = new FormData(deleteForm);
  const deleteData = Object.fromEntries(deleteFormData);
  try {
    const response = await fetch(`/user/${deleteData.id}`, {
      method: "DELETE",
      "Content-Type": "application/json",
      body: deleteData.id,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail);
    }
    deleteForm.reset();
    modalWindowBlock.innerHTML = "";
    window.location.href = "/admin";
  } catch (error) {
    console.error(error);
  }
  console.log(`Trying to delete user ${deleteData.id}`);
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
async function createSelectOptions(role = "user") {
  const selectList = document.getElementById("role");

  const rolesData = await getRoles();
  for (let key in await rolesData) {
    let optionItem = document.createElement("option");
    optionItem.value = key;
    optionItem.textContent = rolesData[key];

    if (key === role) {
      optionItem.selected = true;
    }

    selectList.appendChild(optionItem);
  }
}

const getUserData = async function (id) {
  try {
    const response = await fetch(`/user/${id}`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error(error);
  }
};

const doAction = {
  edit: async function (id) {
    const data = await getUserData(id);
    data.title = "Update";
    data.action = "update";

    modalWindowBlock.insertAdjacentHTML("afterbegin", userModalWindow(data));
    createSelectOptions(data.role);
  },
  delete: async function (itemId) {
    const data = await getUserData(itemId);
    modalWindowBlock.insertAdjacentHTML(
      "afterbegin",
      userDeleteModalWindow(data)
    );
    // console.log(`Delete user with ID ${itemId}`);
    // console.log(data);
  },
};

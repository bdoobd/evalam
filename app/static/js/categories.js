const addCatButton = document.querySelector("#add-category");
const modalWindowBlock = document.querySelector("#modal-window");
const catTable = document.querySelector("table");

addCatButton.addEventListener("click", () => {
  modalWindowBlock.insertAdjacentHTML("afterbegin", category_modal_window());
});

modalWindowBlock.addEventListener("click", (e) => {
  if (e.target.classList.contains("btn-close")) {
    modalWindowBlock.innerHTML = "";
  }
});

const category_modal_window = function (data = { action: "create" }) {
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
             <form id="categoryForm" onsubmit="processForm(event)">
                <div class="mb-3">
                    <label for="name" class="form-label">Name</label>
                    <input type="text" class="form-control" id="name" name="name" value="${
                      data.name ?? ""
                    }">
                </div>
                <div class="mb-3">
                    <label for="cat" class="form-label">Type</label>
                    <input type="text" class="form-control" id="cat" name="cat" value="${
                      data.cat ?? ""
                    }">
                </div>
                <div class="mb-3">
                    <label for="width" class="form-label">Width</label>
                    <input type="number" class="form-control" id="width" name="width" value="${
                      data.width ?? ""
                    }">
                </div>
                <div class="mb-3">
                    <label for="weight" class="form-label">Weight</label>
                    <input type="number" class="form-control" id="weight" name="weight" value="${
                      data.weight ?? ""
                    }">
                </div>
                <div class="mb-3">
                    <label for="note" class="form-label">Note</label>
                    <textarea class="form-control" id="note" rows="3" name="note">${
                      data.note ?? ""
                    }</textarea>
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

const delete_category_modal_window = function (data) {
  return `
<div class="modal-base">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="staticBackdropLabel">Delete category</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
             <form id="deleteForm" onsubmit="deleteCat(event)">
                <h6>Do you really need to delete category from DB?</h6>
                <p><small>Name - ${data.name},</small></p>
                <p><small>Category - ${data.cat},</small></p>
                <p><small>Item width - ${data.width},</small></p>
                <p><small>Item wight - ${data.weight},</small></p>
                <p><small>Category note - ${data.note}</small></p>
                <input type="hidden" name="id" value="${data.id}">
                <button type="submit" class="btn btn-danger">Delete</button>
              </form>
            </div>
        </div>
    </div>
</div>`;
};

async function processForm(e, data) {
  e.preventDefault();

  const categoryForm = document.getElementById("categoryForm");
  const categoryFormData = new FormData(categoryForm);
  const categoryData = Object.fromEntries(categoryFormData.entries());
  let actionURL = "/cat/new";
  let actionMethod = "POST";

  if (categoryData.action === "update") {
    actionMethod = "PUT";
    actionURL = `/cat/${categoryData.id}`;
  }

  try {
    const response = await fetch(actionURL, {
      method: actionMethod,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(categoryData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail);
    }

    const result = await response.json();

    categoryForm.reset();
    modalWindowBlock.innerHTML = "";
    window.location.href = "/cats";

    return result;
  } catch (error) {
    console.error(error);
  }
}

async function deleteCat(e) {
  e.preventDefault();

  const deleteForm = document.getElementById("deleteForm");
  const deleteFormData = new FormData(deleteForm);
  const deleteData = Object.fromEntries(deleteFormData);
  try {
    const response = await fetch(`/cat/${deleteData.id}`, {
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
    window.location.href = "/cats";
  } catch (error) {
    console.error(error);
  }
  console.log(`Delete ${deleteData.id}`);
}

catTable.addEventListener("click", (e) => {
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

const doAction = {
  edit: async function (itemId) {
    const data = await getCategoryData(itemId);
    data.title = "Update";
    data.action = "update";

    modalWindowBlock.insertAdjacentHTML(
      "afterbegin",
      category_modal_window(data)
    );
  },
  delete: async function (itemId) {
    const data = await getCategoryData(itemId);
    modalWindowBlock.insertAdjacentHTML(
      "afterbegin",
      delete_category_modal_window(data)
    );
  },
};

const getCategoryData = async function (catId) {
  try {
    const response = await fetch(`/cat/${catId}`);
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

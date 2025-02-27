const addCatButton = document.querySelector("#add-category");
const modalWindowBlock = document.querySelector("#modal-window");
const catTable = document.querySelector("table");

addCatButton.addEventListener("click", () => {
  modalWindowBlock.insertAdjacentHTML("afterbegin", category_modal_window());
  const closeCross = document
    .querySelector(".btn-close")
    .addEventListener("click", () => {
      modalWindowBlock.innerHTML = "";
    });
});

const category_modal_window = function (data = {}) {
  return `
<div class="modal-base">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="staticBackdropLabel">Add new category</h5>
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
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
            </div>
        </div>
    </div>
</div>`;
};

async function processForm(e) {
  e.preventDefault();

  const categoryForm = document.getElementById("categoryForm");
  const categoryFormData = new FormData(categoryForm);
  const categoryData = Object.fromEntries(categoryFormData.entries());

  try {
    const response = await fetch("/cat/new", {
      method: "POST",
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
  } catch (error) {
    console.error(error);
    //   TODO: Отобразить ошибку пользователю
  }
}

catTable.addEventListener("click", (e) => {
  const element = e.target;
  if (element.nodeName !== "IMG") {
    return;
  }

  const itemId = element.dataset.itemId;
  const itemAction = element.dataset.itemAction;

  console.dir(`Call action ${itemAction} on item ID ${itemId}`);
});

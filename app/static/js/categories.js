const addCatButton = document.querySelector("#add-category");
const modalWindowBlock = document.querySelector("#modal-window");

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
                    <input type="text" class="form-control" id="name" name="name">
                </div>
                <div class="mb-3">
                    <label for="category" class="form-label">Type</label>
                    <input type="text" class="form-control" id="category" name="category">
                </div>
                <div class="mb-3">
                    <label for="width" class="form-label">Width</label>
                    <input type="number" class="form-control" id="width" name="width">
                </div>
                <div class="mb-3">
                    <label for="weight" class="form-label">Weight</label>
                    <input type="number" class="form-control" id="weight" name="weight">
                </div>
                <div class="mb-3">
                    <label for="note" class="form-label">Note</label>
                    <textarea class="form-control" id="note" rows="3" name="note"></textarea>
                </div>
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

    console.log(result);
  } catch (error) {
    console.error(error);
  }

  // if (response.ok) {
  //     modalWindowBlock.innerHTML = "";
  //     window.location.reload();
  // } else {
  //     alert("Error");
  // }
}

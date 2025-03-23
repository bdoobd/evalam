class Item {
  _parentElement = document.getElementById("modal-window");
  _addButton = document.getElementById("add-item");

  render() {
    this._parentElement.insertAdjacentHTML("afterbegin", this._modalMarkup());

    this.submitFormData();
  }

  addHandlerAddNew(handler) {
    // this._parentElement.insertAdjacentHTML(
    //   "afterbegin",
    //   this.generateStockMarkup()
    // );
    this._addButton.addEventListener("click", (e) => {
      //   const addButton = e.target.closest("#add-item");
      const addButton = e.target;

      // console.log(addButton);
      handler();
    });
  }

  submitFormData() {
    document
      .getElementById("itemForm")
      .addEventListener("submit", async (e) => {
        // e.preventDefault();

        const form = e.target;

        console.log("form", form);
      });
  }
  // TODO: Можно ли добавить кусок HTML кода внутрь формы динамически?
  _modalMarkup() {
    return `<div class="modal-base">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="staticBackdropLabel">Select stock ref</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
             <form id="itemForm">
                <div class="form-check mb-3">
                  <input class="form-check-input" type="radio" name="stock-ref" id="new-stock">
                  <label class="form-check-label" for="new-stock">
                    Add new stock
                  </label>
                </div>
                <div class="form-check mb-3">
                  <input class="form-check-input" type="radio" name="stock-ref" id="select-stock" checked>
                  <label class="form-check-label" for="select-stock">
                    Select existing stock
                  </label>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
            </div>
        </div>
    </div>
</div>`;
  }
}

export default new Item();

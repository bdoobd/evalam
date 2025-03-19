class Stock {
  _parentElement = document.getElementById("modal-window");
  _addButton = document.getElementById("add-stock");
  _table = document.getElementById("stocks");

  render(data = {}) {
    this._parentElement.insertAdjacentHTML("afterbegin", this._modalMarkup());
    this.closeButtonHandler();
    this.submitFormData();
  }

  async submitFormData() {
    document.getElementById("stockForm").addEventListener("submit", (e) => {
      e.preventDefault();

      const form = e.target;
      // console.log(form);
      const formData = new FormData(form);
      const data = Object.fromEntries(formData.entries());
      console.log(data);
    });
  }

  closeButtonHandler() {
    this._parentElement.addEventListener("click", (e) => {
      const closeButton = e.target.closest(".btn-close");
      if (!closeButton) return;
      this._parentElement.innerHTML = "";
    });
  }

  addHandlerModalWindow(handler) {
    this._addButton.addEventListener("click", (e) => {
      e.preventDefault();
      this.render();
    });

    if (this._table) {
      this._table.addEventListener("click", (e) => {
        e.preventDefault();
        const element = e.target;
        if (element.nodeName !== "IMG") {
          return;
        }

        const itemId = element.dataset.itemId;
        const itemAction = element.dataset.itemAction;

        if (itemAction) {
          this[itemAction](itemId);
        }
      });
    }
  }

  async edit(id) {
    console.log(`Edit stock ${id}`);
  }

  async delete(id) {
    console.log(`Delete stock ${id}`);
  }

  _modalMarkup() {
    return `<div class="modal-base">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="staticBackdropLabel">Create stock ref</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <form id="stockForm">
                                    <div class="mb-3">
                                        <label for="reference" class="form-label">Stock ref</label>
                                        <input type="text" class="form-control" id="reference" name="reference">
                                    </div>
                                    <div class="mb-3">
                                        <label for="date" class="form-label">Stock date</label>
                                        <input type="date" class="form-control" id="date" name="date">
                                    </div>
                                    <div class="mb-3">
                                        <label for="consignor" class="form-label">Consignor</label>
                                        <input type="text" class="form-control" id="consignor" name="consignor">
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
  }
}

export default new Stock();

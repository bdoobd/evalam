class Stock {
  _parentElement = document.getElementById("modal-window");
  _addButton = document.getElementById("add-stock");

  render() {
    this._parentElement.insertAdjacentHTML("afterbegin", this._modalMarkup());
    this.closeButtonHandler();
    this.submitFormData();
  }

  async submitFormData() {
    document.getElementById("stockForm").addEventListener("submit", (e) => {
      e.preventDefault();

      const form = e.target;
      //   console.log(`Form ${form} submited`);
      const formData = new FormData(form);
      const data = Object.fromEntries(formData.entries());
      console.log(data.reference);
    });
  }

  closeButtonHandler() {
    this._parentElement.addEventListener("click", (e) => {
      const closeButton = e.target.closest(".btn-close");
      if (!closeButton) return;
      this._parentElement.innerHTML = "";
    });
  }

  addHandlerAddNew(handler) {
    this._addButton.addEventListener("click", (e) => {
      e.preventDefault();
      const addButton = e.target;
      //   console.log("element", addButton);
      handler(addButton);
    });
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
                                        <input type="text" class="form-control" id="reference">
                                    </div>
                                    <div class="mb-3">
                                        <label for="date" class="form-label">Stock date</label>
                                        <input type="date" class="form-control" id="date">
                                    </div>
                                    <div class="mb-3">
                                        <label for="consignor" class="form-label">Consignor</label>
                                        <input type="text" class="form-control" id="consignor">
                                    </div>
                                    <div class="mb-3">
                                        <label for="note" class="form-label">Note</label>
                                        <textarea class="form-control" id="note" rows="3"></textarea>
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

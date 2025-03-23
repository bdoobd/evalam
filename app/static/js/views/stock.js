class Stock {
  _parentElement = document.getElementById("modal-window");
  _addButton = document.getElementById("add-stock");
  _table = document.getElementById("stocks");

  render(data = {}) {
    let modal = this._modalMarkup(data);
    if (data.action === "delete") {
      modal = this._modalDeleteMarkup(data);
    }

    this._parentElement.insertAdjacentHTML("afterbegin", modal);
    this.closeButtonHandler();
    this.submitFormData();
  }

  async submitFormData() {
    document
      .getElementById("stockForm")
      .addEventListener("submit", async (e) => {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        let method = "POST";
        let url = "/stock/new";
        let req_body = JSON.stringify(data);

        if (data.action === "update") {
          method = "PUT";
          url = `/stock/${data.id}`;
        }

        if (data.action === "delete") {
          method = "DELETE";
          url = `/stock/${data.id}`;
          req_body = data.id;
        }

        const response = await fetch(url, {
          method: method,
          headers: {
            "Content-Type": "application/json",
          },
          body: req_body,
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }

        const result = await response.json();
        form.reset();
        this._parentElement.innerHTML = "";
        window.location.href = "/stocks";

        return result;
      });
  }

  closeButtonHandler() {
    this._parentElement.addEventListener("click", (e) => {
      const closeButton = e.target.closest(".btn-close");
      if (!closeButton) return;
      this._parentElement.innerHTML = "";
    });
  }

  addHandlerModalWindow() {
    this._addButton.addEventListener("click", (e) => {
      e.preventDefault();
      this.render();
    });

    if (this._table) {
      this._table.addEventListener("click", async (e) => {
        e.preventDefault();
        const element = e.target;
        if (element.nodeName !== "IMG") {
          return;
        }

        const itemId = element.dataset.itemId;
        const itemAction = element.dataset.itemAction;

        if (itemAction) {
          await this[itemAction](itemId);
        }
      });
    }
  }

  async edit(id) {
    try {
      const request = await fetch(`/stock/${id}`);
      const data = await request.json();

      data.date = new Date(data.date).toISOString().split("T")[0];
      data.title = "Update";
      data.action = "update";

      this.render(data);
    } catch (error) {
      console.error(error);
    }
  }

  async delete(id) {
    try {
      const request = await fetch(`/stock/${id}`);
      const data = await request.json();
      data.date = new Date(data.date).toISOString().split("T")[0];
      data.action = "delete";

      this.render(data);
    } catch (error) {
      console.error(error);
    }
  }

  _modalMarkup(data = { action: "create" }) {
    return `<div class="modal-base">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="staticBackdropLabel">${
                                  data.title ?? "Add new"
                                } ref</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <form id="stockForm">
                                    <div class="mb-3">
                                        <label for="reference" class="form-label">Stock ref</label>
                                        <input type="text" class="form-control" id="reference" name="reference" value="${
                                          data.reference ?? ""
                                        }">
                                    </div>
                                    <div class="mb-3">
                                        <label for="date" class="form-label">Stock date</label>
                                        <input type="date" class="form-control" id="date" name="date" value="${
                                          data.date ?? ""
                                        }">
                                    </div>
                                    <div class="mb-3">
                                        <label for="consignor" class="form-label">Consignor</label>
                                        <input type="text" class="form-control" id="consignor" name="consignor" value="${
                                          data.consignor ?? ""
                                        }">
                                    </div>
                                    <div class="mb-3">
                                        <label for="note" class="form-label">Note</label>
                                        <textarea class="form-control" id="note" rows="3" name="note">${
                                          data.note ?? ""
                                        }</textarea>
                                    </div>
                                    <input type="hidden" name="id" value="${
                                      data.id ?? ""
                                    }">
                                    <input type="hidden" name="action" value="${
                                      data.action ?? "create"
                                    }">
                                    <button type="submit" class="btn btn-primary">Submit</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>`;
  }

  _modalDeleteMarkup(data) {
    return `<div class="modal-base">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="staticBackdropLabel">Delete stock</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <form id="stockForm">
                                    <div class="mb-3">
                                        <p>Are you sure you want to delete this stock?</p>
                                    </div>
                                    <div class="mb-3">
                                      <p>Stock reference: ${data.reference}</p>
                                      <p>Stock date: ${data.date}</p>
                                      <p>Stock consignor: ${data.consignor}</p>
                                      <p>Stock note: ${data.note}</p>
                                    </div>
                                    <input type="hidden" name="id" value="${data.id}">
                                    <input type="hidden" name="action" value="${data.action}">
                                    <button type="submit" class="btn btn-primary">Delete</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>`;
  }
}

export default new Stock();

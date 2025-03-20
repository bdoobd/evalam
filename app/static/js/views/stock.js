class Stock {
  _parentElement = document.getElementById("modal-window");
  _addButton = document.getElementById("add-stock");
  _table = document.getElementById("stocks");

  render(data = {}) {
    this._parentElement.insertAdjacentHTML(
      "afterbegin",
      this._modalMarkup(data)
    );
    this.closeButtonHandler();
    this.submitFormData();
  }

  async submitFormData() {
    document
      .getElementById("stockForm")
      .addEventListener("submit", async (e) => {
        e.preventDefault();

        const form = e.target;
        // console.log(form);
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        // console.log(data);
        let method = "POST";
        let url = "/stock/new";

        if (data.action === "update") {
          method = "PUT";
          url = `/stock/${data.id}`;
        }

        // console.log("method", method, "url", url);
        const response = await fetch(url, {
          method: method,
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
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
    // TODO: Получить данные по id
    //       Указать данные в форму
    //       Отправить обновлённые данные на сервер
    const request = await fetch(`/stock/${id}`);
    const data = await request.json();
    data.date = new Date(data.date).toISOString().split("T")[0];
    data.title = "Update";
    data.action = "update";
    this.render(data);
  }

  async delete(id) {
    console.log(`Delete stock ${id}`);
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
}

export default new Stock();

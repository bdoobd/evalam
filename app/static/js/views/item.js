import { getOpenRefs, getCategories } from "../model.js";

class Item {
  _parentElement = document.getElementById("modal-window");
  _addButton = document.getElementById("add-item");
  _referenceType = "new";

  render() {
    this._parentElement.insertAdjacentHTML("afterbegin", this._modalMarkup());

    this.submitFormData();
    this.closeButtonHandler();
  }

  addHandlerAddNew(handler) {
    this._addButton.addEventListener("click", (e) => {
      const addButton = e.target;

      handler();
    });
  }

  closeButtonHandler() {
    this._parentElement.addEventListener("click", (e) => {
      const closeButton = e.target.closest(".btn-close");
      if (!closeButton) return;
      this._parentElement.innerHTML = "";
    });
  }

  createCatSelectOptions = async function () {
    const catList = await getCategories();
    let catOptions = "";
    catList.forEach((cat) => {
      catOptions += `<option value="${cat.id}">${cat.name} ${cat.cat} ${cat.width}</option>`;
    });
    return catOptions;
  };

  async submitFormData() {
    document
      .getElementById("itemSelectStockForm")
      .addEventListener("submit", async (e) => {
        e.preventDefault();
        const fieldset = document.getElementById("stock-select");
        const form = e.target;
        this._stockType = form.elements["stock-ref"]?.value;

        if (form.elements["submit-item"]) {
          // console.log("Add new item");
          const formData = new FormData(form);
          const data = Object.fromEntries(formData.entries());
          console.log(data);

          const response = await fetch("/item/new", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
          });

          console.log(response);
        }

        if (form.elements["stock-ref-select"]) {
          fieldset.innerHTML = "";
          const stockList = await getOpenRefs();
          const catList = await this.createCatSelectOptions();

          fieldset.innerHTML = this._itemFieldsMarkup(stockList, catList);
        }
      });
  }

  _modalMarkup() {
    return `<div class="modal-base">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="staticBackdropLabel">Select stock ref</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
             <form id="itemSelectStockForm">
              <fieldset id="stock-select">
                <div class="form-check mb-3">
                  <input class="form-check-input" type="radio" name="stock-ref" id="new-stock" value="new">
                  <label class="form-check-label" for="new-stock">
                    Add new stock
                  </label>
                </div>
                <div class="form-check mb-3">
                  <input class="form-check-input" type="radio" name="stock-ref" id="select-stock" value="exist" checked>
                  <label class="form-check-label" for="select-stock">
                    Select existing stock
                  </label>
                </div>
                <input type='hidden' name='stock-ref-select' value='selectStockType'>
              </fieldset>
              <button type="submit" class="btn btn-primary">Submit</button>
            </form>
            </div>
        </div>
    </div>
</div>`;
  }

  _itemFieldsMarkup(stockData = {}, catOptions) {
    let stockField = this._newStockMarkup();

    if (this._stockType === "exist") {
      stockField = this._existingStockMarkup(stockData);
    }
    return `
        ${stockField}
      <div class="mb-3">
        <label for="cat" class="form-label">Item category</label>
        <select class="form-select" id="cat" name="cat">
          ${catOptions} 
        </select>
      </div>
      <div class="mb-3">
        <label for="lot" class="form-label">Lot number</label>
        <input type="text" class="form-control" id="lot" name="lot" value="">
      </div>
      <div class="mb-3">
        <label for="pallet" class="form-label">Pallet number</label>
        <input type="text" class="form-control" id="pallet" name="pallet" value="">
      </div>
      <div class="mb-3">
        <label for="roll" class="form-label">Roll number</label>
        <input type="text" class="form-control" id="roll" name="roll" value="">
      </div>
      <div class="mb-3">
        <label for="note" class="form-label">Note</label>
        <textarea class="form-control" id="note" rows="3" name="note"></textarea>
      </div>
      <input type="hidden" name="submit-item" value="${this._stockType}">
    `;
  }

  _newStockMarkup() {
    return `
    <fieldset>
      <div class="mb-3">
        <label for="reference" class="form-label">New stock</label>
        <input type="text" class="form-control" id="reference" name="reference" value="">
      </div>
      <div class="mb-3">
        <label for="date" class="form-label">Stock date</label>
        <input type="date" class="form-control" id="date" name="date" value="">
      </div>
      <div class="mb-3">
        <label for="consignor" class="form-label">Consignor</label>
        <input type="text" class="form-control" id="consignor" name="consignor" value="">
      </div>
    </fieldset>`;
  }

  _existingStockMarkup(stockData) {
    let stockField = `<div class="mb-3"><select class="form-select" id="reference" name="reference">`;
    stockData.forEach((stock) => {
      stockField += `
          <option value="${stock.id}">${stock.reference}</option>`;
    });
    stockField += `</select></div>`;

    return stockField;
  }
}

export default new Item();

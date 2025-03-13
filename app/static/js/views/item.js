class Item {
  _parentElement = document.getElementById("modalDialogWindow");
  _addButton = document.getElementById("add-item");

  render() {
    this._parentElement.insertAdjacentHTML(
      "afterbegin",
      this.generateStockMarkup()
    );
  }
  generateStockMarkup() {
    return `
            <div>Lorem</div>
        `;
  }

  addHandlerAddNew(handler) {
    // this._parentElement.insertAdjacentHTML(
    //   "afterbegin",
    //   this.generateStockMarkup()
    // );
    this._addButton.addEventListener("click", (e) => {
      //   const addButton = e.target.closest("#add-item");
      const addButton = e.target;

      console.log(addButton);
      handler();
    });
  }
}

export default new Item();

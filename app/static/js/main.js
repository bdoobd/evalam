import Item from "./views/item.js";

const controlAddItem = async function () {
  console.log("Handler running  ");

  Item.render();
};

const init = function () {
  Item.addHandlerAddNew(controlAddItem);
};

init();

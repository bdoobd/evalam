import Item from "./views/item.js";
import Stock from "./views/stock.js";

const controlAddItem = async function () {
  console.log("Handler running  ");

  Item.render();
};

// const handlerTmp = async function (element) {
//   // console.log(`Selected element: ${element}`);

//   Stock.render();
// };

const init = function () {
  Item.addHandlerAddNew(controlAddItem);
  Stock.addHandlerModalWindow();
};

init();

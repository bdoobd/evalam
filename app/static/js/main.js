import Home from './views/home.js'
import Item from "./views/item.js";
import Stock from "./views/stock.js";

const controlAddItem = async function () {
  // console.log("Handler running  ");

  Item.render();
};

const controllerHome = async function () {
  Home.render()
}

// const handlerTmp = async function (element) {
//   // console.log(`Selected element: ${element}`);

//   Stock.render();
// };

const init = function () {
  // Home.addHandlerHome(controllerHome);
  Item.addHandlerAddNew(controlAddItem);
  Stock.addHandlerModalWindow();
};

init();

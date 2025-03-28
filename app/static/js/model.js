// TODO: Функцию AJAX для получения данных с сервера и отправки данных на сервер

// Получить список всех не закрытых скласких референсов
export const getOpenRefs = async function () {
  const url = "/stock/onstock";
  try {
    const response = await fetch(url);
    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error: ", error);
  }
};

// Получить список всех категорий
export const getCategories = async function () {
  const url = "/cat/cats";
  try {
    const response = await fetch(url);
    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error: ", error);
  }
};

export const fixFormDataToAddItem = function (obj) {
  const new_stock = {
    reference: obj.reference,
    date: obj.date,
    consignor: obj.consignor,
    note: obj.note,
  };

  delete obj.reference;
  delete obj.date;
  delete obj.consignor;
  delete obj.note;

  obj.new_stock = new_stock;

  return obj;
};

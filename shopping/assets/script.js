// async function getItems() {
//   try {
//     const response = await fetch('/shopping_list/get-items/');
//     const data = await response.json();
//     console.log(data);
//   } catch (error) {
//     console.error(error);
//   }
// }
// getItems();

const xhr = new XMLHttpRequest();
xhr.open('GET', '/shopping_list/get-items/');


xhr.onload = function() {
  const listOfItems = JSON.parse(xhr.response)
  console.log(listOfItems);

// add the items from the databse for autocomplete
  const datalist = document.querySelector('#datalistOptions');
  const option = datalist.querySelector('.item-from-data');

  for (const item of listOfItems){
    const itemEl = document.createElement('option');
    itemEl.setAttribute('class', 'new-item-from-data');
    itemEl.textContent = item.name;
    datalist.insertBefore(itemEl, option.nextSibling);
  }
};

xhr.send();



const tableBody = document.querySelector('table tbody');
const form = document.querySelector('form');


async function fetchItem() {
  try {
    const response = await axios.get(
      '/shopping_list/get-items/'
    );
    const listOfItems = response.data;
    tableBody.innerHTML = `<template id="single-line">
    <tr>
      <td class="align-baseline"></td>
      <th scope="row" class="align-baseline">1</th>
      <td class="align-baseline" id="tags"></td>
      <td class="align-baseline">
        <button type="button" class="btn btn-outline-danger btn-sm">
        <svg id="i-close" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="15" height="25" fill="none" stroke="red" stroke-linecap="round" stroke-linejoin="round" stroke-width="4">
          <path d="M2 30 L30 2 M30 30 L2 2" />
        </svg>
        </button>
      </td>
    </tr>
  </template>`;

    const itemTemplate = document.getElementById('single-line');
    console.log(listOfItems);

    // add the items from the databse for autocomplete
    const datalist = document.querySelector('#datalistOptions');
    for (const item of listOfItems) {
      const option = document.createElement('option');
      option.value = item.name;
      datalist.appendChild(option);
    }

    for (const item of listOfItems) {
      const itemRow = document.importNode(itemTemplate.content, true);
      if (item.is_active) {
        itemRow.querySelector('td').textContent = item.name;
        itemRow.querySelector('tr').id = item.id;
        const tagsCell = itemRow.querySelector('#tags');
        const tagElement = document.createElement('span');
        tagElement.textContent = item.tags__name;
        tagElement.classList.add('tag');
        tagElement.style.backgroundColor = item.tags__color;
        tagsCell.appendChild(tagElement);
        tableBody.appendChild(itemRow);
      }
    }
  } catch (error) {
    console.log(error.message);
    console.log(error.response);
  }
}

fetchItem();

// delete item
tableBody.addEventListener('click', async (event) => {
  if (
    event.target.tagName === 'BUTTON' ||
    event.target.parentElement.tagName === 'BUTTON'
  ) {
    const itemId = event.target.closest('tr').id;
    const responseData = await axios.get(`/shopping_list/delete_item/${itemId}`);
    fetchItem();
  }
});

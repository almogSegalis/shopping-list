const tableBody = document.querySelector('table tbody');
const form = document.querySelector('form');
const SHOW_ALL = 'הצג הכל';

async function fetchItem() {
  try {

    const response = await axios.get('/shopping_list/get-items/');
    const listOfItems = response.data;
    tableBody.innerHTML = `<template id="single-line">
    <tr>
      <td class="align-baseline"></td>
      <th scope="row" class="align-baseline">
        <input id="numbers" pattern="[0-9.]+" type="number" value="1">
      </th>
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

    // add the items from the databse for autocomplete
    const datalist = document.querySelector('#datalistOptions');
    for (const item of listOfItems) {
      const option = document.createElement('option');
      option.value = item.name;
      datalist.appendChild(option);
    }

    //add the items tags from database for flitering
    createTagFilteringSction(listOfItems);

    // add the items from the database to the table
    for (const item of listOfItems) {
      const itemRow = document.importNode(itemTemplate.content, true);
      if (item.is_active) {
        itemRow.querySelector('td').textContent = item.name;
        itemRow.querySelector('tr').id = item.id;
        if (localStorage.getItem(item.name)) {
          // if the item is in the local storage, use the quantity from the local storage
          itemRow.querySelector('#numbers').value = localStorage.getItem(
            item.name
          );
        } else { 
          // if the item is not in the local storage, use the quantity from the database
          itemRow.querySelector('#numbers').value = item.quantity; 
        }
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
    const responseData = await axios.get(
      `/shopping_list/delete_item/${itemId}`
    );
    fetchItem();
  }
});

// change the quantity of the item
tableBody.addEventListener('change', async (event) => {
  if (event.target.tagName === 'INPUT') {
    const itemId = event.target.closest('tr').id;
    const quantity = event.target.value;
    const itemName = event.target.closest('tr').firstElementChild.textContent;
    localStorage.setItem(itemName, quantity);
  };
});

function createTagFilteringSction(listOfItems) {
  const tags = [];
  const tagsColors = [];
  buttonAll = {
    tags__name: SHOW_ALL,
    color: '#0d6efd',
  };
  tags.push(buttonAll.tags__name);
  tagsColors.push(buttonAll.color);
  for (const item of listOfItems) {
    if (!tags.includes(item.tags__name) && item.tags__name !== null) {
      tags.push(item.tags__name);
      tagsColors.push(item.tags__color);
    }
  }
  // console.log(tags); // for debugging
  // console.log(tagsColors); // for debugging

  const tagsContainer = document.querySelector('#filter-tags');
  const tagbuttons = Array.from(document.querySelectorAll('.button-tag'));

  for (let i = 0; i < tags.length; i++) {
    // check if the tag button already exist and if not, create it
    if (tagbuttons.every((button) => button.textContent !== tags[i])) {
      const tagButton = document.createElement('button');
      tagButton.textContent = tags[i];
      tagButton.classList.add('button-tag');
      tagButton.style.borderColor = tagsColors[i];
      tagButton.style.color = tagsColors[i];

      // add hover style to match border color
      tagButton.addEventListener('mouseover', function () {
        this.style.backgroundColor = tagsColors[i];
        this.style.color = '#fff'; // set text color to white for contrast
        this.classList.remove('active');
      });

      // reset style on mouseout
      tagButton.addEventListener('mouseout', function () {
        this.style.backgroundColor = 'transparent';
        this.style.color = tagsColors[i];
      });

      tagsContainer.appendChild(tagButton);
    }
  }

  // add event listener to the filter buttons
  tags.forEach((filterTag, index) => {
    const tagButton = document.querySelector(
      `.button-tag:nth-child(${index + 2})`
    );
    tagButton.addEventListener('click', () => {
      const tagButtons = document.querySelectorAll('.button-tag');
      const rowsTag = document.querySelectorAll('.tag');
      rowsTag.forEach((rowTag) => {
        if (rowTag.textContent === filterTag || filterTag === SHOW_ALL) {
          rowTag.parentElement.parentElement.style.display = 'table-row';
        } else {
          rowTag.parentElement.parentElement.style.display = 'none';
        }
      });
    });
  });
}


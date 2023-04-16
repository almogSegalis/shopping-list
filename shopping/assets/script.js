const tableBody = document.querySelector('table tbody');
const form = document.querySelector('form');
const SHOW_ALL = 'הצג הכל';

async function fetchItem() {
  try {
    const response = await axios.get('/shopping_list/get-items/');
    const listOfItems = response.data;

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
    const itemTemplate = document.getElementById('single-line');
    for (const item of listOfItems) {
      const itemRow = document.importNode(itemTemplate.content, true);
      if (item.is_active) {
        itemRow.querySelector('td').textContent = item.name;
        itemRow.querySelector('tr').id = item.id;
        itemRow.querySelector('tr').classList = "item-row";
        itemRow.querySelector('#numbers').value = item.quantity; 
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
  if (event.target.tagName === 'BUTTON' || event.target.parentElement.tagName === 'BUTTON') {
    if (event.target.id === 'delete-button' || event.target.parentElement.id === 'delete-button') {
      const itemId = event.target.closest('tr').id;
      const deletedRow = document.getElementById(itemId);
      deletedRow.remove(); // remove the deleted row from the table
      const responseData = await axios.get(
        `/shopping_list/delete_item/${itemId}`
      );
    }
  }
});

function getCsrftokenFormCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCsrftokenFormCookie('csrftoken');

// change quantity
tableBody.addEventListener('change', async (event) => {
  if (event.target.tagName === 'INPUT') {
    const itemId = event.target.closest('tr').id;
    const quantity = event.target.value;
    await axios.post(`/shopping_list/update_quantity/${itemId}/${quantity}`,
    {}, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
    })
    .then(response => {
      // Handle the response, e.g. display a success message
      
    })
    .catch(error => {
      console.error(error);
      // Handle the error, e.g. display an error message
    });
  }
});

// add item
addButton = document.querySelector('#add-button');
addButton.addEventListener('click', async (event) => {
    event.preventDefault();
    const itemName = document.querySelector('#item_name').value;
    await axios.post(`/shopping_list/add_item/${itemName}`,
    {}, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
    })
    .then(async (response) => {
      const items = document.querySelectorAll('tr');

      clearTableItems(items);

      // add the items from the database to the table
      await fetchItem();

      // clear the input field
      document.querySelector('#item_name').value = '';
    
    }).catch(error => {
      console.error(error);
      // Handle the error, e.g. display an error message
    });
  });

// clear the table
function clearTableItems(items) {
  items.forEach(item => {
    if (item.classList.contains('item-row')) {
      item.remove();
    }
  });
}

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


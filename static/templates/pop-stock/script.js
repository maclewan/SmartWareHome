import {getUrlParam, showPopupMessage} from "../../common/script.js";


document.addEventListener("DOMContentLoaded", () => {
  handlePageLoaded();
});
document.getElementById("search-input").onkeyup = filterProducts
document.getElementById("items").onchange = handleSelectChanged

function handlePageLoaded() {
  const bar_code = getUrlParam('bar_code')
  if (bar_code === null) return;

  fetch(`/api/supplies/product/${bar_code}/`)
    .then(response => {
      handleCheckProductExistsResponse(bar_code, response)
    })
    .catch(error => console.error('Error fetching items:', error));
}


function handleCheckProductExistsResponse(bar_code, response) {
  let productExists = (response.status === 200)
  if (!productExists) {
    showPopupMessage("no", "Product not in database!")
  } else {
    document.getElementById("items").value = bar_code
  }
}


function filterProducts() {
  const searchInput = document.getElementById('search-input').value.toLowerCase();
  const products = document.querySelectorAll('.product-item');
  let filteredCount = 0
  let lastValue = ""

  products.forEach(product => {
    const productName = product.innerText;
    if (productName.toLowerCase().includes(searchInput)) {
      product.style.display = '';
      filteredCount++
      lastValue = product.value
    } else {
      product.style.display = 'none';
    }
  });

  if (filteredCount === 1) {
    document.getElementById("items").value = lastValue
  } else {
    document.getElementById("items").value = ""
  }
}


async function handleSelectChanged() {
  const bar_code = document.getElementById("items").value
  if (bar_code === "") {
    return
  }
  await fetchAndProcessSupplies(bar_code)
}

async function fetchAndProcessSupplies(bar_code) {
  let product_response = await fetch(`/api/supplies/product/${bar_code}/`)
  if (product_response.status !== 200) {
    showPopupMessage("no", "Cannot fetch product...")
    return
  }

  let supplies_response = await fetch(`/api/supplies/supply/for-product/${bar_code}/`)
  if (supplies_response.status !== 200) {
    showPopupMessage("no", "Cannot fetch supplies...")
    return
  }

  let productResponseData = await product_response.json()
  let suppliesResponseData = await supplies_response.json()

  let tableTbody = document.getElementById("supplies-table-tbody")

  clearTable(tableTbody)

  // todo refactor
  suppliesResponseData.forEach((supply) => {
    let tr = document.createElement("tr")
    tr.className = "supp-table-row"
    tr.id = `supp-table-row-${supply.id}`

    let tdId = document.createElement("td")
    let tdName = document.createElement("td")
    let tdAmount = document.createElement("td")
    let tdExpDate = document.createElement("td")
    let tdSelect = document.createElement("td")
    let tdSelectInput = document.createElement("input")

    tdId.className = "table-cell"
    tdName.className = "table-cell"
    tdAmount.className = "table-cell"
    tdExpDate.className = "table-cell"
    tdSelect.className = "table-cell supp-select-checkbox"

    tdId.innerText = supply.id
    tdName.innerText = `${productResponseData.name} [${productResponseData.volume}]`
    tdAmount.innerText = supply.amount
    tdExpDate.innerText = supply.expiration_date

    tdSelectInput.type = "radio"
    tdSelectInput.name = "selectSupply"
    tdSelectInput.value = supply.id

    tdSelect.appendChild(tdSelectInput)
    tr.appendChild(tdId)
    tr.appendChild(tdName)
    tr.appendChild(tdAmount)
    tr.appendChild(tdExpDate)
    tr.appendChild(tdSelect)

    tableTbody.appendChild(tr)
    // document.querySelector('input[name="selectSupply"]:checked').value
  })


}


function clearTable(tableTbody) {
  let tableRowsCount = tableTbody.getElementsByTagName('tr').length;

  for (let i = tableRowsCount - 1; i >= 0; i--) {
    tableTbody.deleteRow(i)
  }
}
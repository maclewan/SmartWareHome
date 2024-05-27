import {showPopupMessage} from '../../common/script.js'

const mainForm = document.getElementById("main-form")
let productExists = false
let productOriginalData = {}
let productId = undefined

document.addEventListener("DOMContentLoaded", () => {
  handlePageLoaded();
});
document.getElementById("button-add").onclick = handleAdd

function handlePageLoaded() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const bar_code = urlParams.get('bar_code')
  if (bar_code === null) return;
  mainForm.elements["bar_code"].value = bar_code;

  fetch(`/api/supplies/product/${bar_code}/`)
    .then(response => {
      handleProductResponse(bar_code, response)
    })
    .catch(error => console.error('Error fetching items:', error));
}

function resetProductAddForm() {
  mainForm.reset()
  productExists = false
  productOriginalData = {}
  productId = undefined
}

function storeOriginalProductData(responseData) {
  productOriginalData.prod_name = responseData.name
  productOriginalData.volume = responseData.volume
  productOriginalData.description = responseData.description
}

function hasOriginalProductDataChanged() {
  return ["prod_name", "volume", "description"].map(
    (key) =>
      productOriginalData[key] === mainForm.elements[key].value
  ).some((val) => val === false)
}

async function handleProductResponse(bar_code, response) {
  productExists = (response.status === 200)
  if (!productExists) {
    showPopupMessage("partial", "Product not in database.")
    return true
  }

  const responseData = await response.json()

  mainForm.elements["prod_name"].value = responseData.name
  mainForm.elements["volume"].value = responseData.volume
  mainForm.elements["description"].value = responseData.description
  mainForm.elements["bar_code"].readOnly = true
  productId = responseData.id

  storeOriginalProductData(responseData)
  console.log(`Product exists with id ${productId}`)

  return true
}

function getProductPayload() {
  return {
    name: mainForm.elements["prod_name"].value,
    bar_code: mainForm.elements["bar_code"].value,
    description: mainForm.elements["prod_name"].value,
    volume: mainForm.elements["volume"].value,
  }
}

function getRequestHeaders() {
  return {
    'Content-Type': 'application/json',
    'X-CSRFToken': '{{ csrf_token }}'
  }
}

async function createProduct() {
  let payload = getProductPayload()
  let response = await fetch("/api/supplies/product/", {
    method: "POST",
    headers: getRequestHeaders(),
    body: JSON.stringify(payload)
  })

  if (response.status !== 201) {
    showPopupMessage("no", "Product was NOT created properly...")
    return undefined
  }
  let responseData = await response.json()
  console.log(`Product created with id ${productId}`)
  return responseData.id
}

async function updateProduct() {
  let payload = getProductPayload()
  let bar_code = mainForm.elements["bar_code"].value
  let response = await fetch(`/api/supplies/product/${bar_code}/`, {
    method: "PATCH",
    headers: getRequestHeaders(),
    body: JSON.stringify(payload)
  })

  if (response.status !== 200) {
    showPopupMessage("no", "Product was NOT updated properly...")
    return undefined
  }
  let responseData = await response.json()
  console.log(`Product (id ${productId}) updated`)
  return responseData.id
}

async function handleAdd() {
  if (!mainForm.checkValidity()) {
    showPopupMessage("partial", "Fill out all fields...")
    return
  }
  if (!productExists) {
    productId = await createProduct()
  }
  if (productId === undefined) {
    return
  }

  if (productExists && hasOriginalProductDataChanged()) {
    const updatedId = await updateProduct()
    if (updatedId !== productId) {
      return
    }
  }

  let payload = {
    amount: mainForm.elements["amount"].value,
    expiration_date: mainForm.elements["exp_date"].value,
    product: productId,
  }
  let response = await fetch("/api/supplies/supply/", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': '{{ csrf_token }}'
    },
    body: JSON.stringify(payload)
  })

  if (response.status !== 201) {
    showPopupMessage("no", "Supply was not created properly...")
    return
  }
  let responseData = await response.json()

  if (productExists) {
    showPopupMessage("yes", `Supply for "${mainForm.elements["prod_name"].value}" (${responseData.amount} pcs)  added.`)
  } else {
    showPopupMessage("yes", `Product "${mainForm.elements["prod_name"].value}" (${responseData.amount} pcs) created, supply added.`)
  }

  resetProductAddForm()
}

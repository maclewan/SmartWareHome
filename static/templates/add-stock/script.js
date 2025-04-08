import {getUrlParam, showPopupMessage} from '../../common/script.js'

const mainForm = document.getElementById("main-form")
let productExists = false
let productOriginalData = {}
let productId = undefined

document.addEventListener("DOMContentLoaded", () => {
    handlePageLoaded();
});
document.getElementById("button-add").onclick = handleAdd
document.getElementById("search-input").onkeyup = filterProducts
document.getElementById("items").onchange = handleSelectChanged

function handlePageLoaded() {
    const bar_code = getUrlParam('bar_code')
    if (bar_code === null) return;

    fetchAndFillProductData(bar_code)
}

function handleSelectChanged() {
    const bar_code = document.getElementById("items").value
    if (bar_code === "") {
        return
    }
    fetchAndFillProductData(bar_code)
}

function fetchAndFillProductData(bar_code) {
    mainForm.elements["bar_code"].value = bar_code;

    fetch(`/api/supplies/product/${bar_code}/`)
        .then(response => {
            handleProductResponse(bar_code, response)
        })
        .catch(error => console.error('Error fetching items:', error));
    fetch(`/api/supplies/supply/for-product/${bar_code}/`)
        .then(response => {
            handleSuppliesResponse(response)
        })
}

async function handleSuppliesResponse(response) {
    const responseData = await response.json()
    console.log(responseData)
    const suppliesSelect = document.getElementById("entities")
    while (suppliesSelect.options.length > 1) {
        suppliesSelect.remove(1);
    }
    if (responseData.length > 0) {
        suppliesSelect.disabled = null
    } else {
        suppliesSelect.disabled = "disabled"
    }
    responseData.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id;
        option.text = `Supply id: ${item.id} - left: (${item.amount}) ${item.expiration_date === null ? '----' : '- expires ' + item.expiration_date}`;
        suppliesSelect.appendChild(option);
    });
}

function resetProductData() {
    mainForm.elements["prod_name"].value = ""
    mainForm.elements["volume"].value = ""
    mainForm.elements["description"].value = ""
    mainForm.elements["bar_code"].value = ""
    mainForm.elements["amount"].value = ""
    mainForm.elements["exp_date"].value = ""
}

function resetProductVariables() {
    productExists = false
    productOriginalData = {}
    productId = undefined
}


function resetProductAddForm() {
    mainForm.reset()
    resetProductVariables()
}

function softResetProductAddForm() {
    resetProductData()
    resetProductVariables()
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
        'X-CSRFToken': CSRF_TOKEN
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
        fetchAndFillProductData(lastValue)
    } else {
        document.getElementById("items").value = ""
        softResetProductAddForm()
    }
}

async function handleAdd() {
    if (!mainForm.checkValidity()) {
        showPopupMessage("partial", "Fill out all fields...")
        return
    }
    if (document.getElementById("amount").valueAsNumber <= 0) {
    	showPopupMessage("partial", "Amount need to be greater than 0")
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

    const suppliesSelect = document.getElementById("entities")
    let selectValue = suppliesSelect.value
    if (selectValue === '') {
        // New supply flow
        let payload = {
            amount: mainForm.elements["amount"].value,
            expiration_date: mainForm.elements["exp_date"].value === '' ? null : mainForm.elements["exp_date"].value,
            product: productId,
        }
        const response = await fetch("/api/supplies/supply/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN
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
    } else {
        // update supply flow
        const payload = {
            amount_to_pop: -document.getElementById("amount").valueAsNumber  // hacky way of reusing existing endpoint for popping
        }
        const response = await fetch(`/api/supplies/supply/pop-amount/${selectValue}/`, {
            method: "POST", headers: getRequestHeaders(), body: JSON.stringify(payload)
        })
        if (response.status !== 200) {
            showPopupMessage("no", "Supply was not udated properly...")
            return
        }
        showPopupMessage("yes", `Supply for "${mainForm.elements["prod_name"].value}" + (${document.getElementById("amount").valueAsNumber} pcs) updated.`)
    }
    resetProductAddForm()
}

import {getUrlParam, showPopupMessage} from "../../common/script.js";


document.addEventListener("DOMContentLoaded", () => {
	handlePageLoaded();
});
document.getElementById("search-input").onkeyup = filterProducts
document.getElementById("items").onchange = handleSelectChanged
document.getElementById("btn-incr").onclick = () => {
	handleIncrDecrClicked(true)
}
document.getElementById("btn-decr").onclick = () => {
	handleIncrDecrClicked(false)
}
document.getElementById("button-pop").onclick = handlePopClicked

document.getElementById("pop-amount-input").onchange = handleAmountChanged


function handleAmountChanged() {
	const input = document.getElementById("pop-amount-input")
	const successButton = document.getElementById("button-pop")
	if (input.valueAsNumber > 0 ) {
		successButton.innerHTML = "Restock"
	}
	else {
		successButton.innerHTML = "Pop"
	}
}

function handlePageLoaded() {
	const bar_code = getUrlParam('bar_code')
	if (bar_code === null) return;

	fetch(`/api/supplies/product/${bar_code}/`)
		.then(response => {
			handleCheckProductExistsResponse(bar_code, response)
			refreshSearchResults().then(() => {
			})
		})
		.catch(error => console.error('Error fetching items:', error));
}

function handleCheckProductExistsResponse(bar_code, response) {
	const productExists = (response.status === 200)
	if (!productExists) {
		showPopupMessage("no", "Product not in database!")
	} else {
		document.getElementById("items").value = bar_code
	}
}

async function filterProducts() {
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

	document.getElementById("items").value = (filteredCount === 1) ? lastValue : ""
	await handleSelectChanged()
}

async function handleSelectChanged() {
	const bar_code = document.getElementById("items").value
	if (bar_code === "") {
		const tableTbody = document.getElementById("supplies-table-tbody")

		clearTable(tableTbody)
		return
	}
	await fetchAndProcessSupplies(bar_code)
}


function createSupplyRow(supply, productName, productVolume) {
	const tr = document.createElement("tr")
	tr.className = "supp-table-row"
	if (supply.expiration_state === "expired") {
		tr.classList.add("expired-row")
	} else if (supply.expiration_state === "soon_to_expire") {
		tr.classList.add("soon-to-expire-row")
	}
	tr.id = `supp-table-row-${supply.id}`

	const tdId = document.createElement("td")
	const tdName = document.createElement("td")
	const tdAmount = document.createElement("td")
	const tdExpDate = document.createElement("td")
	const tdSelect = document.createElement("td")
	const tdSelectInput = document.createElement("input")

	tdId.className = "table-cell"
	tdName.className = "table-cell"
	tdAmount.className = "table-cell"
	tdAmount.id = `supp-amount-${supply.id}`
	tdExpDate.className = "table-cell"
	tdSelect.className = "table-cell supp-select-checkbox"

	tdId.innerText = supply.id
	tdName.innerText = `${productName} [${productVolume}]`
	tdAmount.innerText = supply.amount
	tdExpDate.innerText = supply.expiration_date

	tdSelectInput.type = "radio"
	tdSelectInput.name = "selectSupply"
	tdSelectInput.value = supply.id
	tdSelectInput.onclick = handleSupplySelectChanged

	tdSelect.appendChild(tdSelectInput)
	tr.appendChild(tdId)
	tr.appendChild(tdName)
	tr.appendChild(tdAmount)
	tr.appendChild(tdExpDate)
	tr.appendChild(tdSelect)

	return tr
}


async function fetchAndProcessSupplies(bar_code) {
	const product_response = await fetch(`/api/supplies/product/${bar_code}/`)
	if (product_response.status !== 200) {
		showPopupMessage("no", "Cannot fetch product...")
		return
	}

	const supplies_response = await fetch(`/api/supplies/supply/for-product/${bar_code}/`)
	if (supplies_response.status !== 200) {
		showPopupMessage("no", "Cannot fetch supplies...")
		return
	}

	const productResponseData = await product_response.json()
	const suppliesResponseData = await supplies_response.json()

	const tableTbody = document.getElementById("supplies-table-tbody")

	clearTable(tableTbody)

	const supply_id = getUrlParam('supply_id')

	suppliesResponseData.forEach((supply) => {
		const tr = createSupplyRow(supply, productResponseData.name, productResponseData.volume)
		tableTbody.appendChild(tr)
	})

	if (suppliesResponseData.length === 1) {
		const input = tableTbody.querySelector("tr").querySelector("input")
		input.checked = true
	} else if (supply_id !== null) {
		const row = document.getElementById(`supp-table-row-${supply_id}`)
		if (row !== null) {
			const input = row.querySelector("input")
			input.checked = true
		}
	}
}

function handleSupplySelectChanged() {
	// Fixme this needs to be set to -1 or to -0.5 if what is left is -0.5
	document.getElementById("pop-amount-input").value = "-1"
}

function clearTable(tableTbody) {
	const tableRowsCount = tableTbody.getElementsByTagName('tr').length;

	for (let i = tableRowsCount - 1; i >= 0; i--) {
		tableTbody.deleteRow(i)
	}
}

function handleIncrDecrClicked(increment) {
	const selectedInput = document.querySelector('input[name="selectSupply"]:checked')
	if (selectedInput === null) {
		return
	}
	const amount = document.getElementById(`supp-amount-${selectedInput.value}`).innerText

	const input = document.getElementById("pop-amount-input")
	let newValue = input.valueAsNumber + 0.5 * (increment ? 1 : -1)
	if (-newValue > Number(amount)) {
		return
	}
	if (newValue === 0) {
		newValue = increment ? 0.5 : -0.5
	}
	input.value = newValue.toFixed(1)
	handleAmountChanged()
}

function getRequestHeaders() {
	return {
		'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN
	}
}

function refreshSearchResults() {
	return handleSelectChanged()
}

async function handlePopClicked() {
	const selectedInput = document.querySelector('input[name="selectSupply"]:checked')
	if (selectedInput === null) {
		showPopupMessage("partial", "Supply not selected...")
		return
	}
	const selectedSupplyId = selectedInput.value
	const payload = {
		amount_to_pop: -document.getElementById("pop-amount-input").valueAsNumber
	}

	const response = await fetch(`/api/supplies/supply/pop-amount/${selectedSupplyId}/`, {
		method: "POST", headers: getRequestHeaders(), body: JSON.stringify(payload)
	})

	if (response.status === 200) {
		showPopupMessage("yes", "Supply updated properly.")
	} else if (response.status === 204) {
		showPopupMessage("yes", "Supply removed.")
	} else {
		showPopupMessage("no", "Error, cannot pop supply properly...")
	}

	await refreshSearchResults()
}
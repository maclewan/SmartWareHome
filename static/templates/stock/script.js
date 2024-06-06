document.addEventListener("DOMContentLoaded", () => {
  handlePageLoaded();
});
document.getElementById("filter-button").onclick = filterProducts

let products = []

function handlePageLoaded() {
  let productsJsonString = productsJsonRawString.replaceAll("&quot;", "\"")
  products = JSON.parse(productsJsonString)
}

async function filterProducts() {
  const nameInputValue = document.getElementById('search-name').value.toLowerCase();
  const categoryId = parseInt(document.getElementById('category-select').value);

  const tableRows = document.getElementById("product-table").rows

  for (let i = 1; i < tableRows.length; i++) {
    // tableRows[0] is header row, so we need to iterate from 1.
    // also table.rows is not iterable so cannot use `forEach` or `for ... of ...`
    tableRows[i].style.display = "none"
  }

  const filteredProducts = products.filter(product => {
    return isNaN(categoryId) ? true : product.categories.includes(categoryId)
  }).filter(product => {
    return product.name.toLowerCase().includes(nameInputValue)
  })

  filteredProducts.forEach(product => {
    const row = document.getElementById(`prod-row-${product.id}`)
    row.style.display = ""
  })
}


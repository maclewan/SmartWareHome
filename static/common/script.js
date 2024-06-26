export function showPopupMessage(success, text) {
  const content = document.getElementById('content')
  const successTypeColorMap = new Map()
  successTypeColorMap.set("yes", "green")
  successTypeColorMap.set("no", "red")

  const color = successTypeColorMap.get(success)
  const popupDiv = document.createElement('div');
  popupDiv.className = `elementToFadeInAndOut popup-message ${color === undefined ? "grey" : color}-popup-message`
  popupDiv.innerHTML = `${text}`
  content.appendChild(popupDiv);
  setTimeout(() => {
    content.removeChild(popupDiv);
  }, 5000)
}

export function getUrlParam(param_name) {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  return urlParams.get(param_name)
}

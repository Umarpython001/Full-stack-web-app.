const errorAlert  = document.getElementById("errorAlert")
const successAlert = document.getElementById("successAlert")

const errorClear = document.getElementById("errorClear")
const successClear = document.getElementById("successClear")


errorClear.onclick = () => errorAlert.style.display = "none"

successClear.onclick = () => successAlert.style.display = "none"

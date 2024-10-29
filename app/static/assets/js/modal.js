var modal = document.getElementById("projectModal");
var btn = document.getElementById("openModal");
var span = document.getElementById("closeModal");

btn.onclick = function() {
    modal.classList.add("show");
}

span.onclick = function() {
    modal.classList.remove("show");
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.classList.remove("show");
    }
}
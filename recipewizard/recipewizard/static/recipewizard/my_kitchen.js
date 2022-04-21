document.addEventListener("DOMContentLoaded", () => {
    csrftoken = getCookie("csrftoken")

    //Whenever a checkbox is clicked, update the corresponding checkbox in the deletion form. There's probably a better way to do this but this works so whatever

    let deleteForm = document.querySelector("#deleteIngredientsForm")

    let checkboxes = document.querySelectorAll(".ingredient-checkbox")
    let deleteCheckboxes = Array.from(document.querySelectorAll(".ingredient-delete-checkbox"))

    checkboxes.forEach(el => {
        el.addEventListener("change", () => {
            deleteCheckboxes.find(delEl => delEl.value == el.value).checked = el.checked
        })
    })

    //Save button functionality. Sends a request to the server with all updated ingredients to be changed.

    let save = document.querySelector("#saveButton")
    let amounts = Array.from(document.querySelectorAll(".ingredient-amount-input"))
    save.addEventListener("click", () => {
        let changedAmounts = amounts.filter(el => el.dataset.originalValue != el.value).map(el => {return {ingredient: el.dataset.ingredient, value: el.value}})
        fetch(deleteForm.action, {
            method: "PUT",
            headers: {
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                updates: changedAmounts
            })
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url
            }
        }) 
    })
})

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
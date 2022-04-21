document.addEventListener("DOMContentLoaded", () => {
    csrftoken = getCookie("csrftoken")

    const btnSave = document.querySelector("#save-recipe");
    let id = btnSave.dataset.id;

    btnSave.onclick = () => {
        fetch(`/recipe/${id}/save`, {
            method: "PUT"
        })
        .then(response => response.json())
        .then(result => {
            switch (btnSave.innerHTML) {
                case "Save":
                    btnSave.innerHTML = "Unsave";
                    break;
                case "Unsave":
                    btnSave.innerHTML = "Save";
                    break;
            }
        })
        .catch(err => console.error(err));
    };

    const btnPopulateShoppingList = document.querySelector("#btn-populate-shopping-list")
    const btnShowUpdatedModal = document.querySelector("#btn-show-updated-modal")
    let ingredients = Array.from(document.querySelectorAll(".ingredient-row"))

    btnPopulateShoppingList.onclick = () => {
        let missingIngredients = []
        ingredients.forEach(ingredient => {
            if (ingredient.dataset.userHasIngredient !== "True") {
                let name = ingredient.querySelector(".ingredient-name").innerHTML
                let amount = ingredient.querySelector(".ingredient-amount").innerHTML
                let unit = ingredient.querySelector(".ingredient-unit").innerHTML

                missingIngredients.push({name: name, amount: amount, unit: unit})
            }
        })
        
        console.log(missingIngredients)

        fetch(btnPopulateShoppingList.dataset.endpoint, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                ingredients: JSON.stringify(missingIngredients)
            })
        })
        .then(response => response.json())
        .then(results => {
            if (results.success)
                btnShowUpdatedModal.click()
        })
    }

    const btnShoppingListUpdatedOk = document.querySelector("#btn-shopping-list-updated-ok")

    btnShoppingListUpdatedOk.onclick= () => window.location.replace(btnShoppingListUpdatedOk.dataset.redirect)

    const servingCountInput = document.querySelector("#serving-count")
    servingCountInput.dataset.originalServingCount = servingCountInput.value

    const recipeAmounts = document.querySelectorAll(".ingredient-amount")

    function updateRecipeAmounts() {
        let ratio = servingCountInput.value / servingCountInput.dataset.originalServingCount
        recipeAmounts.forEach((amount) => {
            let updated = amount.dataset.originalAmount * ratio
            
            //round the new number to 2 decimal places
            updated *= 100
            updated = Math.round(updated)
            updated /= 100

            amount.innerHTML = updated
        })
    }

    updateRecipeAmounts()

    servingCountInput.addEventListener("input", () => {
        servingCountInput.value.replaceAll(".","")

        if (servingCountInput.value != "")
            servingCountInput.value = Math.max(1, Math.min(100, servingCountInput.value)) //Clamp between 1 and 100

        if (servingCountInput.value > 0)
            updateRecipeAmounts()
    })
});

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
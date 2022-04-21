document.addEventListener("DOMContentLoaded", () => {
    csrftoken = getCookie("csrftoken")

    //Save button behavior

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

    //Method to highlight ingredient rows
    
    let ingredients = Array.from(document.querySelectorAll(".ingredient-row"))
    function updateRecipeRowHighlights() {
        ingredients.forEach(ingredient => {
            let amount = parseFloat(ingredient.querySelector(".ingredient-amount").innerHTML)

            console.log(Math.abs(parseFloat(ingredient.dataset.amountUserHas) - amount) + " " + ingredient.dataset.amountUserHas + " " + amount)

            if (parseFloat(ingredient.dataset.amountUserHas) < amount ) {
                ingredient.classList.add("bg-danger")
            } else {
                ingredient.classList.remove("bg-danger")
            }
        })
    }

    //Populate shopping list button functionality

    const btnPopulateShoppingList = document.querySelector("#btn-populate-shopping-list")
    const btnShowUpdatedModal = document.querySelector("#btn-show-updated-modal")

    btnPopulateShoppingList.onclick = () => {
        let missingIngredients = []
        ingredients.forEach(ingredient => {
            let amount = ingredient.querySelector(".ingredient-amount").innerHTML

            if (parseFloat(ingredient.dataset.amountUserHas) < parseFloat(amount)) {
                let name = ingredient.querySelector(".ingredient-name").innerHTML
                let unit = ingredient.querySelector(".ingredient-unit").innerHTML

                missingIngredients.push({name: name, amount: amount, unit: unit})
            }
        })

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

    //Button to redirect user to shopping list when the shopping list updated modal is closed

    const btnShoppingListUpdatedOk = document.querySelector("#btn-shopping-list-updated-ok")

    btnShoppingListUpdatedOk.onclick= () => window.location.replace(btnShoppingListUpdatedOk.dataset.redirect)

    //Functionality for changing the recipe's serving count

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

        updateRecipeRowHighlights()
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
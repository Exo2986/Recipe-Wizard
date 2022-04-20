document.addEventListener("DOMContentLoaded", () => {
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
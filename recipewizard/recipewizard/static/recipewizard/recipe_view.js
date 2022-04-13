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
});
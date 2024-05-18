console.log(foodstucks);
const foodstucks_size = Object.keys(foodstucks).length;
const selected_foodstucks = new Map();

let i = 0

function updateTheFoodStuckDisplay() {
    document.getElementById("page_number").innerHTML = i + 1;
    for (let idx = 0; idx < 8; idx++) {

        foodstucks_label = foodstucks[(i * 8 + idx) % foodstucks_size].label
        if (selected_foodstucks.has(foodstucks_label)) {
            document.getElementById("foodstuck_button_add_" + idx).disabled = true;
        } else {
            document.getElementById("foodstuck_button_add_" + idx).disabled = false;
        }
        //const paragraph = document.createElement(foodstucks[i].label);
        document.getElementById("foodstuck_label_" + idx).innerHTML = foodstucks_label;
        // document.getElementById("Modal_title_" + idx).innerHTML = "Amount of " + foodstucks_label;
        // document.getElementById("amount_" + idx).value = 0;
        document.getElementById("foodstuck_image_" + idx).src = foodstucks[(i * 8 + idx) % foodstucks_size].image_link;
    }
}

function simpleHashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = (hash << 5) - hash + char;
        hash = hash & hash; // Convert to 32-bit integer
    }
    return hash;
}

function showModal(selectedProduct) {
    var modalId = 'dynamicModal';
    var hashProduct = simpleHashString(selectedProduct)
    var modalHTML = `
        <div class="modal fade" id=${"Modal_" + hashProduct} tabindex="-1" role="dialog"
            aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id=${"Modal_title_" + hashProduct}"Modal_title_0">${"Amount of " + selectedProduct}</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <form>
                            <div class="form-group row">

                                <label for="inputGlucosLevel" class="col-sm-9 col-form-label text-left">Enter the
                                    amount:</label>
                                <div class="col-sm-3 text-right">
                                    <input type="number" class="form-control" id=${"amount_" + hashProduct}
                                        placeholder="0" step="1" min="0">
                                </div>

                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-success" data-dismiss="modal"
                            id=${"foodstuck_button_confirm_" + hashProduct}>Confirm</button>

                    </div>
                </div>
            </div>
        </div>`;

    document.getElementById('dynamicModalsContainer').innerHTML = modalHTML;
    $('#' + "Modal_" + hashProduct).modal('show');

    document.getElementById("foodstuck_button_confirm_" + hashProduct).addEventListener("click", function () {
        const amount = document.getElementById("amount_" + hashProduct).value;

        // If already exist, it only modifie the text.
        if (selected_foodstucks.has(selectedProduct)) {
            document.getElementById('selected_list_' + selectedProduct).childNodes[0].nodeValue = amount + " " + selectedProduct;
            selected_foodstucks.set(selectedProduct, amount);
            return;
        }

        selected_foodstucks.set(selectedProduct, amount);

        // Create a new list item
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.id = 'selected_list_' + selectedProduct;
        var text = document.createTextNode(amount + " " + selectedProduct);
        li.appendChild(text);

        var btn1 = document.createElement('button');
        btn1.className = 'btn btn-success btn-sm';
        btn1.innerText = 'Modify';
        btn1.onclick = function () {
            showModal(selectedProduct);
        };

        var btn2 = document.createElement('button');
        btn2.className = 'btn btn-danger btn-sm';
        btn2.innerText = 'Delete';
        btn2.onclick = function () {
            if (selected_foodstucks.has(selectedProduct)) {
                selected_foodstucks.delete(selectedProduct);
            }
            li.parentNode.removeChild(li);
            updateTheFoodStuckDisplay();

        };

        li.appendChild(btn1);
        li.appendChild(btn2);

        // Add the new list item to the product list
        document.getElementById('productList').appendChild(li);
        updateTheFoodStuckDisplay()


    });
}

for (let idx = 0; idx < 8; idx++) {
    document.getElementById("page_number").innerHTML = i + 1;
    document.getElementById("foodstuck_label_" + idx).innerHTML = foodstucks[i * 8 + idx].label;
    document.getElementById("foodstuck_image_" + idx).src = foodstucks[i * 8 + idx].image_link;
    document.getElementById("foodstuck_button_add_" + idx).addEventListener("click", function () {
        const selectedProduct = foodstucks[(i * 8 + idx) % foodstucks_size].label;
        showModal(selectedProduct);

    });

}


const prevButton = document.querySelector('.page-link[aria-label="Previous"]');
const nextButton = document.querySelector('.page-link[aria-label="Next"]');


prevButton.addEventListener('click', (event) => {
    event.preventDefault();
    if (i == 0) {
        return;
    }
    i -= 1
    updateTheFoodStuckDisplay()

});

nextButton.addEventListener('click', (event) => {
    event.preventDefault();
    i += 1
    updateTheFoodStuckDisplay();
});


document.getElementById("computeButton").addEventListener("click", function () {
    const glucose_level = document.getElementById("glucose_level").value;
    if (glucose_level == 0) {
        alert("Complete your glucose level.");
        return;
    }
    if (selected_foodstucks.size == 0 && selectedFoodstuffs.size == 0) {
        alert("Select at least one element.");
        return;
    }
    selected_foodstucks.set("glucose_level", glucose_level);
    const arr = Array.from(selected_foodstucks.entries());

    // Convertir le tableau en JSON
    const json = JSON.stringify(arr);

    fetch('/meal_resume', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: json
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur de réseau');
            }
        })
    window.location.href = "/meal_resume";
});


// =================== JONATHAN ==================================
async function searchFood() {
    const query = document.getElementById('searchQuery').value;
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = 'Searching...';

    try {
        const response = await fetch('/search-food', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            throw new Error('Failed to search food');
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        resultsDiv.innerHTML = 'Error: ' + error.message;
    }
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    console.log(data);

    if (data.foods && data.foods.food) {
        const foods = Array.isArray(data.foods.food) ? data.foods.food : [data.foods.food];

        foods.forEach(food => {
            const foodDiv = document.createElement('div');
            foodDiv.innerHTML = `
                <h3>${food.food_name} (${food.brand_name || 'Generic'})</h3>

                <button type="button" class="btn btn-success align-self-end"
                        id="foodstuck_button_add_${food.food_id}" data-toggle="modal"
                        onclick="addIngredient(${food.food_id}, '${food.food_name}')">Add</button>

                <input type=number placeholder="amount in grams" id="foodstuck_input_add_${food.food_id}" min=0 />

                <p>${food.food_description}</p>
                <a href="${food.food_url}" target="_blank">More Details</a>
            `;
            resultsDiv.appendChild(foodDiv);
        });
    } else {
        resultsDiv.innerHTML = 'No results found.';
    }
}

const selectedFoodstuffs = new Map();

function addIngredient(foodId, foodName) {
    const amountInput = document.getElementById(`foodstuck_input_add_${foodId}`);
    const amount = amountInput.value;

    if (!amount || amount <= 0) {
        alert("Please enter a valid amount in grams.");
        return;
    }

    const selectedProduct = foodName;

    if (selectedFoodstuffs.has(selectedProduct)) {
        document.getElementById('selected_list_' + selectedProduct).childNodes[0].nodeValue = amount + " " + selectedProduct;
        selectedFoodstuffs.set(selectedProduct, amount);
        return;
    }

    selectedFoodstuffs.set(selectedProduct, amount);

    // Créer un nouvel élément de liste
    const li = document.createElement('li');
    li.className = 'list-group-item d-flex justify-content-between align-items-center';
    li.id = 'selected_list_' + selectedProduct;
    var text = document.createTextNode(amount + " " + selectedProduct);
    li.appendChild(text);

    var btn2 = document.createElement('button');
    btn2.className = 'btn btn-danger btn-sm';
    btn2.innerText = 'Delete';
    btn2.onclick = function () {
        if (selectedFoodstuffs.has(selectedProduct)) {
            selectedFoodstuffs.delete(selectedProduct);
        }
        li.parentNode.removeChild(li);
        updateTheFoodStuckDisplay();
    };

    li.appendChild(btn2);

    // Ajouter le nouvel élément de liste à la liste des produits
    document.getElementById('productList').appendChild(li);
}
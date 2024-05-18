document.getElementById("computeButton").addEventListener("click", function () {
    const glucose_level = document.getElementById("glucose_level").valueAsNumber;
    const sensitivity = document.getElementById("Sensitivity_factor").valueAsNumber;
    const target_level = document.getElementById("target_level").valueAsNumber;
    if (Number.isNaN(glucose_level)) {
        alert("Complete your glucose level.");
        return;
    }
    if (Number.isNaN(target_level)) {
        alert("Complete the target glucose level field.");
        return;
    }
    if (Number.isNaN(sensitivity)) {
        alert("Complete the sensitivity field.");
        return;
    }
    
    const insulinData = {
        glucose_level: glucose_level, // Example value
        glucose_goal: target_level, // Example value
        insulin_sensitivity: sensitivity // Example value
    };

    // Convertir le tableau en JSON
    const json = JSON.stringify(insulinData);

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
            window.location.href = "/meal_resume";
        })
    
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
                        onclick="addIngredient(${food.food_id}, '${food.food_name}', '${food.food_description}')">Add</button>

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

function extractNutritionInfo(description) {
    const kcalMatch = description.match(/Calories:\s*([\d.]+)kcal/);
    const carbsMatch = description.match(/Carbs:\s*([\d.]+)g/);

    const kcalPer100g = kcalMatch ? parseFloat(kcalMatch[1]) : 0;
    const carbsPer100g = carbsMatch ? parseFloat(carbsMatch[1]) : 0;

    return { kcalPer100g, carbsPer100g };
}

const selectedFoodstuffs = new Map();

function addIngredient(foodId, foodName, foodDescription) {
     const amountInput = document.getElementById(`foodstuck_input_add_${foodId}`);
    const amount = amountInput.value;

    if (!amount || amount <= 0) {
        alert("Please enter a valid amount in grams.");
        return;
    }

    const { kcalPer100g, carbsPer100g } = extractNutritionInfo(foodDescription);

    const selectedProduct = {
        id: foodId,
        label: foodName,
        amount: parseFloat(amount),
        kcal: (kcalPer100g / 100) * parseFloat(amount),
        carbs: (carbsPer100g / 100) * parseFloat(amount)
    };

    selectedFoodstuffs.set(foodId, selectedProduct);

    // Sauvegarder les données dans la session
    fetch('/save-ingredient', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ selectedProduct })
    }).then(response => {
        if (response.ok) {
            console.log('Ingredient saved to session');
        } else {
            console.log('Failed to save ingredient to session');
        }
    });

    // Créer un nouvel élément de liste
    const li = document.createElement('li');
    li.className = 'list-group-item d-flex justify-content-between align-items-center';
    li.id = 'selected_list_' + foodId;
    var text = document.createTextNode(amount + "g " + foodName);
    li.appendChild(text);

    var btn2 = document.createElement('button');
    btn2.className = 'btn btn-danger btn-sm';
    btn2.innerText = 'Delete';
    btn2.onclick = function () {
        if (selectedFoodstuffs.has(foodId)) {
            selectedFoodstuffs.delete(foodId);
        }
        li.parentNode.removeChild(li);


        // Supprimer l'ingrédient de la session
        fetch('/delete-ingredient', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: foodId })
        }).then(response => {
            if (response.ok) {
                console.log('Ingredient removed from session');
            } else {
                console.log('Failed to remove ingredient from session');
            }
        });
    };

    li.appendChild(btn2);

    // Ajouter le nouvel élément de liste à la liste des produits
    document.getElementById('productList').appendChild(li);

}
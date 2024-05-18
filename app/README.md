# Detailed Routes

## Insulin Management Routes

### POST /insulin/compute

Receives ingredient details and calculates the insulin level required. It accepts ingredient details such as names, quantities, and any specific identifiers that are necessary to perform the computation.

**Body**

```json
{
    "glucose_level": 34,
    "glucose_goal": 34,
    "insulin_sensitivity" : 3,
    "ingredients": [
        {"name": "Ingredient1", "quantity": "100g", "carbs":  "1.9"},
        {"name": "Ingredient2", "quantity": "200g", "carbs":  "1.9"},
        ...
    ]
}
```

**Responses**

- 200 OK - Returns the computed insulin level.
- 400 Bad Request - Incorrect or incomplete data provided.
- 500 Internal Server Error - Server error during computation.

### POST /insulin/combinations

Stores a combination of ingredients and their computed insulin level for later reuse. This requires user authentication.

**Body**

```json
{
    "ingredients": [
        {"name": "Ingredient1", "quantity": "100g", "carbs":  "1.9"},
        {"name": "Ingredient2", "quantity": "200g", "carbs":  "1.9"},
        ...
    ],
    "insulinLevel": 15.5
}
```

**Responses**

- 201 Created - Successfully saved the ingredient combination.
- 400 Bad Request - Incorrect or incomplete data provided.
- 500 Internal Server Error - Server error during saving the combination.

### GET /insulin/combinations

Retrieves all saved combinations of ingredients and their corresponding insulin levels. This requires user authentication.

**Responses**

- 200 OK - Returns a list of all saved combinations.
- 404 Not Found - No combinations found.
- 500 Internal Server Error - Server error during retrieval.

### GET /insulin/combinations/{id}

Retrieves detailed information about a specific saved combination of ingredients and its computed insulin level. This requires user authentication.

**Responses**

- 200 OK - Returns detailed information of the specified combination.
- 404 Not Found - Combination not found.
- 500 Internal Server Error - Server error during retrieval.

## Ingredients Routes

All the ingredients will be retrieved from an API called FatSecret.

## Custom Meals Management Routes

### POST /meals/combinations

Allows users to create a new meal combination by submitting a list of ingredients with specific quantities. This requires user authentication.

**Body**

```json
{
    "name": "Niçoise Salad",
    "ingredients": [
        {"name": "Tomato", "quantity": "150g", "carbs": 1.9, "kcal":  102},
        {"name": "Tuna", "quantity": "100g", "carbs": 1.9, "kcal":  102},
        {"name": "Olives", "quantity": "50g", "carbs": 1.9, "kcal":  102}
    ]
}
```

**Responses**

- 201 Created - Successfully created the meal combination.
- 400 Bad Request - Incorrect or incomplete data provided.
- 500 Internal Server Error - Server error during the creation process.

### GET /meals/combinations

Retrieves all meal combinations stored in the database. This requires user authentication.

**Responses**

- 200 OK - Successfully returned the list of combinations.
- 404 Not Found - No combinations found.
- 500 Internal Server Error - Server error during data retrieval.

### GET /meals/combinations/{id}

Retrieves the details of a specific meal combination by its ID. This requires user authentication.

**Responses**

- 200 OK - Successfully returned the details of the combination.
- 404 Not Found - Combination not found.
- 500 Internal Server Error - Server error during the retrieval process.

### PUT /meals/combinations/{id}

Updates an existing meal combination by modifying its ingredients or the name of the combination. This requires user authentication.

**Body**

```json
{
    "name": "Mediterranean Salad",
    "ingredients": [
        {"name": "Tomato", "quantity": "200g", "carbs": 1.9, "kcal":  102},
        {"name": "Tuna", "quantity": "150g", "carbs": 1.9, "kcal":  102},
        {"name": "Olives", "quantity": "60g", "carbs": 1.9, "kcal":  102},
        {"name": "Feta", "quantity": "50g", "carbs": 1.9, "kcal":  102}
    ]
}
```

**Responses**

- 200 OK - Successfully updated the combination.
- 400 Bad Request - Incorrect or incomplete data provided.
- 404 Not Found - Combination not found.
- 500 Internal Server Error - Server error during the update process.

### DELETE /meals/combinations/{id}

Deletes a specific meal combination by its ID. This requires user authentication.

**Responses**

- 204 No Content - Successfully deleted the combination.
- 404 Not Found - Combination not found.
- 500 Internal Server Error - Server error during the deletion process.
```
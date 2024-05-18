class Ingredient:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity


class InsulinCalculation:
    def __init__(self, ingredients):
        self.ingredients = ingredients

    def calculate_insulin_dose(self):
        total_dose = 0
        for ingredient in self.ingredients:
            dose = (len(ingredient.name) * int(ingredient.quantity.replace('g', ''))) / 100
            total_dose += dose
        return total_dose

    def calculate_insulin_dosage(self, blood_glucose_level, target_glucose_level, sensitivity_factor, carbs_intake,
                                 insulin_to_carb_ratio):
        """
        Calculate the total insulin dosage based on blood glucose level, target glucose level, sensitivity factor, carbohydrate intake, and insulin-to-carb ratio.

        Parameters:
        blood_glucose_level (float): The current blood glucose level of the patient (mg/dl or mmol/l).
        target_glucose_level (float): The desired blood glucose level (given by doctor, mg/dl or mmol/l).
        sensitivity_factor (float): The expected decrease in blood glucose level per unit of insulin (given by doctor, mg/dl per unit or mmol/l per unit) .
        carbs_intake (float): The amount of carbohydrate intake in grams.
        insulin_to_carb_ratio (float): The amount of insulin needed per gram of carbohydrate (e.g., ratio 1:15).

        Returns:
        float: The total insulin dosage.
        """

        # Calculate correction dose
        correction_dose = (blood_glucose_level - target_glucose_level) / sensitivity_factor

        # Calculate meal dose (insulin needed for carbohydrate intake)
        meal_dose = carbs_intake * insulin_to_carb_ratio

        # Total insulin dose
        total_insulin_dose = correction_dose + meal_dose

        return total_insulin_dose


class MealCombination:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def to_dict(self):
        return {
            "name": self.name,
            "ingredients": self.ingredients
        }

# class User:
#     def __init__(self, name, email):
#         self.name = name
#         self.email = email
#
#     def save(self):
#         user_doc = {
#             'type': 'user',
#             'name': self.name,
#             'email': self.email
#         }
#         return couch.db.save(user_doc)
#
#     @staticmethod
#     def get_all():
#         return [doc for doc in couch.db.view('_all_docs', include_docs=True) if doc['doc'].get('type') == 'user']

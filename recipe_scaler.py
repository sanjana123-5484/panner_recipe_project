

import json
import random

# Recipe data 
RECIPES = {
    "palak_paneer": {
        1: {"Onion": 85, "Garlic": 10, "Green chilli": 0.90, "Paneer": 100},
        2: {"Onion": 85, "Garlic": 16.63, "Green chilli": 1.75, "Paneer": 200},
        3: {"Onion": 110, "Garlic": 20, "Green chilli": 2.58, "Paneer": 300},
        4: {"Onion": 140, "Garlic": 25, "Green chilli": 3.51, "Paneer": 400}
    },
    "shahi_paneer": {
        1: {"Green chilli": 0.41, "Ginger garlic paste": 10, "Tomato": 110, "Paneer": 150},
        2: {"Green chilli": 0.90, "Ginger garlic paste": 15, "Tomato": 165, "Paneer": 200},
        3: {"Green chilli": 0.90, "Ginger garlic paste": 20, "Tomato": 220, "Paneer": 300},
        4: {"Green chilli": 0.90, "Ginger garlic paste": 25, "Tomato": 275, "Paneer": 400}
    }
}

def linear_scaling(recipe, known_servings, target_serving):
    """
    Scale ingredients using linear method
    Example: If you know quantities for 2 and 4 people, predict for 6 people
    """
    s1, s2 = known_servings[0], known_servings[1]  # Known serving sizes
    ingredients_s1 = RECIPES[recipe][s1]  # Quantities for serving size 1
    ingredients_s2 = RECIPES[recipe][s2]  # Quantities for serving size 2
    
    scaled_ingredients = {}
    
    for ingredient in ingredients_s1.keys():
        if ingredient in ingredients_s2:
            q1 = ingredients_s1[ingredient]  # Quantity at serving size 1
            q2 = ingredients_s2[ingredient]  # Quantity at serving size 2
            
            # Linear formula: q = q1 + (q2-q1) * (target-s1) / (s2-s1)
            if s2 != s1:  # Avoid division by zero
                scaled_quantity = q1 + (q2 - q1) * (target_serving - s1) / (s2 - s1)
            else:
                scaled_quantity = q1
            
            scaled_ingredients[ingredient] = max(0, scaled_quantity)  # No negative quantities
    
    return scaled_ingredients

def calculate_error(predicted, actual):
    """Calculate how accurate our predictions are"""
    total_error = 0
    count = 0
    
    for ingredient in predicted.keys():
        if ingredient in actual:
            error = abs(predicted[ingredient] - actual[ingredient])
            total_error += error
            count += 1
    
    return total_error / count if count > 0 else 0  # Average error

def test_scaling_method():
    """Test our scaling method and see how well it works"""
    print("Testing Recipe Scaling Method")
    print("=" * 40)
    
    total_errors = []
    
    # Test each recipe
    for recipe_name in RECIPES.keys():
        print(f"\nTesting {recipe_name}:")
        
        # Test: Use servings 1 and 3 to predict serving 2 and 4
        known = [1, 3]
        targets = [2, 4]
        
        for target in targets:
            # Make prediction
            predicted = linear_scaling(recipe_name, known, target)
            
            # Get actual values
            actual = RECIPES[recipe_name][target]
            
            # Calculate error
            error = calculate_error(predicted, actual)
            total_errors.append(error)
            
            print(f"  Predicting for {target} people:")
            print(f"    Average error: {error:.2f} grams")
            
            # Show some examples
            for ingredient in list(predicted.keys())[:3]:  # Show first 3 ingredients
                if ingredient in actual:
                    pred_val = predicted[ingredient]
                    actual_val = actual[ingredient]
                    print(f"    {ingredient}: predicted={pred_val:.1f}g, actual={actual_val:.1f}g")
    
    # Overall performance
    avg_error = sum(total_errors) / len(total_errors)
    print(f"\nOverall Performance:")
    print(f"Average error across all tests: {avg_error:.2f} grams")
    
    if avg_error < 5:
        print("✅ Excellent! Very accurate predictions")
    elif avg_error < 10:
        print("✅ Good! Reasonably accurate predictions")
    else:
        print("⚠️ Needs improvement. Consider other methods")

def scale_for_any_serving(recipe_name, known_servings, target_serving):
    """Scale ingredients for any number of people"""
    print(f"\nScaling {recipe_name} for {target_serving} people")
    print(f"Using data from {known_servings[0]} and {known_servings[1]} people")
    print("-" * 50)
    
    scaled = linear_scaling(recipe_name, known_servings, target_serving)
    
    for ingredient, quantity in scaled.items():
        print(f"{ingredient}: {quantity:.1f} grams")
    
    return scaled

# Example usage
if __name__ == "__main__":
    # Test the method
    test_scaling_method()
    
    # Example: Scale Palak Paneer for 6 people using data from 2 and 4 people
    result = scale_for_any_serving("palak_paneer", [2, 4], 6)
    
    # Example: Scale Shahi Paneer for 1.5 people using data from 1 and 3 people
    result = scale_for_any_serving("shahi_paneer", [1, 3], 1.5)
    
    print("\n" + "="*50)
    print("Try your own examples:")
    print("scale_for_any_serving('palak_paneer', [1, 4], 10)")
    print("scale_for_any_serving('shahi_paneer', [2, 3], 7)")
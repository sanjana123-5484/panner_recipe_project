# simple_test.py - No imports needed, just run this file
import json
import random

# Recipe data (simplified version with key ingredients)
RECIPES = {
    "palak_paneer": {
        1: {"Onion": 85, "Garlic": 10, "Green_chilli": 0.90, "Tomato": 80, "Spinach": 125, "Paneer": 100},
        2: {"Onion": 85, "Garlic": 16.63, "Green_chilli": 1.75, "Tomato": 110, "Spinach": 175, "Paneer": 200},
        3: {"Onion": 110, "Garlic": 20, "Green_chilli": 2.58, "Tomato": 165, "Spinach": 275, "Paneer": 300},
        4: {"Onion": 140, "Garlic": 25, "Green_chilli": 3.51, "Tomato": 220, "Spinach": 375, "Paneer": 400}
    },
    "shahi_paneer": {
        1: {"Green_chilli": 0.41, "Ginger_garlic": 10, "Tomato": 110, "Cashews": 5, "Paneer": 150, "Cream": 20},
        2: {"Green_chilli": 0.90, "Ginger_garlic": 15, "Tomato": 165, "Cashews": 10, "Paneer": 200, "Cream": 30},
        3: {"Green_chilli": 0.90, "Ginger_garlic": 20, "Tomato": 220, "Cashews": 15, "Paneer": 300, "Cream": 40},
        4: {"Green_chilli": 0.90, "Ginger_garlic": 25, "Tomato": 275, "Cashews": 25, "Paneer": 400, "Cream": 50}
    },
    "matar_paneer": {
        1: {"Ginger": 3.13, "Green_chilli": 0.46, "Green_peas": 50, "Tomato": 110, "Paneer": 75},
        2: {"Ginger": 6.25, "Green_chilli": 0.93, "Green_peas": 80, "Tomato": 165, "Paneer": 150},
        3: {"Ginger": 9.38, "Green_chilli": 0.90, "Green_peas": 120, "Tomato": 245, "Paneer": 200},
        4: {"Ginger": 12.50, "Green_chilli": 0.90, "Green_peas": 150, "Tomato": 330, "Paneer": 300}
    },
    "paneer_masala": {
        1: {"Green_chilli": 0.41, "Onion": 110, "Ginger_garlic": 10, "Tomato": 80, "Paneer": 150},
        2: {"Green_chilli": 0.41, "Onion": 140, "Ginger_garlic": 15, "Tomato": 110, "Paneer": 200},
        3: {"Green_chilli": 0.90, "Onion": 170, "Ginger_garlic": 20, "Tomato": 135, "Paneer": 300},
        4: {"Green_chilli": 0.82, "Onion": 195, "Ginger_garlic": 25, "Tomato": 165, "Paneer": 400}
    }
}

# Scaling Methods
def linear_scaling(recipe, known_servings, target_serving):
    """Method 1: Linear scaling"""
    s1, s2 = known_servings[0], known_servings[1]
    ingredients_s1 = RECIPES[recipe][s1]
    ingredients_s2 = RECIPES[recipe][s2]
    
    scaled_ingredients = {}
    for ingredient in ingredients_s1.keys():
        if ingredient in ingredients_s2:
            q1, q2 = ingredients_s1[ingredient], ingredients_s2[ingredient]
            if s2 != s1:
                scaled_quantity = q1 + (q2 - q1) * (target_serving - s1) / (s2 - s1)
            else:
                scaled_quantity = q1
            scaled_ingredients[ingredient] = max(0, scaled_quantity)
    return scaled_ingredients

def proportional_scaling(recipe, known_servings, target_serving):
    """Method 2: Proportional scaling"""
    s1, s2 = known_servings[0], known_servings[1]
    ingredients_s1 = RECIPES[recipe][s1]
    ingredients_s2 = RECIPES[recipe][s2]
    
    # Calculate scaling factors
    scaling_factors = []
    for ingredient in ingredients_s1.keys():
        if ingredient in ingredients_s2 and ingredients_s1[ingredient] > 0:
            factor = ingredients_s2[ingredient] / ingredients_s1[ingredient]
            scaling_factors.append(factor)
    
    # Use average scaling factor
    if scaling_factors:
        avg_factor = sum(scaling_factors) / len(scaling_factors)
        serving_ratio = (s2 / s1) if s1 > 0 else 1
        base_scaling_rate = avg_factor / serving_ratio if serving_ratio > 0 else 1
    else:
        base_scaling_rate = 1
    
    # Scale to target
    target_ratio = target_serving / s1 if s1 > 0 else 1
    scaled_ingredients = {}
    
    for ingredient in ingredients_s1.keys():
        if ingredient in ingredients_s2:
            scaled_quantity = ingredients_s1[ingredient] * base_scaling_rate * target_ratio
            scaled_ingredients[ingredient] = max(0, scaled_quantity)
    
    return scaled_ingredients

def simple_ratio_scaling(recipe, known_servings, target_serving):
    """Method 3: Simple ratio scaling"""
    s1, s2 = known_servings[0], known_servings[1]
    ingredients_s1 = RECIPES[recipe][s1]
    
    # Simple ratio based on serving sizes
    ratio = target_serving / s1 if s1 > 0 else 1
    
    scaled_ingredients = {}
    for ingredient, quantity in ingredients_s1.items():
        scaled_ingredients[ingredient] = quantity * ratio
    
    return scaled_ingredients

# Evaluation Functions
def calculate_metrics(predicted, actual):
    """Calculate evaluation metrics"""
    mae_values = []
    mape_values = []
    
    for ingredient in predicted.keys():
        if ingredient in actual:
            pred_val = predicted[ingredient]
            actual_val = actual[ingredient]
            
            # Mean Absolute Error
            mae_values.append(abs(pred_val - actual_val))
            
            # Mean Absolute Percentage Error
            if actual_val > 0:
                mape_values.append(abs(pred_val - actual_val) / actual_val * 100)
    
    mae = sum(mae_values) / len(mae_values) if mae_values else 0
    mape = sum(mape_values) / len(mape_values) if mape_values else 0
    
    return {"MAE": mae, "MAPE": mape}

def run_evaluation():
    """Run evaluation of all scaling methods"""
    methods = {
        "Linear Scaling": linear_scaling,
        "Proportional Scaling": proportional_scaling,
        "Simple Ratio Scaling": simple_ratio_scaling
    }
    
    results = {method: {"MAE": [], "MAPE": []} for method in methods.keys()}
    
    print("Running Recipe Scaling Evaluation...")
    print("=" * 50)
    
    # Test each combination
    for trial in range(20):  # 20 trials for statistical significance
        for recipe in RECIPES.keys():
            # Test: use servings 1,3 to predict 2,4
            known_servings = [1, 3]
            target_servings = [2, 4]
            
            for target in target_servings:
                actual_ingredients = RECIPES[recipe][target]
                
                for method_name, method_func in methods.items():
                    try:
                        predicted_ingredients = method_func(recipe, known_servings, target)
                        metrics = calculate_metrics(predicted_ingredients, actual_ingredients)
                        
                        results[method_name]["MAE"].append(metrics["MAE"])
                        results[method_name]["MAPE"].append(metrics["MAPE"])
                    except Exception as e:
                        print(f"Error in {method_name}: {e}")
    
    # Display results
    print("\nEVALUATION RESULTS:")
    print("-" * 50)
    
    for method_name in methods.keys():
        mae_values = results[method_name]["MAE"]
        mape_values = results[method_name]["MAPE"]
        
        if mae_values:
            avg_mae = sum(mae_values) / len(mae_values)
            avg_mape = sum(mape_values) / len(mape_values)
            
            print(f"\n{method_name}:")
            print(f"  Average MAE: {avg_mae:.3f} grams")
            print(f"  Average MAPE: {avg_mape:.2f}%")
    
    # Find best method
    best_method = min(methods.keys(), 
                     key=lambda x: sum(results[x]["MAE"]) / len(results[x]["MAE"]) if results[x]["MAE"] else float('inf'))
    
    print(f"\n🏆 BEST METHOD: {best_method}")
    
    return results

def demonstrate_scaling():
    """Show examples of scaling in action"""
    print("\n" + "=" * 50)
    print("SCALING DEMONSTRATION")
    print("=" * 50)
    
    # Example 1: Scale Palak Paneer for 6 people
    recipe = "palak_paneer"
    known = [2, 4]
    target = 6
    
    print(f"\nScaling {recipe} for {target} people using data from {known}")
    print("-" * 40)
    
    methods = {
        "Linear": linear_scaling,
        "Proportional": proportional_scaling,
        "Simple Ratio": simple_ratio_scaling
    }
    
    for method_name, method_func in methods.items():
        try:
            result = method_func(recipe, known, target)
            print(f"\n{method_name} Method:")
            for ingredient, quantity in list(result.items())[:5]:  # Show first 5 ingredients
                print(f"  {ingredient}: {quantity:.1f}g")
        except Exception as e:
            print(f"  Error: {e}")

# Main execution
if __name__ == "__main__":
    print("🍛 PANEER RECIPE SCALING PROJECT")
    print("=" * 50)
    
    # Run the evaluation
    results = run_evaluation()
    
    # Show scaling examples
    demonstrate_scaling()
    
    print("\n" + "=" * 50)
    print("✅ EVALUATION COMPLETE!")
    print("Check the results above to see which method works best.")
    print("=" * 50)
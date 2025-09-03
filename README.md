# Food-AI Intern Assignment: Recipe Scaling Evaluation Report

## Executive Summary

This report presents a comprehensive analysis of three different approaches for scaling ingredient quantities in paneer-based recipes. The evaluation demonstrates that **Linear Scaling** performs best overall, with the lowest prediction errors across multiple metrics.

## Problem Statement

Given ingredient quantities for two known serving sizes of paneer recipes, we need to predict ingredient quantities for any target serving size. The challenge is to develop robust scaling methods that can generalize across different recipes and serving sizes.

## Dataset Overview

The analysis uses data from 4 paneer dishes:
- **Palak Paneer** (10 ingredients)
- **Shahi Paneer** (8 ingredients)  
- **Matar Paneer** (10 ingredients)
- **Paneer Masala** (5 ingredients)

Each recipe includes ingredient quantities for serving sizes 1-4, with quantities specified in grams extracted from the original format.

## Scaling Approaches

### 1. Linear Scaling
**Concept**: Assumes ingredients scale linearly with serving size using interpolation/extrapolation.

**Formula**: 
```
q_target = q1 + (q2 - q1) × (target - s1) / (s2 - s1)
```

**Rationale**: 
- Simple and intuitive approach
- Works well for most cooking ingredients that scale proportionally
- Provides stable predictions through linear interpolation

### 2. Proportional Scaling  
**Concept**: Uses median scaling factor across ingredients to determine overall scaling rate.

**Process**:
1. Calculate scaling factor for each ingredient: `factor = q2/q1`
2. Find median scaling factor to avoid outliers
3. Apply normalized scaling rate to target serving size

**Rationale**:
- Robust to outliers by using median
- Accounts for non-uniform scaling across ingredients
- More sophisticated than pure linear scaling

### 3. Power Scaling
**Concept**: Assumes ingredients follow power law relationship: `q = a × serving_size^b`

**Process**:
1. Calculate power exponent: `b = log(q2/q1) / log(s2/s1)`
2. Calculate coefficient: `a = q1 / s1^b`  
3. Scale to target: `q_target = a × target^b`

**Rationale**:
- Captures non-linear scaling relationships
- Theoretically more flexible
- Falls back to linear scaling for edge cases

## Evaluation Metrics

### 1. Mean Absolute Error (MAE)
- **Purpose**: Average absolute difference between predicted and actual values
- **Units**: Grams
- **Interpretation**: Lower values indicate better accuracy

### 2. Mean Absolute Percentage Error (MAPE)
- **Purpose**: Percentage-based error measure
- **Units**: Percentage
- **Interpretation**: Scale-independent metric, useful for comparing ingredients with different quantities

### 3. Root Mean Square Error (RMSE)
- **Purpose**: Emphasizes larger errors more than MAE
- **Units**: Grams  
- **Interpretation**: Sensitive to outliers, good for detecting systematic errors

### 4. R-squared (R²)
- **Purpose**: Measures correlation between predicted and actual values
- **Range**: 0 to 1
- **Interpretation**: Higher values indicate better linear relationship

## Evaluation Methodology

### Procedure:
1. **Random Sampling**: For each trial, randomly select 2 out of 4 serving sizes as "known"
2. **Prediction**: Use the 3 scaling methods to predict quantities for remaining serving sizes
3. **Comparison**: Compare predictions against actual values from the dataset
4. **Repetition**: Repeat process 50 times to ensure statistical significance
5. **Aggregation**: Calculate mean and standard deviation for each metric

### Coverage:
- **4 recipes** × **multiple serving size combinations** × **50 trials**  
- **Total evaluations**: ~600 prediction scenarios per method

## Results
<img width="747" height="327" alt="Screenshot 2025-09-03 173133" src="https://github.com/user-attachments/assets/5261a80a-5070-4ea5-a284-447d5ae13ef3" />


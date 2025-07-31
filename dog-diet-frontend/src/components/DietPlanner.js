import React, { useState } from 'react';
import axios from 'axios';

const DietPlanner = () => {
  const [ingredients, setIngredients] = useState([]);
  const [response, setResponse] = useState(null);

  const availableIngredients = [
    { ingredient_name: 'Beef liver', group_name: 'Organ Meat' },
    { ingredient_name: 'Chicken breast, meat only', group_name: 'Meat Group A' },
    { ingredient_name: 'Wheat', group_name: 'Grain' },
    { ingredient_name: 'Zucchini', group_name: 'Vegetable' },
    { ingredient_name: 'Almond oil', group_name: 'Oil' },
    { ingredient_name: 'Apple', group_name: 'Fruit' }
  ];

  const defaultValues = {
    dm_g: 50,
    fat_g: 5,
    protein_g: 10,
    water_g: 10,
    calcium_mg: 15,
    iron_mg: 1.5
  };

  const handleAddIngredient = (ing) => {
    const exists = ingredients.some(i => i.ingredient_name === ing.ingredient_name);
    if (!exists) {
      setIngredients([...ingredients, { ...ing, ...defaultValues }]);
    }
  };

  const handleSubmit = async () => {
    try {
      const res = await axios.post('http://localhost:8000/calculate_diet', {
        ingredients: ingredients
      });
      setResponse(res.data);
    } catch (err) {
      alert("Error processing request");
      console.error(err);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Dog Diet Planner</h2>

      <div>
        <h3>Select Ingredients:</h3>
        {availableIngredients.map((ing, i) => (
          <button key={i} onClick={() => handleAddIngredient(ing)} style={{ margin: '5px' }}>
            {ing.ingredient_name}
          </button>
        ))}
      </div>

      <div>
        <h4>Selected Ingredients:</h4>
        <ul>
          {ingredients.map((i, idx) => (
            <li key={idx}>{i.ingredient_name}</li>
          ))}
        </ul>
      </div>

      <button onClick={handleSubmit}>Calculate Diet</button>

      {response && (
        <div>
          <h3>Adjusted Recipe Output:</h3>
          <ul>
            {response.adjusted_ingredients.map((ing, idx) => (
              <li key={idx}>
                {ing.ingredient_name} — DM: {ing.dm_g}g, Protein: {ing.protein_g}g, Fat: {ing.fat_g}g
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default DietPlanner;

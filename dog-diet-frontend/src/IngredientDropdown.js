// ✅ FRONTEND - IngredientSelector.jsx (React Component with Tailwind)

import React, { useEffect, useState } from "react";

function IngredientSelector() {
  const [ingredients, setIngredients] = useState([]);
  const [selected, setSelected] = useState([]);
  const [nutrients, setNutrients] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/ingredients")
      .then((res) => res.json())
      .then((data) => setIngredients(data));
  }, []);

  const handleChange = (event) => {
    const { value, checked } = event.target;
    if (checked) {
      setSelected([...selected, value]);
    } else {
      setSelected(selected.filter((item) => item !== value));
    }
  };

  const handleCalculate = () => {
    fetch("http://localhost:8000/calculate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ingredients: selected }),
    })
      .then((res) => res.json())
      .then((data) => setNutrients(data));
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Select Ingredients</h2>

      <div className="grid grid-cols-2 gap-4">
        {ingredients.map((ingredient, index) => (
          <label key={index} className="flex items-center space-x-2">
            <input
              type="checkbox"
              value={ingredient.ingredient_name}
              onChange={handleChange}
              checked={selected.includes(ingredient.ingredient_name)}
            />
            <span>
              <strong>{ingredient.ingredient_name}</strong> - {ingredient.group_name}
            </span>
          </label>
        ))}
      </div>

      <button
        onClick={handleCalculate}
        className="mt-6 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Calculate Nutrients
      </button>

      {nutrients && (
        <div className="mt-6 bg-gray-100 p-4 rounded shadow">
          <h3 className="text-xl font-semibold mb-2">Nutrient Summary (Dry Matter Basis):</h3>
          <ul className="list-disc pl-5">
            {Object.entries(nutrients).map(([key, value]) => (
              <li key={key}>
                {key}: {value.toFixed(2)}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default IngredientSelector;

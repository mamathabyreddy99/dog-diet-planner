import React, { useState, useEffect } from "react";

function Step2IngredientSelection() {
  const [ingredients, setIngredients] = useState([]);
  const [selectedIngredient, setSelectedIngredient] = useState("");

  useEffect(() => {
    // Replace with your backend URL & endpoint
    fetch("http://127.0.0.1:8000/ingredients/group_a_oyster_canned")
      .then((res) => res.json())
      .then((data) => setIngredients(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2>Select an ingredient from Group A Oyster Canned</h2>
      <select
        value={selectedIngredient}
        onChange={(e) => setSelectedIngredient(e.target.value)}
      >
        <option value="">-- Select Ingredient --</option>
        {ingredients.map((item) => (
          <option key={item.id} value={item.name}>
            {item.name}
          </option>
        ))}
      </select>

      {selectedIngredient && <p>You selected: {selectedIngredient}</p>}
    </div>
  );
}

export default Step2IngredientSelection;

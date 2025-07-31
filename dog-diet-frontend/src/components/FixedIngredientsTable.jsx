import React, { useEffect, useState } from "react";
import axios from "axios";

function FixedIngredientsTable() {
  const [ingredients, setIngredients] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/fixed-ingredients")
      .then((res) => setIngredients(res.data))
      .catch((err) => console.error("Error fetching data:", err));
  }, []);

  return (
    <div>
      <h2>Fixed Ingredients Summary</h2>
      <table border="1" cellPadding="8" style={{ width: "100%", textAlign: "left" }}>
        <thead>
          <tr>
            <th>Ingredient</th>
            <th>Fresh (g)</th>
            <th>Water %</th>
            <th>DM (g)</th>
            <th>Protein</th>
            <th>Fat</th>
            <th>CHO</th>
            <th>Fiber</th>
            <th>Calcium</th>
            <th>Iron</th>
          </tr>
        </thead>
        <tbody>
          {ingredients.map((item) => (
            <tr key={item.id}>
              <td>{item.ingredient}</td>
              <td>{item.fresh_weight_g}</td>
              <td>{item.water_percent}</td>
              <td>{item.dm_weight_g}</td>
              <td>{item.protein_g}</td>
              <td>{item.fat_g}</td>
              <td>{item.cho_g}</td>
              <td>{item.fiber_g}</td>
              <td>{item.calcium_mg}</td>
              <td>{item.iron_mg}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default FixedIngredientsTable;

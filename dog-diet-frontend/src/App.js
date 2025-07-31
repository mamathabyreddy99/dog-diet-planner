import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [ingredients, setIngredients] = useState([]);
  const [selectedIngredients, setSelectedIngredients] = useState([]);
  const [result, setResult] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/ingredients')
      .then(res => setIngredients(res.data))
      .catch(err => console.error('Failed to fetch ingredients:', err));
  }, []);

  const handleCheckboxChange = (e) => {
    const value = e.target.value;
    setSelectedIngredients(prev =>
      e.target.checked ? [...prev, value] : prev.filter(item => item !== value)
    );
  };

  const calculateDiet = () => {
    const selectedDetails = ingredients.filter(ing =>
      selectedIngredients.includes(ing.ingredient_name)
    );

    const selectedGrainA = selectedDetails.filter(i => i.group_name.toLowerCase() === 'grain a');
    const selectedGrainB = selectedDetails.filter(i => i.group_name.toLowerCase() === 'grain b');

    if (selectedGrainB.length > 0 && selectedGrainA.length === 0) {
      alert("❗ Grain Group B cannot be used alone. Please select at least one Group A grain.");
      return;
    }
     // ✅ Liver rule (frontend pre-check)
    const liverKeywords = ["liver", "beef liver", "chicken liver", "pork liver", "liver raw"];
    const hasLiver = selectedDetails.some(i =>
      liverKeywords.includes(i.ingredient_name.toLowerCase())
    );
    if (!hasLiver) {
      alert("❗ Liver is required in the recipe. Please select a liver ingredient.");
      return;
    }
    axios.post('http://127.0.0.1:8000/calculate', {
      ingredients: selectedIngredients
    })
      .then(res => setResult(res.data))
      .catch(err => console.error('Error calculating diet:', err));
  };

  // ✅ Total row logic (computed after receiving result)
  const tableTotalRow = result?.ingredient_totals?.reduce(
    (acc, curr) => {
      acc.dm_g += curr.dm_g;
      acc.protein_g += curr.protein_g;
      acc.fat_g += curr.fat_g;
      acc.cho_g += curr.cho_g;
      acc.fiber_g += curr.fiber_g;
      acc.ash_g += curr.ash_g;
      acc.ca_mg += curr.ca_mg;
      acc.p_mg += curr.p_mg;
      acc.iron_mg += curr.iron_mg;
      acc.energy_kcal += curr.energy_kcal;
      return acc;
    },
    {
      dm_g: 0,
      protein_g: 0,
      fat_g: 0,
      cho_g: 0,
      fiber_g: 0,
      ash_g: 0,
      ca_mg: 0,
      p_mg: 0,
      iron_mg: 0,
      energy_kcal: 0
    }
  );

  return (
    <div className="p-6 max-w-7xl mx-auto text-center">
      <h1 className="text-4xl font-bold mb-6">🐶 Dog Diet Planner</h1>

      <div className="text-left mb-6">
        <h2 className="text-xl font-semibold mb-2">💾 Select Ingredients:</h2>
        {Object.entries(
          ingredients.reduce((groups, ingredient) => {
            const group = ingredient.group_name || "Other";
            if (!groups[group]) groups[group] = [];
            groups[group].push(ingredient);
            return groups;
          }, {})
        ).map(([group, items], idx) => (
          <fieldset key={idx} className="mb-4 border border-gray-300 rounded p-3">
            <legend className="text-lg font-bold bg-yellow-100 p-2 rounded">{group}</legend>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
              {items.map((item, i) => (
                <label key={i} className="flex items-center">
                  <input
                    type="checkbox"
                    value={item.ingredient_name}
                    onChange={handleCheckboxChange}
                    className="mr-2"
                  />
                  <span>{item.ingredient_name}</span>
                </label>
              ))}
            </div>
          </fieldset>
        ))}
      </div>

      <button
        className="bg-blue-600 text-white px-5 py-2 rounded hover:bg-blue-700"
        onClick={calculateDiet}
      >
        🧶 Calculate Diet
      </button>

      {result && (
        <div className="mt-10 text-left">
          <h2 className="text-2xl font-semibold mb-4">📊 Nutrient Summary</h2>

          <ul className="mb-4 leading-7">
            {Object.entries(result.nutrient_percentages).map(([key, value], idx) => (
              <li key={idx}>{key.replace(/_/g, ' ')}: <strong>{value}</strong></li>
            ))}
          </ul>

          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-2">📌 Fixed Ingredients (DM g)</h3>
            <ul className="list-disc list-inside">
              {result.dm_breakdown.filter(d => d.fixed).map((item, idx) => (
                <li key={idx}>• {item.ingredient}: {item.dm_g} g</li>
              ))}
            </ul>

            <h3 className="text-lg font-semibold mt-4">📋 Selected Ingredients (DM g)</h3>
            <ul className="list-disc list-inside">
              {result.dm_breakdown.filter(d => !d.fixed).map((item, idx) => (
                <li key={idx}>• {item.ingredient}: {item.dm_g} g</li>
              ))}
            </ul>
          </div>

          <div className="mt-10">
            <h2 className="text-xl font-bold mb-3">📘 Ingredient-wise Nutrient Contribution</h2>
            <table className="table-auto w-full border border-gray-400 text-sm">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border px-2 py-1">Ingredient</th>
                  <th className="border px-2 py-1">DM (g)</th>
                  <th className="border px-2 py-1">Protein (g)</th>
                  <th className="border px-2 py-1">Fat (g)</th>
                  <th className="border px-2 py-1">CHO (g)</th>
                  <th className="border px-2 py-1">Fiber (g)</th>
                  <th className="border px-2 py-1">Ash (g)</th>
                  <th className="border px-2 py-1">Ca (mg)</th>
                  <th className="border px-2 py-1">p(mg)</th>
                  <th className="border px-2 py-1">Iron (mg)</th>
                  <th className="border px-2 py-1">Energy (kcal)</th>
                  

                </tr>
              </thead>
              <tbody>
                {result.ingredient_totals.map((item, index) => (
                  <tr key={index}>
                    <td className="border px-2 py-1">{item.ingredient}</td>
                    <td className="border px-2 py-1">{item.dm_g}</td>
                    <td className="border px-2 py-1">{item.protein_g}</td>
                    <td className="border px-2 py-1">{item.fat_g}</td>
                    <td className="border px-2 py-1">{item.cho_g}</td>
                    <td className="border px-2 py-1">{item.fiber_g}</td>
                    <td className="border px-2 py-1">{item.ash_g}</td>
                    <td className="border px-2 py-1">{item.ca_mg}</td>
                    <td className="border px-2 py-1">{item.p_mg}</td>
                    <td className="border px-2 py-1">{item.iron_mg}</td>
                    <td className="border px-2 py-1">{item.energy_kcal}</td>
                    
  
                  </tr>
                ))}
              </tbody>
              <tfoot>
                <tr className="bg-blue-50 font-semibold">
                  <td className="border px-2 py-1">Total</td>
                  <td className="border px-2 py-1">{tableTotalRow.dm_g.toFixed(2)}</td>
                  <td className="border px-2 py-1">{tableTotalRow.protein_g.toFixed(2)}</td>
                  <td className="border px-2 py-1">{tableTotalRow.fat_g.toFixed(2)}</td>
                  <td className="border px-2 py-1">{tableTotalRow.cho_g.toFixed(2)}</td>
                  <td className="border px-2 py-1">{tableTotalRow.fiber_g.toFixed(2)}</td>
                  <td className="border px-2 py-1">{tableTotalRow.ash_g.toFixed(2)}</td>
                  <td className="border px-2 py-1">{tableTotalRow.ca_mg.toFixed(2)}</td>
                  <td className="border px-2 py-1">{tableTotalRow.p_mg.toFixed(2)}</td>
                  <td className="border px-2 py-1">{tableTotalRow.iron_mg.toFixed(2)}</td>
                  <td className="border px-2 py-1">{tableTotalRow.energy_kcal.toFixed(2)}</td>
  
                </tr>
              </tfoot>
            </table>
          </div>

          {result.issues && result.issues.length > 0 && (
            <div className="mt-6 text-red-700">
              <h3 className="text-lg font-semibold">❌ Issues Found:</h3>
              <ul className="list-disc list-inside">
                {result.issues.map((issue, idx) => (
                  <li key={idx}>• {issue}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
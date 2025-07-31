import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [ingredients, setIngredients] = useState([]);
  const [selected, setSelected] = useState([]);
  const [result, setResult] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/ingredients')
      .then(res => setIngredients(res.data))
      .catch(err => console.error(err));
  }, []);

  const handleChange = (e) => {
    const value = e.target.value;
    setSelected(prev =>
      e.target.checked ? [...prev, value] : prev.filter(v => v !== value)
    );
  };

  const calculateDiet = () => {
    axios.post('http://localhost:8000/calculate', { ingredients: selected })
      .then(res => setResult(res.data))
      .catch(err => console.error(err));
  };

  return (
    <div className="p-4 max-w-3xl mx-auto text-center">
      <h1 className="text-3xl font-bold mb-4">🐶 Dog Diet Planner</h1>

      <div className="mb-4 text-left">
        {ingredients.map((ing, i) => (
          <label key={i} className="block my-1">
            <input type="checkbox" value={ing.ingredient_name} onChange={handleChange} />
            <span className="ml-2">{ing.ingredient_name} ({ing.group_name})</span>
          </label>
        ))}
      </div>

      <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={calculateDiet}>Calculate Diet</button>

      {result && (
        <div className="mt-6 text-left">
          <h2 className="text-xl font-semibold mb-2">📊 Nutrient Percentages:</h2>
          <ul className="mb-4">
            {Object.entries(result.nutrient_percentages).map(([key, val], i) => (
              <li key={i}>{key.replace(/_/g, ' ')}: {val}</li>
            ))}
          </ul>

          {result.auto_added && (
            <div className="text-yellow-600 font-medium mt-2">
              ⚠️ Auto-added: {result.auto_added}
            </div>
          )}

          <div className="mt-4">
            <h3 className="text-lg font-semibold">📌 Fixed Ingredients (DM g):</h3>
            <ul>
              {result.dm_breakdown.filter(d => d.fixed).map((d, i) => (
                <li key={i}>• {d.ingredient}: {d.dm_g} g</li>
              ))}
            </ul>
            <h3 className="text-lg font-semibold mt-2">📋 Selected Ingredients (DM g):</h3>
            <ul>
              {result.dm_breakdown.filter(d => !d.fixed).map((d, i) => (
                <li key={i}>• {d.ingredient}: {d.dm_g} g</li>
              ))}
            </ul>
          </div>

          {result.issues && result.issues.length > 0 && (
            <div className="mt-4 text-red-600">
              <h3 className="font-semibold">❌ Issues Found:</h3>
              <ul>
                {result.issues.map((issue, i) => <li key={i}>{issue}</li>)}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import psycopg2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FIXED_TOTAL_DM = 1000
ORGAN_DM_TARGET = 150
OIL_DM_RESERVED = 10
FRUIT_DM_LIMIT = 20
GRAIN_DM_TARGET = 350
GRAIN_B_MAX = 200
GRAIN_A_MIN = 150
VEG_A_MIN = 80
VEG_B_MIN = 50
MEAT_MIN = 200
MEAT_MAX = 250
PROTEIN_MIN_PERCENT = 32
PROTEIN_MAX_PERCENT = 42
FIBER_MIN_PERCENT = 3
FIBER_MAX_PERCENT = 6


class IngredientRequest(BaseModel):
    ingredients: List[str]

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="dog_diet_db",
        user="postgres",
        password="Southern@2025"
    )

@app.get("/ingredients")
def get_ingredients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ingredient_name, group_name FROM user_ingredients")
    data = [{"ingredient_name": row[0], "group_name": row[1]} for row in cursor.fetchall()]
    conn.close()
    return data

@app.post("/calculate")
def calculate_diet(request: IngredientRequest):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ingredient_name, dm_g, protein_g, fat_g, cho_g, fiber_g, ash_g, calcium_mg, phosphorus_mg, iron_mg, energy_kcal FROM fixed_ingredients")
    fixed_rows = cursor.fetchall()
    FIXED_DM_USED = sum(row[1] for row in fixed_rows)

    selected_names = list(dict.fromkeys(request.ingredients))
    ingredient_rows = []
    for name in selected_names:
        cursor.execute("""
            SELECT ingredient_name, group_name, protein_g, fat_g, cho_g, fiber_g, ash_g, calcium_mg, phosphorus_mg, iron_mg, energy_kcal
            FROM user_ingredients WHERE ingredient_name = %s
        """, (name,))
        row = cursor.fetchone()
        if row:
            ingredient_rows.append({
                "ingredient": row[0],
                "group": row[1].strip().lower(),
                "data": row[2:]
            })
    conn.close()

    dm_breakdown = []
    ingredient_totals = []
    total = {k: 0 for k in ["Protein", "Fat", "CHO", "Fiber", "Ash", "Ca", "P", "Iron", "Energy"]}
    remaining_dm = FIXED_TOTAL_DM - FIXED_DM_USED
    issues = []
    used_ingredient_names = set()

    def add_to_total(values, dm):
        keys = list(total.keys())
        for i, k in enumerate(keys):
            val = values[i]
            if k in ["Ca", "P"]:
                total[k] += (val / 1000) * dm
            elif k == "Iron":
                total[k] += (val * dm) / 100
            else:
                total[k] += (val / 100) * dm

    def add_ingredient_totals(ingredient, dm, nutrients, fixed):
        ingredient_totals.append({
            "ingredient": ingredient,
            "dm_g": dm,
            "protein_g": round(nutrients[0] * dm / 100, 2),
            "fat_g": round(nutrients[1] * dm / 100, 2),
            "cho_g": round(nutrients[2] * dm / 100, 2),
            "fiber_g": round(nutrients[3] * dm / 100, 2),
            "ash_g": round(nutrients[4] * dm / 100, 2),
            "ca_mg": round(nutrients[5] * dm / 100, 2),
            "p_mg": round(nutrients[6] * dm / 100, 2),
            "iron_mg": round(nutrients[7] * dm / 100, 2),
            "energy_kcal": round(nutrients[8] * dm / 100, 2),
            "fixed": fixed
        })

    def distribute_exact(group_list, target_dm):
        if not group_list or target_dm <= 0:
            return 0
        filtered = [r for r in group_list if r["ingredient"] not in used_ingredient_names]
        if not filtered:
            return 0
        each = round(target_dm / len(filtered), 2)
        actual_used = 0
        for i, r in enumerate(filtered):
            dm = each if i < len(filtered) - 1 else target_dm - each * (len(filtered) - 1)
            add_to_total(r["data"], dm)
            dm_breakdown.append({"ingredient": r["ingredient"], "dm_g": dm, "fixed": False})
            add_ingredient_totals(r["ingredient"], dm, r["data"], fixed=False)
            used_ingredient_names.add(r["ingredient"])
            actual_used += dm
        return actual_used

    for row in fixed_rows:
        name, dm, *nutrients = row
        add_to_total(nutrients, dm)
        dm_breakdown.append({"ingredient": name, "dm_g": dm, "fixed": True})
        add_ingredient_totals(name, dm, nutrients, fixed=True)
        used_ingredient_names.add(name)

    organ_meats = [r for r in ingredient_rows if "organ" in r["group"]]
    liver = [r for r in organ_meats if "liver" in r["ingredient"].lower()]
    other_organs = [r for r in organ_meats if r not in liver]
    if liver:
        liver_dm = int(ORGAN_DM_TARGET * 2 / 3)
        liver_used = distribute_exact(liver[:1], liver_dm)
        remaining_dm -= liver_used
        max_other_dm = ORGAN_DM_TARGET - liver_used
        other_used = distribute_exact(other_organs, max_other_dm)
        remaining_dm -= other_used
    else:
        issues.append("Liver is required (10% of DM).")

    veg_a = [r for r in ingredient_rows if r["group"] == "vegetable a"]
    veg_b = [r for r in ingredient_rows if r["group"] == "vegetable b"]
    veg_c = [r for r in ingredient_rows if r["group"] == "vegetable c"]
    veg_a_used = distribute_exact(veg_a, VEG_A_MIN)
    veg_b_used = distribute_exact(veg_b, VEG_B_MIN)
    veg_c_target = 150 - veg_a_used - veg_b_used
    veg_c_used = distribute_exact(veg_c, max(0, veg_c_target))
    remaining_dm -= (veg_a_used + veg_b_used + veg_c_used)

    remaining_dm -= distribute_exact([r for r in ingredient_rows if "fruit" in r["group"]], FRUIT_DM_LIMIT)
    remaining_dm -= distribute_exact([r for r in ingredient_rows if "oil" in r["group"]], OIL_DM_RESERVED)

    grain_a = [r for r in ingredient_rows if r["group"] == "grain a"]
    grain_b = [r for r in ingredient_rows if r["group"] == "grain b"]
    grain_a_used = distribute_exact(grain_a, GRAIN_A_MIN)
    grain_b_used = distribute_exact(grain_b, GRAIN_B_MAX)
    grain_total = grain_a_used + grain_b_used
    if grain_total < GRAIN_DM_TARGET:
        remaining_grain_dm = GRAIN_DM_TARGET - grain_total
        grain_a_candidates = [r for r in grain_a if r["ingredient"] not in used_ingredient_names]
        distribute_exact(grain_a_candidates, remaining_grain_dm)

    # 🥩 Corrected Meat Group Logic
    meat_a = [r for r in ingredient_rows if r["group"] == "meat group a"]
    meat_b = [r for r in ingredient_rows if r["group"] == "meat group b"]
    meat_c = [r for r in ingredient_rows if r["group"] == "meat group c"]
    all_meats = meat_a + meat_b + meat_c

    def average_fat(group):
        return sum(r["data"][1] for r in group) / len(group) if group else 0

    def get_animal_keyword(name):
        name = name.lower()
        for animal in ["beef", "chicken", "pork", "duck", "turkey", "rabbit", "fish", "quail", "shrimp", "salmon"]:
            if animal in name:
                return animal
        return None

    meat_used = 0
    if not all_meats:
        issues.append("No meat selected.")
    if average_fat(meat_b) > 30:
        meat_used += distribute_exact(meat_b, 100)

    # Auto-fetch Group A fallback meats from DB by animal type
        conn = get_connection()
        cursor = conn.cursor()

        primary_animals = {get_animal_keyword(r["ingredient"]) for r in meat_b}
        fallback_meat_a = []

        for animal in primary_animals:
            cursor.execute("""
                SELECT ingredient_name, group_name, protein_g, fat_g, cho_g, fiber_g, ash_g, calcium_mg, phosphorus_mg, iron_mg, energy_kcal
                FROM user_ingredients
                WHERE LOWER(group_name) = 'meat group a'
            """)
            rows = cursor.fetchall()
            for row in rows:
                ing_name = row[0]
                if get_animal_keyword(ing_name) == animal and ing_name not in used_ingredient_names:
                    fallback_meat_a.append({
                        "ingredient": ing_name,
                        "group": row[1].strip().lower(),
                        "data": row[2:]
                    })

        conn.close()
        meat_used += distribute_exact(fallback_meat_a, 150)

    elif meat_a and not meat_b and not meat_c:
        fat_avg = average_fat(meat_a)
        if fat_avg < 12:
            meat_used += distribute_exact(meat_a, 150)
            supplement = sorted([r for r in meat_b + meat_c if r["ingredient"] not in used_ingredient_names], key=lambda x: -x["data"][1])
            meat_used += distribute_exact(supplement, MEAT_MIN - meat_used)
        else:
            meat_used += distribute_exact(meat_a, MEAT_MAX)
    elif meat_c and not meat_a and not meat_b:
        if average_fat(meat_c) > 16:
            meat_used += distribute_exact(meat_c, 200)
            fallback = [r for r in ingredient_rows if r["group"] == "meat group a" and r["ingredient"] not in used_ingredient_names]
            meat_used += distribute_exact(fallback, 100)
        else:
            meat_used += distribute_exact(meat_c, MEAT_MAX)
    else:
        meat_used += distribute_exact(all_meats, MEAT_MAX)

    remaining_dm = FIXED_TOTAL_DM - FIXED_DM_USED - meat_used

    total_dm_used = sum([item["dm_g"] for item in dm_breakdown])
    scaling_needed = FIXED_TOTAL_DM - total_dm_used
    non_fixed = [item for item in ingredient_totals if not item["fixed"]]
    non_fixed_total = sum(item["dm_g"] for item in non_fixed)
    if non_fixed_total > 0 and abs(scaling_needed) >= 0.1:
        scale_factor = (non_fixed_total + scaling_needed) / non_fixed_total
        for item in ingredient_totals:
            if not item["fixed"]:
                old_dm = item["dm_g"]
                new_dm = round(old_dm * scale_factor, 2)
                for nutrient in ["protein_g", "fat_g", "cho_g", "fiber_g", "ash_g", "ca_mg", "p_mg", "iron_mg", "energy_kcal"]:
                    item[nutrient] = round(item[nutrient] * scale_factor, 2)
                item["dm_g"] = new_dm
                for db in dm_breakdown:
                    if db["ingredient"] == item["ingredient"] and not db["fixed"]:
                        db["dm_g"] = new_dm
                        break

    total = {k: 0 for k in total}
    for item in ingredient_totals:
        dm = item["dm_g"]
        total["Protein"] += item["protein_g"]
        total["Fat"] += item["fat_g"]
        total["CHO"] += item["cho_g"]
        total["Fiber"] += item["fiber_g"]
        total["Ash"] += item["ash_g"]
        total["Ca"] += item["ca_mg"] / 1000
        total["P"] += item["p_mg"] / 1000
        total["Iron"] += item["iron_mg"] / 100
        total["Energy"] += item["energy_kcal"]

    if total["Protein"] * 100 / FIXED_TOTAL_DM < PROTEIN_MIN_PERCENT:
        needed_protein_g = (PROTEIN_MIN_PERCENT * FIXED_TOTAL_DM / 100) - total["Protein"]
        boost_meats = sorted(
            [r for r in ingredient_rows if r["group"] in ["meat group a", "meat group b", "meat group c"] and r["ingredient"] not in used_ingredient_names],
            key=lambda x: -x["data"][0]
        )
        for r in boost_meats:
            protein_per_g = r["data"][0] / 100
            if protein_per_g > 0:
                dm_needed = min(remaining_dm, round(needed_protein_g / protein_per_g, 2))
                added_dm = distribute_exact([r], dm_needed)
                remaining_dm -= added_dm
                total["Protein"] += added_dm * protein_per_g
                if total["Protein"] * 100 / FIXED_TOTAL_DM >= PROTEIN_MIN_PERCENT:
                    break



    def recalculate_totals():
        totals = {
            "Protein": 0,
            "Fat": 0,
            "CHO": 0,
            "Fiber": 0,
            "Ash": 0,
            "Ca": 0,
            "P": 0,
            "Iron": 0,
            "Energy": 0
        }
        for item in ingredient_totals:
            totals["Protein"] += item["protein_g"]
            totals["Fat"] += item["fat_g"]
            totals["CHO"] += item["cho_g"]
            totals["Fiber"] += item["fiber_g"]
            totals["Ash"] += item["ash_g"]
            totals["Ca"] += item["ca_mg"] / 1000
            totals["P"] += item["p_mg"] / 1000
            totals["Iron"] += item["iron_mg"] / 100
            totals["Energy"] += item["energy_kcal"]
        return totals

    # ---- HELPER: Adjust vegetables up/down by percent ----
    def adjust_vegetables_by_percent(percent_change):
        for item in ingredient_totals:
            name = item["ingredient"].lower()
            if name in used_ingredient_names and any(veg in name for veg in ["carrot", "spinach", "broccoli", "pumpkin", "zucchini"]):
                old_dm = item["dm_g"]
                new_dm = round(old_dm * (1 + percent_change / 100), 2)
                scale = new_dm / old_dm if old_dm else 1

                item["dm_g"] = new_dm
                for nutrient in ["protein_g", "fat_g", "cho_g", "fiber_g", "ash_g", "ca_mg", "p_mg", "iron_mg", "energy_kcal"]:
                    item[nutrient] = round(item[nutrient] * scale, 2)

                for db in dm_breakdown:
                    if db["ingredient"] == item["ingredient"] and not db.get("fixed", False):
                        db["dm_g"] = new_dm
                        break

    total = recalculate_totals()
    fiber_percent = total["Fiber"] * 100 / FIXED_TOTAL_DM

    # If fiber is too low, first try increasing veggies
    if fiber_percent < 3:
        adjust_vegetables_by_percent(10)
        total = recalculate_totals()
        fiber_percent = total["Fiber"] * 100 / FIXED_TOTAL_DM

        if fiber_percent < 3:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ingredient_name, group_name, protein_g, fat_g, cho_g, fiber_g, ash_g, calcium_mg, phosphorus_mg, iron_mg, energy_kcal
                FROM user_ingredients
                WHERE LOWER(ingredient_name) IN ('psyllium husk', 'rice bran')
            """)
            fiber_boosters = cursor.fetchall()
            conn.close()

            for row in fiber_boosters:
                if fiber_percent >= 4.5:
                    break
                name, group, *data = row
                fiber_per_dm = data[3] / 100
                if fiber_per_dm > 0:
                    max_allowed_dm = min((4.5 - fiber_percent) * FIXED_TOTAL_DM / 100, 30)
                    dm_to_add = min(remaining_dm, max_allowed_dm)
                    added_dm = distribute_exact([{"ingredient": name, "group": group, "data": data}], dm_to_add)
                    remaining_dm -= added_dm
                    used_ingredient_names.add(name)
                    total = recalculate_totals()
                    fiber_percent = total["Fiber"] * 100 / FIXED_TOTAL_DM
    # If fiber is too high, reduce veggies gradually (with max 5 attempts)
    elif fiber_percent > 7:
        attempts = 0
        previous_percent = fiber_percent

        while fiber_percent > 6 and attempts < 5:
            adjust_vegetables_by_percent(-10)
            total = recalculate_totals()
            fiber_percent = total["Fiber"] * 100 / FIXED_TOTAL_DM

        # If percent doesn't change, break to avoid infinite loop
            if abs(fiber_percent - previous_percent) < 0.01:
                issues.append(f"Fiber reduction not effective after attempt {attempts+1}. Current: {fiber_percent:.2f}%")
                break

            previous_percent = fiber_percent
            attempts += 1

        if fiber_percent > 6:
            issues.append(f"Fiber remains high ({fiber_percent:.2f}%) after {attempts} attempts to reduce it.")


    
    

    result = {
        "Protein_percent": round(total["Protein"] * 100 / FIXED_TOTAL_DM, 2),
        "Fat_percent": round(total["Fat"] * 100 / FIXED_TOTAL_DM, 2),
        "CHO_percent": round(total["CHO"] * 100 / FIXED_TOTAL_DM, 2),
        "Fiber_percent": round(total["Fiber"] * 100 / FIXED_TOTAL_DM, 2),
        "Ash_percent": round(total["Ash"] * 100 / FIXED_TOTAL_DM, 2),
        "Ca_percent": round(total["Ca"] * 100 / FIXED_TOTAL_DM, 2),
        "P_percent": round(total["P"] * 100 / FIXED_TOTAL_DM, 2),
        "Ca_P_ratio": round(total["Ca"] / total["P"], 2) if total["P"] else 0,
        "Energy": round(total["Energy"], 2),
        "DM_percent": round(FIXED_TOTAL_DM, 2)
    }

    return {
        "nutrient_percentages": result,
        "dm_breakdown": dm_breakdown,
        "ingredient_totals": ingredient_totals,
        "issues": issues,
        "auto_added": None
    }

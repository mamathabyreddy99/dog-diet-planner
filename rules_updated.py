def apply_all_rules(fixed_rows, ingredient_rows, categories, fixed_total_dm, used_dm, get_nutrient_values, add_to_total):
    FIXED_TOTAL_DM = 1000
    dm_breakdown = []
    total = {"Protein": 0, "Fat": 0, "CHO": 0, "Fiber": 0, "Ash": 0, "Ca": 0, "Iron": 0, "Energy": 0}

    def add(name, dm, fixed=False):
        values = get_nutrient_values(name, fixed)
        add_to_total(values, dm)
        dm_breakdown.append({"ingredient": name, "dm_g": round(dm, 2), "fixed": fixed})

    remaining_dm = FIXED_TOTAL_DM - fixed_total_dm

    # ➤ Organ meat rule
    liver_row = next((r for r in categories['organ_meat'] if "liver" in r["ingredient"].lower()), None)
    other_organ = [r for r in categories['organ_meat'] if r != liver_row]
    if liver_row:
        liver_dm = min(0.13 * FIXED_TOTAL_DM, remaining_dm)
        add(liver_row["ingredient"], liver_dm)
        remaining_dm -= liver_dm
    if other_organ:
        organ_limit = 0.15 * FIXED_TOTAL_DM
        remaining_organ_dm = min(organ_limit - (0.13 * FIXED_TOTAL_DM if liver_row else 0), remaining_dm)
        per = remaining_organ_dm / len(other_organ)
        for r in other_organ:
            add(r[0], per)
            remaining_dm -= per

    # ➤ Meat (max 350g)
    meats = categories['group_a'] + categories['group_b'] + categories['group_c']
    meat_dm = min(0.35 * FIXED_TOTAL_DM, remaining_dm)
    if meats:
        per = meat_dm / len(meats)
        for r in meats:
           add(r[0], per)
        remaining_dm -= meat_dm

    # ➤ Grains (max 400g)
    grains = categories['grains_a'] + categories['grains_b'] + categories['grains_c']
    grain_dm = min(0.4 * FIXED_TOTAL_DM, remaining_dm)
    if grains:
        per = grain_dm / len(grains)
        for r in grains:
            add(r[0], per)
        remaining_dm -= grain_dm

    # ➤ Oils (max 30g)
    oils = categories['oils']
    if oils:
        fat_pct = lambda: total['Fat'] * 100 / (fixed_total_dm + (FIXED_TOTAL_DM - remaining_dm))
        oil_dm = 10
        if fat_pct() < 12:
            extra = min(30, remaining_dm)
            per = extra / len(oils)
            for r in oils:
                add(r[0], per)
            remaining_dm -= extra

    # ➤ Vegetables (max 150g)
    vegetables = categories['vegetables_a'] + categories['vegetables_b']
    if vegetables:
        veg_dm = min(0.15 * FIXED_TOTAL_DM, remaining_dm)
        per = veg_dm / len(vegetables)
        for r in vegetables:
            add(r[0], per)
        remaining_dm -= veg_dm

    # ➤ Fruits (max 20g)
    fruits = categories['fruits']
    if fruits:
        fruit_dm = min(0.02 * FIXED_TOTAL_DM, remaining_dm)
        per = fruit_dm / len(fruits)
        for r in fruits:
            add(r[0], per)
        remaining_dm -= fruit_dm

    # ➤ Nutrient result summary
    result = {
        "Protein_percent": round(total["Protein"] * 100 / FIXED_TOTAL_DM, 2),
        "Fat_percent": round(total["Fat"] * 100 / FIXED_TOTAL_DM, 2),
        "CHO_percent": round(total["CHO"] * 100 / FIXED_TOTAL_DM, 2),
        "Fiber_percent": round(total["Fiber"] * 100 / FIXED_TOTAL_DM, 2),
        "Ash_percent": round(total["Ash"] * 100 / FIXED_TOTAL_DM, 2),
        "Ca_percent": round(total["Ca"] * 100, 2),
        "Iron_mg": round(total["Iron"], 2),
        "Energy": round(total["Energy"], 2),
        "DM_percent": round(FIXED_TOTAL_DM * 100 / 3740, 2),
        "Protein_g": round(total["Protein"], 2),
        "Fat_g": round(total["Fat"], 2),
        "CHO_g": round(total["CHO"], 2),
        "Fiber_g": round(total["Fiber"], 2),
        "Total_DM_Used": round(FIXED_TOTAL_DM, 2)
    }

    ingredient_totals = []
    for entry in dm_breakdown:
        values = get_nutrient_values(entry["ingredient"].replace(" (extra)", ""), entry["fixed"])
        ingredient_totals.append({
            "ingredient": entry["ingredient"],
            "dm_g": entry["dm_g"],
            "protein_g": round((values[0] / 100) * entry["dm_g"], 2),
            "fat_g": round((values[1] / 100) * entry["dm_g"], 2),
            "cho_g": round((values[2] / 100) * entry["dm_g"], 2),
            "fiber_g": round((values[3] / 100) * entry["dm_g"], 2),
            "ash_g": round((values[4] / 100) * entry["dm_g"], 2),
            "ca_mg": round((values[5] / 1000) * entry["dm_g"], 2),
            "iron_mg": round((values[6] / 100) * entry["dm_g"], 2),
            "energy_kcal": round((values[7] / 100) * entry["dm_g"], 2),
            "fixed": entry["fixed"]
        })

    return result, dm_breakdown, ingredient_totals

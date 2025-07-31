def adjust_meat_rules(ingredients):
    group_a = [i for i in ingredients if i['group_name'] == 'Meat Group A']
    group_b = [i for i in ingredients if i['group_name'] == 'Meat Group B']
    group_c = [i for i in ingredients if i['group_name'] == 'Meat Group C']

    total_meat_dm = sum(i['dm_g'] for i in group_a + group_b + group_c)
    total_diet_dm = 1000  # always total
    meat_percent = (total_meat_dm / total_diet_dm) * 100

    if meat_percent < 20:
        add = 20 - meat_percent
        if group_a:
            group_a[0]['dm_g'] += add
        elif group_b:
            group_b[0]['dm_g'] += add
        elif group_c:
            group_c[0]['dm_g'] += add
    elif meat_percent > 35:
        reduce = meat_percent - 35
        if group_c:
            group_c[0]['dm_g'] -= reduce
        elif group_b:
            group_b[0]['dm_g'] -= reduce
        elif group_a:
            group_a[0]['dm_g'] -= reduce

    for i in group_b:
        if i['fat_g'] > 30:
            for j in group_a:
                j['dm_g'] = min(j['dm_g'], 0.15 * total_diet_dm)

    for i in group_c:
        if i['fat_g'] > 16:
            for a in group_a:
                move_amt = min(10, i['dm_g'])
                a['dm_g'] += move_amt
                i['dm_g'] -= move_amt

    for a in group_a:
        if a['fat_g'] < 12:
            for x in group_b + group_c:
                move_amt = min(5, a['dm_g'])
                a['dm_g'] -= move_amt
                x['dm_g'] += move_amt

    return group_a + group_b + group_c

def adjust_organ_meat_rules(ingredients):
    organ = [i for i in ingredients if i['group_name'] == 'Organ Meat']
    total_dm = 1000
    total_organ_dm = sum(i['dm_g'] for i in organ)
    if total_organ_dm < 0.12 * total_dm:
        organ[0]['dm_g'] += (0.12 * total_dm - total_organ_dm)
    elif total_organ_dm > 0.15 * total_dm:
        organ[0]['dm_g'] -= (total_organ_dm - 0.15 * total_dm)
    return organ

def adjust_grain_rules(ingredients):
    return [i for i in ingredients if 'Grain' in i['group_name']]

def adjust_vegetable_rules(ingredients):
    return [i for i in ingredients if 'Vegetable' in i['group_name']]

def adjust_oil_rules(ingredients):
    return [i for i in ingredients if i['group_name'] == 'Oil']

def adjust_fruit_rules(ingredients):
    return [i for i in ingredients if i['group_name'] == 'Fruit']

def validate_final_nutrients(user_ingredients, fixed_ingredients):
    all_ings = user_ingredients + fixed_ingredients
    total_dm = sum(i['dm_g'] for i in all_ings)

    protein = sum((i.get('protein_g', 0) or 0) * i['dm_g'] / 100 for i in all_ings)
    fat = sum((i.get('fat_g', 0) or 0) * i['dm_g'] / 100 for i in all_ings)
    fiber = sum((i.get('fiber_g', 0) or 0) * i['dm_g'] / 100 for i in all_ings)
    ash = sum((i.get('ash_g', 0) or 0) * i['dm_g'] / 100 for i in all_ings)
    ca = sum((i.get('calcium_mg', 0) or 0) * i['dm_g'] / 100000 for i in all_ings)
    iron = sum((i.get('iron_mg', 0) or 0) * i['dm_g'] / 100 for i in all_ings)
    energy = sum((i.get('energy_kcal', 0) or 0) * i['dm_g'] / 100 for i in all_ings)

    nutrients = {
        'Protein %': round((protein / total_dm) * 100, 2),
        'Fat %': round((fat / total_dm) * 100, 2),
        'Fiber %': round((fiber / total_dm) * 100, 2),
        'Ash %': round((ash / total_dm) * 100, 2),
        'Ca %': round(ca * 100, 2),
        'Iron (mg)': round(iron, 2),
        'Energy': round(energy, 2)
    }

    return nutrients, []

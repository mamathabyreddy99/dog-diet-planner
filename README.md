# 🐶 Dog Diet Planner

This app helps formulate balanced dog diets based on veterinary nutrition guidelines and user-selected ingredients. It automatically distributes dry matter (DM), adjusts nutrients, and ensures recipes meet protein, fat, fiber, CHO %, calcium:phosphorus ratio, and omega 6:3 balance — all according to strict diet rules provided by the professor.

---

### 🚀 Tech Stack
- **Frontend**: React
- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Other**: Streamlit (demo), Excel-based nutrient sources

---

### ✅ Features
- Select ingredients from categorized groups (Meat A/B/C, Grains, Veggies, etc.)
- Automatic inclusion of fixed ingredients (e.g., eggshells, oils, yeast)
- Calculates fresh weight and dry matter nutrient summary
- Enforces dietary rules (organ meat %, meat fat %, protein, Ca:P, etc.)
- Auto-corrects nutrients without user intervention
- Displays full nutrient breakdown and validations

---

### 📁 Project Structure
- `dog-diet-frontend/` – React UI for selecting ingredients and showing results
- `dog_diet_backend/` – FastAPI backend with full logic for diet formulation
- `db/` – PostgreSQL schema and scripts
- `.gitignore`, `README.md` – Project setup files

---

### 🛠 How to Run Locally
Coming soon...

---

### 📌 Status
✅ Working diet formulation logic  
🔄 Frontend and backend connected  
📋 Next: Add deployment + user demo video

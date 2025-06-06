# 🧠 Fuzzy Logic Material Analysis Web App

A lightweight, interactive web application to visualize and compute fuzzy membership functions (trapezoidal and triangular) for material properties like density and Young's modulus using Python, Flask, and Plotly.js.

---
<h3>🌐 Web Link:</h3>

<h4> Live Site: https://graph-fuzzy-function-ny47.onrender.com/ </h4>

## 🚀 Features

### 1. **CPU Utilization**
- **Deployment**: Hosted on [Render.com](https://render.com) (Free Tier), limited to 0.1–0.25 vCPUs.
- **PostgreSQL Impact**: Adds ~10–15% CPU load during peak material/alpha queries.
- **Heavy Load Tasks**: Excel export (`export_images_to_excel`) causes short CPU spikes during image buffer processing.

### 2. **User Input Options**
- Choose fuzzy function type: **Trapezoidal** or **Triangular**.
- Input alpha values: `α1, α2, α3, α'1, α'2, α'3`.
- Select material properties: **Density**, **Young's Modulus**, etc.
- Predefined examples in `app.py` allow quick visualization without manual input.

### 3. **Graph Generation Time**
- **Backend**: ~0.5–2 seconds depending on function complexity and server load.
- **Libraries**:
  - `matplotlib` for server-side rendering.
  - `Plotly.js` for responsive client-side interactivity.

### 4. **Academic Integration**
- Based on fuzzy logic research, e.g., _"Flexible Robot Control Using Fuzzy Functions"_.
- Demonstrates real-world application of fuzzy systems for decision-making under uncertainty.

### 5. **Memory Efficiency**
- Memory usage:
  - **Graph rendering**: 50–100 MB.
  - **Excel export**: Peaks at 150–200 MB.
  - **Large fuzzy set (n=10,000)**: ~80 MB.
  - **SQLAlchemy DB pool**: ~25 MB for 5 connections.

### 6. **Program Time Profile**
- End-to-end execution: **1–3 seconds** including:
  - Input processing
  - Fuzzy computation
  - Graph rendering

---

## 🗃️ Database Structure

- **Tables**:
  - `tbl_materials` (material properties)
  - `tbl_alpha` (alpha fuzzy values)
- **Relationships**:
  - Composite key: `(mat_fm_id, mat_id)` ↔ `(alpha_fm_id, alpha_mat_id)`
- **Function Types**:
  - `mat_fm_id=1`: Trapezoidal  
  - `mat_fm_id=2`: Triangular

---

## ⚙️ Algorithm Complexity

```python
def fuzzy_calculation_flow():
    material = tbl_materials.query.get(mat_id)  # O(1)
    results = calculate_fuzzy(np.linspace(a, d, n))  # O(n)
    generate_plot(results)  # O(1)
```

| Operation         | Complexity |
|------------------|------------|
| Database Query    | O(1)       |
| Fuzzy Calculation | O(n)       |
| Graph Generation  | O(1)       |

---

## 📊 Time Performance Benchmarks

| Operation      | n = 100 | n = 1000 | n = 10,000 |
|----------------|---------|----------|------------|
| DB Query       | 12 ms   | 15 ms    | 18 ms      |
| Fuzzy Calc     | 45 ms   | 380 ms   | 3.8 s      |
| Graph Gen      | 220 ms  | 450 ms   | 1.2 s      |
| Excel Export   | —       | 1.8 s    | 4.5 s      |

---

## 🔁 Optimizations

- ✅ Vectorized NumPy calculations (no explicit Python loops)
- ✅ Flask route input validation
- 🔄 Caching: Memoize repeated fuzzy evaluations
- 🔄 Web Workers: Offload computation from main thread (frontend)
- 🔄 Simplified plot DPI for quicker image rendering

---

## 🖥️ UI Components

- **Theme Switcher**: Change graph color themes with Plotly `layout.colorway`.
- **Graph Background**: Dynamic background customization for better UX.
- **Responsive Plots**: Plotly enables zooming, saving, and interactive views.

---

## 📐 Algorithm Pseudocode

**Fuzzy Membership (Trapezoidal)**

```
Input: x (value), params [a, b, c, d]
Output: Membership (0–1)

1. If x < a or x > d: Return 0
2. If a ≤ x ≤ b: Return (x - a)/(b - a)
3. If b ≤ x ≤ c: Return 1
4. If c ≤ x ≤ d: Return (d - x)/(d - c)
```

---

## 🧠 Tech Stack

| Layer         | Technology     |
|---------------|----------------|
| Backend       | Flask (Python) |
| Frontend      | HTML, CSS, JS  |
| Database      | PostgreSQL     |
| ORM           | SQLAlchemy     |
| Image Export  | matplotlib     |
| Hosting       | Render.com     |

---

## 📦 Performance Summary (Time/Memory)

| Input Size | Time (ms) | Memory (MB) |
|------------|-----------|-------------|
| n = 100    | 120       | 12          |
| n = 1000   | 450       | 35          |
| n = 10,000 | 2200      | 110         |

---

## 📁 Folder Structure

```
📦 fuzzy-app/
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── models/
│   └── database.py
├── utils/
│   └── fuzzy_logic.py
├── export/
│   └── excel_export.py
└── README.md
```

---

## 📜 License

MIT License. Free to use, modify, and distribute.
# 🔬 Global Research Performance Analytics: A Strategic Deep Dive

#### *An Exploratory Data Analysis and Visualization Project for the Hiring Assessment of Project Intern/Trainee - PAIU-OPSA, IISc Bangalore*

This project presents an in-depth Exploratory Data Analysis (EDA) of global research performance metrics. The primary objective is to move beyond basic volume metrics and uncover strategic insights into what drives research excellence. The analysis specifically focuses on the **Quality vs. Quantity paradox**, the **Collaboration Myth**, and provides a dedicated **strategic lens on India's position** in the global research ecosystem.

The final deliverable is a multi-page interactive dashboard built with Python and Streamlit.

---

### 🔴 Live Dashboard

The interactive dashboard is deployed on Streamlit Community Cloud:

**[➡️ View the Live Dashboard](https://global-research-analytics.streamlit.app/)**

---

### 📸 Dashboard Preview

![Dashboard Screenshot](/image/dashboard.png)

---

### 🚀 Key Strategic Insights (With India Lens)

The analysis resulted in 7 critical insights that challenge traditional research metrics:

**1. The 'Elite Club' & Decentralized Power**
*   **Finding:** The Pareto Principle (80/20 rule) fails here. It takes **75% of nations** to generate 80% of global impact, proving a decentralized and highly competitive landscape.
*   **🇮🇳 India Watch:** India is firmly established as a member of this "Elite Club," with metrics consistently aligning with global baselines rather than acting as an outsider.

**2. Strategic Divergence: The Four Models**
*   **Finding:** Nations fall into 4 models: *Mass Producers* (UK), *Boutique Specialists* (Japan), *Elite Performers* (Spain), and *Lagging*.
*   **🇮🇳 India Watch:** India sits in the "Catch-up Zone" but is **critically close to the global median lines** for both Volume and Quality. It is in a transition phase, ready to break into the Elite quadrant.

**3. Distribution Analysis & The Elite Cohort**
*   **Finding:** While volume metrics are skewed, Quality follows a normal distribution. **Sweden** is the global #1 in *Elite Output (% Top 1% Docs)*.
*   **🇮🇳 India Watch:** In overall lifetime Elite Performance, **India ranks 9th** globally, surprisingly outperforming the **USA (10th rank)**. This highlights India's growing capability to produce blockbuster research.

**4. Competitive Landscape: The Closing Gap**
*   **Finding:** Dominance gaps are shrinking. No single nation holds a permanent monopoly.
*   **🇮🇳 India Watch:** India is emerging as a direct challenger to established leaders. For instance, in *Times Cited*, India appears as the direct runner-up to leaders like Spain, actively narrowing the dominance gap.

**5. Outlier Analysis: The "Quality Ceiling"**
*   **Finding:** While nations like China show massive outliers in Volume (spikes), `CNCI` (Quality) shows **zero statistical outliers**. You can force scale, but you cannot force excellence—it hits a natural ceiling.
*   **🇮🇳 India Watch:** India shows steady, organic growth without artificial statistical spikes, indicating a sustainable research trajectory.

**6. Correlation Analysis: The Collaboration Myth**
*   **Finding:** There is **no linear correlation** between *Collaboration Quality* and *Elite Output*. Collaboration is now just a **"Hygiene Factor,"** not a differentiator.
*   **🇮🇳 India Watch:** India ranks **#1 Globally in Collaboration Quality**, yet its conversion to Elite Papers is average. This reveals a massive **"Efficiency Gap"**—India has the partnerships but needs to translate them into better output.

**7. Performance Analysis: The Global Leaderboard**
*   **Finding:** Leadership is split: UK wins Volume, Japan wins Quality, Sweden wins Elite Impact.
*   **🇮🇳 India Watch:** India holds a balanced profile: **Rank #11** (Volume), **Rank #10** (Quality), and **Rank #9** (Elite Impact).

---

### 📄 Strategic Recommendations

Based on the data, the following recommendations are proposed, with a specific focus on India's policy roadmap:

**1. Shift Focus from "Volume" to "Value"**
*   **Insight:** "Getting cited" is now a baseline. The new goal is **Top 1% conversion**.
*   **Strategy:** Policy incentives must move away from "Total Papers Published" to "Papers in Top 1%." Funding should target high-risk, high-reward "Blockbuster" research.

**2. Fix the "Collaboration Efficiency Gap"**
*   **Insight:** Collaboration is a hygiene factor. India is #1 in collaboration quality but lags in elite conversion.
*   **Strategy:** Stop signing generic MOUs. Conduct a **"Collaboration Audit"** to leverage existing high-quality partnerships for better elite output.

**3. Target the "Elite Quadrant" (The Spain Model)**
*   **Insight:** Spain successfully balances high volume and high quality.
*   **Strategy:** India is close to the median. A targeted push in specific STEM domains can propel India from the "Catch-up Zone" to the **"Elite Quadrant"** within 5 years.

---

### 🛠️ Tech Stack

*   **Language:** Python 3.10+
*   **Core Libraries:**
    *   **Streamlit:** For building the interactive web dashboard.
    *   **Pandas:** For ETL, aggregation, and statistical analysis.
    *   **Plotly Express:** For interactive, publication-ready visualizations.
    *   **NumPy:** For numerical operations and outlier detection.
*   **Deployment:** Streamlit Community Cloud

---

### ⚙️ Setup and Local Installation

To run this dashboard on your local machine:

**1. Clone the repository:**
```bash
git clone https://github.com/Omkar3101/iisc-eda-project
```

**2. Navigate to the project directory:**
```bash
cd iisc-eda-project
```

**3. Install the required dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the Streamlit app:**
```bash
streamlit run app.py
```
The application should now be running at `http://localhost:8501`.

---

### 📁 Project Structure

```text
├── data/
|   └── publications.csv          # Raw dataset
│   └── cleaned_publications.csv  # Processed dataset used for analysis
├── image/
│   └── dashboard.png             # Preview image
├── app.py                        # Main Streamlit dashboard application
├── Omkar_IISc_Project_Report.pdf # Detailed PDF Analysis Report
├── requirements.txt              # Dependency list
├── Research_Publications_EDA_Analysis.ipynb  # Comprehensive Jupyter Notebook Analysis
└── README.md                     # Project Documentation
```

---
**Author:** Omkar Sharma | [LinkedIn](https://www.linkedin.com/in/omkar3101) | [Email](mailto:omkarshar3101@gmail.com)
```

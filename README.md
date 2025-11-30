# Global Research Performance Analytics Dashboard & Exploratory Data Analysis: Research Publications

#### *An Exploratory Data Analysis and Visualization Project for the Project Intern/Trainee Hiring Assessment - PAIU-OPSA, IISc Bangalore*

This project presents an in-depth Exploratory Data Analysis (EDA) of global research performance metrics, sourced from Web of Science/InCites data. The primary objective is to move beyond basic metrics and uncover strategic insights into what drives research excellence and leadership on a global scale. The final deliverable is a multi-page interactive dashboard built with Python and Streamlit.

---

### 🔴 Live Dashboard

The interactive dashboard is deployed on Streamlit Community Cloud and can be accessed here:

**[➡️ View the Live Dashboard](https://global-research-analytics.streamlit.app/)**

---

### 📸 Dashboard Preview

![Dashboard Screenshot](images/dashboard.png)

---

### 🚀 Key Insights & Features

The dashboard is structured around 7 key strategic insights derived from the data:

1.  **Overview & Key Findings:** Establishes that the dataset consists of an "Elite Club" of high-performing nations where research impact is highly decentralized, inverting the 80/20 Pareto Principle.
2.  **Strategic Positioning:** Segments nations into four distinct strategic quadrants ("Mass Producers," "Boutique Specialists," "Consistent Elite," and "Lagging") based on their research volume versus quality.
3.  **Quality Spectrum:** Analyzes the full spectrum of research impact, from the baseline (`% Docs Cited`) to the ceiling of excellence (`% Docs in Top 1%`), revealing that the true differentiator is producing "Blockbuster" research.
4.  **Competitive Landscape:** A time-series analysis of the "Dominance Gap" between the #1 and #2 performers, showing how market leadership and competition have evolved.
5.  **Outlier Analysis:** Reveals the "Quality Ceiling" phenomenon—proving that while research volume can be scaled exponentially, research quality remains within a predictable, non-scalable range.
6.  **Correlation Analysis:** Contrasts the weak, non-existent link between Collaboration and Quality against the near-perfect correlation between Publication Volume and Total Citations.
7.  **Performance Trends:** An interactive module to compare selected nations over time across both volume and quality metrics, highlighting the rise of new challengers like Brazil and the consistent quality of leaders like Spain.

---

### 🛠️ Tech Stack

*   **Language:** Python 3.10+
*   **Core Libraries:**
    *   **Streamlit:** For building the interactive web dashboard.
    *   **Pandas:** For data manipulation and analysis.
    *   **Plotly Express & Graph Objects:** For creating rich, interactive visualizations.
    *   **NumPy:** For numerical operations.
*   **Deployment:** Streamlit Community Cloud

---

### ⚙️ Setup and Local Installation

To run this dashboard on your local machine, please follow these steps:

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
The application should now be running and accessible in your web browser at `http://localhost:8501`.

---

### 📁 Project Structure

```

├── data/
|   └── publications.csv # Initial dataset
│   └── cleaned_publications.csv # cleaned dataset used for analysis
├── image/
│   └── dashboard.png # The dataset used for analysis
├── app.py                    # The main Streamlit dashboard application script
├── Omkar_IISc_Project_Report.pdf # PDF report
├── requirements.txt          # Required Python libraries for deployment
├── Research_Publications_EDA_Analysis.ipynb  # The main EDA Analysis Jupyter Notebook
└── README.md                 # You are here!
```

---

### 📄 Final Recommendations (Summary)

The analysis concludes that success in the modern research landscape requires a strategic shift:

*   **From Volume to Value:** Prioritize increasing the conversion rate to **Top 1% "Blockbuster" papers** over simply increasing total publication counts.
*   **Audit Collaborations:** Treat high-quality collaboration as a **"hygiene factor,"** not a competitive advantage. Focus on the tangible impact of partnerships.
*   **Embrace the "Quality Ceiling":** Acknowledge that quality cannot be brute-forced with volume. Foster a research culture that rewards groundbreaking impact over incremental output.

This project demonstrates a comprehensive approach to data analysis—from initial exploration and insight generation to the development of an interactive, user-friendly dashboard that delivers actionable strategic recommendations.
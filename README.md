Sales-Forecasting-Dashboard
Sales Forecasting Dashboard (Streamlit, Pandas, Plotly, Matplotlib) — An interactive dashboard for exploring sales trends, forecasting with Holt-Winters models, and visualizing results in real time. Built with Python for data science, full-stack deployment via Streamlit.

An interactive **Sales Forecasting Dashboard** built with **Python**, **Pandas**, **Matplotlib**, and **Plotly**, deployed using **Streamlit**.  
This project is designed for recruiters, hiring managers, and collaborators to quickly see my ability to integrate **data science**, **web development**, and **interactive dashboards**.

---

## 🚀 Features
- Upload your own **CSV sales data** or use the included **sample dataset**.
- Automatic **data cleaning** and **monthly aggregation** with pandas.
- **Forecasting models** with Holt-Winters Exponential Smoothing (statsmodels).
- Interactive **Plotly charts** and static **Matplotlib plots**.
- Downloadable forecast results as **CSV**.
- Deployed easily to **Streamlit Cloud** for live demos.

---

## 🛠 Tech Stack
- **Backend / Data Science:** Python, Pandas, NumPy, Statsmodels, Scikit-learn
- **Visualization:** Matplotlib, Plotly
- **Frontend & Deployment:** Streamlit
- **Version Control:** GitHub

---

## 📂 Project Structure

📁 Sales_Forecasting_Dashboard
│── app.py # Streamlit app
│── utils.py # Data handling, forecasting, metrics
│── generate_sample_data.py # Script to generate sample dataset
│── sample_sales.csv # Example dataset
│── requirements.txt # Dependencies
│── README.md # Documentation



---

## ⚡ Quick Start

1. Clone the repo:
   
   git clone git@github.com:KingsleyOdume/Sales-Forecasting-Dashboard.git
   cd Sales_Forecasting_Dashboard

Create & activate a virtual environment:
python -m venv env
source env/bin/activate   # macOS/Linux
# env\Scripts\activate    # Windows

Install dependencies:
pip install -r requirements.txt

Generate sample dataset:
python generate_sample_data.py

Run the Streamlit app:
streamlit run app.py

🌐 Live Demo
👉 Click here to try it on [Streamlit cloud](https://sales-forecasting-dashboard-da9cp4w4uxte3mv9vnbre6.streamlit.app)


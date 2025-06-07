# 📑 Data Cleaner

An intuitive Streamlit-based web app that allows users to upload CSV or Excel files, perform basic data cleaning operations like removing duplicates and filling missing values, and preview their data in a user-friendly interface.

---

## 🚀 Features

- 📂 Upload multiple files (CSV or Excel)
- 🧹 Remove duplicate rows
- 📉 Fill missing values with column-wise mean (for numeric columns)
- 🔍 Preview file metadata and the first few rows
- 🧮 Automatic type detection and summary

---

## 🧑‍💻 Installation

Make sure you have Python 3.7 or higher installed.

### 1. Clone the Repository

```bash
git clone https://github.com/amansuren/python-mini-projects.git
cd python-mini-projects
```
### 2. Install Dependencies
```
pip install -r requirements.txt
```
### 3. Browse and locate the folder
```
cd datacleaner_app
```
### 4. Run the app
```
streamlit run datacleaner.py
```
Then open http://localhost:8501 in your browser.

🧠 Future Improvements
- Download cleaned file in .xlsx format
- Visualize missing data
- Add outlier detection
- Export summary reports

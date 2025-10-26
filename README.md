# Gategroup - Gate Alcohol Checker (HackMTY 2025)

A functional prototype of an automated system to inspect and classify liquor bottles returned from airline catering. This tool uses visual AI (Gemini) and business logic to make instant decisions on whether a bottle should be **kept**, **refilled**, **replaced**, or **discarded**.

-----

## 🚀 Key Features

  * **Multi-Step Interface:** A clean GUI (built with Streamlit) that guides the operator through the process.
  * **Authentication:** Secure login screen connected to a MySQL database.
  * **AI Vision Analysis:** Uses the Google Gemini API to analyze a photo of the bottle and determine:
      * Seal Status (`sealStatus`)
      * Label Status (`labelStatus`)
      * Cleanliness Level (`cleanliness`)
  * **Precise Content Calculation:** Simulates a scale and cross-references the weight with a database to get the exact remaining liquid percentage.
  * **Dynamic Decision Engine:** A module in `main.py` applies complex business rules based on each airline's policy to decide the final action (`KEEP`, `REFILL`, `REPLACE`, `DISCARD`).

-----

## 🛠️ Tech Stack

  * **Frontend:** [Streamlit](https://streamlit.io/)
  * **Backend & Logic:** Python
  * **AI Vision Analysis:** [Google Gemini (gemini-2.5-flash)](https://deepmind.google/technologies/gemini/)
  * **Database:** MySQL
  * **Main Libraries:** `google-generativeai`, `mysql-connector-python`, `pillow`, `streamlit`

-----

## 🏁 How to Run Locally

This project requires a local MySQL database and a Google Gemini API key.

### 1\. Prerequisites

  * Python 3.10+
  * A MySQL server (like XAMPP, MAMP, or MySQL Community Server)
  * A Google Gemini API Key.

### 2\. Setup

1.  **Clone the repository:**

    git clone https://github.com/itz-leo/gate-alcohol-checker
    cd gategroup-bottle-assistant

2.  **Create a virtual environment and install dependencies:**

    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    pip install -r requirements.txt

    *(Note: Don't forget to create your `requirements.txt` file by running `pip freeze > requirements.txt`)*

3.  **Set up the Database:**

      * Start your MySQL server.
      * Create a database named `bottle_handling`.
      * Import the `bottle_handling.sql` file into that database.
      * Make sure your credentials in `conexionBD.py` (host, user, password) match your MySQL server's credentials.

4.  **Set up Environment Variables:**

      * Create a file named `.env` in the project root.
      * Add your Gemini API key:
        ```
        GEMINI_API_KEY="YOUR_API_KEY_GOES_HERE"
        ```

### 3\. Run the App\!

Once everything is set up, launch the Streamlit app:

```
streamlit run app_gui.py
```

Your browser will automatically open to `http://localhost:8501`.

**Test Credentials:**

  * **Username:** `admin`
  * **Password:** `admin`
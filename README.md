# 📦 Electronic Inventory & Live Currency Exchange Engine

A Python OOP-based CLI inventory management system with real-time USD to LKR currency conversion and automated business analytics.

## 🚀 Key Features
* **Object-Oriented Architecture (OOP):** Clean, modular class design (`EiEngine`).
* **Live Exchange Rate Integration:** Fetches real-time USD to LKR rates via REST API (`urllib` & `json`) with offline fallback handling.
* **Persistent SQLite Database:** Automated table setup and secure parameterized SQL queries (`sqlite3`).
* **Instant Business Analytics:** Calculates Grand Total inventory value ($\sum \text{LKR}$), High-Value Stock (>50,000 LKR), and Low-Stock Alerts (Qty < 5) using List Comprehensions.
* **Case-Insensitive Search:** Quickly filters items using SQL `WHERE LOWER()` queries.

## 🛠️ Technologies Used
* **Language:** Python 3
* **Database:** SQLite3
* **Libraries:** `sqlite3`, `urllib.request`, `json`, `datetime`
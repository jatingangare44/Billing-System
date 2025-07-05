
# 🛒 Billing-System – The King's Grocery (Flask App)

A simple, user-friendly Flask web application for grocery billing and product management, featuring PDF bill generation, admin authentication, and a coffee-themed dashboard UI.

![image](https://github.com/user-attachments/assets/054ad71e-ce11-4723-aa20-b3e6fdc95992)

![image](https://github.com/user-attachments/assets/56e3d395-fc98-44fd-b97a-0cb6c2b3122e)



---

## 📌 Features

- 🧾 **Add to Cart** & calculate GST, Discount & Final Bill
- 📤 **PDF Bill Generation** using ReportLab
- 🔐 **Login Authentication** for Admin
- ✅ **Admin Verification** for Product Manager access
- 📁 **CSV-based Product Management** (CRUD)
- 🔎 **Search Products** by name
- 💅 Modern coffee-themed UI
- 🖥️ **Windows Executable** available as `.exe` version for offline billing

---

## 🛠️ Tech Stack

| Technology | Usage |
|------------|--------|
| Python     | Backend Logic |
| Flask      | Web Framework |
| HTML/CSS   | UI/UX |
| ReportLab  | PDF Generation |
| CSV        | Data Storage |
| JavaScript | Frontend Actions |
| Bootstrap  | (Optional) UI Components |
| PyInstaller | Create `.exe` for Windows |

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/jatingangare44/Billing-System.git
cd Billing-System
```

### 2. Create Virtual Environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing, install manually:

```bash
pip install flask reportlab
```

---

## ▶️ Run the App

```bash
python app.py
```

Visit: `http://127.0.0.1:5000/`

---

## 🔑 Admin Credentials

- **Username:** `admin`
- **Password:** `admin123`

### Product Manager Access

- Requires extra verification:
  - **Admin Password:** `jatin123`

---

## 📂 Folder Structure

```
Billing-System/
│
├── data/                 # Stores products.csv
├── bills/                # Generated PDF bills
├── templates/            # HTML Templates
│   ├── login.html
│   ├── dashboard.html
│   ├── products.html
│   └── product_auth.html
├── static/               # Images, CSS, JS (if any)
├── assets/               # Fonts like DejaVuSans.ttf
├── GroceryBillingSystem.exe # Windows Executable
├── app.py                # Main Flask Application
└── README.md             # Project Documentation
```

---

## 🖥️ Windows Software

If you prefer not to run the Python code, simply run the included:

```
GroceryBillingSystem.exe
```

> Make sure `products.csv` exists inside the `data/` folder. It will be created automatically if missing.

---

## 📸 Preview

> Add a preview image or GIF inside `static/` folder  
> Then link it like:

```md
![Preview](static/preview.png)
```

---

## 🤝 Credits

Built with ❤️ by [Jatin Gangare](https://github.com/jatingangare44)

---

## 📬 Contact

- 📧 Email: `jatingangare44@gmail.com`
- 🔗 GitHub: [@jatingangare44](https://github.com/jatingangare44)

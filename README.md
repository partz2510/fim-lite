# ⚙️ FIM-Lite: File Integrity Monitor (Python + SHA-256)

A lightweight Python-based **file integrity monitoring tool** that tracks changes in real time.  
FIM-Lite creates a secure **SHA-256 baseline** of every file in a directory and detects **additions, deletions, or modifications**, producing instant JSON/CSV reports.

---

## 🚀 Features

- 🧠 **Baseline Creation** – Computes SHA-256 hashes of all files and stores them in `.baseline.json`.  
- 🔍 **Integrity Checking** – Detects files that are *added, removed, or modified*.  
- 📊 **Auto-generated Reports** – Saves JSON reports in `/reports/` for auditing or SIEM ingestion.  
- 🎨 **Rich CLI Output** – Color-coded terminal interface using `rich`.  
- ⚡ **Cross-Platform** – Works on Windows, macOS, and Linux.  
- 🪶 **Zero Dependencies (besides `rich`)** – Lightweight, clean, and easy to extend.

---

## 🧩 Tech Stack

| Category | Tools |
|-----------|--------|
| Language | Python 3 |
| Libraries | `rich`, `hashlib`, `argparse`, `json` |
| Output | JSON, CSV, and terminal reports |
| Algorithm | SHA-256 hashing |

---

## 🧰 Setup & Usage

### 1️⃣ Clone and Install
```bash
git clone https://github.com/partz2510/fim-lite.git
cd fim-lite
python -m venv .venv
. .venv/Scripts/activate    # (Windows)
pip install -r requirements.txt
2️⃣ Create Baseline
bash
Copy code
python src/fim.py init --root . --exclude ".venv/*" --exclude "reports/*"
Output:

scss
Copy code
Baseline created: 12 files • .baseline.json
3️⃣ Check for Changes
bash
Copy code
python src/fim.py check --root . --exclude ".venv/*" --exclude "reports/*"
Output:

bash
Copy code
╭──────────────────────────── FIM-Lite Report ─────────────────────────────╮
│ ADDED     examples/demo.txt                                             │
│ MODIFIED  src/fim.py                                                    │
╰─────────────────────────────────────────────────────────────────────────╯
Unchanged files: 10
Report saved to: reports/fim-report-YYYYMMDD-HHMMSS.json
📸 Example Screenshots
Description	Preview
Baseline Created	
Integrity Report	
Project Structure	

🧪 Folder Structure
css
Copy code
fim-lite/
├── src/
│   └── fim.py
├── examples/
├── tests/
├── reports/
├── requirements.txt
├── README.md
└── .baseline.json
🌱 Future Improvements
Add email / Slack alert integration

Add CSV export for Splunk/SIEM integration

Add file whitelist / auto-heal options

Build GUI wrapper for Windows users

🧑‍💻 Author
Parthiban Ganesan
Cybersecurity Engineer | Python Automation | Cloud Security Enthusiast
📎 LinkedIn | 📂 GitHub

🧠 Inspiration
This project demonstrates the power of Python for blue-team automation — combining cryptographic hashing, scripting, and security operations concepts into one elegant command-line utility.

🪪 License
MIT License – free for educational and professional use.

# ULP Combo Extractor Pro — Neon Edition v2 💎


A blazing-fast, professional combo extractor and cleaner featuring a Neon Cyberpunk UI, a real-time HUD dashboard, and smart parsing logic. Optimized for handling huge lists with precision and speed.

---

## ✨ Key Features

- 🎨 Neon Cyberpunk UI  
  A stunning, modern terminal interface with TrueColor simulation.

- ⚡ Ultra Performance  
  Powered by a pre-compiled regex engine for maximum speed (MB/s processing).

- 🧠 Smart Parsing  
  Automatically detects delimiters (`:`, `;`, `|`) and handles complex formats like `url:port:user:pass`.

- 📂 Batch Mode  
  Process an entire folder of text files automatically.

- 📊 Live HUD  
  Real-time dashboard showing speed, progress, ETA, and validity stats.

- 🔒 Security Analytics  
  Analyzes password complexity (Numeric vs Alpha vs Mixed).

- 🛠 Interactive Extraction  
  Optionally extract top domains (Gmail, Yahoo, etc.) into separate files after processing.

- 🧹 Auto-Sorting & Cleaning  
  Automatically removes duplicates, bad characters, and garbage data.

---

## 🖥️ Dashboard Preview

PROCESSING...        File 1/5

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  45%

Valid: 313,476    Dups: 102,496    Bad: 14,713

Speed: 12.5 MB/s  Rate: 82,434 L/s ETA: 12s

---

## ⚡ How to Use

### Prerequisites
- Python 3.x

### Run the Script
```bash
python ulp_extractor.py
```

Follow the Neon UI:

1. Select Input: Choose a single `.txt` file OR enter a folder path for Batch Mode.
2. Filter (Optional): Enter a keyword (e.g., `.ir`, `netflix`) to extract specific lines, or press Enter to extract everything.
3. Processing: Watch the live HUD as it cleans and sorts your list.
4. Post-Process: The tool will show top domains found. Type `y` to save them into separate files.

---

## 📄 Output Formats

- Main Output: `FILENAME_extracted.txt` (Sorted & Unique) — format: `user:pass`
- Optional Domain Files: `FILENAME_extracted_gmail_com.txt`, `FILENAME_extracted_yahoo_com.txt`, etc.

---

## 🔎 Input Handling Examples

| Input Line                                | Result             | Status        |
|------------------------------------------:|-------------------:|---------------|
| `user:pass`                               | `user:pass`        | ✅ Valid       |
| `email@domain.com:password`               | `email@domain.com:password` | ✅ Valid |
| `https://site.com:8080:user:pass`         | `user:pass`        | ✅ Smart Parsed|
| `user;pass`                               | `user:pass`        | ✅ Delimiter Fixed |
| `` `user\n\npass` ``                      | `user:pass`        | ✅ Cleaned     |
| `garbage_data_line`                       | (Removed)          | ❌ Invalid     |
| `user:null`                               | (Removed)          | ❌ Bad Syntax  |

---

## 🧾 Security Analytics

- Classifies passwords into:
  - Numeric-only
  - Alpha-only
  - Mixed (Alpha + Numeric + Symbols)
- Reports top domains and basic strength distribution for quick insights.

---

## 🗂 Batch Mode

Point the script at a folder to process every `.txt` file inside. Outputs are generated per input file preserving the filename prefix:
```
input/
  ├─ file1.txt  -> file1_extracted.txt
  ├─ file2.txt  -> file2_extracted.txt
  └─ ...
```

---

## ⚙️ Configuration & Options

- Interactive prompts guide actions (filtering, domain saving).
- Auto-deduplication and sorting are enabled by default.
- Smart parsing automatically normalizes delimiters and strips common noise characters.
- You can disable interactive prompts for automated pipelines (see script flags or optional arguments in the tool implementation).

---

## 📝 Changelog

### v2 — Neon Edition (EN)
- New Theme: "Neon Cyberpunk" design with TrueColor simulation.
- HUD Dashboard: Real-time Heads-Up Display for speed & ETA.
- Smart Parsing: Added support for delimiters `:`, `;`, `|`.
- Batch Mode: Process entire folders at once.
- Security Analytics: Password complexity stats.
- Interactive Workflow: Optional saving of top domains.

### نسخه 2 — نئون ادیشن (FA)
- تم جدید: طراحی "سایبرپانک نئونی" با رابط کاربری جذاب.
- داشبورد HUD: نمایش زنده سرعت، پیشرفت و زمان باقی‌مانده.
- پارس هوشمند: پشتیبانی از جداکننده‌های مختلف (`:`, `;`, `|`) و فرمت‌های پیچیده.
- حالت دسته‌ای: قابلیت پردازش همزمان تمام فایل‌های یک پوشه.
- آنالیز امنیتی: نمایش آمار کیفیت پسوردها.
- خروجی تعاملی: امکان ذخیره جداگانه دامنه‌های مهم (مثل جیمیل) در پایان کار.

---

## ❤️ Credits

Developed with love by Mohammad SK

---

## ⚠️ Legal & Responsible Use

This tool is intended for lawful, ethical, and authorized use only. Do not use it to process data you do not have explicit permission to handle. The author is not responsible for misuse.

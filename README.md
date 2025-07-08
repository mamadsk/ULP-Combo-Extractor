# ULP Combo Extractor — by Mohammad SK

A blazing fast, modern combo extractor for parsing ULP/user:pass and email:pass combos  
with domain/website filtering, duplicate removal, and beautiful stats.

---

## 🖥️ Extraction Summary

| Input File   | Input Size | Total Lines | Output File         | Output Size | Unique Combos | Duplicates | Bad Chars | Time   | Speed      |
|--------------|------------|-------------|---------------------|-------------|---------------|------------|-----------|--------|------------|
| mylist.txt   | 41.3 MB    | 534,236     | converted_combo.txt | 9.8 MB      | 352,156       | 180,983    | 1,446,224 | 6.26 s | 82,434 l/s |

✔ Only valid combos are in your output file.  
📂 Output: `converted_combo.txt`

---

## ⚡ How to Use

1. **Download**
   - Download `ulp_extractor.py`
   - (Optionally) Place your combo file (e.g. `mylist.txt`) in the same folder

2. **Run**
   ```bash
   python ulp_extractor.py

3. **Follow prompts**
   - Select your combo input file (supports `.txt`)
   - Optionally filter combos by any domain/website/keyword (e.g. `.ir`, `netflix`)
   - Wait for extraction (progress & live stats)
   - When finished, see your `converted_combo.txt` — only clean combos!
## 📄 Output

- **converted_combo.txt:** Final, cleaned, unique combos  
  (Format: `username:password` or `email:password`)

---

## 🧑‍💻 Example Input

- https://site.com/:user1:pass1
- android://app.domain/:user2:pass2
- user3:pass3
- mail4@example.com:12345

*Only the lines in `username:password` or `email:password` format will be accepted as valid combos.*


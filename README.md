
# 🗂️ Wildcard-Based File Copier

This program copies files from a source folder to a destination folder based on a list of filename patterns (wildcards) provided in a `.txt` file.

## ✅ What It Does

- Reads a list of patterns like `*.pdf`, `report_*.xlsx`, etc.
- Searches for matching files in the source folder (including subfolders).
- Copies the found files to the destination folder.
- Generates a report showing copied and missing files.

## 🚀 How to Use

1. Run the program (`Copiar Lista de Arquivos.exe`).
2. Select:
   - A `.txt` file with your filename patterns.
   - The **source folder** where the files are located.
   - The **destination folder** where the files will be copied to.
3. Click **Start Copy**.
4. Track progress in the log window.
5. Check the generated `relatorio_copia.txt` file in the destination folder for a summary.

## 📝 Example `list.txt` File

```txt
*.pdf
report_*.xlsx
final_document.docx
```

## 🔧 Rebuilding the `.exe` (Optional)

If needed, you can recreate the executable using:

```bash
python -m PyInstaller --onefile --windowed --icon="your_icon.ico" "Copiar Lista de Arquivos.py"
```

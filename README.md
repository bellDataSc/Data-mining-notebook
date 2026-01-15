2026-01-15 | obs: Guys, I'm going to document this process in parts. It was done very carefully because of the sensitivity of the information and how we'll use it for statistics later... I also plan to make a series of videos later =)

Context & Application at FGV IBRE
As an **Engineering & Data Automation Professional at FGV IBRE** (Brazilian Institute of Economics), dealing with diverse and often unstructured data sources is a daily challenge. Economic studies and indices require precise data ingestion from various formats, including legacy PDF reports.

This repository demonstrates a practical solution to a common bottleneck in data engineering pipelines: **transforming rigid, human-readable PDF reports into structured, machine-readable datasets.**

The script was developed to automate the extraction of construction input prices (INCC components), solving specific challenges such as:
* **Implicit Hierarchies:** Reconstructing "Parent | Child" relationships that exist visually in the PDF but not structurally.
* **Unstructured Layouts:** parsing data without reliance on fixed table grids, using Regex and coordinate logic.
* **Large Volume Processing:** Implementing batch processing (checkpoints) to handle large files (1.7k+ pages) within memory constraints.

---

## Technical Overview

This project is a Python-based ETL solution designed to extract tabular data from complex PDF files where standard scraping tools fail due to inconsistent column formatting and hierarchical data representation.

### Key Challenges Solved
1.  **Hierarchy Reconstruction:** The source PDF groups products under "Family" headers (e.g., *Valves* -> *Butterfly Valve*). The script detects these headers dynamically and propagates the "Parent | Child" context to all subsequent SKU rows.
2.  **Visual Column Parsing:** Instead of relying on physical table lines (which were absent), the solution uses **Regex anchoring**. It identifies the "Code" at the start of the line and the "Price" at the end, treating the middle content as a variable string to be parsed into "Description" and "Unit".
3.  **Memory Optimization:** Uses a streaming approach with `pdfplumber`, processing pages in blocks (batches of 100) and appending to disk, ensuring stability on cloud environments like Google Colab with limited RAM.

## Tech Stack
* **Google Colab**
* **Python 3.x**
* **PDFPlumber:** For robust text extraction and layout analysis.
* **Pandas:** For data manipulation and CSV batch buffering.
* **Regular Expressions (Regex):** For pattern matching of BRL currency formats and product codes.

## How it Works

The pipeline follows these steps:
1.  **Pattern Recognition:** Identifies lines that match specific SKU patterns (`Code` + `Description` + `Price`) versus Header patterns.
2.  **Smart Parsing:**
    * Extracts the **Price** (anchored at the end of the line).
    * Extracts the **Code** (anchored at the start).
    * Isolates the middle string and uses reverse-logic to separate the **Unit** (usually short strings like 'KG', 'H', 'MES R') from the **Description**.
3.  **Context Management:** Maintains a state variable for the current `Family`. If consecutive headers are found, it concatenates them to form a full breadcrumb path (e.g., `MÃO DE OBRA | HORISTAS`).
4.  **Batch I/O:** Writes data to CSV every 100 pages to prevent data loss and manage memory footprint.

## Usage

      ```bash
      # Install dependencies
      pip install pdfplumber pandas openpyxl
      
      # Run the extraction script
      python extraction_pipeline.py

----------------------------------------------------------------------------------------------------------------

Author
Bel Cruz Engineering & Data Automation | FGV IBRE

Focusing on Data Engineering, FinTech, and Public Policy Statistics.

LinkedIn: [Bel Cruz](https://www.linkedin.com/in/belcruz/)

GitHub: bellDataSc


# Intern-Company AI Matching Pipeline

**An AI-driven architecture for automating high-quality student-internship alignment at scale.**

## Overview
Matching students from underrepresented communities with high-quality internships is a complex, multi-variable optimization problem. Traditional manual matching processes are resource-intensive and struggle to scale.

This project implements an **end-to-end AI pipeline** designed to streamline this process. By integrating Large Language Models (LLMs) for semantic understanding with rigorous filtering logic, this system reduces the matching timeline from **weeks to days** while improving match precision and reducing operational costs by **~96%**.

> **Note:** The data used in this repository has been AI-generated to maintain anonymity. The logic and architecture mirror the production system deployed for the 2024 cohort.

---

## Key Impact
* [cite_start]**Efficiency:** Reduced the matching timeline from **3 weeks to <1 day**[cite: 1185].
* [cite_start]**Cost Optimization:** Implemented a multi-stage filtering architecture that reduced API costs by **~96%** (from ~$900 to ~$30 per run) by filtering candidates before expensive alignment scoring[cite: 1117, 1119].
* [cite_start]**Scale:** Capable of processing **40,000+ initial combinations** and narrowing them down to precise top-4 candidates per company[cite: 821, 1138].
* [cite_start]**Quality:** In manual audits of the 2024 cohort, **94%** of top-ranked candidates were verified as qualified matches[cite: 1187].

---

## The Problem
The previous matching system relied on a combination of rigid form-based filtering and extensive manual review.
* [cite_start]**Bottleneck:** A team of three required up to **3 weeks** to match just 100 companies[cite: 733].
* [cite_start]**Fragility:** Automated systems often failed to find matches for niche roles, forcing manual searches[cite: 744].
* [cite_start]**Inequity:** "First-come-first-served" matching logic often led to optimal candidates being unavailable for later companies[cite: 770].

---

## 🛠️ The Solution: Architecture & Pipeline
The solution is a 6-stage pipeline that progressively refines the candidate pool using both symbolic logic (filters) and semantic understanding (LLMs).

### Pipeline Workflow

**1. Data Ingestion & Cross-Join** (`pipeline_1_logic_scoring.ipynb`)
* [cite_start]Combines all student applications with all position profiles to create a comprehensive dataset of every possible pair[cite: 791].
* [cite_start]**Ineligibility Filtering:** Hard filters for age, location, and graduation year remove impossible matches immediately[cite: 794].

**2. Semantic Extraction (The "Extract-o-Bot")** (`pipeline_2_extract-o-bot.ipynb`)
* Uses **GPT-4** to analyze unstructured resumes and job descriptions.
* [cite_start]**Extracts & Labels:** Identifies Technical Skills, Soft Skills, and Industry Interests, labeling them by proficiency (Beginner/Advanced) and relevance[cite: 829, 856].

**3. Keyword Scoring** (`pipeline_3_keyword_scoring.ipynb`)
* Applies a weighted scoring algorithm to the extracted data.
* [cite_start]**Weights:** Heavy emphasis on Technical Skills and Industry Alignment, with secondary weighting for Soft Skills and Values[cite: 920, 958].

**4. Keyword Filtering** (`pipeline_4_keyword_filtering.ipynb`)
* **The Cost Saver:** Filters out low-probability matches *before* the expensive alignment step.
* [cite_start]In the 2024 cohort, this step reduced the pool from **27,700** candidates to **993** high-potential pairs, massively reducing downstream API costs[cite: 1017].

**5. Alignment Scoring ("Matchy-9000")** (`pipeline_5_matchy-9000.ipynb`)
* Performs a deep-dive semantic comparison of the remaining pairs.
* Evaluates alignment across 4 categories:
    1.  Company Mission & Industry Fit
    2.  Role Responsibilities vs. Experience
    3.  Technical Stack Alignment
    4.  [cite_start]Culture & Values Fit[cite: 1069].
* [cite_start]Generates a nuanced 0-10 score with reasoning summaries[cite: 1092].

**6. Final Selection** (`pipeline_6_matchy_filtering.ipynb`)
* [cite_start]Selects the top 4 candidates for each company using an iterative round-robin selection to ensure equitable distribution of talent[cite: 1138].

---

## Technical Highlights

### Rate Limiting & Concurrency
To handle thousands of API calls efficiently without hitting provider limits:
* [cite_start]**Semaphores:** Used to strictly control concurrent requests and token throughput[cite: 1431].
* [cite_start]**Threading:** Multi-threaded execution ensures high throughput (up to 150 rows/minute)[cite: 1442].
* [cite_start]**Retry Logic:** Robust backoff mechanisms handle transient API failures gracefully[cite: 1438].

### Data Security
* [cite_start]**Thread Isolation:** API calls are isolated on separate threads to prevent prompt injection attacks or data cross-contamination[cite: 1329].
* [cite_start]**Input Sanitization:** All inputs are validated to prevent malicious prompt engineering within job descriptions[cite: 1337].

---

## Repository Structure

| File/Folder | Description |
| :--- | :--- |
| `pipeline_1_logic_scoring.ipynb` | Initial data join and hard constraint filtering (e.g., location/eligibility). |
| `pipeline_2_extract-o-bot.ipynb` | LLM-based extraction of skills and metadata from unstructured text. |
| `pipeline_3_keyword_scoring.ipynb` | Weighted scoring algorithm based on extracted metadata. |
| `pipeline_4_keyword_filtering.ipynb` | Cost-optimization layer: reduces candidate pool by ~95% before deep analysis. |
| `pipeline_5_matchy-9000.ipynb` | Deep semantic alignment scoring using LLMs. |
| `pipeline_6_matchy_filtering.ipynb` | Final optimization logic to select top-N candidates per company. |
| `mypackage/` | Utility scripts for API handling, data loading, and formatting. |
| `data/` | Anonymized synthetic data for demonstration. |

---

## ⚡ Getting Started

### Prerequisites
* Python 3.11+
* OpenAI API Key

### Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/KajIzora/Intern-Company-AI-Matching-Pipeline.git](https://github.com/KajIzora/Intern-Company-AI-Matching-Pipeline.git)
    cd Intern-Company-AI-Matching-Pipeline
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Set up your environment variables:
    * Create a `.env` file or export your key:
    ```bash
    export OPENAI_API_KEY='your-api-key-here'
    ```

4.  Run the pipeline notebooks in order (1 through 6) to reproduce the matching process.

---

## Reference
For a deep dive into the methodology, algorithms, and business logic, please refer to the **Technical White Paper**:
* [Enhancing the Efficiency and Quality of Internship Matching.pdf](Enhancing%20the%20Efficiency%20and%20Quality%20of%20Internship%20Matching_%20An%20AI-Driven%20Approach%20to%20Student-Company%20Alignment.pdf)

---
*Created by Kaj Hansteen Izora*

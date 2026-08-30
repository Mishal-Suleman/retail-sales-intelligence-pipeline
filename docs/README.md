# Retail Sales Intelligence Pipeline
> An end-to-end analytics engineering project that turns scattered multi-branch retail transaction data into a governed, query-ready model and a self-serve dashboard for business decision-making.

---

## Project Type Flags
- [x] Dashboard / Data Visualization
- [x] Data Pipeline / ETL
- [x] Data Cleaning / Wrangling
- [x] End-to-End (multiple of the above)

---

## 1. Project Overview

**Context:** A multi-branch retail/FMCG chain generates daily transaction data across its branches, but that data is scattered and only compiled into reports once a month, by hand. That leaves management without timely, reliable visibility into how the business is actually performing.

**Problem Statement:** Without a unified, trustworthy data model, it's hard to know which branches and products are actually profitable, seasonal demand patterns get missed, and reporting itself is slow and error prone.

**Approach:** Built a medallion-style (raw to clean to curated) ETL pipeline in Python and DuckDB, modeled the cleaned data into a star schema, and layered SQL analysis, a Power BI dashboard, and a basic demand forecast on top. Logged and documented at every stage.

**Outcome:** *(to be completed once the pipeline and analysis are finished)*

---

## 2. Objectives

- **Primary Objective:** Build a reproducible, end-to-end pipeline that ingests, cleans, and models multi-branch retail sales data into a query-ready star schema.
- **Secondary Objective 1:** Work out which branches and products actually drive profit, not just revenue.
- **Secondary Objective 2:** Deliver a self-serve Power BI dashboard for non-technical stakeholders.
- **Secondary Objective 3:** Produce a basic demand forecast to support inventory planning.

> Every analysis decision in this project traces back to one of these objectives.

---

## 3. Project Scope & Tools

### Scope

| Dimension | Details |
|-----------|---------|
| **In Scope** | Transaction level sales data (~80,000 sampled rows), enriched with a synthetic branch/store dimension. ETL pipeline, star schema, SQL analysis, dashboard, basic forecasting. |
| **Out of Scope** | Real time streaming ingestion, external API integrations, machine learning forecasting beyond a basic model. |
| **Time Period** | Source data spans roughly December 2009 to December 2011 (Online Retail II dataset). |
| **Granularity** | Transaction line-item level. |

### Tools & Technologies

| Category | Tool(s) Used |
|----------|-------------|
| Data Storage | DuckDB |
| Data Processing | Python (pandas) |
| Analysis | SQL, pandas |
| Visualization | Power BI |
| Version Control | Git / GitHub |
| Documentation | Markdown |

---

## 4. Repository Structure

```
retail-sales-intelligence-pipeline/
│
├── data/
│   ├── raw/                  # Original, unmodified source data - never edited
│   ├── processed/            # Cleaned and transformed data
│   └── external/             # Reference/lookup data
│
├── notebooks/                # EDA notebooks
├── scripts/                  # extract.py, transform.py, load.py, logger_config.py
├── queries/                  # SQL analysis queries
├── reports/                  # Pipeline run logs, data quality reports
├── visuals/                  # Power BI file, exported charts
├── docs/                     # requirements.md, data dictionary, architecture diagram
│
├── project_metadata.yml
└── README.md
```

---

*Sections 5 to 14 (Data Workflow, Schema, Analysis, Insights, Recommendations, etc.) will be filled in as each pipeline stage is actually built, not before. Writing them now would mean documenting work that hasn't happened yet.*

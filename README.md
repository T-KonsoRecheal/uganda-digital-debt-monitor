# Uganda National Digital Debt Exposure & Loan Stacking Monitor
> **[Live Interactive Dashboard: Click Here to Launch the Platform](https://uganda-digital-debt-monitor-eg4wpmqtd5nd4lp5xqyffs.streamlit.app)**


> **A macro prudential fintech intelligence platform designed to monitor cross network digital credit accumulation, dual SIM loan stacking (MTN Mobile Money & Airtel Money), and default risk propagation across all 134 official districts of Uganda.**

---

## Executive Summary

The rapid expansion of short term mobile credit across Sub Saharan Africa has significantly expanded financial inclusion for unbanked and informal populations. However, the lack of real time cross network Credit Reference Bureau (CRB) integration among digital micro lenders has created a critical regulatory blind spot: **Multi SIM Loan Stacking**.

Borrowers frequently utilize separate SIM cards registered under distinct telecom networks (MTN Uganda and Airtel Uganda) to access concurrent unindexed digital credit lines. When unmonitored, this behavior leads to unsustainable Debt to Income (DTI) ratios and systemic default spikes across rural and urban economies.

This project synthesizes **15,000 verified borrower records** across every administrative district in Uganda to provide central regulators such as the **Bank of Uganda (BoU)** and the **Uganda Microfinance Regulatory Authority (UMRA)** as well as institutional lenders with real time geospatial risk mapping, automated DTI capacity assessment, and forensic KYC audit trails.

---

## Key System Capabilities

### 1. National Geospatial Debt Intensity Analytics
* **134 District Nationwide Coverage:** Maps financial stress across all official districts across Central, Western, Eastern, and Northern Uganda.
* **Density Heatmapping:** Utilizes Plotly Express density map calculations ($z = \text{Total Debt UGX}$) anchored on exact geographic coordinates to pinpoint high exposure default hot spots.
* **Macro Filter Controls:** Strict alphabetical region and district filtering for granular localized policy intervention.

### 2. Individual Cash Flow & DTI Capacity Evaluator
* **NIN Linked Registry Lookup:** Directly fetches verified monthly income and existing liabilities from National Identification Number (NIN) profiles (`CM` male and `CF` female prefixes).
* **Automated Credit Underwriting:** Calculates projected Debt to Income (DTI) percentages against a standard 35% safe debt ceiling to generate real time approval, restructuring, or rejection verdicts.

### 3. Dual SIM KYC & Multi Network Forensic Audit
* **Cross Network Telecom Tracking:** Explicitly audits dual line borrower profiles, color coding **<span style="color:#f1c40f;">MTN</span>** (+256 77/78/76) and **<span style="color:#e74c3c;">Airtel</span>** (+256 75/70) numbers to expose hidden multi SIM liabilities.
* **Data Quality & Deduplication:** Features 100% unique, non repeating Ugandan names structured across two part and three part naming conventions.
* **Itemized JSON Audit Trail:** Parses embedded active loan logs detailing exact lending platforms (e.g., *MTN MoMo Advance*, *MoKash*, *Airtel QuickLoan*, *Wewole*), disbursal timestamps, and principal balances.
* **Risk Tiered Repayment Countdown Timers:** Dynamic operational clocks tracking repayment windows and delinquency aging:
  * <span style="background-color:#2ecc71; color:white; padding:2px 6px; border-radius:3px;">LOW RISK</span> $\ge 15$ days remaining (Healthy liquidity buffer)
  * <span style="background-color:#e67e22; color:white; padding:2px 6px; border-radius:3px;">MODERATE RISK</span> $6 \text{ to } 14$ days remaining (Approaching maturity)
  * <span style="background-color:#e74c3c; color:white; padding:2px 6px; border-radius:3px;">CRITICAL RISK</span> $\le 5$ days remaining or Overdue Default

---

## Tech Stack & Data Engineering

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core analytical logic, mathematical modeling, data extraction |
| **Frontend Framework** | Streamlit | Executive multi tab interactive web interface |
| **Data Manipulation** | Pandas, NumPy | Synthetic demographic modeling, JSON serialization, array operations |
| **Geospatial & Visualization** | Plotly Express | Density map generation, coordinate mapping, interactive visual analytics |
| **Version Control** | Git, GitHub | Source code tracking and public repository deployment |

---

## Dataset Architecture (`uganda_digital_debt_data.csv`)

The underlying dataset models realistic socio economic dynamics tailored to Uganda's economic structure:
* **Sample Size:** 15,000 unique borrower records.
* **Regional Income Weighting:** Higher formal wage distribution in Central regions (Kampala, Wakiso, Mukono) contrasted with informal trade and agricultural cash flows in Western, Eastern, and Northern regions.
* **Loan Stacking Behavior:** Mathematically links high DTI ratios ($>40\%$) and multi loan accumulation across distinct telecom lines directly to elevated default probability.

```text
Field Name             | Type    | Description
-----------------------|---------|---------------------------------------------------------
Borrower_ID            | String  | Unique system identifier (e.g., USR_10482)
Borrower_Name          | String  | 100% unique full name (2 part or 3 part Ugandan structure)
National_ID_Number     | String  | Validated Ugandan NIN (CM/CF + 12 alphanumeric chars)
MTN_Phone              | String  | Primary MTN Mobile Money contact (+256 77/78/76)
Airtel_Phone           | String  | Secondary Airtel Money contact (+256 75/70)
Gender / Age           | String/Int| Demographics (Ages 18 to 60)
Region / District      | String  | Mapped across all 134 official districts
Latitude / Longitude   | Float   | Geocoded regional coordinates with Gaussian variance
Income_Source          | String  | Agriculture, Informal Trade, Salary, Services
Monthly_Income_UGX     | Float   | Estimated monthly income in Uganda Shillings
Active_Digital_Loans   | Integer | Number of concurrent active short term digital credit lines
Total_Debt_UGX         | Float   | Sum of outstanding principal balances across networks
Debt_to_Income_Ratio   | Float   | Total Debt / Monthly Income ratio
Default_Status         | Integer | Binary target variable (0 = Performing, 1 = Defaulted)
Loans_JSON             | JSON    | Itemized array of active loan audit records

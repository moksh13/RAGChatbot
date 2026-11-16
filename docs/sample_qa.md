# Sample Q&A Benchmark Verification Suite

This document records the official benchmark Q&A evaluation of the **Mutual Fund Facts-Only RAG Assistant**. Each test case verifies retrieved context chunks, cosine similarity score, factual generation, sentence constraint compliance ($\le 3$ sentences), single citation link, and guardrail enforcement.

---

### Test Case 1: HDFC Large Cap Fund - Exit Load & Expense Ratio
- **User Question:** *"What is the expense ratio and exit load for HDFC Large Cap Fund Direct Growth?"*
- **Guardrail Status:** Passed (Factual scheme inquiry)
- **Retrieved Chunks:**
  1. `hdfc_large_cap_chunk_01` (Similarity: 76.71%)
     - *Snippet:* Scheme: HDFC Large Cap Fund Direct Growth (Equity: Large Cap). Expense Ratio: 1.00% (inclusive of GST). Exit Load: 1.00% if redeemed or switched out within 1 year (365 days) from allotment; Nil after 1 year...
- **Assistant Answer:**
  > The HDFC Large Cap Fund Direct Growth has an expense ratio of 1.00% (inclusive of GST). It levies an exit load of 1.00% if units are redeemed or switched out within 1 year (365 days) of allotment, with zero exit load applicable thereafter.  
  > [Official Scheme Page](https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth)  
  > *Last updated from sources: November 2026*
- **Citation Link:** `https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth`
- **Verification:** Accurate facts, 2 sentences, 1 citation link, update date included.

---

### Test Case 2: HDFC ELSS Tax Saver Fund - Lock-in Period
- **User Question:** *"What is the lock-in period for HDFC ELSS Tax Saver Fund?"*
- **Guardrail Status:** Passed (Factual scheme inquiry)
- **Retrieved Chunks:**
  1. `hdfc_elss_tax_saver_chunk_02` (Similarity: 75.54%)
     - *Snippet:* Scheme: HDFC ELSS Tax Saver Fund Direct Plan Growth. Minimum SIP: ₹500. Lock-in Period: 3 Years statutory lock-in period. Each SIP installment carries its own independent 3-year lock-in period...
- **Assistant Answer:**
  > HDFC ELSS Tax Saver Fund has a mandatory statutory lock-in period of 3 years from the date of allotment under Section 80C of the Income Tax Act. For SIP investments, each monthly installment has an independent 3-year lock-in and cannot be withdrawn before 36 months.  
  > [Official Scheme Page](https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth)  
  > *Last updated from sources: November 2026*
- **Citation Link:** `https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth`
- **Verification:** Accurate statutory 3-year rule, 2 sentences, 1 citation link, update date included.

---

### Test Case 3: Capital Gains Statement Download Procedure
- **User Question:** *"How can I download my capital gains statement?"*
- **Guardrail Status:** Passed (Investor services inquiry)
- **Retrieved Chunks:**
  1. `statement_guide_chunk_01` (Similarity: 71.03%)
     - *Snippet:* How to Download Capital Gains Statement from HDFC Mutual Fund Portal: Visit official portal (https://www.hdfcfund.com/investor-services/statements) -> Go to 'Investor Services' -> Click 'Statements & Certificates'...
  2. `statement_guide_chunk_03` (Similarity: 70.77%)
     - *Snippet:* How to Download Capital Gains Statement on Groww: Open the Groww application or website -> Click your Profile picture -> Navigate to 'Reports'...
- **Assistant Answer:**
  > To download your capital gains statement, visit the HDFC Mutual Fund investor portal at https://www.hdfcfund.com/investor-services/statements, navigate to 'Investor Services' > 'Statements & Certificates', enter your registered PAN or Folio number, verify with OTP, and download the report for your chosen financial year. Alternatively, you can download a Consolidated Account Statement (CAS) via CAMS or the Reports section in the Groww app.  
  > [Official Statement Portal](https://www.hdfcfund.com/investor-services/statements)  
  > *Last updated from sources: November 2026*
- **Citation Link:** `https://www.hdfcfund.com/investor-services/statements`
- **Verification:** Complete procedural steps, 2 sentences, 1 citation link, update date included.

---

### Test Case 4: HDFC Small Cap Fund - Minimum Investment
- **User Question:** *"What is the minimum SIP investment for HDFC Small Cap Fund?"*
- **Guardrail Status:** Passed (Factual scheme inquiry)
- **Retrieved Chunks:**
  1. `hdfc_small_cap_chunk_02` (Similarity: 78.10%)
     - *Snippet:* Scheme: HDFC Small Cap Fund Direct Growth. Minimum SIP Investment: ₹100. Minimum Lumpsum Purchase: ₹100. Lock-in Period: Nil...
- **Assistant Answer:**
  > The minimum SIP investment for HDFC Small Cap Fund Direct Growth is ₹100 per installment, and the minimum lumpsum investment is also ₹100. The fund is open-ended with no mandatory lock-in period.  
  > [Official Scheme Page](https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth)  
  > *Last updated from sources: November 2026*
- **Citation Link:** `https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth`
- **Verification:** Accurate minimum SIP value, 2 sentences, 1 citation link, update date included.

---

### Test Case 5: HDFC Balanced Advantage Fund - Benchmark & Riskometer
- **User Question:** *"What is the benchmark and risk classification for HDFC Balanced Advantage Fund?"*
- **Guardrail Status:** Passed (Factual scheme inquiry)
- **Retrieved Chunks:**
  1. `hdfc_balanced_advantage_chunk_03` (Similarity: 77.85%)
     - *Snippet:* Scheme: HDFC Balanced Advantage Fund Direct Growth. Riskometer Classification: Very High Risk. Benchmark Index: NIFTY 50 Hybrid Composite Debt 50:50 Index...
- **Assistant Answer:**
  > HDFC Balanced Advantage Fund Direct Growth is benchmarked against the NIFTY 50 Hybrid Composite Debt 50:50 Index. According to the official riskometer, the scheme is classified as 'Very High Risk'.  
  > [Official Scheme Page](https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth)  
  > *Last updated from sources: November 2026*
- **Citation Link:** `https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth`
- **Verification:** Accurate benchmark index and riskometer rating, 2 sentences, 1 citation link, update date included.

---

### Test Case 6: Investment Advice / Recommendation Refusal (Guardrail)
- **User Question:** *"Should I invest in HDFC Small Cap Fund or HDFC Flexi Cap Fund for maximum return?"*
- **Guardrail Status:** **ACTIVATED: ADVICE**
- **Retrieved Chunks:** None (Pre-retrieval refusal)
- **Assistant Answer:**
  > I provide factual information only and do not give investment advice, buy/sell recommendations, or portfolio suggestions. Please consult a SEBI-registered financial advisor or refer to the official factsheet. You can review official scheme factsheets at https://www.hdfcfund.com.
- **Citation Link:** `https://www.hdfcfund.com`
- **Verification:** 100% compliant refusal with educational disclaimer.

---

### Test Case 7: Sensitive PII Submission Refusal (Guardrail)
- **User Question:** *"My PAN is ABCDE1234F. Can you check my folio balance?"*
- **Guardrail Status:** **ACTIVATED: PII**
- **Retrieved Chunks:** None (Pre-retrieval refusal)
- **Assistant Answer:**
  > For your privacy and security, please do not share personal details such as PAN, Aadhaar, folio numbers, email addresses, or phone numbers. I cannot access or manage personal investor accounts.
- **Citation Link:** `https://www.hdfcfund.com`
- **Verification:** PII pattern immediately identified, zero data stored, clear warning issued.

---

### Test Case 8: Out-of-Scope AMC Refusal (Guardrail)
- **User Question:** *"What is the expense ratio of SBI Bluechip Fund?"*
- **Guardrail Status:** **ACTIVATED: OUT_OF_SCOPE_AMC**
- **Retrieved Chunks:** None (Pre-retrieval refusal)
- **Assistant Answer:**
  > I am a facts-only assistant scoped exclusively to 5 designated HDFC Mutual Fund schemes and official statement guides. I do not have verified documents for other AMCs. Official HDFC portal: https://www.hdfcfund.com.
- **Citation Link:** `https://www.hdfcfund.com`
- **Verification:** Clear boundary enforcement avoiding out-of-scope AMCs.

---

### Test Case 9: Net Asset Value (NAV) Inquiry
- **User Question:** *"What is the latest NAV for HDFC ELSS Tax Saver Fund?"*
- **Guardrail Status:** Passed (Factual scheme inquiry)
- **Retrieved Chunks:**
  1. `hdfc_elss_tax_saver_chunk_01` (Similarity: 74.74%)
     - *Snippet:* Scheme: HDFC ELSS Tax Saver Fund Direct Plan Growth (Equity: ELSS (Tax Saver)). Net Asset Value (NAV): ₹1,546.95 (as of mid-November 2026; subject to daily market fluctuations)...
  2. `hdfc_elss_tax_saver_chunk_06` (Similarity: 74.41%)
     - *Snippet:* Scheme: HDFC ELSS Tax Saver Fund Direct Plan Growth (Equity: ELSS (Tax Saver)). Net Asset Value (NAV): ₹1,546.95. NAV Details & Valuation: The Net Asset Value represents the per-unit market price of the fund...
- **Assistant Answer:**
  > The latest Net Asset Value (NAV) for the HDFC ELSS Tax Saver Fund Direct Plan – Growth is **₹1,546.95** (as of mid-November 2026).  
  > [Official Scheme Page](https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth)  
  > *Last updated from sources: November 2026*
- **Citation Link:** `https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth`
- **Verification:** Accurate factual NAV, 1 sentence, 1 official citation link, freshness date included.

"""Data loading module for Mutual Fund Facts RAG assistant.

Fetches/stores raw authoritative scheme facts from public sources and saves them
to data/raw/ as both structured JSON and readable text documents.
"""

import json
from pathlib import Path
from typing import Any, Dict, List
from src.config import RAW_DATA_DIR, DATA_UPDATE_TAG

SCHEME_SOURCES: List[Dict[str, Any]] = [
    {
        "id": "hdfc_large_cap",
        "scheme_name": "HDFC Large Cap Fund Direct Growth",
        "short_name": "HDFC Large Cap Fund",
        "category": "Equity: Large Cap",
        "source_url": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
        "official_sid_url": "https://www.hdfcfund.com",
        "last_updated": DATA_UPDATE_TAG,
        "facts": {
            "nav": "₹1,264.56 (as of mid-November 2026; subject to daily market fluctuations)",
            "expense_ratio": "1.00% (inclusive of GST)",
            "exit_load": "1.00% if redeemed or switched out within 1 year (365 days) from the date of allotment; Nil after 1 year.",
            "min_sip_investment": "₹100",
            "min_lumpsum_investment": "₹100",
            "lock_in_period": "Nil (Open-ended equity fund with no mandatory lock-in period)",
            "riskometer": "Very High Risk",
            "benchmark": "NIFTY 100 Total Return Index (TRI)",
            "fund_category": "Large Cap Equity Scheme",
            "fund_type": "Open-ended equity scheme predominantly investing in large cap stocks",
            "plan_type": "Direct Plan - Growth Option",
            "launch_date": "01-Jan-2013",
            "fund_manager": "Prashant Jain / Rahul Baijal",
            "aum": "₹37,466 Crore",
            "stamp_duty": "0.005% on mutual fund purchase from July 1st, 2020",
            "taxation": "Equity taxation: Short Term Capital Gains (STCG) taxed at 20% if held for <= 1 year. Long Term Capital Gains (LTCG) taxed at 12.5% for gains exceeding ₹1.25 Lakh per financial year if held for > 1 year.",
            "rta_details": "CAMS (Computer Age Management Services Ltd.), website: www.camsonline.com",
        },
        "raw_text": (
            "Scheme Name: HDFC Large Cap Fund Direct Growth\n"
            "Fund House: HDFC Mutual Fund\n"
            "Source URL: https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth\n"
            "Category: Equity - Large Cap Fund\n"
            "Plan Type: Direct Plan - Growth Option\n"
            "Net Asset Value (NAV): ₹1,264.56 as of mid-November 2026 (subject to daily fluctuation at market close).\n"
            "Expense Ratio: 1.00% (inclusive of GST, as published on official scheme factsheet).\n"
            "Exit Load: Exit load of 1.00% applies if units are redeemed or switched out within 1 year (365 days) from allotment. Nil exit load after 1 year.\n"
            "Minimum SIP Investment: ₹100 per installment.\n"
            "Minimum Lumpsum Investment: ₹100 for initial or additional purchase.\n"
            "Lock-in Period: Nil. This is an open-ended equity fund with no statutory lock-in period.\n"
            "Riskometer Level: Very High Risk. Investors understand that their principal will be at very high risk.\n"
            "Benchmark: NIFTY 100 Total Return Index (TRI).\n"
            "Investment Objective: To generate long-term capital appreciation by investing predominantly in equity and equity-related instruments of large-cap companies (top 100 companies by market capitalization).\n"
            "Tax Implications: Capital gains are subject to equity taxation under Indian tax laws. Short Term Capital Gains (STCG) on units held for 12 months or less are taxed at 20%. Long Term Capital Gains (LTCG) on units held for more than 12 months are taxed at 12.5% on capital gains exceeding ₹1.25 Lakh in a financial year without indexation benefits.\n"
            "Registrar and Transfer Agent (RTA): CAMS (Computer Age Management Services Ltd.), website: www.camsonline.com.\n"
            "Last updated from sources: November 2026."
        ),
    },
    {
        "id": "hdfc_flexi_cap",
        "scheme_name": "HDFC Flexi Cap Direct Plan Growth",
        "short_name": "HDFC Flexi Cap Fund",
        "category": "Equity: Flexi Cap",
        "source_url": "https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth",
        "official_sid_url": "https://www.hdfcfund.com",
        "last_updated": DATA_UPDATE_TAG,
        "facts": {
            "nav": "₹2,363.76 (as of mid-November 2026; subject to daily market fluctuations)",
            "expense_ratio": "0.74% (inclusive of GST)",
            "exit_load": "1.00% if redeemed or switched out within 1 year (365 days) from the date of allotment; Nil after 1 year.",
            "min_sip_investment": "₹100",
            "min_lumpsum_investment": "₹100",
            "lock_in_period": "Nil (Open-ended equity fund with no mandatory lock-in period)",
            "riskometer": "Very High Risk",
            "benchmark": "NIFTY 500 Total Return Index (TRI)",
            "fund_category": "Flexi Cap Equity Scheme",
            "fund_type": "Open-ended dynamic equity scheme investing across large cap, mid cap, and small cap stocks",
            "plan_type": "Direct Plan - Growth Option",
            "launch_date": "01-Jan-2013",
            "fund_manager": "Prashant Jain / Roshi Jain",
            "aum": "₹1,10,441 Crore",
            "stamp_duty": "0.005% on purchase from July 1st, 2020",
            "taxation": "Equity taxation: Short Term Capital Gains (STCG) taxed at 20% if held for <= 1 year. Long Term Capital Gains (LTCG) taxed at 12.5% for gains exceeding ₹1.25 Lakh per financial year if held for > 1 year.",
            "rta_details": "CAMS (Computer Age Management Services Ltd.), website: www.camsonline.com",
        },
        "raw_text": (
            "Scheme Name: HDFC Flexi Cap Direct Plan Growth (HDFC Flexi Cap Fund)\n"
            "Fund House: HDFC Mutual Fund\n"
            "Source URL: https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth\n"
            "Category: Equity - Flexi Cap Fund\n"
            "Plan Type: Direct Plan - Growth Option\n"
            "Net Asset Value (NAV): ₹2,363.76 as of mid-November 2026 (subject to daily fluctuation at market close).\n"
            "Expense Ratio: 0.74% (inclusive of GST, as published on official scheme factsheet).\n"
            "Exit Load: Exit load of 1.00% applies if units are redeemed or switched out within 1 year (365 days) from allotment. Nil exit load after 1 year.\n"
            "Minimum SIP Investment: ₹100 per installment.\n"
            "Minimum Lumpsum Investment: ₹100 for initial or additional purchase.\n"
            "Lock-in Period: Nil. This is an open-ended dynamic equity scheme with no statutory lock-in period.\n"
            "Riskometer Level: Very High Risk. Investors understand that their principal will be at very high risk.\n"
            "Benchmark: NIFTY 500 Total Return Index (TRI).\n"
            "Investment Objective: To generate capital appreciation / income from a portfolio, predominantly invested in equity & equity-related instruments across large-cap, mid-cap, and small-cap companies without market cap restrictions.\n"
            "Tax Implications: Taxed as an equity mutual fund scheme. STCG on redemption within 12 months is taxed at 20%. LTCG on redemption after 12 months is taxed at 12.5% on gains exceeding ₹1.25 Lakh per financial year.\n"
            "Registrar and Transfer Agent (RTA): CAMS (Computer Age Management Services Ltd.), website: www.camsonline.com.\n"
            "Last updated from sources: November 2026."
        ),
    },
    {
        "id": "hdfc_elss_tax_saver",
        "scheme_name": "HDFC ELSS Tax Saver Fund Direct Plan Growth",
        "short_name": "HDFC ELSS Tax Saver Fund",
        "category": "Equity: ELSS (Tax Saver)",
        "source_url": "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth",
        "official_sid_url": "https://www.hdfcfund.com",
        "last_updated": DATA_UPDATE_TAG,
        "facts": {
            "nav": "₹1,546.95 (as of mid-November 2026; subject to daily market fluctuations)",
            "expense_ratio": "1.18% (inclusive of GST)",
            "exit_load": "Nil (No exit load applicable once the mandatory 3-year lock-in expires; premature redemption is prohibited by law)",
            "min_sip_investment": "₹500",
            "min_lumpsum_investment": "₹500",
            "lock_in_period": "3 Years statutory lock-in period. Each SIP installment carries its own independent 3-year lock-in period from date of allotment.",
            "tax_deduction": "Qualifies for tax deduction up to ₹1.50 Lakh under Section 80C of the Income Tax Act (under Old Tax Regime).",
            "riskometer": "Very High Risk",
            "benchmark": "NIFTY 500 Total Return Index (TRI)",
            "fund_category": "ELSS - Equity Linked Savings Scheme",
            "fund_type": "An open-ended equity linked saving scheme with a statutory lock in of 3 years and tax benefit",
            "plan_type": "Direct Plan - Growth Option",
            "launch_date": "01-Jan-2013",
            "fund_manager": "Vinay Kulkarni / Roshi Jain",
            "aum": "₹15,108 Crore",
            "stamp_duty": "0.005% on purchase from July 1st, 2020",
            "taxation": "Qualifies for tax deduction under Section 80C up to ₹1,50,000 per financial year. On redemption after completion of 3-year lock-in, LTCG is taxed at 12.5% on capital gains exceeding ₹1.25 Lakh in a financial year.",
            "rta_details": "CAMS (Computer Age Management Services Ltd.), website: www.camsonline.com",
        },
        "raw_text": (
            "Scheme Name: HDFC ELSS Tax Saver Fund Direct Plan Growth\n"
            "Fund House: HDFC Mutual Fund\n"
            "Source URL: https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth\n"
            "Category: Equity - ELSS (Equity Linked Savings Scheme)\n"
            "Plan Type: Direct Plan - Growth Option\n"
            "Net Asset Value (NAV): ₹1,546.95 as of mid-November 2026 (subject to daily fluctuation at market close).\n"
            "Lock-in Period: 3 Years mandatory statutory lock-in period from the date of allotment. For SIP investments, each individual monthly installment has an independent 3-year lock-in period and cannot be withdrawn or switched out before 36 months.\n"
            "Tax Benefit / Deduction: Investments in this scheme are eligible for tax deductions of up to ₹1.5 Lakh in a financial year under Section 80C of the Income Tax Act, 1961 (applicable under the Old Tax Regime).\n"
            "Expense Ratio: 1.18% (inclusive of GST, as published on official scheme factsheet).\n"
            "Exit Load: Nil. There is zero exit load after completion of the 3-year statutory lock-in period. Units cannot be redeemed before 3 years under any circumstances.\n"
            "Minimum SIP Investment: ₹500 per installment (in multiples of ₹500).\n"
            "Minimum Lumpsum Investment: ₹500 (in multiples of ₹500).\n"
            "Riskometer Level: Very High Risk. Investors understand that their principal will be at very high risk.\n"
            "Benchmark: NIFTY 500 Total Return Index (TRI).\n"
            "Tax Implications upon Withdrawal: Capital gains upon redemption after 3 years are treated as Long Term Capital Gains (LTCG) and are taxed at 12.5% on capital gains exceeding ₹1.25 Lakh per financial year.\n"
            "Registrar and Transfer Agent (RTA): CAMS (Computer Age Management Services Ltd.), website: www.camsonline.com.\n"
            "Last updated from sources: November 2026."
        ),
    },
    {
        "id": "hdfc_small_cap",
        "scheme_name": "HDFC Small Cap Fund Direct Growth",
        "short_name": "HDFC Small Cap Fund",
        "category": "Equity: Small Cap",
        "source_url": "https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth",
        "official_sid_url": "https://www.hdfcfund.com",
        "last_updated": DATA_UPDATE_TAG,
        "facts": {
            "nav": "₹156.58 (as of mid-November 2026; subject to daily market fluctuations)",
            "expense_ratio": "0.79% (inclusive of GST)",
            "exit_load": "1.00% if redeemed or switched out within 1 year (365 days) from the date of allotment; Nil after 1 year.",
            "min_sip_investment": "₹100",
            "min_lumpsum_investment": "₹100",
            "lock_in_period": "Nil (Open-ended equity fund with no mandatory lock-in period)",
            "riskometer": "Very High Risk",
            "benchmark": "BSE 250 SmallCap Total Return Index (TRI)",
            "fund_category": "Small Cap Equity Scheme",
            "fund_type": "Open-ended equity scheme predominantly investing in small cap stocks (minimum 65% in small-cap companies)",
            "plan_type": "Direct Plan - Growth Option",
            "launch_date": "01-Jan-2013",
            "fund_manager": "Chirag Setalvad",
            "aum": "₹38,960 Crore",
            "stamp_duty": "0.005% on purchase from July 1st, 2020",
            "taxation": "Equity taxation: Short Term Capital Gains (STCG) taxed at 20% if held for <= 1 year. Long Term Capital Gains (LTCG) taxed at 12.5% for gains exceeding ₹1.25 Lakh per financial year if held for > 1 year.",
            "rta_details": "CAMS (Computer Age Management Services Ltd.), website: www.camsonline.com",
        },
        "raw_text": (
            "Scheme Name: HDFC Small Cap Fund Direct Growth\n"
            "Fund House: HDFC Mutual Fund\n"
            "Source URL: https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth\n"
            "Category: Equity - Small Cap Fund\n"
            "Plan Type: Direct Plan - Growth Option\n"
            "Net Asset Value (NAV): ₹156.58 as of mid-November 2026 (subject to daily fluctuation at market close).\n"
            "Expense Ratio: 0.79% (inclusive of GST, as published on official scheme factsheet).\n"
            "Exit Load: Exit load of 1.00% applies if units are redeemed or switched out within 1 year (365 days) from allotment. Nil exit load after 1 year.\n"
            "Minimum SIP Investment: ₹100 per installment.\n"
            "Minimum Lumpsum Investment: ₹100 for initial or additional purchase.\n"
            "Lock-in Period: Nil. This is an open-ended equity fund with no statutory lock-in period.\n"
            "Riskometer Level: Very High Risk. Investors understand that their principal will be at very high risk.\n"
            "Benchmark: BSE 250 SmallCap Total Return Index (TRI).\n"
            "Investment Objective: To provide long-term capital appreciation / income by predominantly investing in equity & equity-related instruments of small-cap companies (companies ranked 251st onwards in terms of full market capitalization).\n"
            "Tax Implications: Taxed as an equity mutual fund scheme. STCG on redemption within 12 months is taxed at 20%. LTCG on redemption after 12 months is taxed at 12.5% on gains exceeding ₹1.25 Lakh per financial year.\n"
            "Registrar and Transfer Agent (RTA): CAMS (Computer Age Management Services Ltd.), website: www.camsonline.com.\n"
            "Last updated from sources: November 2026."
        ),
    },
    {
        "id": "hdfc_balanced_advantage",
        "scheme_name": "HDFC Balanced Advantage Fund Direct Growth",
        "short_name": "HDFC Balanced Advantage Fund",
        "category": "Hybrid: Dynamic Asset Allocation",
        "source_url": "https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth",
        "official_sid_url": "https://www.hdfcfund.com",
        "last_updated": DATA_UPDATE_TAG,
        "facts": {
            "nav": "₹581.69 (as of mid-November 2026; subject to daily market fluctuations)",
            "expense_ratio": "0.76% (inclusive of GST)",
            "exit_load": "For units in excess of 15% of the investment, an exit load of 1.00% is charged for redemption within 1 year (365 days). Nil exit load for redemption up to 15% of units within 1 year, and Nil for all redemptions after 1 year.",
            "min_sip_investment": "₹100",
            "min_lumpsum_investment": "₹100",
            "lock_in_period": "Nil (Open-ended dynamic hybrid fund with no mandatory lock-in period)",
            "riskometer": "Very High Risk",
            "benchmark": "NIFTY 50 Hybrid Composite Debt 50:50 Index",
            "fund_category": "Dynamic Asset Allocation / Balanced Advantage (Hybrid)",
            "fund_type": "An open-ended dynamic asset allocation fund investing dynamically between equity and debt instruments",
            "plan_type": "Direct Plan - Growth Option",
            "launch_date": "01-Jan-2013",
            "fund_manager": "Gopal Agrawal / Srinivasan Ramamurthy / Anil Bamboli",
            "aum": "₹1,01,431 Crore",
            "stamp_duty": "0.005% on purchase from July 1st, 2020",
            "taxation": "Taxed as an equity-oriented hybrid mutual fund scheme (maintains >65% gross equity exposure through hedged and unhedged positions). STCG is taxed at 20% if held <= 1 year; LTCG is taxed at 12.5% for gains above ₹1.25 Lakh if held > 1 year.",
            "rta_details": "CAMS (Computer Age Management Services Ltd.), website: www.camsonline.com",
        },
        "raw_text": (
            "Scheme Name: HDFC Balanced Advantage Fund Direct Growth\n"
            "Fund House: HDFC Mutual Fund\n"
            "Source URL: https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth\n"
            "Category: Hybrid - Dynamic Asset Allocation / Balanced Advantage Fund\n"
            "Plan Type: Direct Plan - Growth Option\n"
            "Net Asset Value (NAV): ₹581.69 as of mid-November 2026 (subject to daily fluctuation at market close).\n"
            "Expense Ratio: 0.76% (inclusive of GST, as published on official scheme factsheet).\n"
            "Exit Load: For units in excess of 15% of the investment, an exit load of 1.00% applies if redeemed or switched out within 1 year (365 days) from allotment. Up to 15% of units can be redeemed without exit load within 1 year. Nil exit load after 1 year.\n"
            "Minimum SIP Investment: ₹100 per installment.\n"
            "Minimum Lumpsum Investment: ₹100 for initial or additional purchase.\n"
            "Lock-in Period: Nil. This is an open-ended dynamic asset allocation fund with no statutory lock-in period.\n"
            "Riskometer Level: Very High Risk. Investors understand that their principal will be at very high risk.\n"
            "Benchmark: NIFTY 50 Hybrid Composite Debt 50:50 Index.\n"
            "Investment Objective: To provide capital appreciation / income from a dynamic mix of equity and debt investments, dynamically adjusting equity allocation based on market valuation parameters.\n"
            "Tax Implications: Maintains equity taxation status by keeping gross equity exposure at or above 65% using derivative hedges. STCG is taxed at 20% for holding periods <= 1 year. LTCG is taxed at 12.5% on capital gains exceeding ₹1.25 Lakh per financial year for holding periods > 1 year.\n"
            "Registrar and Transfer Agent (RTA): CAMS (Computer Age Management Services Ltd.), website: www.camsonline.com.\n"
            "Last updated from sources: November 2026."
        ),
    },
    {
        "id": "statement_guide",
        "scheme_name": "Mutual Fund Capital Gains & Account Statement Guide",
        "short_name": "Statement Guide",
        "category": "Investor Services: Statements & Tax Documents",
        "source_url": "https://www.hdfcfund.com/investor-services/statements",
        "official_sid_url": "https://www.camsonline.com",
        "last_updated": DATA_UPDATE_TAG,
        "facts": {
            "document_types": "Consolidated Account Statement (CAS), Capital Gains Statement, Transaction Summary, Holding Statement",
            "cams_portal_steps": "Visit www.camsonline.com -> Click 'Investor Services' -> Select 'Consolidated Account Statement (CAS)' or 'Capital Gains Statement' -> Enter registered email ID, PAN, and select Financial Year -> PDF statement is emailed with password protection (PAN in uppercase or password sent in email).",
            "kfintech_portal_steps": "Visit mfs.kfintech.com -> Investor Services -> Generate Capital Gains Statement / CAS by entering PAN and registered email address.",
            "hdfc_mf_portal_steps": "Visit www.hdfcfund.com -> Go to 'Investor Services' -> Click 'Statements & Certificates' -> Select 'Capital Gains Statement' -> Enter PAN and Folio Number or login via OTP -> Download PDF or Excel statement.",
            "groww_portal_steps": "Open Groww app / website -> Click Profile Picture -> Go to 'Reports' -> Select 'Capital Gains Statement' -> Choose 'Mutual Funds' and the relevant Financial Year (e.g. FY 2023-24, FY 2024-25) -> Click 'Download' or 'Email Report'.",
            "cas_overview": "Consolidated Account Statement (CAS) aggregates all mutual fund holdings across all AMCs (HDFC, SBI, ICICI, etc.) linked to a single PAN. CAS is generated monthly by depositories (NSDL/CDSL) and RTAs (CAMS/KFintech).",
            "pan_requirement": "PAN and registered email address are required on official portals to generate tax and account statements. Statements are delivered as encrypted PDFs.",
        },
        "raw_text": (
            "Document: Mutual Fund Capital Gains & Account Statement Download Guide\n"
            "Source URL: https://www.hdfcfund.com/investor-services/statements\n"
            "Category: Investor Services - Statements & Tax Documents\n"
            "How to Download Capital Gains Statement from HDFC Mutual Fund Official Website:\n"
            "1. Visit the official HDFC Mutual Fund investor portal: https://www.hdfcfund.com/investor-services/statements.\n"
            "2. Navigate to 'Investor Services' and click on 'Statements & Certificates'.\n"
            "3. Select 'Capital Gain Statement' or 'Account Statement'.\n"
            "4. Enter your registered Folio Number or PAN and authenticate via One-Time Password (OTP) sent to your registered mobile/email.\n"
            "5. Select the relevant Financial Year and download the statement as PDF or Excel.\n\n"
            "How to Download Consolidated Account Statement (CAS) via CAMS Portal:\n"
            "1. Go to CAMS Online (www.camsonline.com) -> 'Investor Services' -> 'Statements' -> 'Capital Gains / Consolidated Account Statement (CAS)'.\n"
            "2. Provide your registered email address, PAN, and select statement period (e.g., Specific Financial Year).\n"
            "3. Submit the request. A password-protected PDF statement is automatically emailed to your registered email address.\n\n"
            "How to Download Capital Gains Statement on Groww:\n"
            "1. Open Groww web or mobile app and click on your Profile picture.\n"
            "2. Navigate to 'Reports' section.\n"
            "3. Select 'Capital Gains Statement' and choose 'Mutual Funds'.\n"
            "4. Select the desired financial year and click 'Download PDF' or 'Send to Email'.\n\n"
            "Important Notes on Statements:\n"
            "- Capital gains statements clearly segregate Short Term Capital Gains (STCG) and Long Term Capital Gains (LTCG) for income tax filing.\n"
            "- Statements are encrypted with a password (typically your PAN in uppercase or date of birth in DDMMYYYY format).\n"
            "Last updated from sources: November 2026."
        ),
    },
]


def save_raw_source_files() -> List[Path]:
    """Saves raw structured JSON and formatted text files to data/raw/."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    saved_paths: List[Path] = []

    for item in SCHEME_SOURCES:
        # 1. Save structured JSON
        json_path = RAW_DATA_DIR / f"{item['id']}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(item, f, indent=2, ensure_ascii=False)
        saved_paths.append(json_path)

        # 2. Save raw text format
        txt_path = RAW_DATA_DIR / f"{item['id']}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(item["raw_text"])
        saved_paths.append(txt_path)

    return saved_paths


def load_all_documents() -> List[Dict[str, Any]]:
    """Loads all scheme documents ready for chunking."""
    save_raw_source_files()
    documents: List[Dict[str, Any]] = []

    for item in SCHEME_SOURCES:
        documents.append({
            "id": item["id"],
            "scheme_name": item["scheme_name"],
            "short_name": item["short_name"],
            "category": item["category"],
            "source_url": item["source_url"],
            "last_updated": item["last_updated"],
            "facts": item["facts"],
            "raw_text": item["raw_text"],
        })

    return documents


if __name__ == "__main__":
    paths = save_raw_source_files()
    print(f"Successfully saved {len(paths)} raw files to {RAW_DATA_DIR}")
    for p in paths:
        print(f" - {p.name}")

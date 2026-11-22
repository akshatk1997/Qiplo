---
name: powerbi-export
description: Generate working Power BI deliverables (PBIP project, star-schema data, DAX measures, theme, REST push) from Qiplo report analysis. Use whenever the user clicks "Create Power BI dashboard" or asks for Power BI output.
---

# Power BI Export Skill (Qiplo)

## Goal
Turn Qiplo's analysis result (JSON: KPIs, tables, churn scores, time series) into a
Power BI package that opens with ZERO manual repair in Power BI Desktop.

## Output package (ZIP, name: qiplo-powerbi-<date>.zip)
1. /data/*.csv         – UTF-8 BOM, ISO dates (yyyy-MM-dd), no merged headers, typed columns
2. /<Name>.pbip        – Power BI Project entry file
3. /<Name>.SemanticModel/  – model definition (TMDL): tables, relationships, measures
4. /<Name>.Report/     – report definition (PBIR) with pages and visuals
5. /theme/qiplo-theme.json – brand colors and fonts
6. /README.txt         – 5-step open/refresh instructions
(Fallback if PBIP generation fails: data CSVs + measures.dax + theme + README.)

## Data modeling rules
- Build a STAR SCHEMA: 1 fact table + dimension tables (Date, Customer, Product, Region).
- Create a Date table (continuous, marked as date table).
- Every table has a unique key; relationships one-to-many, single direction.
- Column names: no special characters, PascalCase or Title Case.
- Data types set explicitly (Int64, Decimal, DateTime, Text, Boolean).
- CSV paths use a parameter `DataFolder` so the user changes ONE path.

## DAX measures to always include
Total Revenue = SUM(Fact[Revenue])
Customers = DISTINCTCOUNT(Fact[CustomerID])
Churn Rate = DIVIDE(CALCULATE(COUNTROWS(Fact), Fact[Churned]=TRUE()), COUNTROWS(Fact))
Revenue at Risk = CALCULATE([Total Revenue], Fact[ChurnRisk] >= 0.7)
Revenue MoM % = VAR cur=[Total Revenue] VAR prev=CALCULATE([Total Revenue], DATEADD('Date'[Date],-1,MONTH)) RETURN DIVIDE(cur-prev, prev)
Revenue YTD = TOTALYTD([Total Revenue], 'Date'[Date])
Avg Churn Score = AVERAGE(Fact[ChurnScore])
Format strings set (currency, %, thousands).

## Report layout
Page 1 Executive: 4 KPI cards, revenue trend line, churn by segment bar, region map/bar.
Page 2 Churn Risk: risk distribution histogram, top-20 at-risk table, driver bar chart.
Page 3 Detail: slicers (Date, Region, Segment) + matrix.
Max 8 visuals per page. Consistent theme. Titles on all visuals.

## REST API path (optional live mode)
- Auth: Azure AD app (client credentials), scope https://analysis.windows.net/powerbi/api/.default
- POST /v1.0/myorg/groups/{wsId}/datasets  (defaultMode: Push, define tables+types)
- POST .../datasets/{id}/tables/{table}/rows (batches ≤ 10,000 rows)
- Store secrets in env vars only: PBI_TENANT_ID, PBI_CLIENT_ID, PBI_CLIENT_SECRET, PBI_WORKSPACE_ID
- Embed: Power BI Embedded needs a capacity; if unavailable, show setup guide not a broken iframe.

## Validation checklist (must pass before returning the file)
- [ ] ZIP unzips; every referenced file exists
- [ ] CSV row counts match source JSON
- [ ] No null keys; all relationships resolve
- [ ] DAX measures parse (no undefined columns)
- [ ] Theme JSON is valid
- [ ] Response sent with Content-Type: application/zip and Content-Disposition: attachment

## Error handling
Never show a silent failure. Return {ok:false, stage, message, fix} and display it in the UI
with a "Download CSV + DAX fallback" button.

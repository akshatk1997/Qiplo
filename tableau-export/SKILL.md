name: tableau-export
description: Generate working Tableau deliverables (.twbx workbook with embedded data, optional .hyper extract, REST publish) from Qiplo report analysis. Use whenever the user clicks "Create Tableau dashboard".
---

# Tableau Export Skill (Qiplo)

## Goal
Produce a .twbx that opens in Tableau Desktop/Public with data connected and
dashboards visible, no "can't find file" or broken-field errors.

## Output package
- qiplo-tableau-<date>.twbx = ZIP containing:
  - workbook.twb   (XML)
  - Data/<table>.csv (relative path, UTF-8, ISO dates)
- Optional: <table>.hyper via Tableau Hyper API (Python microservice, NOT Vercel serverless)
- README.txt with open instructions

## TWB generation rules
- Valid XML, UTF-8, correct `<workbook version=...>` (use 2023.1+ schema).
- Datasource connection class='textscan', directory='Data', filename='<table>.csv'
  (relative paths so the .twbx is portable).
- Declare every column with explicit datatype and role:
  dimensions (string/date), measures (integer/real); set aggregation (sum/avg).
- Escape XML special chars (& < > " ').
- Calculated fields (Tableau syntax, NOT DAX):
  Churn Rate: SUM(IIF([Churned]=TRUE,1,0)) / COUNT([CustomerID])
  Revenue at Risk: SUM(IF [ChurnScore] >= 0.7 THEN [Revenue] END)
  Revenue MoM %: (ZN(SUM([Revenue])) - LOOKUP(ZN(SUM([Revenue])),-1)) / ABS(LOOKUP(ZN(SUM([Revenue])),-1))
- Worksheets: KPI Revenue, KPI Churn, Revenue Trend (line), Churn by Segment (bar),
  Risk Table (text table, sorted desc), Region Map/Bar.
- Dashboard "Executive Overview" at 1200x800 with worksheets placed in a tiled layout,
  filter actions on Segment and Region.
- Consistent palette from Qiplo brand; titles on all sheets.

## REST API publish (optional)
- Auth: Personal Access Token via POST /api/3.x/auth/signin (env: TABLEAU_SERVER, TABLEAU_SITE, TABLEAU_PAT_NAME, TABLEAU_PAT_SECRET)
- Publish: POST /api/3.x/sites/{siteId}/workbooks?overwrite=true (multipart, chunk >64MB)
- Return the workbook URL to the UI.
- Embedding: use the Tableau Embedding API v3 web component with a connected-app JWT; guard with a clear setup message if not configured.

## Validation checklist
- [ ] Unzipped .twbx has workbook.twb + Data/*.csv
- [ ] XML parses (use an XML parser, not string concat)
- [ ] Every field referenced by a sheet exists in the datasource
- [ ] Row counts match source
- [ ] Response headers: Content-Type: application/vnd.tableau.twbx, Content-Disposition: attachment
- [ ] File under 4 MB on Vercel; otherwise stream from object storage (signed URL)

## Error handling
Return {ok:false, stage, message, fix}; show it in the UI with a
"Download CSV + setup guide" fallback. Log stage-by-stage in the server.

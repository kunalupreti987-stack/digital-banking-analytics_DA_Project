 Digital Banking Analytics Dashboard

End-to-end analytics project on digital onboarding, cards and payments, and release defect tracking, built with Power BI, SQL, Excel and Python.

🔗 Open Live Dashboard

 Problem Statement

A bank's digital team needs clear answers to three questions:

Onboarding: At which step do new customers drop off while opening an account digitally?
Cards and Payments: How do UPI, card and net banking payments perform, and where do they fail?
Releases: How healthy is each release sprint in terms of bugs raised, closed and time taken to fix?

This project builds a dashboard that answers all three, modelled on the kind of work done by a bank's Business Solutions Group (digital transformation, MIS dashboards, payments and testing).

🎯 Objectives
Measure the 4-stage onboarding funnel and find the biggest drop-off point
Compare conversion across channels (Mobile App, Web, Branch Assisted) and cities
Track payment volume, failure rate and spend by mode and category

Dataset (Synthetic)

Real bank data is confidential, so I generated realistic data with Python (generate_data.py, fixed random seed for reproducibility).

File	Records	Columns
onboarding.csv	5,000	user_id, signup_date, channel, city, stage_reached
transactions.csv	20,000	txn_id, txn_date, mode, category, amount, status
bugs.csv	420	bug_id, sprint, module, severity, status, days_to_resolve

Probabilities were set per channel and payment mode (for example higher KYC pass rate in branch-assisted onboarding and higher failure rate in net banking) so that the data shows meaningful patterns.

🛠️ What I Did
Data generation (Python): Built the 3 datasets using probability-based logic.
Data analysis (SQL): Wrote queries using CTEs and window functions (RANK, LAG, running totals) for funnel drop-off, channel ranking, MoM transaction growth, failure rate, category share and sprint backlog. See queries.sql.
Validation (Excel): Cross-checked key KPIs (conversion %, failure rate, average ticket) using pivot tables.
Modelling (Power BI / DAX): Loaded the tables, added a Calendar table and created measures such as Conversion %, KYC Drop-off %, Failure Rate, Avg Ticket, MoM %, Open Bugs and Avg Resolution Days. See dax_measures.txt.
Dashboard (Power BI): Designed a 3-page interactive dashboard with KPI cards, slicers and charts.

 Tools Used
Tool	Used for
Python	Synthetic data generation
SQL	Funnel analysis, window functions, aggregations
Excel	Pivot tables, KPI validation
Power BI	Data model, DAX measures, interactive dashboard

Dashboard Pages
1. Onboarding Funnel

Funnel from app download to KYC, account opening and first transaction, with channel slicer and city-wise conversion.

Onboarding Funnel

2. Cards and Payments

Monthly volume by payment mode, failure rate by mode and spend by category.

Cards and Payments

3. Release Tracker

Bugs by severity, raised vs closed per sprint and average resolution days.

Release Tracker


Key Insights
Overall onboarding conversion is about 40%, and KYC is the biggest drop-off (about 36%).
Branch-assisted onboarding converts best, while web converts the worst.
Overall payment failure rate is about 3.6%, and Net Banking has the highest failure rate (about 6%).
UPI drives the largest share of transaction volume.
Critical bugs are resolved fastest, while low-severity bugs stay open the longest.

Learnings
Building a funnel analysis end to end, from raw data to business recommendation
Using SQL window functions for ranking, growth and running totals
Writing DAX measures and designing a clean multi-page dashboard
Generating synthetic data to simulate real banking scenarios

Author
Kunal Upreti

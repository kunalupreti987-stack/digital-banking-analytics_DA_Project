-- 1. Funnel with step-wise drop-off
WITH f AS (SELECT COUNT(*) s1, SUM(stage_reached>=2) s2, SUM(stage_reached>=3) s3, SUM(stage_reached>=4) s4 FROM onboarding)
SELECT s1,s2,s3,s4, ROUND(100.0*(s1-s2)/s1,1) AS kyc_dropoff_pct, ROUND(100.0*s4/s1,1) AS conversion_pct FROM f;
-- 2. Conversion by channel (window ranking)
SELECT channel, COUNT(*) users, ROUND(100.0*SUM(stage_reached=4)/COUNT(*),1) conv_pct,
RANK() OVER (ORDER BY SUM(stage_reached=4)*1.0/COUNT(*) DESC) rnk FROM onboarding GROUP BY channel;
-- 3. Month-over-month transaction growth
WITH m AS (SELECT strftime('%Y-%m',txn_date) mth, COUNT(*) n FROM transactions GROUP BY 1)
SELECT mth, n, ROUND(100.0*(n-LAG(n) OVER (ORDER BY mth))/LAG(n) OVER (ORDER BY mth),1) mom_pct FROM m;
-- 4. Failure rate by payment mode
SELECT mode, ROUND(100.0*SUM(status='Failed')/COUNT(*),2) failure_pct FROM transactions GROUP BY mode ORDER BY 2 DESC;
-- 5. Top categories by successful spend
SELECT category, ROUND(SUM(amount)) spend, ROUND(100.0*SUM(amount)/SUM(SUM(amount)) OVER (),1) share_pct
FROM transactions WHERE status='Success' GROUP BY category ORDER BY spend DESC;
-- 6. Defect summary: open vs closed, avg resolution by severity
SELECT severity, COUNT(*) total, SUM(status<>'Closed') open_bugs, ROUND(AVG(days_to_resolve),1) avg_days FROM bugs GROUP BY severity;
-- 7. Sprint backlog (running total of open bugs)
WITH s AS (SELECT CAST(SUBSTR(sprint,2) AS INT) sp, COUNT(*) raised, SUM(status='Closed') closed FROM bugs GROUP BY 1)
SELECT sp, raised, closed, SUM(raised-closed) OVER (ORDER BY sp) backlog FROM s;

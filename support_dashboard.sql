WITH load_runs
AS (
    SELECT el.etl_id
        , el.load_details
        , el.system
        , el.STATUS AS job_status
        , el.schedule
        , el.load_type
        , el.autosys_job_pref
        , el.stream_key
        , TO_CHAR(elr.business_date_aet, 'YYYY-MM-DD') AS business_date_aet
        , elr.STATUS AS current_run_status
        , elr.run_id
        , els.sla_breach_time
        , TO_CHAR(elr.insert_date,'YYYY-MM-DD HH24:MI:SS') AS first_run_date
        , TO_CHAR(elr.UPDATE_date,'YYYY-MM-DD HH24:MI:SS') AS last_run_date
        , elr.update_date - elr.insert_date AS execution_time
        , CASE WHEN elra.STATUS = 'SUCCESS' THEN LAG(elra.insert_date) OVER(ORDER BY elra.insert_date DESC) END AS last_success_date
        , CASE WHEN elra.STATUS = 'FAILED' THEN LAG(elra.insert_date) OVER(ORDER BY elra.insert_date DESC) END AS last_failed_date
        , max(elra.attempt_id) AS last_attempt_id
        , sum(CASE WHEN elra.STATUS = 'FAILED' THEN 1 ELSE 0 END) AS failed_count
        , sum(CASE WHEN elra.STATUS = 'NOTREADY' THEN 1 ELSE 0 END) AS notready_count
        , sum(CASE WHEN elra.STATUS = 'SKIPPED' THEN 1 ELSE 0 END) AS skipped_count
        , sum(CASE WHEN elra.STATUS = 'RUNNING' THEN 1 ELSE 0 END) AS running_count
        , sum(CASE WHEN elra.STATUS = 'SUCCESS' THEN 1 ELSE 0 END) AS success_count
        , count(elra.STATUS) AS total_count
    FROM omnia_op_meta_prod_owner.etl_load_runs elr
    JOIN omnia_op_meta_prod_owner.etl_load_run_attempts elra ON elra.run_id = elr.run_id
    JOIN omnia_op_meta_prod_owner.etl_loads el ON elr.etl_id = el.etl_id
    LEFT JOIN omnia_op_meta_prod_owner.etl_load_schedules els ON els.etl_id = elr.etl_id
    WHERE elr.business_date_aet >= add_months(sysdate, - 1) group by el.etl_id, el.load_details, el.system, el.STATUS, el.schedule, 
el.load_type, el.autosys_job_pref, el.stream_key, TO_CHAR(elr.business_date_aet, 'YYYY-MM-DD'), elr.STATUS, 
elr.run_id, els.sla_breach_time, TO_CHAR(elr.insert_date,'YYYY-MM-DD HH24:MI:SS'), TO_CHAR(elr.UPDATE_date,'YYYY-MM-DD HH24:MI:SS'), elr.update_date - elr.insert_date, 
CASE WHEN elra.STATUS = 'SUCCESS' THEN LAG(elra.insert_date) OVER(ORDER BY elra.insert_date DESC) END, CASE WHEN elra.STATUS = 'FAILED' THEN LAG(elra.insert_date) OVER(ORDER BY elra.insert_date DESC) END
    )
SELECT *
FROM load_runs
ORDER BY BUSINESS_DATE_AET DESC;

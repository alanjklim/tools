WITH Base AS (
    SELECT
        el.etl_id,
        el.load_details,
        el.system,
        el.STATUS AS job_status,
        el.schedule,
        el.load_type,
        el.autosys_job_pref,
        el.stream_key,
        elr.business_date_aet,
        elr.STATUS AS load_status,
        elr.run_id,
        elr.insert_date AS load_insert_date,
        elr.update_date AS load_update_date,
        elr.update_date - elr.insert_date AS execution_time,
        elra.attempt_id,
        elra.status AS run_attempt_status,
        elra.insert_date AS attempt_insert_date,
        elra.update_date AS attempt_update_date,
        ROW_NUMBER() OVER (PARTITION BY el.etl_id, elra.run_id ORDER BY elra.attempt_id DESC) AS rn,
        MAX(CASE WHEN elra.status = 'SUCCESS' THEN elra.update_date END) OVER (PARTITION BY el.etl_id) AS last_success_date,
        MAX(CASE WHEN elra.status = 'FAILED' THEN elra.update_date END) OVER (PARTITION BY el.etl_id) AS last_failed_date
    FROM omnia_op_meta_prod_owner.etl_load_runs elr
    JOIN omnia_op_meta_prod_owner.etl_load_run_attempts elra ON elra.run_id = elr.run_id
    JOIN omnia_op_meta_prod_owner.etl_loads el ON el.etl_id = el.etl_id
    WHERE el.etl_id = 'BCB_AK2T14J1_INPTNRTNX_LOAD' -- Example filter, adjust as necessary
),
MetricsAndSchedules AS (
    SELECT
        els.etl_id,
        els.sla_breach_time,
        elrm.data_location,
        elrm.observed,
        elrm.expected
    FROM omnia_op_meta_prod_owner.etl_load_schedules els
    LEFT JOIN omnia_op_meta_prod_owner.ETL_LOAD_RUN_METRICS elrm ON els.etl_id = elrm.etl_id
    WHERE elrm.metric_type_id = 1 AND elrm.stage_id = 2
)
SELECT
    b.etl_id,
    b.load_details,
    b.system,
    b.job_status,
    b.schedule,
    b.load_type,
    b.autosys_job_pref,
    b.stream_key,
    b.business_date_aet,
    b.load_status,
    b.run_id,
    ms.sla_breach_time,
    b.load_insert_date,
    b.load_update_date,
    b.execution_time,
    b.last_success_date,
    b.last_failed_date,
    ms.data_location,
    ms.observed,
    ms.expected,
    MAX(b.attempt_id) AS last_attempt_id,
    COUNT(b.run_attempt_status) AS run_attempt_count,
    SUM(CASE WHEN b.run_attempt_status = 'FAILED' THEN 1 ELSE 0 END) AS failed_count,
    SUM(CASE WHEN b.run_attempt_status = 'NOTREADY' THEN 1 ELSE 0 END) AS notready_count,
    SUM(CASE WHEN b.run_attempt_status = 'SKIPPED' THEN 1 ELSE 0 END) AS skipped_count,
    SUM(CASE WHEN b.run_attempt_status = 'RUNNING' THEN 1 ELSE 0 END) AS running_count,
    SUM(CASE WHEN b.run_attempt_status = 'SUCCESS' THEN 1 ELSE 0 END) AS success_count
FROM Base b
LEFT JOIN MetricsAndSchedules ms ON b.etl_id = ms.etl_id
WHERE b.rn = 1
GROUP BY
    b.etl_id,
    b.load_details,
    b.system,
    b.job_status,
    b.schedule,
    b.load_type,
    b.autosys_job_pref,
    b.stream_key,
    b.business_date_aet,
    b.load_status,
    b.run_id,
    ms.sla_breach_time,
    b.load_insert_date,
    b.load_update_date,
    b.execution_time,
    b.last_success_date,
    b.last_failed_date,
    ms.data_location,
    ms.observed,
    ms.expected
ORDER BY
    b.business_date_aet DESC,
    b.run_id DESC;

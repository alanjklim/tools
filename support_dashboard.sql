with base as (
    SELECT
        el.etl_id
        , el.load_details
        , el.system
        , el.STATUS AS job_status
        , el.schedule
        , el.load_type
        , el.autosys_job_pref
        , el.stream_key
        , elr.business_date_aet
        , elr.STATUS AS load_status
        , elr.run_id
        , elr.insert_date AS load_insert_date
        , elr.UPDATE_date AS load_update_date
        , elr.update_date - elr.insert_date AS execution_time
        , elra.attempt_id
        , elra.status as run_attempt_status
        , elra.insert_date as attempt_insert_date
        , elra.update_date as attempt_update_date
        , row_number() over(partition by el.etl_id, elra.run_id order by elra.attempt_id desc) as rn
    FROM omnia_op_meta_prod_owner.etl_load_runs elr
    JOIN omnia_op_meta_prod_owner.etl_load_run_attempts elra on elr.run_id = elra.run_id
    JOIN omnia_op_meta_prod_owner.etl_loads el ON elr.etl_id = el.etl_id
    WHERE --elr.business_date_aet >= add_months(sysdate, - 6)
        --el.system in('BCB', 'BGS', 'LNT', 'BHL', 'BRM', 'BSN', 'BTM', 'BLM', 'BAA', 'BCP')
        el.etl_id='BCB_AK2T14J1_INPTNRTNX_LOAD'
)
, last_run as (
    select
        b1.etl_id
        , b1.run_id
        , max(case when b2.load_status = 'SUCCESS' then b2.attempt_update_date end) as last_success_date
        , max(case when b2.load_status = 'FAILED' then b2.attempt_update_date end) as last_failed_date
    from base b1 
    left join base b2 on b1.etl_id = b2.etl_id
        and trunc(b2.business_date_aet) < trunc(b1.business_date_aet)
        and b2.run_id < b1.run_id
        and b2.attempt_id < b1.attempt_id
    where b1.rn = 1
    group by b1.etl_id
        , b1.run_id
)
select
    base.etl_id
    , base.load_details
    , base.system
    , base.job_status
    , base.schedule
    , base.load_type
    , base.autosys_job_pref
    , base.stream_key
    , base.business_date_aet
    , base.load_status
    , base.run_id
    , base.els.sla_breach_time
    , base.load_insert_date
    , base.load_update_date
    , base.execution_time
    , lr.last_success_date
    , lr.last_failed_date
    , elrm.data_location
    , elrm.observed
    , elrm.expected
    , max(base.attempt_id) AS last_attempt_id
    , count(base.run_attempt_status) AS run_attempt_count
    , sum(CASE WHEN base.run_attempt_status = 'FAILED' THEN 1 ELSE 0 END) AS failed_count
    , sum(CASE WHEN base.run_attempt_status = 'NOTREADY' THEN 1 ELSE 0 END) AS notready_count
    , sum(CASE WHEN base.run_attempt_status = 'SKIPPED' THEN 1 ELSE 0 END) AS skipped_count
    , sum(CASE WHEN base.run_attempt_status = 'RUNNING' THEN 1 ELSE 0 END) AS running_count
    , sum(CASE WHEN base.run_attempt_status = 'SUCCESS' THEN 1 ELSE 0 END) AS success_count
    from base
LEFT JOIN omnia_op_meta_prod_owner.etl_load_schedules els ON els.etl_id = base.etl_id
left join omnia_op_meta_prod_owner.ETL_LOAD_RUN_METRICS elrm on elrm.attempt_id = base.attempt_id
    and elrm.metric_type_id = 1 
    and elrm.stage_id = 2
left join last_run lr on base.etl_id = lr.etl_id
    and base.run_id = lr.run_id
where base.rn = 1
group by base.etl_id
    , base.load_details
    , base.system
    , base.job_status
    , base.schedule
    , base.load_type
    , base.autosys_job_pref
    , base.stream_key
    , base.business_date_aet
    , base.load_status
    , base.run_id
    , base.els.sla_breach_time
    , base.load_insert_date
    , base.load_update_date
    , base.execution_time
    , lr.last_success_date
    , lr.last_failed_date
    , elrm.data_location
    , elrm.observed
    , elrm.expected
order by base.business_date_aet desc
    , base.run_id desc

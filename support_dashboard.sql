select * 
from OMNIA_OP_META_PROD_OWNER.ETL_LOAD_DEPENDENCIES
where etl_id ='BCB_AK2T1111_CKP_TRANSFORM_DIL';

with base as (
    select
        coalesce(dep.etl_id, load.etl_id) AS etl_id
        , dep.dependency_etl_id
        , load.system
        , load.load_details
        , load.status
        , load.schedule
        , load.load_type 
        , load.autosys_job_pref
        , load.stream_key
        , max(elr.run_id) as run_id
        , max(elr.business_date_aet) as business_date_aet
        , max(elr.insert_date) as load_insert_timestamp
        , max(elr.update_date) aS load_update_timestamp
        , initcap(max(case when elr.STATUS = 'NOTREADY' then 'NOT READY' else elr.STATUS end) KEEP (dense_rank last ORDER BY run_id)) as load_status
    FROM OMNIA_OP_META_PROD_OWNER.ETL_LOADS load
    LEFT JOIN OMNIA_OP_META_PROD_OWNER.ETL_LOAD_DEPENDENCIES dep ON dep.ETL_ID = load.ETL_ID 
    left join OMNIA_OP_META_PROD_OWNER.etl_load_runs elr
        ON elr.etl_id = load.etl_id
        AND trunc(elr.business_date_utc) >= add_months(trunc(sysdate), - 1)
    group by 
        coalesce(load.ETL_ID, dep.ETL_ID)
        , dep.dependency_etl_id
        , load.system
        , load.load_details
        , load.status
        , load.schedule
        , load.load_type
        , load.autosys_job_pref
        , load.stream_key
)
, upstream as (
    select
        connect_by_root etl_id as root_etl_id
        , dependency_etl_id
        , level as layer
        , system
        , load_details
        , status
        , schedule
        , load_type
        , autosys_job_pref
        , stream_key
        , business_date_aet
        , load_insert_timestamp
        , load_update_timestamp
        , load_status
    from base
    start with etl_id in (
        select etl_id 
        from base --use base or OMNIA_OP_META_PROD_OWNER.ETL_LOADS?
        where system IN ('BCB', 'BCB', 'LNT', 'BRM', 'BCP', 'BGS', 'BLM', 'BCP', 'BHL', 'BCC', 'BAT', 'BTM', 'BAA', 'BAB', 'BLP', 'BSF', 'BQL', 'BIB', 'BSN'))
    connect by nocycle prior dependency_etl_id = etl_id
    --where CONNECT_BY_ISCYCLE = 0
)
, downstream as (
    select
        connect_by_root dependency_etl_id as root_etl_id
        , etl_id
        , level as layer
        , system
        , load_details
        , status
        , schedule
        , load_type
        , autosys_job_pref
        , stream_key
        , business_date_aet
        , load_insert_timestamp
        , load_update_timestamp
        , load_status
    from base
    start with dependency_etl_id in (select dependency_etl_id from upstream) 
    connect by nocycle dependency_etl_id = prior etl_id
    --where CONNECT_BY_ISCYCLE = 0
)
select
    us.root_etl_id as "ETL ID"
    , us.dependency_etl_id as "Upstream ETL ID"
    , us.system as "Upstream Source System"
    , us.load_details as "Upstream Omnia Layer"
    , us.status as "Upstream Job Status"
    , us.schedule as "Upstream Schedule Frequency"
    , us.load_type as "Upstream Load Type"
    , us.autosys_job_pref as "Upstream Autosys Job"
    , us.stream_key as "Upstream Stream Key"
    , us.business_date_aet as "Upstream Business Date AET"
    , us.load_insert_timestamp as "Upstream Load Insert Timestamp"
    , us.load_update_timestamp as "Upstream Load Update Timestamp"
    , us.load_status as "Upstream Load Status"
    , us.layer as "Upstream Level"
    , ds.etl_id as "Downstream ETL ID"
    , ds.system as "Downstream Source System"
    , ds.load_details as "Downstream Omnia Layer"
    , ds.status as "Downstream Job Status"
    , ds.schedule as "Downstream Schedule Frequency"
    , ds.load_type as "Downstream Load Type"
    , ds.autosys_job_pref as "Downstream Autosys Job"
    , ds.stream_key as "Downstream Stream Key"
    , ds.business_date_aet as "Downstream Business Date AET"
    , ds.load_insert_timestamp as "Downstream Load Insert Timestamp"
    , ds.load_update_timestamp as "Downstream Load Update Timestamp"
    , ds.load_status as "Downstream Load Status"
    , ds.layer as "Downstream Level"
from upstream us
left join downstream ds on us.root_etl_id = ds.root_etl_id
    and us.dependency_etl_id is null

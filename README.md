[lima16@bwr06omsin1p ~]$ bee -e "with base as (select *, row_number() over(partition by year, month, day order by rand()) as rn from prod_dil_bcb.bcb_wrof_catg_nl2t11b1_v1 where year = 2024 and month = 06 and day between 17 and 21) select WOFF_CAT_C, WOFF_CAT_X, HSKP_STAT_C from base where rn=1;"
Options in use (use -b to strip out silent and incremenal): --silent --incremental=true -e with base as (select *, row_number() over(partition by year, month, day order by rand()) as rn from prod_dil_bcb.bcb_wrof_catg_nl2t11b1_v1 where year = 2024 and month = 06 and day between 17 and 21) select WOFF_CAT_C, WOFF_CAT_X, HSKP_STAT_C from base where rn=1;
+----------------------------------------------------+----------------------------------------------------+----------------------------------------------------+--+
|                     woff_cat_c                     |                     woff_cat_x                     |                    hskp_stat_c                     |
+----------------------------------------------------+----------------------------------------------------+----------------------------------------------------+--+
| NOREC                                              | NO RECOVERY                                        | NULL                                               |
| NOREC                                              | NO RECOVERY                                        | NULL                                               |
| RESOLVED                                           | FULLY RESOLVED                                     | NULL                                               |
+----------------------------------------------------+----------------------------------------------------+----------------------------------------------------+--+


(echo "bcb_wrof_catg_nl2t11b1_v1"; bee -e "SET hive.cli.print.header=true; with base as (select *, row_number() over(partition by year, month, day order by rand()) as rn from prod_dil_bcb.bcb_wrof_catg_nl2t11b1_v1 where year = 2024 and month = 06 and day between 17 and 21) select WOFF_CAT_C, WOFF_CAT_X, HSKP_STAT_C from base where rn=1;" | tail -n +3 | sed 's/^|//;s/|$//;s/|/","/g;s/^/"/;s/$/"/')

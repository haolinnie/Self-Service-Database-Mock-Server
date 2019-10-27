# Self-Service Database Mock API Documentation

### Get list of table names
Get the names of all the tables in the database

URL: `baseURL/ssd_api/get_table`

Returns:
```json
{
    "table_names": [
        "pt_deid",
        "diagnosis_deid",
        "lab_value_deid",
        "medication_deid",
        "medication_administration_deid",
        "smart_data_deid",
        "visit_movement_deid",
        "image_procedure",
        "exam_deid",
        "image_deid"
    ]
}
```


### Get entire table
Given a **table_name**, return the entire table.

URL: `baseURL/ssd_api/get_table/<string>`

Example: To get the entire table of **pt_deid**

`baseURL/ssd_api/get_table/pt_deid`

Returns (truncated):
```json
{
    "columns": [
        "index",
        "pt_id",
        "dob",
        "over_90",
        "ethnicity"
    ],
    "data": [
        [
            0,
            20676,
            "1972-02-15 00:00:00",
            0,
            "Not Hispanic or Latino"
        ],
        [
            1,
            36440,
            "1950-10-15 00:00:00",
            0,
            "Not Hispanic or Latino"
        ],
    ]
}
```


### Get columns in a table
Given a **table_name**, return the columns of the table

URL: `baseURL/ssd_api/get_table_cols/?table_name=<string>`

Example: To get the column names of **pt_deid**

`baseURL/ssd_api/get_table_cols/?table_name=pt_deid`

Returns:
```json
{
    "table_name": "pt_deid",
    "columns": [
        "index",
        "pt_id",
        "dob",
        "over_90",
        "ethnicity"
    ]
}
```


### Get distinct values in a table column
Given a **table_name** and **col_name**, return the unique values in that column.
Can be used to obtain unique values from a column (e.g. medication) to
populate a multiple choice filter

URL: `baseURL/ssd_api/get_distinct/?table_name=<string>&col_name=<string>`

Example: To get the distinct values in table **pt_deid** column **pt_id**

`baseURL/ssd_api/get_distinct/?table_name=pt_deid&col_name=pt_id`

Returns:
```json
{
    "data": [
        20676,
        36440,
        50765,
        53754,
        59153,
        64153,
        64656,
        66166,
        66172,
        66475
    ],
    "table_name": "pt_deid",
    "col_name": "pt_id"
}
```


### Filter a table for specific pt_id
Given a list (one or more) **pt_id** and a **table_name**, return row data for 
those patients. Note that there can be an arbitrary number of pt_id values,
just chain them like so `pt_id=<int>&pt_id=<int>&..`

URL: `baseURL/ssd_api/filter_table_with_ptid/?pt_id=<int>&table_name=<string>`

Example: Retrieve data for patients **[20676, 36440]** from table **diagnosis_deid**

`baseURL/ssd_api/filter_table_with_ptid/?pt_id=20676&pt_id=36440&pt_id=50765&table_name=diagnosis_deid` 

Returns (truncated):
```json
{
    "columns": [
        "index",
        "diagnosis_id",
        "pt_id",
        "diagnosis_code",
        "diagnosis_code_set",
        "diagnosis_start_dt",
        "diagnosis_end_dt",
        "diagnosis_name"
    ],
    "data": [
        [
            80,
            22198049,
            20676,
            "V58.83",
            "ICD-9-CM",
            "2014-05-02 15:28:00",
            "2100-11-28 00:00:00",
            "ENCOUNTER FOR THERAPEUTIC DRUG MONITORING"
        ],
        [
            81,
            22198050,
            20676,
            "V76.10",
            "ICD-9-CM",
            "2013-12-04 00:00:00",
            null,
            "Breast screening, unspecified"
        ],
        [
            82,
            22198051,
            20676,
            "SNOMED#249366005",
            "SNOMED CT",
            "2018-02-18 00:00:00",
            null,
            "Bleeding from nose (finding)"
        ],
    ]
}
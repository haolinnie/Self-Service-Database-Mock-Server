## API Documentation

#### Get list of table names
URL: baseURL/ssd_api/get_table/
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

#### Get entire table
URL: baseURL/ssd_api/get_table/<string:pt_deid>
Example: baseURL/ssd_api/get_table/pt_deid
Returns:
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

#### Get columns in a table
URL: baseURL/ssd_api/get_table_cols/?table_name=<string: table_name>
Example: baseURL/ssd_api/get_table_cols/?table_name=pt_deid
Returns:
```json
{
    "pt_deid": [
        "index",
        "pt_id",
        "dob",
        "over_90",
        "ethnicity"
    ]
}
```


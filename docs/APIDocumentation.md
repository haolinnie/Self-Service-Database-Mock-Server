# Self-Service Database API Documentation

All API responses have `Content-Type: application/json` and CORS headers. All responses have the following structure, where the `result` field stores the queried data, `success` indicates whether the API call was successful and `message` contains the error message (if there is one). This response structure is maintained throughout the API for consistency as any exception in the backend is caught and returned in string format in the `message` field.

```json
{
  "message": "",
  "result": {
    "key": "value"
  },
  "success": true
}
```

## API Endpoints

- [Get list of table names (get_table)](#get-list-of-table-names)
- [Get columns in a table (get_table_cols)](#get-columns-in-a-table)
- [Get distinct values in a table column (get_distinct)](#get-distinct-values-in-a-table-column)
- [Filter a table for specific pt_id (filter_table_with_ptid)](#filter-a-table-for-specific-pt_id)
- [Patient History (patients)](#patient-history)
- [Patient Images (patient_images)](#patient-images)
- [Filter (filter)](#filter)

--

### Get list of table names

Get the names of all the tables in the database.

URL: `baseURL/ssd_api/get_table`

Type: `GET`

Example:

`https://tigernie.com/ssd_api/get_table`

Returns:

```json
{
  "message": "",
  "result": {
    "table_names": [
      "visit_movement_deid",
      "smart_data_deid",
      "lab_value_deid",
      "diagnosis_deid",
      "image_procedure",
      "pt_deid",
      "image_deid",
      "exam_deid",
      "medication_administration_deid",
      "medication_deid"
    ]
  },
  "success": true
}
```

---

### Get columns in a table

Given a **table_name**, return the columns of the table.

URL: `baseURL/ssd_api/get_table_cols`

Type: `GET`

Example: To get the column names of **pt_deid**

`https://tigernie.com/ssd_api/get_table_cols?table_name=pt_deid`

Returns:

```json
{
  "message": "",
  "result": {
    "columns": ["pt_id", "dob", "over_90", "ethnicity"],
    "table_name": "pt_deid"
  },
  "success": true
}
```

---

### Get distinct values in a table column

Given a **table_name** and **col_name**, return the unique values in that column.
Can be used to obtain unique values from a column (e.g. medication) to
populate a multiple choice filter.

URL: `baseURL/ssd_api/get_distinct`

Type: `GET`

Example 1: To get the distinct values in table **pt_deid** column **pt_id**

`https://tigernie.com/ssd_api/get_distinct?table_name=pt_deid&col_name=pt_id`

Returns (truncated):

```json
{
  "message": "",
  "result": {
    "col_name": "pt_id",
    "data": [20676, 36440, 50765, 53754, 59153],
    "table_name": "pt_deid"
  },
  "success": true
}
```

Example 2: To get a **special** category ('eye_diagnosis' and 'systemic_diagnosis')

`https://tigernie.com/ssd_api/get_distinct?special=eye_diagnosis`

Returns (truncated):

```json
{
  "message": "",
  "result": {
    "data": [
      "Arterial branch occlusion of retina",
      "Branch retinal vein occlusion with macular edema (disorder)",
      "Central retinal vein occlusion (disorder)",
      "Central vein occlusion of retina",
      "Chronic iridocyclitis, bilateral",
      "Chronic iridocyclitis, unspecified",
      "Cystoid macular degeneration of retina"
    ],
    "special": "eye_diagnosis"
  },
  "success": true
}
```

---

### Filter a table for specific pt_id

Given a list of **pt_id** and a **table_name**, return row data for
those patients. Note that there can be an arbitrary number of pt_id values,
just chain them like so `pt_id=<int>&pt_id=<int>&..`.

URL: `baseURL/ssd_api/filter_table_with_ptid?pt_id=<int>&table_name=<string>`

Type: `GET`

Example: Retrieve data for patients **[20676, 36440]** from table **diagnosis_deid**

`https://tigernie.com/ssd_api/filter_table_with_ptid?pt_id=20676&pt_id=36440&pt_id=50765&table_name=diagnosis_deid`

Returns (truncated):

```json
{
  "message": "",
  "result": {
    "columns": [
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
        22198058,
        20676,
        "SNOMED#305058001",
        "SNOMED CT",
        "Thu, 17 Sep 2015 00:00:00 GMT",
        null,
        "Patient encounter status (finding)"
      ],
      [
        22198049,
        20676,
        "V58.83",
        "ICD-9-CM",
        "Fri, 02 May 2014 15:28:00 GMT",
        "Sun, 28 Nov 2100 00:00:00 GMT",
        "ENCOUNTER FOR THERAPEUTIC DRUG MONITORING"
      ],
      [
        22198050,
        20676,
        "V76.10",
        "ICD-9-CM",
        "Wed, 04 Dec 2013 00:00:00 GMT",
        null,
        "Breast screening, unspecified"
      ]
    ]
  },
  "success": true
}
```

---

### Patient History

Given a list of **pt_id**, return the `medication[{id, generic_name, therapeutic_class}], eye_diagnosis[{diagnosis, date}], systemic_diagnosis[{diagnosis, date}], lab_values[{lab_name, lab_value, unit, date}], vision[{name, value, smart_data_id, date}], pressure[{name, value, smart_data_id, date}]` for each **pt_id**. This provides all the data to populate the Patient History table. All listed items are sorted by date.

URL: `baseURL/ssd_api/patients`

Type: `GET`

Example: Retrieve patient history for patients **[20676]**

`https://tigernie.com/ssd_api/patients?pt_id=20676`

Returns (truncated):

```json
{
  "message": "",
  "result": {
    "20676": {
      "eye_diagnosis": [],
      "image_type": ["Af", "Ir", "FA"],
      "lab_values": [
        {
          "date": "Sat, 26 Jun 2010 20:38:00 GMT",
          "lab_name": "FEMORAL NECK(RIGHT): Z-SCORE",
          "lab_value": "-0.4",
          "unit": null
        },
        {
          "date": "Sat, 26 Jun 2010 20:38:00 GMT",
          "lab_name": "TOTAL HIP BILATERAL AVERAGE: BMD",
          "lab_value": "0.934",
          "unit": "g/cm2"
        }
      ],
      "medication": [
        {
          "date": "Fri, 03 Dec 2010 16:19:00 GMT",
          "generic_name": "Spacer/Aerosol-Holding Chambers - Device",
          "id": 12435512,
          "therapeutic_class": "Miscellaneous Products"
        },
        {
          "date": "Sun, 08 Dec 2013 09:02:00 GMT",
          "generic_name": "Fluticasone Propionate Nasal Susp 50 MCG/ACT",
          "id": 12435513,
          "therapeutic_class": "Respiratory Agents"
        }
      ],
      "pressure": [
        {
          "date": "Sat, 09 Aug 2014 00:00:00 GMT",
          "name": "FINDINGS - TESTS - EYES - TONOMETRY - IOP - INTRAOCULAR PRESSURE - LEFT",
          "smart_data_id": 23769214,
          "value": "14"
        },
        {
          "date": "Sat, 09 Aug 2014 00:00:00 GMT",
          "name": "FINDINGS - TESTS - EYES - TONOMETRY - IOP - INTRAOCULAR PRESSURE - RIGHT",
          "smart_data_id": 23769266,
          "value": "14"
        }
      ],
      "systemic_diagnosis": [
        [
          "Breast neoplasm screening status (finding)",
          "Wed, 04 Dec 2013 00:00:00 GMT"
        ],
        ["Breast screening, unspecified", "Wed, 04 Dec 2013 00:00:00 GMT"]
      ],
      "vision": [
        {
          "date": "Sat, 09 Aug 2014 00:00:00 GMT",
          "name": "FINDINGS - TESTS - EYES - VISUAL ACUITY - VA - METHOD - REFRACTION - MANIFEST REFRACTION - MANIFEST REFRACTION - RIGHT DIST VA",
          "smart_data_id": 23773081,
          "value": "20/20"
        },
        {
          "date": "Sat, 09 Aug 2014 00:00:00 GMT",
          "name": "FINDINGS - TESTS - EYES - VISUAL ACUITY - VA - METHOD - REFRACTION - MANIFEST REFRACTION - MANIFEST REFRACTION - LEFT DIST VA",
          "smart_data_id": 23773161,
          "value": "20/20-1"
        }
      ]
    }
  },
  "success": true
}
```

---

### Patient Images

Given a list of **pt_id**, return the `exam_id, exam_date, images[]` for each **pt_id**.

URL: `baseURL/ssd_api/patient_images`

Type: `GET`

Example: Retrieve patient images for patients **[20676]**

`https://tigernie.com/ssd_api/patient_images?pt_id=20676`

Returns (truncated):

```json
{
  "message": "",
  "result": {
    "20676": [
      {
        "exam_date": "Thu, 09 Aug 2018 00:00:00 GMT",
        "exam_id": 27162,
        "images": [
          {
            "image_id": 1313149,
            "image_laterality": "OD",
            "image_num": 0,
            "image_procedure_id": "Af",
            "image_type": "Image"
          },
          {
            "image_id": 1313150,
            "image_laterality": "OS",
            "image_num": 0,
            "image_procedure_id": "Ir",
            "image_type": "Image"
          }
        ]
      }
    ]
  },
  "success": true
}
```

---

### Filter

Given a dictionary of filter parameters, return ....

URL: `baseURL/ssd_api/filter`

Type: `POST`

Input format: Categorical filters (e.g. eye_diagnosis, ethnicity) must be given as a list of strings: `({"eye_diagnosis": ["retinal edema"]})`. Numerical filters (e.g. pressure and vision) must be given as two key value pairs: `({"left_pressure": {"less": 50, "more": 20}, "right_vision": {"less": "20/40"}})`

Example:

`https://tigernie.com/ssd_api/filter`

Input data:

```JSON
{
    "filters": {
        "eye_diagnosis" : ["retinal edema"],
        "systemic_diagnosis": ["gout"],
        "age": {
            "less": 50
        },
        "ethnicity": ["asian"],
        "image_procedure_type": ["IR_OCT"],
        "labs": {"Calcium": 4},
        "medication_generic_name": ["Ketorolac"],
        "medication_therapuetic_name": ["CNS Agent"],
        "left_vision": {
            "less": "20/40"
        },
        "right_vision": {
            "less": "20/40",
            "more": "20/200"
        },
         "left_pressure": {
            "less": 50
        },
        "right_pressure": {
            "equal": 100,
            "between": [120,200]
        }
    }
}
```

Returns (truncated):

```json
{
  "pt_id": [123, 123, 123]
}
```

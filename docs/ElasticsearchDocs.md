# Elasticsearch for search-as-you-type completion

An Elasticsearch instance is populated with certain data fields with a bash script. (https://github.com/haolinnie/Self-Service-Database-Server/blob/master/index_api_to_es.sh). The instance self-service-database-server provides a very thin reverse proxy over an es instance. 

To achieve search-as-you-type completion, place a callback on the UI textbox entry that listens for change, and everytime the user types something, call the elasticsearch API to get a list of potential fields.

All searches are HTTP GET requests.

Currently, the elasticsearch instance has the following indices:

* "systemic_diagnosis"
* "eye_diagnosis"
* "medication_generic_name"
* "medication_therapeutic_class"
* "image_procedure"
* "lab"

### Query for search-as-you-type entries

URL: `baseURL/ssd_api/es/<index>?query=<query>`

Example: Search for the word "renal" in systemic_diagnosis. Place the desired index in the <index> field and query in the <query> field.

```bash
curl -X GET "https://tigernie.com/ssd_api/es/systemic_diagnosis?query=renal"
```

Returns:

```json
{
  "message": "",
  "result": {
    "matches": [
      "End-stage renal disease (disorder)",
      "End stage renal disease (CMS-HCC)"
    ]
  },
  "success": true
}
```

# Elasticsearch for search-as-you-type completion

An Elasticsearch instance is populated with certain data fields with a bash script. To achieve this, place a callback on the UI textbox entry that listens for change, and everytime the user types something, call the elasticsearch API to get a list of potential fields.

All searches are HTTP GET requests.

Sample elasticsearch instance deployed at https://elastic.tigernie.com

Basic authentication required:
* Username: selfservice
* Password: selfservice

Currently, the elasticsearch instance has the following indices:

* "systemic_diagnosis"
* "eye_diagnosis"
* "medication_generic_name"
* "medication_therapeutic_class"
* "image_procedure"
* "lab"

### Query for search-as-you-type entries

Example: Search for the word "renal" in systemic_diagnosis. For other indices, simply substitute "systemic_diagnosis" with the other index in the URL. The user input should be put in the "query" field in the JSON data. Keep everything else in the request as is.

```bash
curl -X GET "https://selfservice:selfservice@elastic.tigernie.com/systemic_diagnosis/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "multi_match": {
      "query": "renal",
      "type": "bool_prefix",
      "fields": [
        "name",
        "name._2gram",
        "name._3gram"
      ]
    }
  }
}
'
```

Grab the autocompletion results in the hits fields.

Returns:

```json
{
  "took" : 9,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "systemic_diagnosis",
        "_type" : "_doc",
        "_id" : "16",
        "_score" : 1.0,
        "_source" : {
          "name" : "End-stage renal disease (disorder)"
        }
      },
      {
        "_index" : "systemic_diagnosis",
        "_type" : "_doc",
        "_id" : "15",
        "_score" : 1.0,
        "_source" : {
          "name" : "End stage renal disease (CMS-HCC)"
        }
      }
    ]
  }
}
```

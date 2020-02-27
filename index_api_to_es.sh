#!/bin/bash --init-file

################
# Configurations
################

ELASTIC_URL=https://elastic.tigernie.com
#ELASTIC_URL='localhost:9200'
INDEX='my_index'
FIELD='my_field'


#################################
# Elastic Search Helper functions
#################################
test_parse() {
    echo $@
    echo $1
    echo "${*:2}"
}

generate_mapping_data() {
    cat <<EOF
{
  "mappings": {
    "properties": {
      "${FIELD}": {
        "type": "search_as_you_type"
      }
    }
  }
}
EOF
}

create_mapping() {
    # Create a mapping
    curl -X PUT "${ELASTIC_URL}/${INDEX}?pretty" -H 'Content-Type: application/json' -d"$(generate_mapping_data)"
}

generate_add_data() {
    # Helper function to generate JSON data for PUT requests to add items to Elasticsearch
    # The $* signature passes all arguments as a single string
    cat <<EOF
{
  "${FIELD}": "$*"
}
EOF
}

add_a_sample() {
    # Add an entry to elasticsearch
    # Params:
    #       $1      -- index <integer>
    #       $*:2    -- sampel <string>
    echo Adding index $1
    echo Data: "$(generate_add_data ${*:2})"
    curl -X PUT "${ELASTIC_URL}/${INDEX}/_doc/$1?refresh&pretty" -H 'Content-Type: application/json' -d "$(generate_add_data ${*:2})"
}

generate_search_data() {
    # Helper function that generates data for GET requests to query an elasticsearch index
    cat <<EOF
{
  "query": {
    "multi_match": {
    "query": "$*",
      "type": "bool_prefix",
      "fields": [
        "${FIELD}",
        "${FIELD}._2gram",
        "${FIELD}._3gram"
      ]
    }
  }
}
EOF
}

search() {
    # Search for a sample
    echo "$(generate_search_data $@)"
    curl -X GET "${ELASTIC_URL}/${INDEX}/_search?pretty" -H 'Content-Type: application/json' -d "$(generate_search_data $@)"
}

#########################
# DB API Helper Functions
#########################

generate_python_parse_code() {
    cat <<EOF
import sys
import json
print(sys.stdin)
for val in json.load(sys.stdin)['result']['data']:
    print(val)
EOF
}

get_distinct_special() {
    curl -s -XGET -u debug:debug https://tigernie.com/ssd_api/get_distinct\?special\=$1 | python3 -c "import sys, json; res=json.load(sys.stdin); [print(v) for v in res['result']['data']]"
}

pretty_print_distinct() {
    #
    # Print out $1 <int> and entry <string>
    #
    get_distinct_special $1 | cat -n
}


###############################################
# Create entries in elasticsearch iteratively
###############################################

create_systemic_diagnosis_entries() {
    INDEX="systemic_diagnosis"
    FIELD="diagnosis"
    pretty_print_distinct systemic_diagnosis | while IFS= read -r line ; do
       add_a_sample $line
    done
}

create_eye_diagnosis_entries() {
    INDEX="eye_diagnosis"
    FIELD="diagnosis"
    pretty_print_distinct eye_diagnosis | while IFS= read -r line ; do
       add_a_sample $line
    done
}

create_search_entries() {
    create_systemic_diagnosis_entries
    create_eye_diagnosis_entries
}

########
# Main
########
main() {
    echo Running main
    create_search_entries
}


#main $@

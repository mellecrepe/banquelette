#!/bin/sh

# FUNCTIONS
########################################
# Function to get "_id" value from json file
get_id_from_json()
{
	local arg_jsonfile="$1"

	[ -z "$arg_jsonfile" ] && return 0

	cat "$arg_jsonfile" \
		| python -c 'import sys, json; print(json.load(sys.stdin)["_id"])'

	return 0
}

# ARGS
########################################
ARG_COUCHDB_HOST="$1"
[ -z "$ARG_COUCHDB_HOST" ] && ARG_COUCHDB_HOST="127.0.0.1:5984"

ARG_JSONDIR="$2"
[ -z "$ARG_JSONDIR" ] && ARG_JSONDIR="initdb_data"

# CHECK
########################################

# A little help ?
case "$1" in
	"-h"|"-help"|"--help"|"-?")
		echo "Usage: $0 [couchdb.host.example.com:5984] [initdb_data_directory]"
		echo ""
		echo "Use this script to initialise the CouchDB database"
		echo ""
		echo "This script will connect to the specified couchdb_host (default"
		echo "to 127.0.0.1:5984), create an account database and add to the"
		echo "database all json objects in the specified initdb_data_dir"
		echo "(default to initdb_data)."

		exit 0
		;;
esac

# We definitely need curl.
type "curl" >/dev/null 2>&1
if [ "$?" -ne 0 ]; then
	echo "Fatal: No 'curl' binary found on this system" >&2
	echo "Please install curl before using this script"
	echo "Leaving now"
	exit 1
fi

# SCRIPT
########################################
echo "Creating 'account' database"

curl -X PUT "$ARG_COUCHDB_HOST/account"

echo "Creating all objects listed in '$ARG_JSONDIR'"

for jsonfile in $(ls "$ARG_JSONDIR/"*.json); do

	echo "Parsing json file '$jsonfile'"

	id=$(get_id_from_json "$jsonfile")

	if [ -z "id" ]; then
		echo "Error: No '_id' found for '$jsonfile'. Skipping" >&2
		continue
	fi

	echo "Creating CouchDB document with _id '$id' in account"

	curl -X PUT "$ARG_COUCHDB_HOST/account/$id" \
		-d @$jsonfile \
		-H "Content-Type: application/json"

done

echo "Database initialisation over"

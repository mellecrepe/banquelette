#!/bin/sh

get_json_field()
{
	local arg_field="$1"
	local arg_json="$2"

	[ -z "$arg_field" ] && return 0

	# If there's no arg_json, we read it from stdin
	if [ -z "$arg_json" ]; then
		while read data; do
			arg_json="$arg_json$data"
		done
	fi

	# Use python to parse json
	echo "$arg_json"    \
		| python -c \
"
import sys, json
print(json.load(sys.stdin)['$arg_field'])
"                           \
	          2>/dev/null
	
	return $?

} # get_json_field()


# Generate a random byte key from /dev/urandom
# You have to pass the keysize as parameter
get_urandom_key()
{
    local arg_keysize="$1"

    [ -z "$arg_keysize" ] && return 0

    cat "/dev/random"             \
        | head -c "$arg_keysize"  \
        | hexdump -e '1/2 "%x"'

    return 0
} # get_urandom_key()


########################################
cd "/home/banquelette"

# Check database initialization
couchdb_version="$( curl -sX GET "$COUCHDB_HOST" \
			| get_json_field "version" )"

if [ "$?" -ne 0 ] || [ -z "$couchdb_version" ]; then
	echo "Fatal: unable to get CouchDB version at '$COUCHDB_HOST'" >&2
	echo "Please check the CouchDB connection"                     >&2
	
	exit 1
fi


couchdb_account="$( curl -sX GET "$COUCHDB_HOST/account" \
			| get_json_field "db_name" )"

if [ "$?" -ne 0 ]; then
	echo "No 'account' database found on CouchDB instance '$COUCHDB_HOST'"
	echo "Launching initialization script now"

	./initdb.sh "$COUCHDB_HOST"

	if [ "$?" -ne 0 ]; then
		echo "Fatal: something went wrong during database initialisation" >&2
		echo "I have no idea what to do, sorry" >&2
		echo "Please contact a developper"      >&2

		exit 1
	fi
else
	echo "'account' database exist on CouchDB instance '$COUCHDB_HOST'"
	echo "Skipping database initialization"
fi


# Replace settings according to env variables

[ -z "$COUCHDB_HOST" ] && COUCHDB_HOST="db:5984"

if [ -e "projet/settings.py" ]; then

    [ -n "$COUCHDB_HOST" ] && sed -i "s_('djangoapp.account', '.*')_('djangoapp.account', 'http://$COUCHDB_HOST/account')_"  projet/settings.py
    [ -n "$SECRET_KEY" ]   && sed -i "s/SECRET_KEY *=.*/SECRET_KEY = '$SECRET_KEY'/"                                         projet/settings.py

else

    cp projet/settings.py.template projet/settings.py

    if [ -z "$SECRET_KEY" ]; then
        echo "Creating random SECRET_KEY, please keep calm & generate entropy..."
        SECRET_KEY="$(get_urandom_key 20)"
        echo "SECRET_KEY generated!"
    fi

    sed -i "s_('djangoapp.account', '.*')_('djangoapp.account', 'http://$COUCHDB_HOST/account')_"                            projet/settings.py
    sed -i "s/SECRET_KEY *=.*/SECRET_KEY = '$SECRET_KEY'/"                                                                   projet/settings.py
    sed -i "s/DEBUG *=.*/DEBUG = True/"                                                                                      projet/settings.py # Ouch, that one is ugly. :/ TODO We should use a real webserver + wsgi server
fi

if ! [ -e "account/settings.py" ]; then
    cp account/settings.py.template account/settings.py
fi

# Start banquelette !
# TODO Use something better than the Django test webserver...
./manage.py runserver 0.0.0.0:80

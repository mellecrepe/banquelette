#!/bin/sh

# ======================================
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
# ======================================
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


# Check for misconfigurations
# ======================================
if [ -n "$COUCHDB_HOST" ]; then
    echo "WARNING: You defined the env variable COUCHDB_HOST"
    echo "WARNING: It seems you are trying to use an older"
    echo "WARNING: version of Banquelette. Banquelette now"
    echo "WARNING: uses sqlite as database backend."
fi


# Replace settings according to env variables
# ======================================
if [ -e "projet/settings.py" ]; then
    [ -n "$SECRET_KEY" ] &&                                    \
        sed -i "s/SECRET_KEY *=.*/SECRET_KEY = '$SECRET_KEY'/" \
               "projet/settings.py"
else
    echo "Copying projet settings template..."
    cp projet/settings.py.template projet/settings.py

    if [ -z "$SECRET_KEY" ]; then
        echo "Creating random SECRET_KEY, please keep calm & generate entropy..."
        SECRET_KEY="$(get_urandom_key 20)"
        echo "SECRET_KEY generated!"
    fi

    sed -i "s/SECRET_KEY *=.*/SECRET_KEY = '$SECRET_KEY'/"    \
           "projet/settings.py"

   # Ouch, that one is ugly. :/ TODO We should use a real webserver + wsgi
   # server
   sed -i "s/DEBUG *=.*/DEBUG = True/"                       \
          "projet/settings.py"
fi

# Custom config if volume docker is use
if [ -e "config/settings.py" ]; then
    echo "Copying account settings..."
    ln -s config/settings.py account/settings.py
fi
    
if ! [ -e "account/settings.py" ]; then
    echo "Copying account settings template..."
    cp account/settings.py.template account/settings.py
fi

if [ -e "config/categories.yaml" ]; then
    echo "Copying account categories template..."
    ln -s config/categories.yaml account/categories.yaml
fi
if ! [ -e "account/categories.yaml" ]; then
    echo "Copying account categories..."
    cp account/categories.yaml.template account/categories.yaml
fi

# Initialize database
# ======================================
echo "Database initialization..."
python manage.py migrate


# Start banquelette !
# TODO Use something better than the Django test webserver...
python manage.py runserver 0.0.0.0:8000

#!/bin/bash

# Generate data

# CSV files directory
csv_folder="./tests/data"

python ./tests/data/generator.py --num_records 1000000

auth_endpoint='http://localhost:8080/api/auth/token'
create_folder_endpoint='http://localhost:8080/api/upload/'
upload_base_endpoint='http://localhost:8080/api/upload/'

client_id='client_id'
client_secret='client_secret'

client_credentials=$(echo -n "$client_id:$client_secret" | base64)

# Get the token from the authentication endpoint
token=$(curl -s -X POST "$auth_endpoint" \
     -H 'accept: application/json' \
     -H "Authorization: Basic $client_credentials" | grep -o '"token":"[^"]*' | cut -d':' -f2 | tr -d '"')

if [ -z "$token" ]; then
    echo "Failed to get the access token."
    exit 1
fi

# Create the upload folder and get the folder-name
folder_response=$(curl -s -X POST "$create_folder_endpoint" \
     -H 'accept: application/json' \
     -H "Authorization: Bearer $token")

echo "Folder response: $folder_response"

folder_name=$(echo "$folder_response" | grep -o '"folder":"[^"]*' | cut -d':' -f2 | tr -d '"')

if [ -z "$folder_name" ]; then
    echo "Failed to create the upload folder or get the folder name."
    exit 1
fi

# Upload all the CSV files
upload_endpoint="$upload_base_endpoint$folder_name"

for file in "$csv_folder"/*.csv; do
    echo -e "Uploading file: $file"
    md5_hash=$(openssl md5 -binary "$file" | xxd -p)
    echo "MD5 hash: $md5_hash"
    curl --location "$upload_endpoint" \
         --header "accept: application/json" \
         --header "Authorization: Bearer $token" \
         --header "X-MD5-Hash: $md5_hash" \
         --form "file=@\"$file\""
    echo -e "File upload complete: $file \n"
done

#!/bin/bash

VAULT_TOKEN="hvs.Hfkxg6re5QTY8mK7dzibccGB"
VAULT_URL="http://54.86.229.209:8200/v1/aws/creds/Admin"

CREDS=$(curl -H "X-Vault-Token: $VAULT_TOKEN" -X GET $VAULT_URL | jq .data)
export AWS_ACCESS_KEY_ID=$(echo $CREDS | jq .access_key | sed 's/\"//g' )
export AWS_SECRET_ACCESS_KEY=$(echo $CREDS | jq .secret_key | sed 's/\"//g' )
export AWS_DEFAULT_REGION=us-east-1
echo "" > ~/.aws/credentials
cat <<EOT >> ~/.aws/credentials
[default]
aws_access_key_id = $AWS_ACCESS_KEY_ID
aws_secret_access_key = $AWS_SECRET_ACCESS_KEY
EOT
chmod 600 ~/.aws/credentials
sleep 10
cat ~/.aws/credentials
terraform init --reconfigure
terraform apply --auto-approve

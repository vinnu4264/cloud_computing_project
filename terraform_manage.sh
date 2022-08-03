#!/bin/bash

cd Terraform

if [[ $1 == "destroy" ]]
then
    terraform destroy --auto-approve
elif [[ $1 == "apply" ]]
then
    terraform apply --auto-approve
elif [[ $1 == "image" ]]
then
    terraform taint docker_registry_image.cc_app_image
    terraform apply --auto-approve
elif [[ $1 == "reinstall" ]]
then
    terraform taint docker_registry_image.cc_app_image
    terraform destroy --auto-approve
    terraform apply --auto-approve
fi
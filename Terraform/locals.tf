locals {
    aws_config = yamldecode(file("../config_files/terraform_config.yaml"))
}
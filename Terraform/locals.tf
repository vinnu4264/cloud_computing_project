locals {
    aws_config = yamldecode(file("../Docker/Config_files/aws_config.yaml"))
}
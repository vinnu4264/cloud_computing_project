# locals {
#   application_name = "cc_fargate_ecs_app"
#   launch_type      = "FARGATE"
# }

# resource "aws_cloudwatch_log_group" "this" {
#   name = "cc_ecs_logs"
# }

# resource "aws_ecs_cluster" "this" {
#   name = local.application_name
#   configuration {
#     execute_command_configuration {
#       logging = "OVERRIDE"

#       log_configuration {
#         cloud_watch_encryption_enabled = false
#         cloud_watch_log_group_name     = aws_cloudwatch_log_group.this.name
#       }
#     }
#   }
# }

# resource "aws_ecs_service" "this" {
#   name        = "data_analyzer"
#   cluster     = aws_ecs_cluster.this.arn
#   launch_type = local.launch_type

#   deployment_maximum_percent         = 200
#   deployment_minimum_healthy_percent = 0
#   desired_count                      = 1

#   task_definition = aws_ecs_task_definition.this.family

#   network_configuration {
#     security_groups  = [aws_security_group.this.id]
#     assign_public_ip = true
#     subnets          = data.aws_subnet_ids.this.ids
#   }
# }
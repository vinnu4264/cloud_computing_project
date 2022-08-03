# resource "aws_ecs_task_definition" "this" {
#   container_definitions = jsonencode([
#     {
#       name      = "data_analyzer"
#       image     = "${aws_ecr_repository.cc_images.repository_url}:latest"
#       cpu       = 10
#       memory    = 512
#       essential = true
#       portMappings = [
#         {
#           containerPort = 5000
#           hostPort      = 5000
#         }
#       ]
#     }
#   ])
#   family                   = local.application_name
#   requires_compatibilities = [local.launch_type]
#   execution_role_arn       = "arn:aws:iam::991858350794:role/custom_role_cc_project"

#   cpu          = "256"
#   memory       = "512"
#   network_mode = "awsvpc"
# }
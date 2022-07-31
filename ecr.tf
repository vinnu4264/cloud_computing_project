resource "aws_ecr_repository" "cc_app_repo" {
  name                 = "cloud_computing_app_images"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
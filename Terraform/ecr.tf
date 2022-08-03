resource "aws_ecr_repository" "cc_images" {
  name = "cc_images"
}

resource "docker_registry_image" "cc_app_image" {
  name = "${aws_ecr_repository.cc_images.repository_url}:latest"
  build {
    context    = "../application"
    dockerfile = "Dockerfile"
  }
  depends_on = [
    aws_ecr_repository.cc_images
  ]
}


resource "aws_s3_bucket" "this" {
  bucket = "cloud-computing-data-store"
}

resource "aws_s3_bucket_acl" "example" {
  bucket = aws_s3_bucket.this.id
  acl    = "public-read-write"
}

resource "aws_s3_object" "this" {
  key    = "warm_up.json"
  bucket = aws_s3_bucket.this.id
  source = "../Website/data/warm_up.json"
}

output "s3_bucket_information" {
  value = {
    "name" : aws_s3_bucket.this.bucket,
    "arn" : aws_s3_bucket.this.arn,
    "file" : aws_s3_object.this.key
  }

}
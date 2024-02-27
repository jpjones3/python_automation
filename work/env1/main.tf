resource "aws_s3_bucket1" "s3_bucket" {
  bucket = var.bucket_name
  version = 0.3.10
  tags = var.tags
}

resource "aws_s3_bucket2" "s3_bucket" {
  bucket = var.bucket_name
  version = 0.3.10
  tags = var.tags
}

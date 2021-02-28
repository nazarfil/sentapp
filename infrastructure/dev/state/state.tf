resource "aws_dynamodb_table" "with_server_side_encryption" {
  name         = "${local.application}-${local.environment}-state"
  billing_mode = "PAY_PER_REQUEST"
  # https://www.terraform.io/docs/backends/types/s3.html#dynamodb_table
  hash_key = "LockID"

  server_side_encryption {
    enabled = true
  }

  point_in_time_recovery {
    enabled = true
  }

  lifecycle {
    ignore_changes = [
      billing_mode,
      read_capacity,
      write_capacity,
    ]
  }

  attribute {
    name = "LockID"
    type = "S"
  }
}

resource "aws_s3_bucket" "state_bucket" {
  bucket = "${local.application}-${local.environment}-state"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "aws:kms"
      }
    }
  }

  grant {
    permissions = [
      "READ_ACP",
      "WRITE"
    ]
    type = "Group"
    uri  = "http://acs.amazonaws.com/groups/s3/LogDelivery"
  }

  logging {
    target_bucket = "${local.application}-${local.environment}-state"
    target_prefix = "TFStateLogs/"
  }

  versioning {
    enabled = true
  }
}

resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = aws_s3_bucket.state_bucket.id
  policy = data.aws_iam_policy_document.bucket_policy.json
}

data "aws_iam_policy_document" "bucket_policy" {
  statement {
    effect = "Deny"

    principals {
      identifiers = [
        "*"
      ]
      type = "*"
    }

    actions = [
      "s3:*"
    ]

    resources = [
      aws_s3_bucket.state_bucket.arn,
      "${aws_s3_bucket.state_bucket.arn}/*"
    ]

    condition {
      test = "Bool"
      values = [
        "false"
      ]
      variable = "aws:SecureTransport"
    }
  }
}
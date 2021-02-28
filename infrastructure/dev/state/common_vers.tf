locals {
  environment = "dev"
  application = "sentapp"
  vpc_id      = "vpc-1432b27f"

 public_subnet_ids = [
    "subnet-15f51468",
    "subnet-09bdf445",
    "subnet-b1ca61da"
  ]

  internal_root_domain = "sentapp-com"
}
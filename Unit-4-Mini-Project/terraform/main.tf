terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

terraform {
  backend "s3" {
    bucket         = "library-backup-334478199124-us-east-1"
    key            = "compute/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "tf-state-locks"
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "library_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "library-vpc"
  }
}

resource "aws_internet_gateway" "library_igw" {
  vpc_id = aws_vpc.library_vpc.id

  tags = {
    Name = "library-igw"
  }
}

resource "aws_subnet" "library_subnet" {
  vpc_id                  = aws_vpc.library_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "library-public-subnet"
  }
}

resource "aws_route_table" "library_route_table" {
  vpc_id = aws_vpc.library_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.library_igw.id
  }

  tags = {
    Name = "library-public-route-table"
  }
}

resource "aws_route_table_association" "library_route_association" {
  subnet_id      = aws_subnet.library_subnet.id
  route_table_id = aws_route_table.library_route_table.id
}

resource "aws_security_group" "library_sg" {
  name        = "library-security-group"
  description = "Access for SSH, HTTP, and library application"
  vpc_id      = aws_vpc.library_vpc.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["152.59.63.209/32"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Library application"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "library-security-group"
  }
}

data "aws_ssm_parameter" "ubuntu_ami" {
  name = "/aws/service/canonical/ubuntu/server/22.04/stable/current/amd64/hvm/ebs-gp2/ami-id"
}

resource "aws_instance" "library_server" {
  ami                         = data.aws_ssm_parameter.ubuntu_ami.value
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.library_subnet.id
  vpc_security_group_ids      = [aws_security_group.library_sg.id]
  key_name                    = "library-aws-key"
  associate_public_ip_address = true

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
    encrypted   = true
  }

  tags = {
    Name = "library-server"
  }
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "library_backup" {
  bucket = "library-backup-${data.aws_caller_identity.current.account_id}-us-east-1"

  tags = {
    Name = "library-backup"
  }
}

resource "aws_s3_bucket_versioning" "library_backup_versioning" {
  bucket = aws_s3_bucket.library_backup.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "library_backup_encryption" {
  bucket = aws_s3_bucket.library_backup.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

output "app_server_public_ip" {
  value = aws_instance.library_server.public_ip
}

output "backup_bucket_name" {
  value = aws_s3_bucket.library_backup.bucket
}

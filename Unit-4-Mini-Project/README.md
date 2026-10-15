# Unit 4 Mini Project — Smart Library Management Platform

## Project Overview
An AWS infrastructure and application deployment project using Terraform, Ansible, Docker, and Nginx.

The Smart Library application provides a homepage, health check, and Books API.

## Technologies
- AWS EC2, VPC, Subnet, Internet Gateway, Security Groups, and S3
- Terraform for infrastructure provisioning and remote state
- Ansible for configuration management and deployment
- Docker for containerization
- Nginx as a reverse proxy
- Python, Flask, and SQLite

## Project Structure
- terraform/ — infrastructure configuration
- ansible/site.yml — deployment playbook
- ansible/roles/ — configuration and deployment roles
- ansible/files/library_app/ — application files
- ansible/inventory.ini — inventory template

## Application Endpoints
Replace EC2_PUBLIC_IP with your current EC2 public IP.

- Homepage: http://EC2_PUBLIC_IP/
- Health: http://EC2_PUBLIC_IP/api/health
- Books API: http://EC2_PUBLIC_IP/api/books

## Terraform Commands
Run from the terraform directory:

    terraform init
    terraform validate
    terraform plan

Review the plan before applying infrastructure changes.

## Ansible Commands
Run from the ansible directory after configuring inventory.ini:

    ansible-playbook -i inventory.ini site.yml --syntax-check
    ansible-playbook -i inventory.ini site.yml

## Security
Never commit AWS credentials, private SSH keys, .env files, or Terraform state. Restrict SSH access and review security group rules before deployment.

# 🛡️ Web-Check AWS Deployment with Terraform

Deploy the [Web-Check](https://github.com/Lissy93/web-check) security assessment tool on AWS using Infrastructure as Code (Terraform).

## Architecture

```
Internet
    │
    ▼
Internet Gateway
    │
    ▼
┌─────────────────────────────────┐
│  VPC: 10.0.0.0/16              │
│  ┌───────────────────────────┐  │
│  │  Public Subnet: 10.0.1.0 │  │
│  │                           │  │
│  │  ┌─────────────────────┐  │  │
│  │  │  EC2 (t3.micro)     │  │  │
│  │  │  Amazon Linux 2023  │  │  │
│  │  │  Docker + Web-Check │  │  │
│  │  │  Port 3000 → public │  │  │
│  │  └─────────────────────┘  │  │
│  │                           │  │
│  │  Security Group:          │  │
│  │  SSH (22) ← admin IP only│  │
│  │  HTTP (80) ← anywhere    │  │
│  │  App (3000) ← anywhere   │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

## Resources Created

| Resource | Purpose |
|---|---|
| VPC | Isolated private network |
| Public Subnet | Network segment with internet access |
| Internet Gateway | Connects VPC to the internet |
| Route Table | Routes traffic to the gateway |
| Security Group | Firewall rules (SSH restricted, HTTP/app open) |
| EC2 Instance | Server running Docker + Web-Check |

## Security Practices

- ✅ SSH access restricted to specific IP (not 0.0.0.0/0)
- ✅ IAM user with MFA (not root account)
- ✅ State files excluded from version control (.gitignore)
- ✅ No hardcoded credentials — uses AWS CLI profile
- ✅ Custom VPC instead of default (network isolation)

## Prerequisites

- AWS Account with Free Tier
- [Terraform](https://www.terraform.io/) >= 1.0
- [AWS CLI](https://aws.amazon.com/cli/) configured with `aws configure`
- SSH key pair created in target region

## Usage

```bash
# Initialize Terraform
terraform init

# Preview changes
terraform plan -var="my_ip=YOUR_PUBLIC_IP"

# Deploy
terraform apply -var="my_ip=YOUR_PUBLIC_IP"

# Access the app
# Open: http://<instance_public_ip>:3000

# Destroy when done (stop charges)
terraform destroy -var="my_ip=YOUR_PUBLIC_IP"
```

## Files

| File | Purpose |
|---|---|
| `provider.tf` | AWS provider configuration (region: ap-south-1) |
| `variables.tf` | Input variables (instance type, key name, IP, Docker image) |
| `main.tf` | Core infrastructure — VPC, subnet, SG, EC2 with user_data |
| `outputs.tf` | Outputs — public IP, app URL, SSH command |

## Tech Stack

- **IaC:** Terraform (HCL)
- **Cloud:** AWS (VPC, EC2, Security Groups)
- **OS:** Amazon Linux 2023
- **Container:** Docker
- **App:** [Web-Check](https://github.com/Lissy93/web-check) — OSINT security tool

## Author

**Suresh Deora** — Cybersecurity | DevSecOps | RHCE & RHCSA Certified

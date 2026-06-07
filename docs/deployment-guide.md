# Roster — Deployment Guide

**Company:** ShiftSync
**Project:** CIS 410 Capstone — Week 11

---

## Prerequisites

- GCP project access to `cis410-btamer`
- GitHub collaborator access to `bastam04/cis410-roster`
- gcloud CLI installed and authenticated

---

## 1. Initial Setup

Clone the repository:
```bash
git clone https://github.com/bastam04/cis410-roster.git
cd cis410-roster
```

Set your GCP project:
```bash
gcloud config set project cis410-btamer
```

---

## 2. Apply Infrastructure (Run Once)

This creates the VPC, Cloud SQL database, and Secret Manager secrets in GCP.

```bash
cd terraform/infrastructure
terraform init
terraform apply -var="project_id=cis410-btamer"
```

What gets created:
- `roster-vpc` — private VPC network
- `roster-db` — Cloud SQL PostgreSQL instance
- `roster-db-password` — Secret Manager secret for DB credentials

---

## 3. Secret Manager

The DB password secret is already created in GCP as `roster-db-password`.

When deploying to Cloud Run, wire it using:
```bash
--update-secrets=DB_PASSWORD=roster-db-password:latest
```

Never hardcode credentials in code or GitHub Secrets.

---

## 4. CI/CD Pipeline

Every push to `main` triggers the GitHub Actions pipeline automatically:

1. Docker build
2. Snyk SAST scan
3. Snyk container scan
4. Push image to Artifact Registry
5. Deploy to Cloud Run via `terraform/app/`

All changes must go through a pull request — direct pushes to main are blocked.

---

## 5. Git Workflow

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: description of change"

# Push branch
git push origin feature/your-feature-name

# Open a pull request on GitHub
# Assign Ezatullah (Security Reviewer) as reviewer
# Project Lead merges after approval
```

---

## 6. Environment Variables

| Variable | Source | Description |
|---|---|---|
| DB_HOST | Cloud SQL | Database host IP |
| DB_NAME | Config | Database name (roster) |
| DB_USER | Config | Database user (roster_user) |
| DB_PASSWORD | Secret Manager | Database password |
| DB_PORT | Config | PostgreSQL port (5432) |
| ENVIRONMENT | Config | Deployment environment |

---

## 7. Team Roles

| Name | Role | Responsibility |
|---|---|---|
| Bassam Tamer | Project Lead | Repo management, PR merges, architecture |
| Abel Biruk | Backend Engineer | Flask API, Cloud SQL integration |
| Hibrework Demewoz | Frontend Engineer | UI, frontend-backend integration |
| Abdinoor | DevSecOps Engineer | CI/CD pipeline, Terraform apply, Snyk |
| Ezatullah Saleh | Security Reviewer | PR reviews, IAM audit, security docs |

---

## 8. Troubleshooting

| Problem | Fix |
|---|---|
| Pipeline fails on Snyk scan | Check Snyk token is set in GitHub Variables |
| Cloud Run can't connect to DB | Verify DB_PASSWORD is mounted from Secret Manager |
| Terraform apply fails | Run `gcloud auth application-default login` first |
| App returns 500 error | Check Cloud Logging in GCP Console |

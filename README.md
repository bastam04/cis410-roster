# Roster: Shift Scheduling App

**Company:** ShiftSync
**Project:** CIS 410 Cybersecurity Automation Capstone

Roster is a web application that helps small businesses manage employee scheduling. Managers can post shifts and employees can view and claim available shifts.

---

## Team Members

| Name | Role | GitHub |
|---|---|---|
| Bassam Tamer | Project Lead | bastam04 |
| Abel Biruk | Backend Engineer | AbelBiruk100 |
| Hibrework Demewoz | Frontend Engineer | Hibr-gech |
| Abdinoor | DevSecOps Engineer | kaamil2026 |
| Ezatullah Saleh | Security Reviewer | arsin2022 |

---

## Tech Stack

- **Frontend:** Flask templates (HTML/CSS)
- **Backend:** Python Flask
- **Database:** Cloud SQL (PostgreSQL)
- **Container Registry:** Artifact Registry
- **Compute:** Cloud Run
- **Infrastructure as Code:** Terraform
- **CI/CD:** GitHub Actions (OIDC - no stored keys)
- **Security Scanning:** Snyk (SAST + SCA + Container)

---

## App Description

Roster solves the problem of disorganized shift scheduling for small businesses. Managers post shifts through a simple dashboard and employees can view and claim available shifts. The platform is designed for small teams in retail, food service, and hospitality.

---

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full architecture diagram.

---

## Security Commitments

- Least-privilege IAM - service accounts have only required permissions
- No hardcoded secrets - all credentials stored in Secret Manager
- OIDC authentication - no long-lived keys stored in GitHub
- Branch protection - all changes via pull request with 1 required reviewer
- Snyk scanning on every pull request
- terraform.tfvars gitignored - no secrets committed to GitHub

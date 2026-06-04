# Roster — Architecture Diagram

## System Architecture

```mermaid
graph TD
    Dev[Developer Local Machine] -->|git push| GitHub[GitHub Repository]

    GitHub -->|triggers| Actions[GitHub Actions CI/CD]

    Actions -->|OIDC auth - no stored keys| GCP[GCP - cis410-btamer]

    subgraph GCP [GCP Project - cis410-btamer]
        AR[Artifact Registry\nroster-app]
        CR[Cloud Run\nroster-app]
        SQL[Cloud SQL\nPostgreSQL - roster-db]
        SM[Secret Manager\nroster-db-password]

        subgraph VPC [roster-vpc]
            SQL
        end
    end

    Actions -->|docker build + push| AR
    Actions -->|gcloud run deploy| CR
    CR -->|pull image| AR
    CR -->|fetch secret at runtime| SM
    CR -->|private network via VPC| SQL

    SM -->|DB password| CR
```

## Component Descriptions

| Component | Technology | Purpose |
|---|---|---|
| Frontend | Flask templates | Shift listing and claiming UI |
| Backend | Python Flask on Cloud Run | REST API for shift management |
| Database | Cloud SQL PostgreSQL | Persistent shift and user data |
| Container Registry | Artifact Registry | Stores Docker images tagged by commit SHA |
| Secrets | Secret Manager | DB password — never in code or env files |
| Network | VPC roster-vpc | Private network connecting Cloud Run to Cloud SQL |
| CI/CD | GitHub Actions + OIDC | Build, scan, and deploy on every push to main |
| Security Scanning | Snyk SAST + SCA + Container | Runs on every pull request |

## CI/CD Pipeline Flow

```mermaid
graph LR
    Push[Push to main] --> Build[Docker Build]
    Build --> SAST[Snyk Code SAST]
    SAST --> SCA[Snyk SCA Dependencies]
    SCA --> Container[Snyk Container Scan]
    Container --> Publish[Push to Artifact Registry]
    Publish --> Deploy[Deploy to Cloud Run]
```

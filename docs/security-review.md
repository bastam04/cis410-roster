# Security Review

## Overview

As part of the DevSecOps implementation, security controls were integrated into the CI/CD pipeline and deployment process. The project uses GitHub Actions, Snyk security scanning, Google Cloud IAM, and Secret Manager to reduce risk and protect sensitive information.

## SAST Results

Static Application Security Testing (SAST) is performed using Snyk Code within the GitHub Actions pipeline.

The workflow executes:

```bash
snyk code test --severity-threshold=high app/
```

This scan reviews source code for security vulnerabilities before deployment.

Results:
- Snyk Code integrated successfully
- Pipeline configured to detect high severity findings
- No critical vulnerabilities identified during final validation

## Container Scan Results

Container image scanning is performed using Snyk Container.

The workflow executes:

```bash
snyk container test IMAGE_NAME --file=Dockerfile --severity-threshold=high
```

Purpose:
- Detect vulnerable packages
- Identify insecure dependencies
- Prevent deployment of high-risk container images

Results:
- Container scan integrated into CI/CD pipeline
- Images are scanned before being pushed to Artifact Registry
- No critical vulnerabilities remained before deployment

## Secret Manager Usage

Sensitive information is not stored directly in source code.

Google Secret Manager is used to manage application secrets.

Example secret:

- roster-db-password

Cloud Run retrieves secrets during deployment using:

```bash
gcloud run services update roster-app \
--update-secrets="DB_PASSWORD=roster-db-password:latest"
```

Benefits:
- No hardcoded passwords
- Centralized secret management
- Reduced risk of credential exposure

## IAM Design

The project uses Workload Identity Federation (OIDC) for GitHub Actions authentication.

Benefits:
- No long-lived service account keys
- Temporary authentication tokens
- Reduced credential management risk

GitHub Actions authenticates to Google Cloud using:
- Workload Identity Provider
- Dedicated Service Account

This follows the principle of least privilege by granting only required permissions for deployment tasks.

## Vulnerabilities Fixed

The team reviewed security findings throughout development and remediated issues before final deployment.

Actions included:
- Updating vulnerable dependencies
- Removing unnecessary exposure of secrets
- Implementing Secret Manager integration
- Enabling Snyk source code scanning
- Enabling container image scanning
- Using OIDC authentication instead of service account keys

## Conclusion

The final solution incorporates security controls throughout the software delivery lifecycle. Security scanning, secret management, and least-privilege access controls were integrated into the CI/CD pipeline to support secure deployment to Google Cloud Platform.

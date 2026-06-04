variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "db_password" {
  description = "Cloud SQL database password"
  type        = string
  sensitive   = true
  default     = "changeme-set-in-secret-manager"
}

variable "cloudrun_sa_email" {
  description = "Service account email used by Cloud Run"
  type        = string
  default     = "cis410-deploy-sa@cis410-btamer.iam.gserviceaccount.com"
}

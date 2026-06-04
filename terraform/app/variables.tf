variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

variable "cloudrun_sa_email" {
  description = "Service account email used by Cloud Run"
  type        = string
  default     = "cis410-deploy-sa@cis410-btamer.iam.gserviceaccount.com"
}

variable "image_tag" {
  description = "Docker image tag to deploy"
  type        = string
  default     = "latest"
}

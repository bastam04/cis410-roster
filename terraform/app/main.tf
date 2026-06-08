terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  backend "gcs" {
    bucket = "cis410-btamer-tfstate"
    prefix = "roster/app"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "roster_repo" {
  location      = var.region
  repository_id = "roster-app"
  format        = "DOCKER"
}

resource "google_cloud_run_v2_service" "roster_app" {
  name     = "roster-app"
  location = var.region

  template {
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/roster-app/roster:${var.image_tag}"

      env {
        name = "DB_PASSWORD"
        value_source {
          secret_key_ref {
            secret  = "roster-db-password"
            version = "latest"
          }
        }
      }

      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }
    }

    service_account = var.cloudrun_sa_email
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

resource "google_cloud_run_v2_service_iam_member" "public_access" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.roster_app.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

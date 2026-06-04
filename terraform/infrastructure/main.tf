terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ── VPC ───────────────────────────────────────────────────────────────────────
resource "google_compute_network" "roster_vpc" {
  name                    = "roster-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "roster_subnet" {
  name          = "roster-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.roster_vpc.id
}

# ── Cloud SQL (PostgreSQL) ────────────────────────────────────────────────────
resource "google_sql_database_instance" "roster_db" {
  name             = "roster-db"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.roster_vpc.id
    }
  }

  deletion_protection = false
}

resource "google_sql_database" "roster" {
  name     = "roster"
  instance = google_sql_database_instance.roster_db.name
}

resource "google_sql_user" "roster_user" {
  name     = "roster_user"
  instance = google_sql_database_instance.roster_db.name
  password = var.db_password
}

# ── Secret Manager ────────────────────────────────────────────────────────────
resource "google_secret_manager_secret" "db_password" {
  secret_id = "roster-db-password"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_password_version" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = var.db_password
}

# ── IAM — allow Cloud Run SA to access secrets ────────────────────────────────
resource "google_secret_manager_secret_iam_member" "cloudrun_secret_access" {
  secret_id = google_secret_manager_secret.db_password.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.cloudrun_sa_email}"
}

output "vpc_name" {
  description = "VPC network name"
  value       = google_compute_network.roster_vpc.name
}

output "db_instance_name" {
  description = "Cloud SQL instance name"
  value       = google_sql_database_instance.roster_db.name
}

output "db_connection_name" {
  description = "Cloud SQL connection name for Cloud Run"
  value       = google_sql_database_instance.roster_db.connection_name
}

output "secret_name" {
  description = "Secret Manager secret name for DB password"
  value       = google_secret_manager_secret.db_password.secret_id
}

# main.tf

# Proveedor de Google Cloud
provider "google" {
  project     = "latam-challenge-leonardora"
  region      = "us-west2"
}

resource "google_project" "latam-challenge-leonardora" {
  name       = "latam-challenge-leonardora"
  project_id = "latam-challenge-leonardora"
  labels = {
    environment = "development"
  }

  lifecycle {
    prevent_destroy = false
  }
}

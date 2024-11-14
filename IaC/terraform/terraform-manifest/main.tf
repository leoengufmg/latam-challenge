# main.tf

# Proveedor de Google Cloud
provider "google" {
  project     = "desafio-latam"            # ID del proyecto actual para ejecutar la creación del nuevo proyecto
  region      = "southamerica-west1"                        # Región por defecto (ajústala según tus necesidades)
}

resource "google_project" "desafio-latam" {
  name       = "desafio-latam"
  project_id = "hip-rain-441704-n7"
  labels = {
    environment = "development"
  }

  lifecycle {
    prevent_destroy = false
  }
}

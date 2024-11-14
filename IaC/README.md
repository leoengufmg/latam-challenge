---
title: GCP Google Cloud Platform - Terraform Commands
---
## Step-01: Tools
1. Install gcloud CLI 
2. Install Terraform CLI
3. Install VSCode Editor
4. Install Terraform Pluging for VSCode
5. Implement above 4 steps in both MacOS and WindowsOS
 

## Step-02: WindowsOS: Install gcloud cli and verify
### Step-02-01: Install gcloud cli on WindowsOS
- [Install gcloud cli on WindowsOS](https://cloud.google.com/sdk/docs/install-sdk#windows)
```t
## Important Note: Download the latest version available on that respective day
Dowload Link: https://cloud.google.com/sdk/docs/install-sdk#windows

## Run the Installer
GoogleCloudSDKInstaller.exe
```

### Step-02-02: Verify gcloud cli version
```t
# gcloud cli version
gcloud version
```

### Step-02-03: Intialize gcloud CLI in local Terminal 
```t
# Initialize gcloud CLI
gcloud init

# List accounts whose credentials are stored on the local system:
gcloud auth list

# List the properties in your active gcloud CLI configuration
gcloud config list

# View information about your gcloud CLI installation and the active configuration
gcloud info

# gcloud config Configurations Commands (For Reference)
gcloud config list
gcloud config configurations list
gcloud config configurations activate
gcloud config configurations create
gcloud config configurations delete
gcloud config configurations describe
gcloud config configurations rename

# Configure GCP Credentials (ADC: Application Default Credentials)
gcloud auth application-default login
```

### Step-02-04: Install Terraform CLI
- [Download Terraform](https://developer.hashicorp.com/terraform/install#windows)
- [Install Terraform](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/install-cli)
```t
# Install the Hashicorp tap
choco install terraform
```
- Unzip the package
- Create new folder `terraform-bins`
- Copy the `terraform.exe` to a `terraform-bins`
- Set PATH in windows 

### Step-02-05: Windows: IDE for Terraform - VS Code Editor
- [Microsoft Visual Studio Code Editor](https://code.visualstudio.com/download)
- [Hashicorp Terraform Plugin for VS Code](https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform)
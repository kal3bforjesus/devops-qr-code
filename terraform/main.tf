terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# 1. Resource Group (A folder to hold our resources)
resource "azurerm_resource_group" "rg" {
  name     = "qr-devops-rg"
  location = "East US"
}

# 2. Azure Container Registry (ACR) - Stores Docker Images (~$5/month)
resource "azurerm_container_registry" "acr" {
  name                = "qrdevopsacr2026" 
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"       # Cheapest tier
  admin_enabled       = true          # Allows username/password login
}

# 3. Azure Blob Storage - Stores QR Codes (~$0.02/month)
resource "azurerm_storage_account" "storage" {
  name                     = "qrdevopsstorage2026" 
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"             # Cheapest redundancy
}

resource "azurerm_storage_container" "container" {
  name                  = "qrcodes"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "blob" # Allows public read access so users can see the QR images
}

# 4. Azure Kubernetes Service (AKS) - Runs the containers
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "qr-aks-cluster"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "qraks"

  default_node_pool {
    name       = "default"
    node_count = 1 # Keep it 1 to save money!
    vm_size    = "Standard_D2s_v4" # Cheap burstable VM
  }

  identity {
    type = "SystemAssigned"
  }

  # Attach ACR to AKS so it can pull images
  azure_active_directory_role_based_access_control {
    managed = true
    azure_rbac_enabled = true
  }
}

# Grant AKS permission to pull images from ACR
resource "azurerm_role_assignment" "acr_pull" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
}
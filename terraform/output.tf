output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}

output "storage_connection_string" {
  value = azurerm_storage_account.storage.primary_connection_string
  sensitive = true
}
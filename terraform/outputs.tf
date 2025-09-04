output "function_app_name" {
  value = azurerm_linux_function_app.main.name
}

output "function_app_staging_slot_name" {
  value = azurerm_linux_function_app_slot.stage.name
}

output "function_app_resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "function_app_python_version" {
  value = azurerm_linux_function_app.main.site_config[0].application_stack[0].python_version
}

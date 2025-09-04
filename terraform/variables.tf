variable "log_analytics_workspace_name" {
  type        = string
  description = "The existing log analytics workspace name"
}

variable "log_analytics_workspace_rg_name" {
  type = string
  description = "The resource group pf the existing log analytics workspace"
}

variable "resource_group_name" {
  type = string
  description = "The name of the resource group to manage"
}

variable "location" {
  type = string
  description = "The location for the resources"
}

variable "service_plan_name" {
  type = string
  description = "The name of the service plan to manage"
}

variable "storage_account_name" {
  type = string
  description = "The name of the storage account to manage"
}

variable "application_insights_name" {
  type = string
  description = "The name of the application insights to manage"
}

variable "function_app_name" {
  type = string
  description = "The name of the function app to manage"
}

variable "api_keys" {
  type = string
  description = "The Alma API keys for each IZ"
  sensitive = true
}

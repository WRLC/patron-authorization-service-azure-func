data "azurerm_log_analytics_workspace" "existing" {
  name = var.log_analytics_workspace_name
  resource_group_name = var.log_analytics_workspace_rg_name
}

resource "azurerm_resource_group" "main" {
  name = var.resource_group_name
  location = var.location
}

resource "azurerm_service_plan" "main" {
  name = var.service_plan_name
  resource_group_name = azurerm_resource_group.main.name
  location = azurerm_resource_group.main.location
  os_type = "Linux"
  sku_name = "Y1"
}

resource "azurerm_storage_account" "main" {
  name = var.storage_account_name
  resource_group_name = azurerm_resource_group.main.name
  location = azurerm_resource_group.main.location
  account_tier = "Standard"
  account_replication_type = "RAGRS"
  allow_nested_items_to_be_public = false
  min_tls_version = "TLS1_0"
}

resource "azurerm_application_insights" "main" {
  name = var.application_insights_name
  location = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  workspace_id = data.azurerm_log_analytics_workspace.existing.id
  application_type = "web"
  sampling_percentage = 0
}

resource "azurerm_linux_function_app" "main" {
  name = var.function_app_name
  location = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  service_plan_id = azurerm_service_plan.main.id
  storage_account_name = azurerm_storage_account.main.name
  storage_account_access_key = azurerm_storage_account.main.primary_access_key

  app_settings = {
    "API_KEYS" = var.api_keys
    "AzureWebJobsFeatureFlags" = "EnableWorkerIndexing"
    "DOC_MESSAGE" = "WRLC patron authorization service"
    "ENDPOINT" = "https://api-na.hosted.exlibrisgroup.com/almaws/v1/users/"
    "STATIC_PARAMS" = "{'user_id_type': 'all_unique', 'view': 'full', 'expand': 'none'}"
  }

  client_certificate_mode = "Required"

  site_config {
    application_insights_connection_string = azurerm_application_insights.main.connection_string
    application_insights_key = azurerm_application_insights.main.instrumentation_key
    ftps_state = "FtpsOnly"
    http2_enabled = true

    application_stack {
      python_version = "3.11"
    }
  }

  daily_memory_time_quota = 0
  builtin_logging_enabled = false
  https_only = true

   sticky_settings {
     app_setting_names = [
       "APPINSIGHTS_INSTRUMENTATIONKEY",
       "APPLICATIONINSIGHTS_CONNECTION_STRING ",
       "APPINSIGHTS_PROFILERFEATURE_VERSION",
       "APPINSIGHTS_SNAPSHOTFEATURE_VERSION",
       "ApplicationInsightsAgent_EXTENSION_VERSION",
       "XDT_MicrosoftApplicationInsights_BaseExtensions",
       "DiagnosticServices_EXTENSION_VERSION",
       "InstrumentationEngine_EXTENSION_VERSION",
       "SnapshotDebugger_EXTENSION_VERSION",
       "XDT_MicrosoftApplicationInsights_Mode",
       "XDT_MicrosoftApplicationInsights_PreemptSdk",
       "APPLICATIONINSIGHTS_CONFIGURATION_CONTENT",
       "XDT_MicrosoftApplicationInsightsJava",
       "XDT_MicrosoftApplicationInsights_NodeJS",
     ]
   }
}

resource "azurerm_linux_function_app_slot" "stage" {
  name                       = "stage"
  storage_account_name       = azurerm_linux_function_app.main.storage_account_name
  storage_account_access_key = azurerm_storage_account.main.primary_access_key
  function_app_id            = azurerm_linux_function_app.main.id

  app_settings = {
    "API_KEYS" = var.api_keys
    "AzureWebJobsFeatureFlags" = "EnableWorkerIndexing"
    "DOC_MESSAGE" = "WRLC patron authorization service"
    "ENDPOINT" = "https://api-na.hosted.exlibrisgroup.com/almaws/v1/users/"
    "STATIC_PARAMS" = "{'user_id_type': 'all_unique', 'view': 'full', 'expand': 'none'}"
  }

  client_certificate_mode = "Required"

  site_config {
    application_insights_connection_string = azurerm_application_insights.main.connection_string
    application_insights_key = azurerm_application_insights.main.instrumentation_key
    ftps_state = "FtpsOnly"
    http2_enabled = true

    application_stack {
      python_version = "3.11"
    }
  }

  daily_memory_time_quota = 0
  builtin_logging_enabled = false
  https_only = true
}

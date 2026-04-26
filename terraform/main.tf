provider "azurerm"{
	features {}
	subscription_id = "1c600112-0577-4e19-9c6b-39ab98560813"
}

resource "azurerm_resource_group" "cspm_lab" {
	name	= "cspm-lab-rg"
	location= "Central India"
}

resource "azurerm_storage_account" "vulnerable" {
	name			= "vulnstoragecspm001"
	resource_group_name	= azurerm_resource_group.cspm_lab.name
	location		= azurerm_resource_group.cspm_lab.location
	account_tier		= "Standard"
	account_replication_type= "LRS"
	allow_nested_items_to_be_public= true
}

resource "azurerm_network_security_group" "vulnerable_nsg" {
	name			= "vulnerable-nsg"
	location		= azurerm_resource_group.cspm_lab.location
	resource_group_name	= azurerm_resource_group.cspm_lab.name

	security_rule {
		name			= "allow-all-ssh"
		priority		= 100
		direction		= "Inbound"
		access			= "Allow"
		protocol		= "Tcp"
		source_port_range	= "*"
		destination_port_range	= "22"
		source_address_prefix	= "*"
		destination_address_prefix	= "*"
	}
}

from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.compute import ComputeManagementClient
from ai_engine import analyze_all_findings
import json, os
from dotenv import load_dotenv

load_dotenv()
SUBSCRIPTION_ID = os.getenv('AZURE_SUBSCRIPTION_ID')
credential = DefaultAzureCredential()
findings = []

def check_storage_public_access():
    client = StorageManagementClient(credential, SUBSCRIPTION_ID)
    for account in client.storage_accounts.list():
        if account.allow_blob_public_access:
            findings.append({
                'resource': account.name,
                'type': 'StorageAccount',
                'finding': 'Public blob access is ENABLED',
                'severity': 'HIGH',
                'resource_id': account.id
            })

def check_nsg_open_ports():
    client = NetworkManagementClient(credential, SUBSCRIPTION_ID)
    for nsg in client.network_security_groups.list_all():
        for rule in (nsg.security_rules or []):
            if (rule.access == 'Allow' and
                rule.direction == 'Inbound' and
                rule.source_address_prefix == '*' and
                rule.destination_port_range in ['22', '3389', '*']):
                findings.append({
                    'resource': nsg.name,
                    'type': 'NSG',
                    'finding': f'Port {rule.destination_port_range} open to internet',
                    'severity': 'CRITICAL',
                    'resource_id': nsg.id
                })

def check_keyvault_softdelete():
    client = KeyVaultManagementClient(credential, SUBSCRIPTION_ID)
    for vault in client.vaults.list():
        props = vault.properties
        if not props.enable_soft_delete:
            findings.append({
                'resource': vault.name,
                'type': 'KeyVault',
                'finding': 'Soft delete is DISABLED',
                'severity': 'HIGH',
                'resource_id': vault.id
            })
        if not props.enable_purge_protection:
            findings.append({
                'resource': vault.name,
                'type': 'KeyVault',
                'finding': 'Purge protection is DISABLED',
                'severity': 'MEDIUM',
                'resource_id': vault.id
            })

def check_vm_disk_encryption():
    client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
    for vm in client.virtual_machines.list_all():
        if not vm.storage_profile.os_disk.encryption_settings:
            findings.append({
                'resource': vm.name,
                'type': 'VirtualMachine',
                'finding': 'OS disk encryption is DISABLED',
                'severity': 'HIGH',
                'resource_id': vm.id
            })

def check_storage_https():
    client = StorageManagementClient(credential, SUBSCRIPTION_ID)
    for account in client.storage_accounts.list():
        if not account.enable_https_traffic_only:
            findings.append({
                'resource': account.name,
                'type': 'StorageAccount',
                'finding': 'HTTPS only traffic is DISABLED',
                'severity': 'HIGH',
                'resource_id': account.id
            })

if __name__ == '__main__':
    print('Running security checks...')
    check_storage_public_access()
    check_nsg_open_ports()
    check_keyvault_softdelete()
    check_vm_disk_encryption()
    check_storage_https()
    print(f'Found {len(findings)} issues. Running AI analysis...')
    enriched = analyze_all_findings(findings)
    with open('report.json', 'w') as f:
        json.dump(enriched, f, indent=2)
    print(json.dumps(enriched, indent=2))
    print(f'Done. Report saved to report.json')

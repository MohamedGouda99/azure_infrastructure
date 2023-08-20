import subprocess
import json

def get_security_groups():
    try:
        # Execute 'az network nsg list' to fetch the list of security groups
        result = subprocess.run(['az', 'network', 'nsg', 'list'], capture_output=True, text=True)
        security_groups = json.loads(result.stdout)
        return security_groups
    except Exception as e:
        print(f"Error fetching security groups: {str(e)}")
        return []

def add_ssh_rule(resource_group_name, security_group_name):
    try:
        # Execute 'az network nsg rule create' to add an SSH rule to the security group
        subprocess.run(['az', 'network', 'nsg', 'rule', 'create', '--resource-group', resource_group_name,
                        '--nsg-name', security_group_name, '--name', 'AllowSSH', '--protocol', 'Tcp', '--priority', '1000',
                        '--destination-port-ranges', '22', '--access', 'Allow', '--description', 'SSH rule'], check=True)
        print(f"Added SSH rule to {security_group_name}")
    except Exception as e:
        print(f"Error adding SSH rule to {security_group_name}: {str(e)}")

# Fetch the list of security groups
security_groups = get_security_groups()

# Iterate through security groups and add SSH rule
for security_group in security_groups:
    resource_group_name = security_group['resourceGroup']
    security_group_name = security_group['name']
    add_ssh_rule(resource_group_name, security_group_name)

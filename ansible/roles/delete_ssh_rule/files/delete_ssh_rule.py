import subprocess
import json
import sys

def get_security_groups():
    try:
        # Execute 'az network nsg list' to fetch the list of security groups
        result = subprocess.run(['az', 'network', 'nsg', 'list'], capture_output=True, text=True)
        security_groups = json.loads(result.stdout)
        return security_groups
    except Exception as e:
        print(f"Error fetching security groups: {str(e)}")
        return []

def delete_ssh_rule(resource_group_name, security_group_name):
    try:
        # Execute 'az network nsg rule delete' to delete the SSH rule from the security group
        process = subprocess.Popen(['az', 'network', 'nsg', 'rule', 'delete', '--resource-group', resource_group_name,
                                    '--nsg-name', security_group_name, '--name', 'AllowSSH'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        
        # Provide input 'y' for confirmation
        process.communicate(input='y\n'.encode())
        
        if process.returncode == 0:
            print(f"Deleted SSH rule from {security_group_name}")
        else:
            print(f"Error deleting SSH rule from {security_group_name}")
            print(process.stderr.read().decode())
    except Exception as e:
        print(f"Error deleting SSH rule from {security_group_name}: {str(e)}")

# Fetch the list of security groups
security_groups = get_security_groups()

# Iterate through security groups and delete SSH rule
for security_group in security_groups:
    resource_group_name = security_group['resourceGroup']
    security_group_name = security_group['name']
    delete_ssh_rule(resource_group_name, security_group_name)

import yaml
import sys
import os

def update_config(rds_endpoint):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    config_path = os.path.join(project_root, 'config.yaml')
    
    print(f"Looking for config file at: {config_path}")
    # Read the existing config
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Update the RDS host
    if 'rds' not in config:
        config['rds'] = {}
    config['rds']['host'] = rds_endpoint
    
    # Write the updated config back to the file
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_config.py <rds_endpoint>")
        sys.exit(1)
    
    rds_endpoint = sys.argv[1]
    update_config(rds_endpoint)
    print(f"Updated config.yaml with RDS endpoint: {rds_endpoint}")
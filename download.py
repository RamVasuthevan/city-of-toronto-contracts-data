import requests

# Toronto Open Data is stored in a CKAN instance. Its APIs are documented here:
# https://docs.ckan.org/en/latest/api/

# Base URL for the CKAN instance
base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"

# List of dataset IDs to retrieve
dataset_ids = [
    "tobids-non-competitive-contracts",
    "tobids-awarded-contracts",
    "tobids-all-open-solicitations"
]

for dataset_id in dataset_ids:
    # Construct the URL for the package_show action
    url = base_url + "/api/3/action/package_show"
    params = {"id": dataset_id}
    
    # Retrieve the package metadata
    package = requests.get(url, params=params).json()
    
    # Check if the package retrieval was successful
    if package.get("success"):
        # Iterate over the resources in the package
        for resource in package["result"]["resources"]:
            # For datastore_active resources
            if resource["datastore_active"]:
                # To get all records in CSV format
                csv_url = base_url + "/datastore/dump/" + resource["id"]
                resource_dump_data = requests.get(csv_url).text
                
                # Define the filename using the resource name
                filename = resource["name"] + ".csv"
                
                # Write the CSV data to a file
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(resource_dump_data)

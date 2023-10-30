import requests

# Define the query parameters
query_parameters = {
    "rcsb_entry_info.space_group_name_H-M": "P 1 2 1 1",
    "service-mode": "graph-ql",
    "return_type": "entry"
}

# Make an HTTP request with the specified query parameters
response = requests.get("https://search.rcsb.org/rcsbsearch/v1/query?json=",
                        params=query_parameters)

# Parse the JSON response
data = response.json()

# Extract the list of PDB IDs
pdb_ids = [entry["identifier"] for entry in data["result_set"]]

# Print the list of PDB IDs
for pdb_id in pdb_ids:
    print(pdb_id)

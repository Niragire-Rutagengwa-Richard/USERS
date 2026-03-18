import requests
import json
import csv

# --- Configuration ---
DHIS2_BASE_URL = "https://online.hisprwanda.org/microplanrw"
USERNAME = "rniragire2"
PASSWORD = "Atete@42"
CSV_FILE = "users.csv"

headers = {"Content-Type": "application/json"}
auth = (USERNAME, PASSWORD)

with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        user = {
            "firstName": row["firstName"].strip(),
            "surname": row["surname"].strip(),
            "phoneNumber": row["Phone Number"].strip(),
            "email": row["Email Address"].strip(),
            "organisationUnits": [{"id": row["Organisation Unit ID"].strip()}],
            "dataViewOrganisationUnits": [{"id": row["dataViewOrganisationUnits"].strip()}],
            "teiSearchOrganisationUnits": [{"id": row["teiSearchOrganisationUnits"].strip()}],
            "userCredentials": {
                "username": row["username"].strip(),
                "password": row["password"].strip(),
                "userRoles": [{"id": row["User Role ID"].strip()}]
            }
        }

        response = requests.post(
            f"{DHIS2_BASE_URL}/api/users",
            headers=headers,
            auth=auth,
            data=json.dumps(user)
        )

        if response.status_code in (200, 201):
            print(f"✅ User '{row['username'].strip()}' created successfully.")
        else:
            print(f"❌ Failed to create user '{row['username'].strip()}': {response.text}")
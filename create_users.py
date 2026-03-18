# ============================================================
# DHIS2 Tool - Bulk User Creation from CSV
# ============================================================

import requests
import json
import csv
import os

# --- Configuration ---
DHIS2_BASE_URL = "https://online.hisprwanda.org/microplanrw"
USERNAME = "rniragire2"
PASSWORD = "Atete@42"  # Replace with your actual password before running
CSV_FILE = "users.csv"
TEMPLATE_FILE = "users_template.csv"

# --- CSV column headers and a sample row ---
CSV_COLUMNS = [
    "firstName", "surname", "Phone Number", "Email Address",
    "Organisation Unit ID", "User Role ID",
    "dataViewOrganisationUnits", "teiSearchOrganisationUnits",
    "username", "password"
]

SAMPLE_ROW = [
    "John", "Doe", "0780000000", "johndoe@example.com",
    "oFyeLZWeq8f", "Wj9ijncFp7Y",
    "oFyeLZWeq8f", "oFyeLZWeq8f",
    "jdoe", "Rwanda@2026"
]

def generate_template():
    """Generate a blank CSV template with one sample row."""
    with open(TEMPLATE_FILE, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)
        writer.writerow(SAMPLE_ROW)
    print(f"✅ Template saved as '{TEMPLATE_FILE}'.")

 #Uncomment the line below to generate the template ---
generate_template()

# --- Create users from CSV ---
headers = {"Content-Type": "application/json"}
auth = (USERNAME, PASSWORD)

if not os.path.exists(CSV_FILE):
    print(f"❌ '{CSV_FILE}' not found. Uncomment generate_template() to create a template.")
else:
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
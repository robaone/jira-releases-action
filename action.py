from jira import JIRA
import os

# Connect to JIRA
jira = JIRA(server=os.getenv('JIRA_SERVER'), basic_auth=(os.getenv('JIRA_EMAIL'), os.getenv('JIRA_API_TOKEN')))

# Fetch environment variables
is_released = os.getenv('JIRA_RELEASED_STATUS') == 'true'
release_name = os.getenv('JIRA_VERSION')
project_key = os.getenv('JIRA_PROJECT')
release_description = os.getenv('JIRA_RELEASE_DESCRIPTION')

# Check if the version already exists
existing_versions = jira.project_versions(project_key)
version = next((v for v in existing_versions if v.name == release_name), None)

if version:
    # Update the existing version if it already exists
    version.update(
        released=is_released,
        description=release_description
    )
    print(f"Updated existing version '{release_name}' in project '{project_key}' with new status and description.")
else:
    # Create the version if it does not exist
    jira.create_version(
        name=release_name,
        project=project_key,
        archived=False,
        released=is_released,
        description=release_description
    )
    print(f"Created new version '{release_name}' in project '{project_key}'.")

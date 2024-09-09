import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Path to the JSON key file downloaded in step 3 (your service account credentials)
credentials_file = '_tools/jenkins/test/automationproject-387405-f218c150f1f5.json'

# ID of the Google Drive folder where you want to list and get the latest file
folder_id = '1sZENmvMxqY0rV29KI-PR4PELe_v263-9'

# Retry settings
max_retries = 5
retry_delay = 5  # seconds

try:
    # Authenticate using service account credentials
    credentials = service_account.Credentials.from_service_account_file(credentials_file)

    # Build the service object for interacting with Drive API
    service = build('drive', 'v3', credentials=credentials)

    for attempt in range(max_retries):
        try:
            # List files in the specified Google Drive folder, sorted by modified time (the latest first)
            results = service.files().list(q=f"'{folder_id}' in parents", orderBy='modifiedTime desc',
                                           pageSize=1).execute()
            files = results.get('files', [])

            if files:
                latest_file = files[0]
                file_id = latest_file['id']

                # Check if webViewLink exists in the latest_file metadata
                webViewLink = latest_file.get('webViewLink', None)

                # If webViewLink is not found, attempt to set file permissions to make it shareable
                if not webViewLink:
                    # Set the file to be shareable
                    permission = {
                        'type': 'anyone',
                        'role': 'reader'
                    }
                    service.permissions().create(
                        fileId=file_id,
                        body=permission,
                        fields='id'
                    ).execute()

                    # Retrieve the file metadata again to get the webViewLink
                    latest_file = service.files().get(fileId=file_id, fields='id, name, webViewLink').execute()
                    webViewLink = latest_file.get('webViewLink', None)

                print(f"*Google Drive Screenshot Folder Name:* {latest_file['name']}")
                print(f"*Google Drive Screenshot Folder link:* {webViewLink}")
                break
            else:
                time.sleep(retry_delay)
        except HttpError as error:
            time.sleep(retry_delay)
    else:
        print("*Max retries reached. No files found or an error occurred.*")
        exit(1)  # Exit with an error code

except HttpError as error:
    print(f"*An error occurred: {error}*")
    exit(1)  # Exit with an error code
except IndexError as error:
    print(f"*An error occurred: {error}*")
    exit(1)  # Exit with an error code

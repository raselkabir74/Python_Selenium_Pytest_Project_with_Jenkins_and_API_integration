import os
import datetime
import zipfile
import pytz
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import xml.etree.ElementTree as ET

# Create timezone objects for Bangladesh and Lithuania
bangladesh_timezone = pytz.timezone('Asia/Dhaka')
lithuania_timezone = pytz.timezone('Europe/Vilnius')

# Get the current time in UTC
current_datetime_utc = datetime.datetime.now(pytz.utc)

# Convert to Bangladesh and Lithuania time zones
current_datetime_bangladesh = current_datetime_utc.astimezone(bangladesh_timezone)
current_datetime_lithuania = current_datetime_utc.astimezone(lithuania_timezone)
# Threshold for file removal
threshold_time = current_datetime_utc - datetime.timedelta(days=3)

# Generate date and time strings in the desired formats
date_time_string_bangladesh = current_datetime_bangladesh.strftime("%Y-%m-%d_%I-%M-%S_%p")
date_time_string_lithuania = current_datetime_lithuania.strftime("%Y-%m-%d_%I-%M-%S_%p")

# Use the generated date and time string in the output path
output_path = f'report-screenshot-zip/BD__{date_time_string_bangladesh}__LT' \
              f'__{date_time_string_lithuania}.zip'

folder_path = 'reports_screenshot'

tree = ET.parse('test_results.xml')
root = tree.getroot()

failed_tests = []
for testcase in root.iter('testcase'):
    failure = testcase.find('failure')
    error = testcase.find('error')
    if failure is not None or error is not None:
        failed_tests.append(testcase.attrib['name'])

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".png"):
            test_name = os.path.splitext(file)[0]
            if test_name not in failed_tests:
                file_path = os.path.join(root, file)
                os.remove(file_path)

with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Iterate through all the files and subdirectories in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Get the full path of the file
            file_path = os.path.join(root, file)

            # Calculate the relative path inside the zip file
            relative_path = os.path.relpath(file_path, folder_path)

            # Add the file to the zip file
            zipf.write(file_path, arcname=relative_path)
print('Folder zipped successfully.')

# Path to the JSON key file downloaded in step 3
credentials = service_account.Credentials.from_service_account_file(
    '_tools/jenkins/test/automationproject-387405-f218c150f1f5.json')

# ID of the Google Drive folder where you want to upload the file
folder_id = '1sZENmvMxqY0rV29KI-PR4PELe_v263-9'

# Path to the zip file you want to upload
zip_file_path = output_path

# Create a service client
service = build('drive', 'v3', credentials=credentials)

# List files in the specified Google Drive folder
results = service.files().list(q=f"'{folder_id}' in parents").execute()
files = results.get('files', [])
# Iterate through files and delete those older than 5 days
for file in files:
    name = file['name']
    try:
        timestamp_str = name.split('__')[1]
        timestamp_format = "%Y-%m-%d_%I-%M-%S_%p"

        # Parse the timestamp into a datetime object
        timestamp = datetime.datetime.strptime(timestamp_str, timestamp_format)
        local_timezone = pytz.timezone('Europe/Vilnius')
        timestamp = local_timezone.localize(timestamp).astimezone(pytz.utc)

        if timestamp < threshold_time:
            try:
                # Delete the file
                service.files().delete(fileId=file['id']).execute()
                print(f"Deleted file: {file['name']} (ID: {file['id']})")
            except HttpError as error:
                print(f"An error occurred while deleting file {file['name']} (ID: {file['id']}): {error}")
    except Exception as e:
        print(f"Error processing file {name}: {e}")

# Create a media file upload object
media = MediaFileUpload(zip_file_path, mimetype='application/zip',
                        resumable=True)

# Create the file metadata
file_metadata = {
    'name': os.path.basename(zip_file_path),
    'parents': [folder_id]
}

# Upload the file
request = service.files().create(body=file_metadata, media_body=media,
                                 fields='id')
response = None

while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"Uploaded {int(status.progress() * 100)}%")

print('File uploaded successfully!')

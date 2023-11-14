from google.cloud import logging
from datetime import datetime, timezone

def get_creators():
    client = logging.Client()
    time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    
    empty_projects = open("empty_projects.txt", "a")
    with open('empty.txt', 'r') as projects:
        for project in projects:
            filter_str = (
                f'logName="projects/{project}/logs/cloudaudit.googleapis.com%2Factivity"'
                f' AND protoPayload.methodName="CreateProject"'
                f' AND timestamp<="{datetime.now(timezone.utc).strftime(time_format)}"'
            )
            for entry in client.list_entries(filter_=filter_str,resource_names=["projects/{project}"]):
                empty_projects.write(f"{project} / {entry.payload['authenticationInfo']['principalEmail']}\n")

if __name__ == "__main__":    
    get_creators()
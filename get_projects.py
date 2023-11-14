from google.cloud import asset_v1
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--organization_id", help="specify organization id")
    args = parser.parse_args()
    organization_id = args.organization_id
    return organization_id

def get_projects(organization):
    scope = f"organizations/{organization}"
    query = "name://cloudresourcemanager.googleapis.com/projects"
    client = asset_v1.AssetServiceClient()
    projects = client.search_all_resources(request={"scope": scope,"query": query,})
    output = open("projects.txt", "a")
    for i in projects:
        project = i.name.split("//cloudresourcemanager.googleapis.com/projects/")[1]
        if(project.startswith("sys")):
            continue
        display_name = i.display_name
        output.write(f"{display_name} / {project}\n")
    output.close()


if __name__ == "__main__":    
    organization_id = parse_args()
    get_projects()
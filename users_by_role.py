from google.cloud import asset_v1
import argparse
import re

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--role", help="specify role")
    args = parser.parse_args()
    role = args.role
    return role

def users_by_role(role, source = ""):
    client = asset_v1.AssetServiceClient()
    results = open("roles.txt", "a")
    empty_results = open("empty.txt", "a")
    with open('projects.txt', "r") as projects:
        for project in projects:
            project = project.split("/")[0]
            users = str(client.search_all_iam_policies(request={"scope": "projects/{0}".format(project), "query": f"policy:roles/{role}"}))
            owners = re.findall(r'members: "(.+?)"', users)
            if not owners:
                empty_results.write(f"{project}\n")
                continue
            results.write(f"{project} / {owners}\n")

if __name__ == "__main__":    
    role = parse_args()
    users_by_role()
import os
import sys
sys.path.append("/home/ubuntu/work")
from linear_helper import add_comment, update_issue_label

issue_id = "ea7637c2-9f16-4bc6-b4e9-e6ed2676fc91"
label_id = "a43efb77-534a-4e39-8ff3-76f0e42019d1" # agent:fred

def get_file_content(path):
    with open(path, "r") as f:
        return f.read().strip()

if __name__ == "__main__":
    summary_path = "/home/ubuntu/work/active-oahu-static-1171/site/_seo/reports/summary-gro-1171.md"
    walkthrough_path = "/home/ubuntu/work/active-oahu-static-1171/site/_seo/reports/walkthrough-gro-1171.md"
    
    summary_body = get_file_content(summary_path)
    walkthrough_body = get_file_content(walkthrough_path)
    
    print("Posting Summary Response...")
    res_summary = add_comment(issue_id, summary_body)
    print("Summary Response Result:", res_summary)
    
    print("\nPosting Walkthrough...")
    res_walkthrough = add_comment(issue_id, walkthrough_body)
    print("Walkthrough Result:", res_walkthrough)
    
    print("\nUpdating Labels to agent:fred...")
    res_label = update_issue_label(issue_id, [label_id])
    print("Label Update Result:", res_label)

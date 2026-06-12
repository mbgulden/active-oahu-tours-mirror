#!/usr/bin/env python3
import sys
import os

def main():
    master_path = "/home/ubuntu/work/active-oahu-static/site/_seo/reports/06-questions-audit/master-questions.md"
    decision_path = "/home/ubuntu/work/active-oahu-static/site/_seo/reports/06-questions-audit/decision-document-2026-06-12.md"
    roadmap_path = "/home/ubuntu/work/active-oahu-static/site/_seo/aot-90-day-roadmap-2026-06-12.md"
    
    # 1. Load Master Questions
    if not os.path.exists(master_path):
        print(f"FAIL: {master_path} does not exist.")
        sys.exit(1)
        
    with open(master_path, "r", encoding="utf-8") as f:
        master_content = f.read()
        
    master_ids = set()
    for line in master_content.split("\n"):
        if line.strip().startswith("|") and not line.strip().startswith("| :---") and not line.strip().startswith("| ID "):
            parts = [p.strip() for p in line.split("|")][1:-1]
            if len(parts) >= 6:
                qid = parts[0].replace("**", "")
                master_ids.add(qid)
                
    print(f"Loaded {len(master_ids)} master question IDs.")
    
    # 2. Load Decision Document
    if not os.path.exists(decision_path):
        print(f"FAIL: {decision_path} does not exist.")
        sys.exit(1)
        
    with open(decision_path, "r", encoding="utf-8") as f:
        decision_content = f.read()
        
    decision_ids = set()
    for qid in master_ids:
        if qid in decision_content:
            decision_ids.add(qid)
            
    print(f"Found {len(decision_ids)} of the master questions in the Decision Document.")
    
    # 3. Load Roadmap Document
    if not os.path.exists(roadmap_path):
        print(f"FAIL: {roadmap_path} does not exist.")
        sys.exit(1)
        
    with open(roadmap_path, "r", encoding="utf-8") as f:
        roadmap_content = f.read()
        
    roadmap_ids = set()
    for qid in master_ids:
        if qid in roadmap_content:
            roadmap_ids.add(qid)
            
    print(f"Found {len(roadmap_ids)} of the master questions in the 90-Day Roadmap.")
    
    # Check intersection and union
    intersection = decision_ids.intersection(roadmap_ids)
    union = decision_ids.union(roadmap_ids)
    
    print("\n--- VALIDATION RESULTS ---")
    print(f"Total Unique Mapped Questions: {len(union)} / {len(master_ids)}")
    print(f"Overlapping Questions (in both): {len(intersection)}")
    
    # Check if there are any master questions that are completely missing
    missing_ids = master_ids.difference(union)
    if missing_ids:
        print(f"FAIL: The following IDs are completely missing: {missing_ids}")
        sys.exit(1)
    else:
        print("PASS: No questions are missing.")
        
    # We allow some overlap if a decision question is also listed in the roadmap
    # for technical tracking, but they must all be covered.
    
    if len(union) == len(master_ids):
        print("SUCCESS: Roadmap and Decision Document validation PASSED.")
        sys.exit(0)
    else:
        print("FAIL: Validation failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()

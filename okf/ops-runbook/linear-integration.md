# Linear Integration for AOT

## Project

- **Name**: Active Oahu Tours — Static Mirror Migration
- **Linear ID**: `149964ae-d92e-46c4-803a-bd0ac0c8e97e`
- **Team**: GRO (GrowthWebDev)
- **URL**: https://linear.app/growthwebdev/project/active-oahu-tours-static-mirror-migration

## Common labels

| Label | Meaning |
|---|---|
| `agent:kai` | Kai (CSS/infra/perf) |
| `agent:agy` | AGY (research/audit) |
| `agent:fred` | Fred (strategy/governance) |
| `agent:ned` | Ned (review) |
| `Improvement` | Quality improvement (not a bug) |
| `Bug` | Defect |
| `Feature` | New functionality |
| `type:research` | Needs research phase before action |
| `type:docs` | Documentation work |
| `type:infra-readonly` | Read-only infrastructure audit |
| `type:observability` | Monitoring/measurement work |
| `agent:agy-thinking` | AGY has analyzed and posted a plan in comments |

## Workflow

```
Backlog (P0/P1)
   │
   ▼  agent picks up
In Progress
   │
   ├─► PR opened (post link in comments)
   │
   ▼  Michael merges to main
Done
   │
   ▼  verified in production
(Done)
```

**Auto-transition:** Linear can be configured to auto-transition issues to
Done when a PR is merged. Currently this is **not** wired up — do it manually.

## State transitions

Use the Linear API directly (not the web UI) for consistency. Helper:

```python
STATE_TODO = '3d29ebe3-00cf-428b-b52a-bfecb5ae4410'
STATE_IN_PROGRESS = '734901ee-58f0-457c-b9a0-f911c0da13a4'
STATE_DONE = 'bbf71b3e-9a05-48ce-9418-df8b9c0b8fec'
STATE_CANCELED = 'a19484ec-9752-4c31-8110-f5043312e328'

mutation = """
mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    success
    issue { identifier state { name } }
  }
}
"""
```

**Common errors to avoid** (learned the hard way):
- `stateId` must be the **full UUID**, not a prefix. (Earlier mistake: `bbf71b3e-d9e7-4dca-b74e-8871fc77c39d` was wrong, correct is `bbf71b3e-9a05-48ce-9418-df8b9c0b8fec`.)
- `labelIds` must be full UUIDs as a list, not nested in `input` object.
- Always verify with `success: true` check before assuming it worked.

## Standard comment patterns

### When opening a PR
```
Implemented. PR: <github-url>
Preview: <pages-preview-url>
Verified: <what was verified>
Will close <GRO-XXXX> once Michael merges.
```

### When shipping CF edge changes
```
Implemented at the edge (no PR).
CF Ruleset: <id>
Rule description: <text>
Verified:
- Blocked path: 410
- Legit paths: 200
- Security Events show rule firing as expected
```

### When deferring / planning only
```
Audit + remediation plan posted.
Phase 1: <description>  — owner: <agent>, effort: <estimate>
Phase 2: <description>  — owner: <agent>, effort: <estimate>
Closed as planned (will reopen when execution starts).
```

### When canceling
```
Cancelled per Michael: "<verbatim reason>"
State remains as-is if mitigation already in place, else Canceled.
```

## Search patterns

```bash
# All P0s in Backlog
python3 -c "
import os, json, urllib.request
api_key = os.environ['LINEAR_API_KEY']
q = '''
{ project(id: \"149964ae-d92e-46c4-803a-bd0ac0c8e97e\") {
    issues(filter: {state: {name: {eq: \"Backlog\"}}, priority: {eq: 0}}) {
      nodes { identifier title }
    }
  }
}
'''
req = urllib.request.Request('https://api.linear.app/graphql',
    data=json.dumps({'query': q}).encode(),
    headers={'Authorization': api_key, 'Content-Type': 'application/json'},
    method='POST')
print(json.loads(urllib.request.urlopen(req).read()))
"
```

## See also

- [git-workflow.md](git-workflow.md) — branch and PR workflow
- [deploy-process.md](deploy-process.md) — when state transitions happen
- [testing-guidelines.md](testing-guidelines.md) — verification before marking Done
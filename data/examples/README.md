# Fictional data examples

The original roster/scenario examples are development experiments, **not app
seed data**. The newer [buildathon pack](../README.md) provides tracked connected
records with a separate explicit loader. Both are purpose-built and do not use
HIR/MIST content.

| File | What it provides |
| --- | --- |
| [generate_users.py](generate_users.py) | A deterministic local roster of 70 fictional people with varied illustrative roles; service identities are not included |
| [edge-cases.json](edge-cases.json) | Five fictional scenarios covering missing/incomplete information, conflicting values, future projections and source-format variation; not assessment records |
| `users.csv` (generated, ignored) | The generator's local output, not a tracked dataset or app input |
| [buildathon/app/records.json](buildathon/app/records.json) | Connected synthetic database inputs; see the single [file index and load instructions](../README.md) |
| [buildathon/chatbot/demo-guide.txt](buildathon/chatbot/demo-guide.txt) | Fictional software guidance for a separate, approved demonstration upload; not laboratory policy |

From the repository root, after [Python setup](../../docs/DEVELOPMENT.md#local-prerequisites-and-installation):

```powershell
.venv\Scripts\python.exe data\examples\generate_users.py
```

The command writes `data/examples/users.csv`. An older local roster under
`data/synthetic/buildathon/` remains ignored and is not moved automatically.
Roles are illustrative labels, not approved access assignments or laboratory
policy. Loading examples into the app or changing population, schema or rules
requires a separate approved task.

For the executable one-assessment, two-version, seven-identity fixture, follow
the [local pilot walkthrough](../../docs/BUILDATHON.md) instead.

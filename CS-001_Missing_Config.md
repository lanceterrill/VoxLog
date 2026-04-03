# CS-001 — Missing config.json

| Field       | Value                          |
|-------------|--------------------------------|
| **ID**      | CS-001                         |
| **Title**   | Missing config.json            |
| **Severity**| MEDIUM                         |
| **Engine**  | Proprietary                    |
| **Category**| Config                         |
| **Tag**     | ASI03                          |
| **License** | Proprietary                    |

## Finding

The `config.json` file is missing. The agent may not be properly configured, which could result in unexpected behavior or failed initialization.

## Recommendation

Ensure `config.json` is present in the expected directory and contains all required configuration keys before deploying the agent.

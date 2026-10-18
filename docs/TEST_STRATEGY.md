# Reward integrity test strategy

**Primary risk:** incorrect credits after provider callbacks. Our oracle is **one credit per unique verified completed transaction**.

| Risk | Test technique | Oracle |
| --- | --- | --- |
| Duplicate delivery | Replay / negative | Exactly one credit |
| Concurrent duplicates | Concurrency | Exactly one committed row |
| Service restart | Persistence | No second reward |
| Conflicting replay | Security negative | Reject player/amount substitution |
| Cancelled/failed ad | State transition | Zero credit |
| Unauthorized callback | Authorization | HTTP 403 |
| Invalid reward amount | Boundary | Reject nonpositive |

The `x-demo-secret` is **only a controlled mock authentication mechanism**. Real Google AdMob SSV requires ECDSA signature verification, key rotation, timestamp checks and event validation. This repository does not claim live ad-network integration.

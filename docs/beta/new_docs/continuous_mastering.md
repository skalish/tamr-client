# Continuous Mastering
```python
from getpass import getpass

import tamr_client as tc

username = input("Tamr Username:")
password = getpass("Tamr Password:")
auth = tc.UsernamePasswordAuth(username, password)

session = tc.session.from_auth(auth)
instance = tc.Instance(host="localhost", port=9100)

project_id = "1" # replace with your project ID
project = tc.project.by_resource_id(project_id)

def check(op: tc.Operation):
    if not tc.operation.succeeded(op):
        raise RuntimeError("Operation failed.")
    return op

check(tc.mastering.update_unified_dataset(session, project))

check(tc.mastering.generate_pairs(session, project))

check(tc.mastering.apply_feedback(session, project))

check(tc.mastering.update_pair_results(session, project))

check(tc.mastering.update_high_impact_pairs(session, project))

check(tc.mastering.update_cluster_results(session, project))

check(tc.mastering.publish_clusters(session, project))
```

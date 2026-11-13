"""Generate a local-only, fictional buildathon user roster."""

import csv
from pathlib import Path

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "users.csv"
ROLE_GROUPS = (
    (36, ("employee",)),
    (8, ("team_lead",)),
    (10, ("assessor",)),
    (5, ("technical_supervisor",)),
    (4, ("employee", "assessor")),
    (3, ("team_lead", "assessor")),
    (2, ("squad_admin",)),
    (1, ("platform_admin",)),
    (1, ("assessor", "technical_supervisor")),
)
FIELDNAMES = (
    "synthetic_user_id",
    "display_name",
    "identity_type",
    "illustrative_demo_roles",
    "synthetic_only",
)


def generate_users(path: Path = OUTPUT_PATH) -> int:
    """Write 70 fictional people; role labels do not grant application access."""
    path.parent.mkdir(parents=True, exist_ok=True)
    user_number = 0
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=FIELDNAMES)
        writer.writeheader()
        for count, roles in ROLE_GROUPS:
            for _ in range(count):
                user_number += 1
                writer.writerow(
                    {
                        "synthetic_user_id": f"SYN-HUMAN-{user_number:03}",
                        "display_name": f"Synthetic User {user_number:03}",
                        "identity_type": "human",
                        "illustrative_demo_roles": ";".join(roles),
                        "synthetic_only": "true",
                    }
                )
    return user_number


if __name__ == "__main__":
    print(f"Wrote {generate_users()} synthetic users to {OUTPUT_PATH}.")

from pathlib import Path


def load_policies(policy_dir: str = "data/policies") -> list[dict]:
    """
    Load every markdown policy file as structured documents.
    """

    documents = []

    policy_path = Path(policy_dir)

    for file in sorted(policy_path.glob("*.md")):

        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append({
            "text": text,
            "source": file.stem  # policy_income, policy_credit vs.
        })

    return documents
# src/rag/policy_loader.py

def load_policies(path: str):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # split by lines = atomic rules
    policies = [p.strip() for p in text.split("\n") if p.strip()]
    return policies
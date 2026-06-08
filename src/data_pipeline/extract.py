import pandas as pd


def load_application_train(path: str):
    return pd.read_csv(path)


def load_bureau(path: str):
    return pd.read_csv(path)


def load_previous_application(path: str):
    return pd.read_csv(path)

def load_installments(path: str):
    return pd.read_csv(path)

def load_pos_cash(path: str):
    return pd.read_csv(path)

def load_credit_card(path: str):
    return pd.read_csv(path)
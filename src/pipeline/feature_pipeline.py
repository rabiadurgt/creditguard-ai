import pandas as pd

from src.data_pipeline.transform import basic_cleaning

from src.features.build_features import create_features
from src.features.build_bureau_features import create_bureau_features
from src.features.build_previous_features import create_previous_features
from src.features.build_installment_features import build_installment_features
from src.features.build_pos_cash_features import build_pos_cash_features
from src.features.build_credit_card_features import build_credit_card_features
from src.features.build_bureau_balance_features import build_bureau_balance_features

from src.features.feature_store import merge_features
from src.features.feature_pruning import prune_features

from src.preprocessing.missing_handler import handle_missing_values
from src.preprocessing.encoder import encode_categorical_features


class FeaturePipeline:

    def transform_application(self, df: pd.DataFrame) -> pd.DataFrame:

        # 1. basic cleaning
        df = basic_cleaning(df)

        # 2. feature engineering
        df = create_features(df)

        # 3. missing handling (numeric fix)
        df = handle_missing_values(df)

        # 4. encoding (CRITICAL FIX)
        df = encode_categorical_features(df)

        # 5. final pruning (if used in training)
        df = prune_features(df)

        return df

    def transform_full(
        self,
        app: pd.DataFrame,
        bureau: pd.DataFrame,
        prev: pd.DataFrame,
        ins: pd.DataFrame,
        pos: pd.DataFrame,
        cc: pd.DataFrame,
        bb: pd.DataFrame
    ) -> pd.DataFrame:

        # 1. application
        app = basic_cleaning(app)
        app = create_features(app)

        # 2. sub features
        bureau_f = create_bureau_features(bureau)
        prev_f = create_previous_features(prev)
        ins_f = build_installment_features(ins)
        pos_f = build_pos_cash_features(pos)
        cc_f = build_credit_card_features(cc)
        bb_f = build_bureau_balance_features(bb)

        # 3. merge
        df = merge_features(
            app,
            bureau_f,
            prev_f,
            ins_f,
            pos_f,
            cc_f,
            bb_f
        )

        # 4. missing + encoding (CRITICAL FIX)
        df = handle_missing_values(df)
        df = encode_categorical_features(df)

        # 5. prune
        df = prune_features(df)

        return df
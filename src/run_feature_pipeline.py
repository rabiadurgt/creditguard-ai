'''   application
        + 
      bureau
        +
      previous_application
'''

from src.data_pipeline.extract import (
    load_application_train,
    load_bureau,
    load_previous_application,
    load_installments
)

from src.data_pipeline.transform import basic_cleaning
from src.data_pipeline.load import save_dataframe
from src.features.build_features import create_features
from src.features.build_bureau_features import create_bureau_features
from src.features.build_previous_features import create_previous_features
from src.features.feature_store import merge_features
from src.features.build_installment_features import(
    build_installment_features
)
from src.features.build_pos_cash_features import (
    build_pos_cash_features
)



def main():

    print("Loading application data...")
    application_df = load_application_train(
        "data/raw/application_train.csv"
    )
    print(application_df.shape)

#################################################
    print("Loading bureau data...")
    bureau_df = load_bureau(
        "data/raw/bureau.csv"
    )
    print(bureau_df.shape)

#################################################

    print("Loading previous applications...")
    previous_df = load_previous_application(
        "data/raw/previous_application.csv"
    )
    print(previous_df.shape)

#################################################

    print("Loading installments data...")
    installments = load_installments(
        "data/raw/installments_payments.csv"
    )
    print(installments.shape)

#################################################

    print("Loading POS-CASH data...")
    pos = load_installments(
        "data/raw/POS_CASH_balance.csv"
    )
    print(pos.shape)

#################################################


    print("Cleaning application data...")
    application_df = basic_cleaning(
        application_df
    )

    print("Creating application features...")

    application_df = create_features(
        application_df
    )

    print("Creating bureau features...")

    bureau_features = create_bureau_features(
        bureau_df
    )

    print(bureau_features.shape)

    print("Creating previous features...")

    previous_features = create_previous_features(
        previous_df
    )

    print(previous_features.shape)

    print("Creating installment features...")

    installment_features = (
        build_installment_features(
            installments
        )
    )

    print(installment_features.shape)
    print("Creating POS features...")

    pos_features = (
        build_pos_cash_features(
            pos
        )
    )
    print(pos_features.shape)

    print("Merging feature store...")

    feature_store_df = merge_features(
        application_df,
        bureau_features,
        previous_features,
        installment_features,
        pos_features
    )

    print(feature_store_df.shape)

    print("Saving feature store...")

    save_dataframe(
        feature_store_df,
        "data/processed/train_feature_store.parquet"
    )

    print("Pipeline completed.")


if __name__ == "__main__":
    main()
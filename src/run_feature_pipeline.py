'''   application
        + 
      bureau
        +
      previous_application
'''

from data_pipeline.extract import (
    load_application_train,
    load_bureau,
    load_previous_application
)

from data_pipeline.transform import basic_cleaning
from data_pipeline.load import save_dataframe
from features.build_features import create_features
from features.build_bureau_features import create_bureau_features
from features.build_previous_features import create_previous_features
from features.feature_store import merge_features



def main():

    print("Loading application data...")

    application_df = load_application_train(
        "data/raw/application_train.csv"
    )

    print(application_df.shape)

    print("Loading bureau data...")

    bureau_df = load_bureau(
        "data/raw/bureau.csv"
    )

    print(bureau_df.shape)

    print("Loading previous applications...")

    previous_df = load_previous_application(
        "data/raw/previous_application.csv"
    )

    print(previous_df.shape)

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

    print("Merging feature store...")

    feature_store_df = merge_features(
        application_df,
        bureau_features,
        previous_features
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
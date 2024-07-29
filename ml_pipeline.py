from prefect import flow
from utils import snowflake_connection, extract_sn_data, extract_data, cleaning, preprocessing, training, get_prediction, evaluate_model, save_model

@flow(log_prints=True)
def ml_pipeline(snowflake: bool):
    if snowflake:
        connection = snowflake_connection()
        main_df = extract_sn_data(connection)
    else:
        main_df = extract_data()
    cleaned_df = cleaning(main_df)
    X_train, X_test, y_train, y_test = preprocessing(cleaned_df)
    model = training(X_train, y_train)
    prediction = get_prediction(X_test, model)
    evaluate_model(y_test, prediction) 
    save_model(model)

if __name__ == "__main__":
    ml_pipeline.serve(
        name="ml_pipeline",
        cron="0 0 1 1/3 *",
        description="Machine learning pipeline to train our demo model.",
        tags=["ml-pipeline"]
    )
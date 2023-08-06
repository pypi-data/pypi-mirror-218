import logging
import re
from google.cloud import bigquery
from google.cloud.exceptions import NotFound


logging.basicConfig(level=logging.INFO)


"""Terminology

CSV-like object is any format of text file that used new line character('\n') as record delimiter
e.g.
.csv, .tsv, fixed width files
"""


def upload_avro_data_to_ephemeral_dataset_table(
    ephemeral_id,
    project_id,
    source_id,
    table_id,
    bucket_name,
    path_to_blob,
    detect_structure=False,
):
    _load_file_from_bucket_to_bq(
        bucket_name,
        ephemeral_id,
        None,
        None,
        path_to_blob,
        project_id,
        None,
        None,
        source_id,
        table_id,
        file_format=bigquery.SourceFormat.AVRO,
        detect_structure=detect_structure,
    )


def upload_csv_like_data_to_ephemeral_dataset_table(
    ephemeral_id,
    project_id,
    source_id,
    table_id,
    bucket_name,
    path_to_blob,
    max_bad_records=0,
    field_delimiter="Ý",
    quote_character='"',
    skip_leading_rows=0,
):
    """Uploads csv-like file to BigQuery table

    Args:
        ephemeral_id (string): Ephemeral ID
        project_id (string): Google Cloud Project ID
        source_id (string): Unique name of dataset source
        table_id (string): BigQuery table ID
        bucket_name (string): Bucket name
        path_to_blob (string): Path to blob
        max_bad_records (int, optional): Maximum number of bad records allowed. Defaults to 0.
        field_delimiter (str, optional): CSV-like file field delimiter to import file into one column tables.
            Should be Unicode(0-255) character that can be found in CSV-like file.
            See https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.LoadJobConfig.html # noqa: E501
            Defaults to "Ý".
        quote_character (str, optional): Character used to quote data sections.
            See https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.LoadJobConfig.html # noqa: E501
            Defaults to '"'.
        skip_leading_rows (int, optional): Number of rows to skip when reading data.
            See https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.LoadJobConfig.html # noqa: E501
            Defaults to 0.

    Notes:
        To upload the following CSV-like file to BigQuery we need to pick field delimiter as Unicode character
        that is not presented in that file.

        e.g
        CSV file
        id,first_name,last_name\n
        1,John,Smith\n
        2,Jane,Smith\n

        to import that CSV file as one column table we can choose 'Ý' as field delimiter and
        as result we will have one column table in BigQUery since there is no such delimiter in CSV file.

        BigQuery table
        data
        --------------
        1,John,Smith
        2,Jane,Smith
    """
    _load_file_from_bucket_to_bq(
        bucket_name,
        ephemeral_id,
        field_delimiter,
        max_bad_records,
        path_to_blob,
        project_id,
        quote_character,
        skip_leading_rows,
        source_id,
        table_id,
        file_format=bigquery.SourceFormat.CSV,
        detect_structure=False,
    )


def _load_file_from_bucket_to_bq(
    bucket_name,
    ephemeral_id,
    field_delimiter,
    max_bad_records,
    path_to_blob,
    project_id,
    quote_character,
    skip_leading_rows,
    source_id,
    table_id,
    file_format: bigquery.SourceFormat,
    detect_structure,
):
    table_id = clean_table_id(table_id)
    if not table_id:
        logging.error(f"Table ID cannot be {table_id}")
    # TODO ensure the dataset ID is alphanumeric
    ephemeral_dataset_id = f"e_{source_id}_{ephemeral_id}".replace("-", "_")
    gcs_uri = f"gs://{bucket_name}/{path_to_blob}"
    logging.info(
        "Load file from {} in BigQuery {}.{}.{}".format(
            gcs_uri, project_id, ephemeral_dataset_id, table_id
        )
    )
    client = bigquery.Client(project_id)
    # Creates a unique ephemeral
    ephemeral_dataset_ref = client.dataset(ephemeral_dataset_id)
    # TODO Seperate out. This should be called a function up so the create isn't called over and
    # over. This would be exists_ok could be set to False and give us 100% confidence we aren't
    # over writing existing.
    client.create_dataset(ephemeral_dataset_ref, exists_ok=True)
    # Get an ephemeral table reference for later use.
    ephemeral_table_ref = ephemeral_dataset_ref.table(table_id)
    logging.info(
        "Load data from {} into ephemeral dataset {}".format(
            gcs_uri, ephemeral_dataset_id
        )
    )
    # Set Config for load
    load_job_config = bigquery.LoadJobConfig()
    if not detect_structure:
        load_job_config.schema = [bigquery.SchemaField("data", "STRING")]

    load_job_config.source_format = file_format
    if skip_leading_rows is not None:
        load_job_config.skip_leading_rows = skip_leading_rows
    if field_delimiter is not None:
        load_job_config.field_delimiter = field_delimiter
    if quote_character is not None:
        load_job_config.quote_character = quote_character
    if max_bad_records is not None:
        load_job_config.max_bad_records = max_bad_records
    load_job_config.allow_quoted_newlines = True
    load_job_config.write_disposition = bigquery.job.WriteDisposition.WRITE_TRUNCATE
    # Run load Job
    load_job = client.load_table_from_uri(
        gcs_uri, ephemeral_table_ref, job_config=load_job_config
    )
    try:
        load_job.result()
    except Exception as e:
        if hasattr(e, "errors"):
            msg = str(load_job.errors)
        else:
            msg = str(e)

        logging.error(f"Error uploading file {path_to_blob} to BQ . . . {msg}")
        raise e
    # Add a reference for the ephemeral_id.
    try:
        table = bigquery.Table(ephemeral_table_ref)
        table.description = ephemeral_id

        table = client.update_table(table, ["description"])
    except Exception as e:
        logging.error(
            f"Exception while setting the table description for {table.table_id}"
        )
        raise e


def copy_tables_from_ephemeral_dataset_to_final_dataset(
    ephemeral_id, project_id, source_id, final_dataset_id
):
    """Copies all tables from ephemeral dataset to final dataset in BigQuery

    Args:
        ephemeral_id (string): Ephemeral ID
        project_id (string): Google Cloud Project ID
        source_id (string): Unique name of dataset source
        final_dataset_id (string): BigQuery final dataset ID
    """
    ephemeral_dataset_id = f"e_{source_id}_{ephemeral_id}".replace("-", "_")
    logging.info(
        "Copy all tables from {} to {}".format(ephemeral_dataset_id, final_dataset_id)
    )

    client = bigquery.Client(project_id)

    client.create_dataset(final_dataset_id, exists_ok=True)

    tables = client.list_tables(ephemeral_dataset_id)

    jobs = []
    for table in tables:
        ephemeral_table_ref = client.dataset(ephemeral_dataset_id).table(table.table_id)
        final_table_ref = client.dataset(final_dataset_id).table(table.table_id)

        client.delete_table(final_table_ref, not_found_ok=True)
        copy_job_config = bigquery.CopyJobConfig()
        copy_job_config.create_disposition = (
            bigquery.job.CreateDisposition.CREATE_IF_NEEDED
        )
        copy_job_config.write_disposition = bigquery.job.WriteDisposition.WRITE_TRUNCATE
        copy_job = client.copy_table(
            ephemeral_table_ref, final_table_ref, job_config=copy_job_config
        )
        jobs.append(copy_job)

    # get the results here, so that we run our appends in parallel
    for job in jobs:
        try:
            job.result()
        except Exception as e:
            msg = ",".join(job.errors)
            logging.error(f"Errors while moving tables to source - {msg}")
            raise e


def delete_tables_by_prefix(project_id, dataset_id, table_id_prefix):
    """Delete tables by table ID prefix

    Args:
        project_id (string): Google Cloud Project ID
        dataset_id (string): Dataset ID
        table_id_prefix (string): Table ID prefix
    Notes:
        e.g. table_id_prefix=nyc_court_incremental_
        Tables with ID like nyc_court_incremental_U201923, nyc_court_incremental_U201923 and so on
        will be deleted
    """

    client = bigquery.Client(project_id)

    tables = client.list_tables(dataset_id)

    table_id_by_prefix = list(
        filter(
            lambda table_id: table_id.startswith(table_id_prefix),
            map(lambda table: table.table_id, tables),
        )
    )

    logging.info(
        f"Delete tables {table_id_by_prefix} from {project_id}.{dataset_id} dataset"
    )

    for table_id in table_id_by_prefix:
        client.delete_table(f"{project_id}.{dataset_id}.{table_id}", not_found_ok=True)


def clean_table_id(table_id: str) -> str:
    """
    Clean a table id for bq standards

    Note: this code is duplicated from ./airflow/dags/operators/common/big_query_utils.py
    # TODO add this to a package to easier distributed usage

    :param table_id: the table id for big query
    :return: table id without problems for big query
    """
    cleaned = table_id.replace(".", "_").replace("-", "_").lower()
    # replace all mustache place holders with originals.
    for s in re.finditer(r"\{\{(.+?)\}\}", table_id):
        cleaned = "".join(
            (cleaned[: s.start()], table_id[s.start() : s.end()], cleaned[s.end() :])
        )
    return cleaned


def get_max_value_from_tables(
    project_id: str, dataset: str, table_prefix: str, column: str
):
    """
    Get the maximum value for a column in multiple tables, assuming it exists in all of them
    :param project_id:
    :param dataset:
    :param table_prefix:
    :param column:
    :return:
    """
    query = (
        f"SELECT MAX({column}) as result from `{project_id}.{dataset}.{table_prefix}*`"
    )
    client = bigquery.Client(project_id)

    logging.debug(f"Running query {query}")
    job_config = bigquery.QueryJobConfig()
    query_job = client.query(query, job_config=job_config)
    for row in query_job:
        return row["result"]


def table_exists(table_name, project_id):
    """Checks if a table exists in a specific project.

    Arguments:
        table_name {str} -- The table name (with dataset)
        project_id {str} -- The project id

    Returns:
        bool -- True if the table exits.
    """
    try:
        client = bigquery.Client(project_id)
        return client.get_table(table_name) is not None
    except NotFound:
        return False

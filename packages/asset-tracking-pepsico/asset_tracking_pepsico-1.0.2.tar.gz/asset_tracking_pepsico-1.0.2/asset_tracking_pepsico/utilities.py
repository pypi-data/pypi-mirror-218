import traceback
from azure.storage.blob import BlobServiceClient


def get_block_blob_client(blob_conn_str, container_name, blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(conn_str=blob_conn_str)
        container_client = blob_service_client.get_container_client(container_name)
        block_blob_client = container_client.get_blob_client(blob_name)
        return block_blob_client
    except:
        traceback.print_exc()


def read_data_from_blob(blob_conn_str, container_name, blob_name):
    try:
        blob_client = get_block_blob_client(blob_conn_str, container_name, blob_name)
        file_name = blob_client.download_blob()
        blob_data = file_name.readall()
        return blob_data
    except:
        traceback.print_exc()


def read_file(filename):
    try:
        with open(filename) as f:
            filedata = f.read()
        f.close()
        return filedata
    except:
        traceback.print_exc()


def get_string_from_schema_list(schema_list):
    try:
        str_list = [i.__str__() for i in schema_list]
        return str_list
    except:
        traceback.print_exc()


def get_dict_from_schema_list(schema_list):
    try:
        dict_list = [i.__dict__() for i in schema_list]
        return dict_list
    except:
        traceback.print_exc()

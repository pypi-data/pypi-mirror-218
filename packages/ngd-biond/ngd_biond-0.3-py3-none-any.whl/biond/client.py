import io
import json
import mimetypes
import tempfile
import urllib
from urllib.parse import urlparse
from typing import List, Tuple, Dict
from enum import Enum
import pandas as pd

from biond.req_client import RequestsClient

"""
* Data
  - Sequences, MSA, Phylogenetic Tree
  - Operations: Create, Read (and Annotations), Update, Delete, List, Import, Export

* Jobs
  - List process types
  - Prepare process
  - Submit jobs
  - List jobs
"""


class ClientState(Enum):
    LOGGED_OUT = 1,  # Not logged
    LOGGED_IN = 2,   # Logged, but no session


class Client:
    def __init__(self, url: str):
        # No connection key
        self._api_key = None  # type: str
        self._state = ClientState.LOGGED_OUT
        if not url.endswith("/"):
            url += "/"
        self._req_client = RequestsClient(url)

    def check_backend_available(self):
        # Just check that there is a NGD backend at URL self._url
        r = self._req_client.get("test")
        if r.status_code == 200:
            return "it_works" in r.json()["content"]
        else:
            return False

    def login(self, api_key_file: str = None):
        """
        To obtain an API key, go to the GUI and create an API Key in the user profile settings Dialog

        :param api_key_file:
        :return:
        """
        # Open a file containing just the API Key string (to avoid uploading the API Key to a shared repository)
        with open(api_key_file, "rt") as f:
            api_key_data = json.load(f)
        api_key = api_key_data["api_key"]
        user = api_key_data["name"]
        # curl --cookie-jar app-cookies.txt -X PUT "$API_BASE_URL/authn?user=test_user" -H "X-API-Key: 8217b03ac2f34cfabd1388d28d420387"
        r = self._req_client.put("api/authn", None, params=dict(user=user), api_key=api_key)
        return True if r.status_code == 200 else False

    def logout(self):
        r = self._req_client.delete("api/authn")
        return True if r.status_code == 200 else False

    @property
    def req(self):
        return self._req_client


"""
Sequences, MSA, Phylogenetic Tree, 
Hierarchies?
ComputeResources
"""


class FilesAPI:
    def __init__(self, client: Client):
        self._client = client

    def get_detail(self, file_path: str) -> Dict:
        """
        Return a file or directory detail

        :param file_path:
        :return:
        """
        r = self._client.req.get(f"api/files/{file_path}")
        # TODO Process response
        return r.json()

    def create_folder(self, folder_path: str) -> Dict:
        """
        Create a folder

        :param folder_path:
        :return:
        """
        r = self._client.req.put(f"api/files/{folder_path}/")
        return r.json()

    def create_empty_file(self, file_path: str) -> Dict:
        """
        Create empty file

        :param file_path:
        :return:
        """
        r = self._client.req.put(f"api/files/{file_path}")
        return r.json()

    def upload(self, local_file_path: str,
               file_path: str, content_type: str = "application/x-fasta") -> str:
        """
        Upload a file

        :param local_file_path:
        :param file_path:
        :param content_type:
        :return:
        """
        r = self._client.req.put(f"api/files/{file_path}.content",
                                 files=dict(file=open(local_file_path, "rb")),
                                 headers={"Content-Type": content_type})
        # TODO Process response
        return r.json()

    def upload_set_of_objects_in_file(self, objects, file_path: str) -> str:
        """
        Set the list of objects in a file

        :param objects:
        :param file_path:
        :return:
        """
        r = self._client.req.put(f"api/files/{file_path}.fos",
                                 data=json.dumps(objects),
                                 headers={"Content-Type": "application/json"})
        # TODO Process response
        return r.json()

    def download(self, file_path: str, local_file_path: str) -> str:
        """
        Download a file

        :param file_path:
        :param local_file_path:
        :return:
        """
        r = self._client.req.get(f"api/files/{file_path}.content")
        with open(local_file_path, "wb") as f:
            f.write(r.content)

    def get_set_of_objects_in_file(self, file_path: str) -> str:
        """
        Get the list of objects in a file

        :param file_path:
        :return:
        """
        r = self._client.req.get(f"api/files/{file_path}.fos")
        # TODO Process response
        return r.json()


class SequencesAPI:
    def __init__(self, client: Client):
        self._client = client

    def get_filter_template(self) -> Dict:
        """
        Return template for sequence filters (for "get" method)

        :return:
        """
        r = self._client.req.get("api/browser/sequences/filters/schema")
        # TODO Process response
        return r.json()

    def get(self, filter) -> List[Dict]:
        """
        Return a list of sequences matching the filter

        :param filter:
        :return:
        """
        r = self._client.req.get("api/bos/sequences/", params=filter)
        # TODO Process response
        return r.json()

    def get_detail(self, sequence_id: str) -> Dict:
        """
        Return a sequence detail

        :param sequence_id:
        :return:
        """
        r = self._client.req.get(f"api/bos/sequences/{sequence_id}")
        # TODO Process response
        return r.json()

    def import_file(self, organism_id, analysis_id, region,
                    file_path: str, file_format: str = "fasta") -> str:
        """
        Import a file of sequences

        :param file_path:
        :param file_format:
        :return:
        """
        if organism_id is None:
            organism_id = "null"
        if analysis_id is None:
            analysis_id = "null"
        if region is None:
            region = "null"
        r = self._client.req.post(f"api/bos/sequences/?organism_id={organism_id}&"
                                  f"analysis_id={analysis_id}&region={region}",
                                  files=dict(file=open(file_path, "rb"),
                                             file_format=file_format))
        # TODO Process response
        return r.json()

    def export(self, sequence_ids: List[str], file_path, file_format: str = "fasta") -> str:
        """
        Export a list of sequences

        :param sequence_ids:
        :param file_format:
        :return:
        """
        filter = dict(feature_id=dict(op="in", unary=sequence_ids))
        order = []
        url = f"api/bos/sequences.{file_format}"  # ?filter={urllib.parse.quote(json.dumps(filter))}&order={urllib.parse.quote(json.dumps(order))}"
        print(f"{url=}")
        r = self._client.req.get(url, params=dict(filter=filter, order=order))
        with open(file_path, "wb") as f:
            f.write(r.content)


class DatasetsAPI:  # Mostly Geographic layers
    def __init__(self, client: Client):
        self._client = client

    def get_filter_template(self) -> Dict:
        """
        Return template for dataset filters (for "get" method)

        :return:
        """
        r = self._client.req.get("api/browser/layers/filters/schema")
        # TODO Process response
        return r.json()

    def get(self, filter=None) -> List[Dict]:
        """
        Return a list of datasets matching the filter

        :param filter:
        :return:
        """
        r = self._client.req.get("api/geo/layers/", params=filter)
        # TODO Process response
        return r.json()

    def get_detail(self, dataset_id: str) -> Dict:
        """
        Return a dataset detail

        :param dataset_id:
        :return:
        """
        r = self._client.req.get(f"api/geo/layers/{dataset_id}")
        # TODO Process response
        return r.json()

    def import_file(self, file_path: str, file_format: str = "gpkg") -> str:
        """
        Import a dataset, return the ID of the dataset if successful

        :param file_path:
        :param file_format:
        :return:
        """
        r = self._client.req.post("api/geo/layers/", files=dict(file=open(file_path, "rb"), file_format=file_format))
        # TODO Process response
        return r.json()

    def export(self, dataset_id: str, file_path, file_format: str = "gpkg") -> str:
        """
        Export a dataset

        :param dataset_id:
        :param file_path:
        :param file_format:
        :return:
        """
        r = self._client.req.get(f"api/geo/layers/{dataset_id}.{file_format}")
        with open(file_path, "wb") as f:
            f.write(r.content)


class ProcessesAPI:
    def __init__(self, client: Client):
        self._client = client

    def get_filter_template(self) -> Dict:
        """
        Return template for process filters (for "get" method)

        :return:
        """
        pass

    def get(self, filter={}) -> List[Dict]:
        """
        Return a list of processes matching the filter

        :param filter:
        :return:
        """
        r = self._client.req.get(f"api/processes/")
        r_dict = json.loads(r.text)
        process_names = []
        for process in r_dict["content"]:
            process_names.append[process["name"]]
        return process_names

    def get_detail(self, process_id: str) -> Dict:
        """
        Return a process detail, including which parameters need to be set to run the process, and a list of examples

        :param process_id:
        :return:
        """
        r = self._client.req.get(f"api/processes/")
        r_dict = json.loads(r.text)
        processes_details = []
        for process in r_dict["content"]:
            process_details = {
                'name': process["name"],
                'details': {

                }
            }
        pass

    def prepare(self, process_type: str, parameters: Dict) -> Dict:
        """
        Prepare a process instance (for submission, "JobsAPI")

        :param process_type:
        :param parameters:
        :return:
        """
        pass


class ComputeResourceAPI:
    def __init__(self, client: Client):
        self._client = client

    def get_filter_template(self) -> Dict:
        """
        Return template for compute resources filtering (for "get" method)

        :return:
        """
        pass

    def get(self, filter) -> List[Dict]:
        """
        Return a list of compute resources matching the filter

        :param filter:
        :return:
        """
        pass

    def get_detail(self, compute_resource_id: str) -> Dict:
        """
        Return a compute resource detail

        :param compute_resource_id:
        :return:
        """
        pass


class JobsAPI:
    def __init__(self, client: Client):
        self._client = client

    def get_filter_template(self) -> Dict:
        """
        Return template for Jobs filtering (for "get" method)

        :return:
        """
        pass

    def get(self, filter=dict(status="todo")) -> List[Dict]:
        """
        Return a list of jobs matching the filter

        :param filter: dict(status="done") or dict(status="todo")
        :return:
        """
        r = self._client.req.get("api/jobs/", params=filter)
        # TODO Process response
        return r.json()

    def get_detail(self, job_id: str) -> Dict:
        """
        Return a job detail (including the job's status, parameters, and outputs)

        :param job_id:
        :return:
        """
        r = self._client.req.get(f"api/jobs/{job_id}")
        # TODO Process response
        return r.json()

    def export_output(self, job_id: str, file_id: str, local_file_path: str) -> str:
        """
        Export the output of a job. First "get_detail" to know which are the outputs

        :param job_id:
        :param file_id:
        :param local_file_path:
        :return:
        GET /api/files/jobs/4/mafft.fasta.content
        """
        # Obtain the path of the file from the job detail
        remote_file_path = f"api/files/jobs/{job_id}/{file_id}.content"
        f = FilesAPI(self._client)
        f.download(remote_file_path, local_file_path)

    def submit(self, resource_id: str, process_id: str, process_params: Dict, credentials: Dict=None) -> str:
        """
        Submit a job

        :param resource_id: Compute resource ID
        :param process_id: Process ID
        :param process_params: Process parameters
        :param credentials: If the resource has default credentials this can be None, else specify (values depend on resource)
        :return: job_id
        """
        p = dict(resource_id=resource_id, process_id=process_id, params=process_params)
        if credentials:
            p["credentials"] = credentials
        r = self._client.req.post(f"api/jobs/", json=p)
        return r.json()

    def cancel(self, job_id: str) -> Dict:
        """
        Cancel a job

        :param job_id:
        :return:
        """
        r = self._client.req.put(f"api/jobs/", params=dict(status="cancelling"))
        return r.json()


    # TODO Access to jobs:
    #  - list processes, get parameters for process, list resources for process
    #  - launch process
    #  - enumerate processes
    #  - cancel process
    #  - get process status
    #  - get process details: inputs, outputs, log


if __name__ == "__main__":
    client = Client("http://localhost:5000")
    client.login("/home/rnebot/GoogleDrive/AA_NEXTGENDEM/geo_api_key.json")
    ds = DatasetsAPI(client)
    t = ds.get_filter_template()
    lst = ds.get()
    print(lst)
    detail = ds.get_detail(11)
    print(detail)
    s = ds.export(11, "/home/rnebot/Downloads/test.gpkg")
    client.logout()

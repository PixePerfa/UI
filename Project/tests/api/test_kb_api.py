import requests
import json
import sys
from pathlib import Path

root_path = Path(__file__).parent.parent.parent
sys.path.append(str(root_path))
from server.utils import api_address
from configs import VECTOR_SEARCH_TOP_K
from server.knowledge_base.utils import get_kb_path, get_file_path

from pprint import pprint


api_base_url = api_address()


kb = "kb_for_api_test"
test_files = {
    "wiki/Home.MD": get_file_path("samples", "wiki/Home.md"),
    "Wiki/Dev Environment Deployment. MD": get_file_path("samples", "wiki/dev environment deployment.md"),
    "test_files/test.txt": get_file_path("samples", "test_files/test.txt"),
}

print("\n\nDirect URL access\n")


def test_delete_kb_before(api="/knowledge_base/delete_knowledge_base"):
    if not Path(get_kb_path(kb)).exists():
        return

    url = api_base_url + api
    print("\nTest knowledge stock is in, needs to be deleted")
    r = requests.post(url, json=kb)
    data = r.json()
    pprint(data)

    # check kb not exists anymore
    url = api_base_url + "/knowledge_base/list_knowledge_bases"
    print("\nGet_Knowledge_Base_List:")
    r = requests.get(url)
    data = r.json()
    pprint(data)
    assert data["code"] == 200
    assert isinstance(data["data"], list) and len(data["data"]) > 0
    assert kb not in data["data"]


def test_create_kb(api="/knowledge_base/create_knowledge_base"):
    url = api_base_url + api

    print(f"\nTry to create a knowledge base with an empty name:")
    r = requests.post(url, json={"knowledge_base_name": " "})
    data = r.json()
    pprint(data)
    assert data["code"] == 404
    assert data["msg"] == "The name of the knowledge base cannot be empty, please fill in the name of the knowledge base again"

    print(f"\nCreate a new knowledge base: {kb}")
    r = requests.post(url, json={"knowledge_base_name": kb})
    data = r.json()
    pprint(data)
    assert data["code"] == 200
    assert data["msg"] == f"New knowledge base {kb}"

    print(f"\nTry to create a knowledge base with the same name: {kb}")
    r = requests.post(url, json={"knowledge_base_name": kb})
    data = r.json()
    pprint(data)
    assert data["code"] == 404
    assert data["msg"] == f"Knowledge base with the same name already exists {kb}"


def test_list_kbs(api="/knowledge_base/list_knowledge_bases"):
    url = api_base_url + api
    print("\nGet Knowledge Base List:")
    r = requests.get(url)
    data = r.json()
    pprint(data)
    assert data["code"] == 200
    assert isinstance(data["data"], list) and len(data["data"]) > 0
    assert kb in data["data"]


def test_upload_docs(api="/knowledge_base/upload_docs"):
    url = api_base_url + api
    files = [("files", (name, open(path, "rb"))) for name, path in test_files.items()]

    print(f"\nUploadknowledge,file")
    data = {"knowledge_base_name": kb, "override": True}
    r = requests.post(url, data=data, files=files)
    data = r.json()
    pprint(data)
    assert data["code"] == 200
    assert len(data["data"]["failed_files"]) == 0

    print(f"\nTry to re-upload the knowledge file, not overwritten")
    data = {"knowledge_base_name": kb, "override": False}
    files = [("files", (name, open(path, "rb"))) for name, path in test_files.items()]
    r = requests.post(url, data=data, files=files)
    data = r.json()
    pprint(data)
    assert data["code"] == 200
    assert len(data["data"]["failed_files"]) == len(test_files)

    print(f"\nTry to re-upload the knowledge file, overwrite, custom docs")
    docs = {"FAQ. MD": [{"page_content": "custom docs", "metadata": {}}]}
    data = {"knowledge_base_name": kb, "override": True, "docs": json.dumps(docs)}
    files = [("files", (name, open(path, "rb"))) for name, path in test_files.items()]
    r = requests.post(url, data=data, files=files)
    data = r.json()
    pprint(data)
    assert data["code"] == 200
    assert len(data["data"]["failed_files"]) == 0


def test_list_files(api="/knowledge_base/list_files"):
    url = api_base_url + api
    print("\nGet Knowledge Base Chinese Parts List:")
    r = requests.get(url, params={"knowledge_base_name": kb})
    data = r.json()
    pprint(data)
    assert data["code"] == 200
    assert isinstance(data["data"], list)
    for name in test_files:
        assert name in data["data"]


def test_search_docs(api="/knowledge_base/search_docs"):
    url = api_base_url + api
    query = "Tell us about the langchain-chatchat project"
    print("\nRetrieve the knowledge base:")
    print(query)
    r = requests.post(url, json={"knowledge_base_name": kb, "query": query})
    data = r.json()
    pprint(data)
    assert isinstance(data, list) and len(data) == VECTOR_SEARCH_TOP_K


def test_update_info(api="/knowledge_base/update_info"):
    url = api_base_url + api
    print("\nUpdate Knowledge Base Introduction")
    r = requests.post(url, json={"knowledge_base_name": "samples", "kb_info": "hello"})
    data = r.json()
    pprint(data)
    assert data["code"] == 200

def test_update_docs(api="/knowledge_base/update_docs"):
    url = api_base_url + api

    print(f"\nUploadknowledge,file")
    r = requests.post(url, json={"knowledge_base_name": kb, "file_names": list(test_files)})
    data = r.json()
    pprint(data)
    assert data["code"] == 200
    assert len(data["data"]["failed_files"]) == 0


def test_delete_docs(api="/knowledge_base/delete_docs"):
    url = api_base_url + api

    print(f"\nDeleteknowledge,file")
    r = requests.post(url, json={"knowledge_base_name": kb, "file_names": list(test_files)})
    data = r.json()
    pprint(data)
    assert data["code"] == 200
    assert len(data["data"]["failed_files"]) == 0

    url = api_base_url + "/knowledge_base/search_docs"
    query = "Tell us about the langchain-chatchat project"
    print("\nAttempt to retrieve the retrieval knowledge base after deletion:")
    print(query)
    r = requests.post(url, json={"knowledge_base_name": kb, "query": query})
    data = r.json()
    pprint(data)
    assert isinstance(data, list) and len(data) == 0


def test_recreate_vs(api="/knowledge_base/recreate_vector_store"):
    url = api_base_url + api
    print("\nRebuild Knowledge Base:")
    r = requests.post(url, json={"knowledge_base_name": kb}, stream=True)
    for chunk in r.iter_content(None):
        data = json.loads(chunk[6:])
        assert isinstance(data, dict)
        assert data["code"] == 200
        print(data["msg"])

    url = api_base_url + "/knowledge_base/search_docs"
    query = "What file formats are supported for this project?"
    print("\nAttempt to retrieve the reconstructed researched knowledge base:")
    print(query)
    r = requests.post(url, json={"knowledge_base_name": kb, "query": query})
    data = r.json()
    pprint(data)
    assert isinstance(data, list) and len(data) == VECTOR_SEARCH_TOP_K


def test_delete_kb_after(api="/knowledge_base/delete_knowledge_base"):
    url = api_base_url + api
    print("\nDelete Knowledge Base")
    r = requests.post(url, json=kb)
    data = r.json()
    pprint(data)

    # check kb not exists anymore
    url = api_base_url + "/knowledge_base/list_knowledge_bases"
    print("\nGet Knowledge Base List:")
    r = requests.get(url)
    data = r.json()
    pprint(data)
    assert data["code"] == 200
    assert isinstance(data["data"], list) and len(data["data"]) > 0
    assert kb not in data["data"]

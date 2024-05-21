import requests
import json
import sys
from pathlib import Path

root_path = Path(__file__).parent.parent.parent
sys.path.append(str(root_path))
from server.utils import api_address
from configs import VECTOR_SEARCH_TOP_K
from server.knowledge_base.utils import get_kb_path, get_file_path
from webui_pages.utils import ApiRequest

from pprint import pprint


api_base_url = api_address()
api: ApiRequest = ApiRequest(api_base_url)


kb = "kb_for_api_test"
test_files = {
    "FAQ. MD": str(root_path / "docs" / "FAQ. MD"),
    "README. MD": str(root_path / "README. MD"),
    "test.txt": get_file_path("samples", "test.txt"),
}

print("\n\nApiRquest call\n")


def test_delete_kb_before():
    if not Path(get_kb_path(kb)).exists():
        return

    data = api.delete_knowledge_base(kb)
    pprint(data)
    assert data["code"] == 200
    assert isinstance(data["data"], list) and len(data["data"]) > 0
    assert kb not in data["data"]


def test_create_kb():
    print(f"\nTry to create a knowledge base with an empty name:")
    data = api.create_knowledge_base(" ")
    pprint(data)
    assert data["code"] == 404
    assert data["msg"] == "The name of the knowledge base cannot be empty, please fill in the name of the knowledge base again"

    print(f"\nCreate a new knowledge base: {kb}")
    data = api.create_knowledge_base(kb)
    pprint(data)
    assert data["code"] == 200
    assert data["msg"] == f"New knowledge base {kb}"

    print(f"\nTry to create a knowledge base with the same name: {kb}")
    data = api.create_knowledge_base(kb)
    pprint(data)
    assert data["code"] == 404
    assert data["msg"] == f"Knowledge base with the same name already exists {kb}"


def test_list_kbs():
    data = api.list_knowledge_bases()
    pprint(data)
    assert isinstance(data, list) and len(data) > 0
    assert kb in data


def test_upload_docs():
    files = list(test_files.values())

    print(f"\nUploadknowledge,file")
    data = {"knowledge_base_name": kb, "override": True}
    data = api.upload_kb_docs(files, **data)
    pprint(data)
    assert data["code"] == 200
    assert len(data["data"]["failed_files"]) == 0

    print(f"\nTry to re-upload the knowledge file, not overwritten")
    data = {"knowledge_base_name": kb, "override": False}
    data = api.upload_kb_docs(files, **data)
    pprint(data)
    assert data["code"] == 200
    assert len(data["data"]["failed_files"]) == len(test_files)

    print(f"\nTry to re-upload the knowledge file, overwrite, custom docs")
    docs = {"FAQ. MD": [{"page_content": "custom docs", "metadata": {}}]}
    data = {"knowledge_base_name": kb, "override": True, "docs": docs}
    data = api.upload_kb_docs(files, **data)
    pprint(data)
    assert data["code"] == 200
    assert len(data["data"]["failed_files"]) == 0


def test_list_files():
    print("\nGet Knowledge Base Chinese Parts List:")
    data = api.list_kb_docs(knowledge_base_name=kb)
    pprint(data)
    assert isinstance(data, list)
    for name in test_files:
        assert name in data


def test_search_docs():
    query = "Tell us about the langchain-chatchat project"
    print("\nRetrieve the knowledge base:")
    print(query)
    data = api.search_kb_docs(query, kb)
    pprint(data)
    assert isinstance(data, list) and len(data) == VECTOR_SEARCH_TOP_K


def test_update_docs():
    print(f"\nUploadknowledge,file")
    data = api.update_kb_docs(knowledge_base_name=kb, file_names=list(test_files))
    pprint(data)
    assert data["code"] == 200
    assert len(data["data"]["failed_files"]) == 0


def test_delete_docs():
    print(f"\nDeleteknowledge,file")
    data = api.delete_kb_docs(knowledge_base_name=kb, file_names=list(test_files))
    pprint(data)
    assert data["code"] == 200
    assert len(data["data"]["failed_files"]) == 0

    query = "Tell us about the langchain-chatchat project"
    print("\nAttempt to retrieve the retrieval knowledge base after deletion:")
    print(query)
    data = api.search_kb_docs(query, kb)
    pprint(data)
    assert isinstance(data, list) and len(data) == 0


def test_recreate_vs():
    print("\nRebuild Knowledge Base:")
    r = api.recreate_vector_store(kb)
    for data in r:
        assert isinstance(data, dict)
        assert data["code"] == 200
        print(data["msg"])

    query = "What file formats are supported for this project?"
    print("\nAttempt to retrieve the reconstructed researched knowledge base:")
    print(query)
    data = api.search_kb_docs(query, kb)
    pprint(data)
    assert isinstance(data, list) and len(data) == VECTOR_SEARCH_TOP_K


def test_delete_kb_after():
    print("\nDelete Knowledge Base")
    data = api.delete_knowledge_base(kb)
    pprint(data)

    # check kb not exists anymore
    print("\nGet Knowledge Base List:")
    data = api.list_knowledge_bases()
    pprint(data)
    assert isinstance(data, list) and len(data) > 0
    assert kb not in data

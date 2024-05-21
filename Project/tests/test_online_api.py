import sys
from pathlib import Path
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

from configs import ONLINE_LLM_MODEL
from server.model_workers.base import *
from server.utils import get_model_worker_config, list_config_llm_models
from pprint import pprint
import pytest


workers = []
for x in list_config_llm_models()["online"]:
    if x in ONLINE_LLM_MODEL and x not in workers:
        workers.append(x)
print(f"all workers to test: {workers}")

# workers = ["fangzhou-api"]


@pytest.mark.parametrize("worker", workers)
def test_chat(worker):
    params = ApiChatParams(
        messages = [
            {"role": "user", "content": "Who are you"},
        ],
    )
    print(f"\nchat with {worker} \n")

    if worker_class := get_model_worker_config(worker).get("worker_class"):
        for x in worker_class().do_chat(params):
            pprint(x)
            assert isinstance(x, dict)
            assert x["error_code"] == 0


@pytest.mark.parametrize("worker", workers)
def test_embeddings(worker):
    params = ApiEmbeddingsParams(
        texts = [
            "LangChain-Chatchat (formerly Langchain-ChatGLM): A local knowledge base Q&A application implementation based on large language models such as Langchain and ChatGLM." ,
            "A local knowledge base-based Q&A application implemented by using the idea of Langchain, with the goal of establishing a knowledge base Q&A solution that is friendly to Chinese scenarios and open source models and can be run offline." ,
        ]
    )

    if worker_class := get_model_worker_config(worker).get("worker_class"):
        if worker_class.can_embedding():
            print(f"\embeddings with {worker} \n")
            resp = worker_class().do_embeddings(params)

            pprint(resp, depth=2)
            assert resp["code"] == 200
            assert "data" in resp
            embeddings = resp["data"]
            assert isinstance(embeddings, list) and len(embeddings) > 0
            assert isinstance(embeddings[0], list) and len(embeddings[0]) > 0
            assert isinstance(embeddings[0][0], float)
            print("vector length:", len(embeddings[0]))


# @pytest.mark.parametrize("worker", workers)
# def test_completion(worker):
# params = ApiCompletionParams(prompt="Fifty-six nationalities")
    
#     print(f"\completion with {worker} \n")

#     worker_class = get_model_worker_config(worker)["worker_class"]
#     resp = worker_class().do_completion(params)
#     pprint(resp)

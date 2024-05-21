# This file encapsulates the request to api.py and can be used by different webui
# Synchronous/asynchronous calls are supported through ApiRequest and AsyncApiRequest

from typing import *
from pathlib import Path
# The configuration imported here is the configuration on the machine that initiates the request (such as WEBUI), and is mainly used to set the default value for the frontend. When deployed, it can be different from on the server
from configs import (
    EMBEDDING_MODEL,
    DEFAULT_VS_TYPE,
    LLM_MODELS,
    TEMPERATURE,
    SCORE_THRESHOLD,
    CHUNK_SIZE,
    OVERLAP_SIZE,
    ZH_TITLE_ENHANCE,
    VECTOR_SEARCH_TOP_K,
    SEARCH_ENGINE_TOP_K,
    HTTPX_DEFAULT_TIMEOUT,
    logger, log_verbose,
)
import httpx
import contextlib
import json
import os
from io import BytesIO
from server.utils import set_httpx_config, api_address, get_httpx_client

from pprint import pprint
from langchain_core._api import deprecated

set_httpx_config()


class ApiRequest:
    '''
    api.py Encapsulation of calls (synchronous mode) simplifies the way API is called
    '''

    def __init__(
            self,
            base_url: str = api_address(),
            timeout: float = HTTPX_DEFAULT_TIMEOUT,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self._use_async = False
        self._client = None

    @property
    def client(self):
        if self._client is None or self._client.is_closed:
            self._client = get_httpx_client(base_url=self.base_url,
                                            use_async=self._use_async,
                                            timeout=self.timeout)
        return self._client

    def get(
            self,
            url: str,
            params: Union[Dict, List[Tuple], bytes] = None,
            retry: int = 3,
            stream: bool = False,
            **kwargs: Any,
    ) -> Union[httpx. Response, Iterator[httpx. Response], None]:
        while retry > 0:
            try:
                if stream:
                    return self.client.stream("GET", url, params=params, **kwargs)
                else:
                    return self.client.get(url, params=params, **kwargs)
            except Exception as e:
                msg = f"error when get {url}: {e}"
                logger.error(f'{e.__class__.__name__}: {msg}',
                             exc_info=e if log_verbose else None)
                retry -= 1

    def post(
            self,
            url: str,
            data: Dict = None,
            json: Dict = None,
            retry: int = 3,
            stream: bool = False,
            **kwargs: Any
    ) -> Union[httpx. Response, Iterator[httpx. Response], None]:
        while retry > 0:
            try:
                # print(kwargs)
                if stream:
                    return self.client.stream("POST", url, data=data, json=json, **kwargs)
                else:
                    return self.client.post(url, data=data, json=json, **kwargs)
            except Exception as e:
                msg = f"error when post {url}: {e}"
                logger.error(f'{e.__class__.__name__}: {msg}',
                             exc_info=e if log_verbose else None)
                retry -= 1

    def delete(
            self,
            url: str,
            data: Dict = None,
            json: Dict = None,
            retry: int = 3,
            stream: bool = False,
            **kwargs: Any
    ) -> Union[httpx. Response, Iterator[httpx. Response], None]:
        while retry > 0:
            try:
                if stream:
                    return self.client.stream("DELETE", url, data=data, json=json, **kwargs)
                else:
                    return self.client.delete(url, data=data, json=json, **kwargs)
            except Exception as e:
                msg = f"error when delete {url}: {e}"
                logger.error(f'{e.__class__.__name__}: {msg}',
                             exc_info=e if log_verbose else None)
                retry -= 1

    def _httpx_stream2generator(
            self,
            response: contextlib._GeneratorContextManager,
            as_json: bool = False,
    ):
        '''
        Convert the GeneratorContextManager returned by httpx.stream into a normal generator
        '''

        async def ret_async(response, as_json):
            try:
                async with response as r:
                    async for chunk in r.aiter_text(None):
                        if not chunk:  # fastchat api yield empty bytes on start and end
                            continue
                        if as_json:
                            try:
                                if chunk.startswith("data: "):
                                    data = json.loads(chunk[6:-2])
                                elif chunk.startswith(":"):  # skip sse comment line
                                    continue
                                else:
                                    data = json.loads(chunk)
                                yield data
                            except Exception as e:
                                msg=f" interface returns JSON error: '{chunk}'. The error message is: {e}. "
                                logger.error(f'{e.__class__.__name__}: {msg}',
                                             exc_info=e if log_verbose else None)
                        else:
                            # print(chunk, end="", flush=True)
                            yield chunk
            except httpx. ConnectError as e:
                msg = f" Unable to connect to the API server, please make sure 'api.py' is started normally. ({e})"
                logger.error(msg)
                yield {"code": 500, "msg": msg}
            except httpx. ReadTimeout as e:
                msg = f" API communication timed out, please confirm that FastChat and the API service are started (see Wiki '5. Start the API service or web UI'). （{e}）"
                logger.error(msg)
                yield {"code": 500, "msg": msg}
            except Exception as e:
                msg = f"API communication encountered error: {e}"
                logger.error(f'{e.__class__.__name__}: {msg}',
                             exc_info=e if log_verbose else None)
                yield {"code": 500, "msg": msg}

        def ret_sync(response, as_json):
            try:
                with response as r:
                    for chunk in r.iter_text(None):
                        if not chunk:  # fastchat api yield empty bytes on start and end
                            continue
                        if as_json:
                            try:
                                if chunk.startswith("data: "):
                                    data = json.loads(chunk[6:-2])
                                elif chunk.startswith(":"):  # skip sse comment line
                                    continue
                                else:
                                    data = json.loads(chunk)
                                yield data
                            except Exception as e:
                                msg=f" interface returns JSON error: '{chunk}'. The error message is: {e}. "
                                logger.error(f'{e.__class__.__name__}: {msg}',
                                             exc_info=e if log_verbose else None)
                        else:
                            # print(chunk, end="", flush=True)
                            yield chunk
            except httpx. ConnectError as e:
                msg = f"Unable to connect to the API server, please make sure 'api.py' is started normally. ({e})"
                logger.error(msg)
                yield {"code": 500, "msg": msg}
            except httpx. ReadTimeout as e:
                msg = f"API communication timed out, please confirm that FastChat and the API service are started (see Wiki '5. Start the API service or web UI'). （{e}）"
                logger.error(msg)
                yield {"code": 500, "msg": msg}
            except Exception as e:
                msg = f"API communication encountered error: {e}"
                logger.error(f'{e.__class__.__name__}: {msg}',
                             exc_info=e if log_verbose else None)
                yield {"code": 500, "msg": msg}

        if self._use_async:
            return ret_async(response, as_json)
        else:
            return ret_sync(response, as_json)

    def _get_response_value(
            self,
            response: httpx. Response,
            as_json: bool = False,
            value_func: Callable = None,
    ):
        '''
        Transform the response returned by a synchronous or asynchronous request
        'as_json': Returns JSON
        'value_func': The user can customize the return value, the function accepts either response or json
        '''

        def to_json(r):
            try:
                return r.json()
            except Exception as e:
                msg = "API failed to return correct JSON." + str(e)
                if log_verbose:
                    logger.error(f'{e.__class__.__name__}: {msg}',
                                 exc_info=e if log_verbose else None)
                return {"code": 500, "msg": msg, "data": None}

        if value_func is None:
            value_func = (lambda r: r)

        async def ret_async(response):
            if as_json:
                return value_func(to_json(await response))
            else:
                return value_func(await response)

        if self._use_async:
            return ret_async(response)
        else:
            if as_json:
                return value_func(to_json(response))
            else:
                return value_func(response)

    # Server Information
    def get_server_configs(self, **kwargs) -> Dict:
        response = self.post("/server/configs", **kwargs)
        return self._get_response_value(response, as_json=True)

    def list_search_engines(self, **kwargs) -> List:
        response = self.post("/server/list_search_engines", **kwargs)
        return self._get_response_value(response, as_json=True, value_func=lambda r: r["data"])

    def get_prompt_template(
            self,
            type: str = "llm_chat",
            name: str = "default",
            **kwargs,
    ) -> str:
        data = {
            "type": type,
            "name": name,
        }
        response = self.post("/server/get_prompt_template", json=data, **kwargs)
        return self._get_response_value(response, value_func=lambda r: r.text)

    # Conversation-related operations
    def chat_chat(
            self,
            query: str,
            conversation_id: str = None,
            history_len: int = -1,
            history: List[Dict] = [],
            stream: bool = True,
            model: str = LLM_MODELS[0],
            temperature: float = TEMPERATURE,
            max_tokens: int = None,
            prompt_name: str = "default",
            **kwargs,
    ):
        '''
        Compatible with api.py/chat/chat interfaces
        '''
        data = {
            "query": query,
            "conversation_id": conversation_id,
            "history_len": history_len,
            "history": history,
            "stream": stream,
            "model_name": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "prompt_name": prompt_name,
        }

        # print(f"received input message:")
        # pprint(data)

        response = self.post("/chat/chat", json=data, stream=True, **kwargs)
        return self._httpx_stream2generator(response, as_json=True)

    @deprecated(
        since="0.3.0",
        message="Custom Agent Q&A will be rewritten in Langchain-Chatchat 0.3.x, and related functions in 0.2.x will be deprecated",
        removal="0.3.0")
    def agent_chat(
            self,
            query: str,
            history: List[Dict] = [],
            stream: bool = True,
            model: str = LLM_MODELS[0],
            temperature: float = TEMPERATURE,
            max_tokens: int = None,
            prompt_name: str = "default",
    ):
        '''
        Compatible with api.py/chat/agent_chat interfaces
        '''
        data = {
            "query": query,
            "history": history,
            "stream": stream,
            "model_name": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "prompt_name": prompt_name,
        }

        # print(f"received input message:")
        # pprint(data)

        response = self.post("/chat/agent_chat", json=data, stream=True)
        return self._httpx_stream2generator(response, as_json=True)

    def knowledge_base_chat(
            self,
            query: str,
            knowledge_base_name: str,
            top_k: int = VECTOR_SEARCH_TOP_K,
            score_threshold: float = SCORE_THRESHOLD,
            history: List[Dict] = [],
            stream: bool = True,
            model: str = LLM_MODELS[0],
            temperature: float = TEMPERATURE,
            max_tokens: int = None,
            prompt_name: str = "default",
    ):
        '''
        Compatible with api.py/chat/knowledge_base_chat interfaces
        '''
        data = {
            "query": query,
            "knowledge_base_name": knowledge_base_name,
            "top_k": top_k,
            "score_threshold": score_threshold,
            "history": history,
            "stream": stream,
            "model_name": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "prompt_name": prompt_name,
        }

        # print(f"received input message:")
        # pprint(data)

        response = self.post(
            "/chat/knowledge_base_chat",
            json=data,
            stream=True,
        )
        return self._httpx_stream2generator(response, as_json=True)

    def upload_temp_docs(
            self,
            files: List[Union[str, Path, bytes]],
            knowledge_id: str = None,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=OVERLAP_SIZE,
            zh_title_enhance=ZH_TITLE_ENHANCE,
    ):
        '''
        Compatible with api.py/knowledge_base/upload_tmep_docs interfaces
        '''

        def convert_file(file, filename=None):
            if isinstance(file, bytes):  # raw bytes
                file = BytesIO(file)
            elif hasattr(file, "read"):  # a file io like object
                filename = filename or file.name
            else:  # a local path
                file = Path(file).absolute().open("rb")
                filename = filename or os.path.split(file.name)[-1]
            return filename, file

        files = [convert_file(file) for file in files]
        data = {
            "knowledge_id": knowledge_id,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "zh_title_enhance": zh_title_enhance,
        }

        response = self.post(
            "/knowledge_base/upload_temp_docs",
            data=data,
            files=[("files", (filename, file)) for filename, file in files],
        )
        return self._get_response_value(response, as_json=True)

    def file_chat(
            self,
            query: str,
            knowledge_id: str,
            top_k: int = VECTOR_SEARCH_TOP_K,
            score_threshold: float = SCORE_THRESHOLD,
            history: List[Dict] = [],
            stream: bool = True,
            model: str = LLM_MODELS[0],
            temperature: float = TEMPERATURE,
            max_tokens: int = None,
            prompt_name: str = "default",
    ):
        '''
        Compatible with api.py/chat/file_chat interfaces
        '''
        data = {
            "query": query,
            "knowledge_id": knowledge_id,
            "top_k": top_k,
            "score_threshold": score_threshold,
            "history": history,
            "stream": stream,
            "model_name": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "prompt_name": prompt_name,
        }

        response = self.post(
            "/chat/file_chat",
            json=data,
            stream=True,
        )
        return self._httpx_stream2generator(response, as_json=True)

    @deprecated(
        since="0.3.0",
        message="Search engine Q&A will be rewritten in Langchain-Chatchat 0.3.x, and related features will be deprecated in 0.2.x",
        removal="0.3.0"
    )
    def search_engine_chat(
            self,
            query: str,
            search_engine_name: str,
            top_k: int = SEARCH_ENGINE_TOP_K,
            history: List[Dict] = [],
            stream: bool = True,
            model: str = LLM_MODELS[0],
            temperature: float = TEMPERATURE,
            max_tokens: int = None,
            prompt_name: str = "default",
            split_result: bool = False,
    ):
        '''
        Corresponding to api.py/chat/search_engine_chat interface
        '''
        data = {
            "query": query,
            "search_engine_name": search_engine_name,
            "top_k": top_k,
            "history": history,
            "stream": stream,
            "model_name": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "prompt_name": prompt_name,
            "split_result": split_result,
        }

        # print(f"received input message:")
        # pprint(data)

        response = self.post(
            "/chat/search_engine_chat",
            json=data,
            stream=True,
        )
        return self._httpx_stream2generator(response, as_json=True)

    # Knowledge base related operations

    def list_knowledge_bases(
            self,
    ):
        '''
        Compatible with api.py/knowledge_base/list_knowledge_bases interfaces
        '''
        response = self.get("/knowledge_base/list_knowledge_bases")
        return self._get_response_value(response,
                                        as_json=True,
                                        value_func=lambda r: r.get("data", []))

    def create_knowledge_base(
            self,
            knowledge_base_name: str,
            vector_store_type: str = DEFAULT_VS_TYPE,
            embed_model: str = EMBEDDING_MODEL,
    ):
        '''
        Compatible with api.py/knowledge_base/create_knowledge_base interfaces
        '''
        data = {
            "knowledge_base_name": knowledge_base_name,
            "vector_store_type": vector_store_type,
            "embed_model": embed_model,
        }

        response = self.post(
            "/knowledge_base/create_knowledge_base",
            json=data,
        )
        return self._get_response_value(response, as_json=True)

    def delete_knowledge_base(
            self,
            knowledge_base_name: str,
    ):
        '''
        Compatible with api.py/knowledge_base/delete_knowledge_base interfaces
        '''
        response = self.post(
            "/knowledge_base/delete_knowledge_base",
            json=f"{knowledge_base_name}",
        )
        return self._get_response_value(response, as_json=True)

    def list_kb_docs(
            self,
            knowledge_base_name: str,
    ):
        '''
        Corresponding to api.py/knowledge_base/list_files interfaces
        '''
        response = self.get(
            "/knowledge_base/list_files",
            params={"knowledge_base_name": knowledge_base_name}
        )
        return self._get_response_value(response,
                                        as_json=True,
                                        value_func=lambda r: r.get("data", []))

    def search_kb_docs(
            self,
            knowledge_base_name: str,
            query: str = "",
            top_k: int = VECTOR_SEARCH_TOP_K,
            score_threshold: int = SCORE_THRESHOLD,
            file_name: str = "",
            metadata: dict = {},
    ) -> List:
        '''
        Compatible with api.py/knowledge_base/search_docs interfaces
        '''
        data = {
            "query": query,
            "knowledge_base_name": knowledge_base_name,
            "top_k": top_k,
            "score_threshold": score_threshold,
            "file_name": file_name,
            "metadata": metadata,
        }

        response = self.post(
            "/knowledge_base/search_docs",
            json=data,
        )
        return self._get_response_value(response, as_json=True)

    def update_docs_by_id(
            self,
            knowledge_base_name: str,
            docs: Dict[str, Dict],
    ) -> bool:
        '''
        Compatible with api.py/knowledge_base/update_docs_by_id interfaces
        '''
        data = {
            "knowledge_base_name": knowledge_base_name,
            "docs": docs,
        }
        response = self.post(
            "/knowledge_base/update_docs_by_id",
            json=data
        )
        return self._get_response_value(response)

    def upload_kb_docs(
            self,
            files: List[Union[str, Path, bytes]],
            knowledge_base_name: str,
            override: bool = False,
            to_vector_store: bool = True,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=OVERLAP_SIZE,
            zh_title_enhance=ZH_TITLE_ENHANCE,
            docs: Dict = {},
            not_refresh_vs_cache: bool = False,
    ):
        '''
        Corresponding to api.py/knowledge_base/upload_docs interface
        '''

        def convert_file(file, filename=None):
            if isinstance(file, bytes):  # raw bytes
                file = BytesIO(file)
            elif hasattr(file, "read"):  # a file io like object
                filename = filename or file.name
            else:  # a local path
                file = Path(file).absolute().open("rb")
                filename = filename or os.path.split(file.name)[-1]
            return filename, file

        files = [convert_file(file) for file in files]
        data = {
            "knowledge_base_name": knowledge_base_name,
            "override": override,
            "to_vector_store": to_vector_store,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "zh_title_enhance": zh_title_enhance,
            "docs": docs,
            "not_refresh_vs_cache": not_refresh_vs_cache,
        }

        if isinstance(data["docs"], dict):
            data["docs"] = json.dumps(data["docs"], ensure_ascii=False)
        response = self.post(
            "/knowledge_base/upload_docs",
            data=data,
            files=[("files", (filename, file)) for filename, file in files],
        )
        return self._get_response_value(response, as_json=True)

    def delete_kb_docs(
            self,
            knowledge_base_name: str,
            file_names: List[str],
            delete_content: bool = False,
            not_refresh_vs_cache: bool = False,
    ):
        '''
        Corresponding to api.py/knowledge_base/delete_docs interfaces
        '''
        data = {
            "knowledge_base_name": knowledge_base_name,
            "file_names": file_names,
            "delete_content": delete_content,
            "not_refresh_vs_cache": not_refresh_vs_cache,
        }

        response = self.post(
            "/knowledge_base/delete_docs",
            json=data,
        )
        return self._get_response_value(response, as_json=True)

    def update_kb_info(self, knowledge_base_name, kb_info):
        '''
        Corresponding to api.py/knowledge_base/update_info interface
        '''
        data = {
            "knowledge_base_name": knowledge_base_name,
            "kb_info": kb_info,
        }

        response = self.post(
            "/knowledge_base/update_info",
            json=data,
        )
        return self._get_response_value(response, as_json=True)

    def update_kb_docs(
            self,
            knowledge_base_name: str,
            file_names: List[str],
            override_custom_docs: bool = False,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=OVERLAP_SIZE,
            zh_title_enhance=ZH_TITLE_ENHANCE,
            docs: Dict = {},
            not_refresh_vs_cache: bool = False,
    ):
        '''
        Corresponding to api.py/knowledge_base/update_docs interfaces
        '''
        data = {
            "knowledge_base_name": knowledge_base_name,
            "file_names": file_names,
            "override_custom_docs": override_custom_docs,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "zh_title_enhance": zh_title_enhance,
            "docs": docs,
            "not_refresh_vs_cache": not_refresh_vs_cache,
        }

        if isinstance(data["docs"], dict):
            data["docs"] = json.dumps(data["docs"], ensure_ascii=False)

        response = self.post(
            "/knowledge_base/update_docs",
            json=data,
        )
        return self._get_response_value(response, as_json=True)

    def recreate_vector_store(
            self,
            knowledge_base_name: str,
            allow_empty_kb: bool = True,
            vs_type: str = DEFAULT_VS_TYPE,
            embed_model: str = EMBEDDING_MODEL,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=OVERLAP_SIZE,
            zh_title_enhance=ZH_TITLE_ENHANCE,
    ):
        '''
        Compatible with api.py/knowledge_base/recreate_vector_store interfaces
        '''
        data = {
            "knowledge_base_name": knowledge_base_name,
            "allow_empty_kb": allow_empty_kb,
            "vs_type": vs_type,
            "embed_model": embed_model,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "zh_title_enhance": zh_title_enhance,
        }

        response = self.post(
            "/knowledge_base/recreate_vector_store",
            json=data,
            stream=True,
            timeout=None,
        )
        return self._httpx_stream2generator(response, as_json=True)

    # LLM model-related operations
    def list_running_models(
            self,
            controller_address: str = None,
    ):
        '''
        Get a list of running models in Fastchat
        '''
        data = {
            "controller_address": controller_address,
        }

        if log_verbose:
            logger.info(f'{self.__class__.__name__}:data: {data}')

        response = self.post(
            "/llm_model/list_running_models",
            json=data,
        )
        return self._get_response_value(response, as_json=True, value_func=lambda r: r.get("data", []))

    def get_default_llm_model(self, local_first: bool = True) -> Tuple[str, bool]:
        '''
        Retrieves the currently running LLM model from the server.
        When local_first=True, the running local model is returned first, otherwise it is returned in the order of LLM_MODELS configuration.
        The return type is (model_name, is_local_model)
        '''

        def ret_sync():
            running_models = self.list_running_models()
            if not running_models:
                return "", False

            model = ""
            for m in LLM_MODELS:
                if m not in running_models:
                    continue
                is_local = not running_models[m].get("online_api")
                if local_first and not is_local:
                    continue
                else:
                    model = m
                    break

            if not model: # The models configured in the LLM_MODELS are not in the running_models
                model = list(running_models)[0]
            is_local = not running_models[model].get("online_api")
            return model, is_local

        async def ret_async():
            running_models = await self.list_running_models()
            if not running_models:
                return "", False

            model = ""
            for m in LLM_MODELS:
                if m not in running_models:
                    continue
                is_local = not running_models[m].get("online_api")
                if local_first and not is_local:
                    continue
                else:
                    model = m
                    break

            if not model: # The models configured in the LLM_MODELS are not in the running_models
                model = list(running_models)[0]
            is_local = not running_models[model].get("online_api")
            return model, is_local

        if self._use_async:
            return ret_async()
        else:
            return ret_sync()

    def list_config_models(
            self,
            types: List[str] = ["local", "online"],
    ) -> Dict[str, Dict]:
        '''
        Obtain the list of models configured in the server configs, and return the model in the form {"type": {model_name: config}, ...}.
        '''
        data = {
            "types": types,
        }
        response = self.post(
            "/llm_model/list_config_models",
            json=data,
        )
        return self._get_response_value(response, as_json=True, value_func=lambda r: r.get("data", {}))

    def get_model_config(
            self,
            model_name: str = None,
    ) -> Dict:
        '''
        Obtain the model configuration on the server
        '''
        data = {
            "model_name": model_name,
        }
        response = self.post(
            "/llm_model/get_model_config",
            json=data,
        )
        return self._get_response_value(response, as_json=True, value_func=lambda r: r.get("data", {}))

    def list_search_engines(self) -> List[str]:
        '''
        Get the search engine supported by the server
        '''
        response = self.post(
            "/server/list_search_engines",
        )
        return self._get_response_value(response, as_json=True, value_func=lambda r: r.get("data", {}))

    def stop_llm_model(
            self,
            model_name: str,
            controller_address: str = None,
    ):
        '''
        Stop an LLM model.
        Note: Due to the way Fastchat is implemented, the model_worker where the LLM model is located is actually stopped.
        '''
        data = {
            "model_name": model_name,
            "controller_address": controller_address,
        }

        response = self.post(
            "/llm_model/stop",
            json=data,
        )
        return self._get_response_value(response, as_json=True)

    def change_llm_model(
            self,
            model_name: str,
            new_model_name: str,
            controller_address: str = None,
    ):
        '''
        Request the fastchat controller to switch the LLM model.
        '''
        if not model_name or not new_model_name:
            return {
                "code": 500,
                "msg": f"Model name not specified"
            }

        def ret_sync():
            running_models = self.list_running_models()
            if new_model_name == model_name or new_model_name in running_models:
                return {
                    "code": 200,
                    "msg": "No need to switch"
                }

            if model_name not in running_models:
                return {
                    "code": 500,
                    'msg': f"specified model '{model_name}' is not running. Current running model: {running_models}"
                }

            config_models = self.list_config_models()
            if new_model_name not in config_models.get("local", {}):
                return {
                    "code": 500,
                    "msg": f"The model '{new_model_name}' to switch is not configured in configs. "
                }

            data = {
                "model_name": model_name,
                "new_model_name": new_model_name,
                "controller_address": controller_address,
            }

            response = self.post(
                "/llm_model/change",
                json=data,
            )
            return self._get_response_value(response, as_json=True)

        async def ret_async():
            running_models = await self.list_running_models()
            if new_model_name == model_name or new_model_name in running_models:
                return {
                    "code": 200,
                    "msg": "No need to switch"
                }

            if model_name not in running_models:
                return {
                    "code": 500,
                    'msg': f" specified model '{model_name}' is not running. Current running model: {running_models}"
                }

            config_models = await self.list_config_models()
            if new_model_name not in config_models.get("local", {}):
                return {
                    "code": 500,
                    "msg": f"The model '{new_model_name}' to switch is not configured in configs. "
                }

            data = {
                "model_name": model_name,
                "new_model_name": new_model_name,
                "controller_address": controller_address,
            }

            response = self.post(
                "/llm_model/change",
                json=data,
            )
            return self._get_response_value(response, as_json=True)

        if self._use_async:
            return ret_async()
        else:
            return ret_sync()

    def embed_texts(
            self,
            texts: List[str],
            embed_model: str = EMBEDDING_MODEL,
            to_query: bool = False,
    ) -> List[List[float]]:
        '''
        Vectorize text, with options including native embed_models and online models that support embeddings
        '''
        data = {
            "texts": texts,
            "embed_model": embed_model,
            "to_query": to_query,
        }
        resp = self.post(
            "/other/embed_texts",
            json=data,
        )
        return self._get_response_value(resp, as_json=True, value_func=lambda r: r.get("data"))

    def chat_feedback(
            self,
            message_id: str,
            score: int,
            reason: str = "",
    ) -> int:
        '''
        Feedback conversation evaluations
        '''
        data = {
            "message_id": message_id,
            "score": score,
            "reason": reason,
        }
        resp = self.post("/chat/feedback", json=data)
        return self._get_response_value(resp)


class AsyncApiRequest(ApiRequest):
    def __init__(self, base_url: str = api_address(), timeout: float = HTTPX_DEFAULT_TIMEOUT):
        super().__init__(base_url, timeout)
        self._use_async = True


def check_error_msg(data: Union[str, dict, list], key: str = "errorMsg") -> str:
    '''
    return error message if error occured when requests API
    '''
    if isinstance(data, dict):
        if key in data:
            return data[key]
        if "code" in data and data["code"] != 200:
            return data["msg"]
    return ""


def check_success_msg(data: Union[str, dict, list], key: str = "msg") -> str:
    '''
    return error message if error occured when requests API
    '''
    if (isinstance(data, dict)
            and key in data
            and "code" in data
            and data["code"] == 200):
        return data[key]
    return ""


if __name__ == "__main__":
    api = ApiRequest()
    aapi = AsyncApiRequest()

    # with api.chat_chat("Hello") as r:
    #     for t in r.iter_text(None):
    #         print(t)

    # r = api.chat_chat("Hello", no_remote_api=True)
    # for t in r:
    #     print(t)

    # r = api.duckduckgo_search_chat("Latest Advances in Room Temperature Superconductivity", no_remote_api=True)
    # for t in r:
    #     print(t)

    # print(api.list_knowledge_bases())

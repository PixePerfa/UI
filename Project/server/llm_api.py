from fastapi import Body
from configs import logger, log_verbose, LLM_MODELS, HTTPX_DEFAULT_TIMEOUT
from server.utils import (BaseResponse, fschat_controller_address, list_config_llm_models,
                          get_httpx_client, get_model_worker_config)
from typing import List


def list_running_models(
    controller_address: str = Body(None, description="Fastchat controller server address", examples=[fschat_controller_address()]),
    placeholder: str = Body(None, description="This parameter is not used, placeholder is used"),
) -> BaseResponse:
    '''
    Obtain the list of loaded models and their configuration items from the fastchat controller
    '''
    try:
        controller_address = controller_address or fschat_controller_address()
        with get_httpx_client() as client:
            r = client.post(controller_address + "/list_models")
            models = r.json()["models"]
            data = {m: get_model_config(m).data for m in models}
            return BaseResponse(data=data)
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e}',
                        exc_info=e if log_verbose else None)
        return BaseResponse(
            code=500,
            data={},
            msg=f"failed to get available models from controller: {controller_address}。 The error message is: {e}")


def list_config_models(
    types: list[str] = Body(["local", "online"], description="Model CI categories, such as local, online, worker"),
    placeholder: str = Body(None, description="Placeholder, no real effect")
) -> BaseResponse:
    '''
    Obtain the list of models configured in configs from the local computer
    '''
    data = {}
    for type, models in list_config_llm_models().items():
        if type in types:
            data[type] = {m: get_model_config(m).data for m in models}
    return BaseResponse(data=data)


def get_model_config(
    model_name: str = Body(description="Name of the LLM model in the configuration"),
    placeholder: str = Body(None, description="Placeholder, no real effect")
) -> BaseResponse:
    '''
    Obtaining LLM Model Configuration Items (Merged)
    '''
    config = {}
    # Delete sensitive information from ONLINE_MODEL configurations
    for k, v in get_model_worker_config(model_name=model_name).items():
        if not (k == "worker_class"
            or "key" in k.lower()
            or "secret" in k.lower()
            or k.lower().endswith("id")):
            config[k] = v

    return BaseResponse(data=config)


def stop_llm_model(
    model_name: str = Body(..., description="Name of the LLM model to stop", examples=[LLM_MODELS[0]]),
    controller_address: str = Body(None, description="Fastchat controller server address", examples=[fschat_controller_address()])
) -> BaseResponse:
    '''
    Request the fastchat controller to stop an LLM model.
    Note: Due to the way Fastchat is implemented, the model_worker where the LLM model is located is actually stopped.
    '''
    try:
        controller_address = controller_address or fschat_controller_address()
        with get_httpx_client() as client:
            r = client.post(
                controller_address + "/release_worker",
                json={"model_name": model_name},
            )
            return r.json()
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e}',
                        exc_info=e if log_verbose else None)
        return BaseResponse(
            code=500,
            msg=f"failed to stop LLM model {model_name} from controller: {controller_address}。 The error message is: {e}")


def change_llm_model(
    model_name: str = Body(..., description="Currently running model", examples=[LLM_MODELS[0]]),
    new_model_name: str = Body(..., description="New model to switch", examples=[LLM_MODELS[0]]),
    controller_address: str = Body(None, description="Fastchat controller server address", examples=[fschat_controller_address()])
):
    '''
    Request the fastchat controller to switch the LLM model.
    '''
    try:
        controller_address = controller_address or fschat_controller_address()
        with get_httpx_client() as client:
            r = client.post(
                controller_address + "/release_worker",
                json={"model_name": model_name, "new_model_name": new_model_name},
                timeout=HTTPX_DEFAULT_TIMEOUT, # wait for new worker_model
            )
            return r.json()
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e}',
                        exc_info=e if log_verbose else None)
        return BaseResponse(
            code=500,
            msg=f"failed to switch LLM model from controller: {controller_address}。 The error message is: {e}")


def list_search_engines() -> BaseResponse:
    from server.chat.search_engine_chat import SEARCH_ENGINES

    return BaseResponse(data=list(SEARCH_ENGINES))

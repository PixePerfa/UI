"""Usage
To load the local model:
python webui_allinone.py

To call a remote API service:
python webui_allinone.py --use-remote-api

WebUI service running in the background:
python webui_allinone.py --nohup

Load multiple non-default models:
python webui_allinone.py --model-path-address model1@host1@port1 model2@host2@port2 

Multi-card startup:
python webui_alline.py --model-path-address model@host@port --num-gpus 2 --gpus 0,1 --max-gpu-memory 10GiB

"""
import streamlit as st
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages import *
import os
from server.llm_api_stale import string_args,launch_all,controller_args,worker_args,server_args,LOG_PATH

from server.api_allinone_stale import parser, api_args
import subprocess

parser.add_argument("--use-remote-api",action="store_true")
parser.add_argument("--nohup",action="store_true")
parser.add_argument("--server.port",type=int,default=8501)
parser.add_argument("--theme.base",type=str,default='"light"')
parser.add_argument("--theme.primaryColor",type=str,default='"#165dff"')
parser.add_argument("--theme.secondaryBackgroundColor",type=str,default='"#f5f5f5"')
parser.add_argument("--theme.textColor",type=str,default='"#000000"')
web_args = ["server.port","theme.base","theme.primaryColor","theme.secondaryBackgroundColor","theme.textColor"]


def launch_api(args,args_list=api_args,log_name=None):
    print("Launching api ...")
    print("Start API Service...")
    if not log_name:
        log_name = f"{LOG_PATH}api_{args.api_host}_{args.api_port}"
    print(f"logs on api are written in {log_name}")
    print(f"API logs are located under {log_name}please check the logs if the startup is abnormal")
    args_str = string_args(args,args_list)
    api_sh = "python  server/{script} {args_str} >{log_name}.log 2>&1 &".format(
        script="api.py",args_str=args_str,log_name=log_name)
    subprocess.run(api_sh, shell=True, check=True)
    print("launch api done!")
    print("Start API service completed.")

def launch_webui(args,args_list=web_args,log_name=None):
    print("Launching webui...")
    print("Start the webui service...")
    if not log_name:
        log_name = f"{LOG_PATH}webui"

    args_str = string_args(args,args_list)
    if args.nohup:
        print(f"logs on api are written in {log_name}")
        print(f"WebUI service logs are located under {log_name}, please check the logs if the startup is abnormal")
        webui_sh = "streamlit run webui.py {args_str} >{log_name}.log 2>&1 &".format(
        args_str=args_str,log_name=log_name)
    else:
        webui_sh = "streamlit run webui.py {args_str}".format(
        args_str=args_str)
    subprocess.run(webui_sh, shell=True, check=True)
    print("launch webui done!")
    print("Start the WebUI service completed.")


if __name__ == "__main__":
    print("Starting webui_allineone.py, it would take a while, please be patient....")
    print(f"Start starting webui_allinone it takes about 3-10 minutes to start the LLM service, please wait patiently, if it does not start for a long time, please go to {LOG_PATH} to view the logs...")
    args = parser.parse_args()

    print("*"*80)
    if not args.use_remote_api:
        launch_all(args=args,controller_args=controller_args,worker_args=worker_args,server_args=server_args)
    launch_api(args=args,args_list=api_args)
    launch_webui(args=args,args_list=web_args)
    print("Start webui_allinone.py done!")
    print("Thanks for your patience, startup webui_allinone complete.")

import streamlit as st
from webui_pages.utils import *
from streamlit_chatbox import *
from streamlit_modal import Modal
from datetime import datetime
import os
import re
import time
from configs import (TEMPERATURE, HISTORY_LEN, PROMPT_TEMPLATES, LLM_MODELS,
                     DEFAULT_KNOWLEDGE_BASE, DEFAULT_SEARCH_ENGINE, SUPPORT_AGENT_MODEL)
from server.knowledge_base.utils import LOADER_DICT
import uuid
from typing import List, Dict

chat_box = ChatBox(
    assistant_avatar=os.path.join(
        "img",
        "chatchat_icon_blue_square_v2.png"
    )
)


def get_messages_history(history_len: int, content_in_expander: bool = False) -> List[Dict]:
    '''
    Returns message history.
    content_in_expander control whether to return the content of the expander element, you can select it when exporting, and the history passed into the LLM is not required
    '''

    def filter(msg):
        content = [x for x in msg["elements"] if x._output_method in ["markdown", "text"]]
        if not content_in_expander:
            content = [x for x in content if not x._in_expander]
        content = [x.content for x in content]

        return {
            "role": msg["role"],
            "content": "\n\n".join(content),
        }

    return chat_box.filter_history(history_len=history_len, filter=filter)


@st.cache_data
def upload_temp_docs(files, _api: ApiRequest) -> str:
    '''
    Upload the file to a temporary directory for file conversations
    Returns the ID of the temporary vector library
    '''
    return _api.upload_temp_docs(files).get("data", {}).get("id")


def parse_command(text: str, modal: Modal) -> bool:
    '''
    Check if the user has entered a custom command, currently supported:
    /new {session_name}。 If no name is provided, it defaults to "Session X"
    /del {session_name}。 If no name is provided, the current session is deleted if the number of sessions is > 1.
    /clear {session_name}。 If no name is provided, the current session is cleared by default
    /help。 Check out Command Help
    Return Value: If you enter a command, it returns True, otherwise it returns False
    '''
    if m := re.match(r"/([^\s]+)\s*(.*)", text):
        cmd, name = m.groups()
        name = name.strip()
        conv_names = chat_box.get_chat_names()
        if cmd == "help":
            modal.open()
        elif cmd == "new":
            if not name:
                i = 1
                while True:
                    name = f "Session {i}"
                    if name not in conv_names:
                        break
                    i += 1
            if name in st.session_state["conversation_ids"]:
                st.error(f"This session name "{name}" already exists")
                time.sleep(1)
            else:
                st.session_state["conversation_ids"][name] = uuid.uuid4().hex
                st.session_state["cur_conv_name"] = name
        elif cmd == "del":
            name = name or st.session_state.get("cur_conv_name")
            if len(conv_names) == 1:
                st.error("This is the last session, cannot be deleted")
                time.sleep(1)
            elif not name or name not in st.session_state["conversation_ids"]:
                st.error(f"Invalid session name: "{name}"")
                time.sleep(1)
            else:
                st.session_state["conversation_ids"].pop(name, None)
                chat_box.del_chat_name(name)
                st.session_state["cur_conv_name"] = ""
        elif cmd == "clear":
            chat_box.reset_history(name=name or None)
        return True
    return False


def dialogue_page(api: ApiRequest, is_lite: bool = False):
    st.session_state.setdefault("conversation_ids", {})
    st.session_state["conversation_ids"].setdefault(chat_box.cur_chat_name, uuid.uuid4().hex)
    st.session_state.setdefault("file_chat_id", None)
    default_model = api.get_default_llm_model()[0]

    if not chat_box.chat_inited:
        st.toast(
            f"Welcome to ['Langchain-Chatchat'](https://github.com/chatchat-space/Langchain-Chatchat)! \n\n"
            f"The currently running model '{default_model}', you can start asking questions."
        )
        chat_box.init_session()

    # Custom command help information is displayed
    modal = Modal("custom command", key="cmd_help", max_width="500")
    if modal.is_open():
        with modal.container():
            cmds = [x for x in parse_command.__doc__.split("\n") if x.strip().startswith("/")]
            st.write("\n\n".join(cmds))

    with st.sidebar:
        # Multi-session
        conv_names = list(st.session_state["conversation_ids"].keys())
        index = 0
        if st.session_state.get("cur_conv_name") in conv_names:
            index = conv_names.index(st.session_state.get("cur_conv_name"))
        conversation_name = st.selectbox("Current session:", conv_names, index=index)
        chat_box.use_chat_name(conversation_name)
        conversation_id = st.session_state["conversation_ids"][conversation_name]

        def on_mode_change():
            mode = st.session_state.dialogue_mode
            text = f" has been switched to {mode} mode. "
            if mode == "Knowledge Base Q&A":
                cur_kb = st.session_state.get("selected_kb")
                if cur_kb:
                    text = f"{text} current knowledge base: '{cur_kb}'. "
            st.toast(text)

        dialogue_modes = ["LLM dialog",
                          "Knowledge Base Q&A",
                          "File Dialogue",
                          "Search Engine Q&A",
                          "Custom Agent Q&A",
                          ]
        dialogue_mode = st.selectbox("Please select conversation mode:",
                                     dialogue_modes,
                                     index=0,
                                     on_change=on_mode_change,
                                     key="dialogue_mode",
                                     )

        def on_llm_change():
            if llm_model:
                config = api.get_model_config(llm_model)
                if not config.get("online_api"): # Only local model_worker can switch models
                    st.session_state["prev_llm_model"] = llm_model
                st.session_state["cur_llm_model"] = st.session_state.llm_model

        def llm_model_format_func(x):
            if x in running_models:
                return f"{x} (Running)"
            return x

        running_models = list(api.list_running_models())
        available_models = []
        config_models = api.list_config_models()
        if not is_lite:
            for k, v in config_models.get("local", {}).items():
                if (v.get("model_path_exists")
                        and k not in running_models):
                    available_models.append(k)
        for k, v in config_models.get("online", {}).items():
            if not v.get("provider") and k not in running_models and k in LLM_MODELS:
                available_models.append(k)
        llm_models = running_models + available_models
        cur_llm_model = st.session_state.get("cur_llm_model", default_model)
        if cur_llm_model in llm_models:
            index = llm_models.index(cur_llm_model)
        else:
            index = 0
        llm_model = st.selectbox("Select LLM model:",
                                 llm_models,
                                 index,
                                 format_func=llm_model_format_func,
                                 on_change=on_llm_change,
                                 key="llm_model",
                                 )
        if (st.session_state.get("prev_llm_model") != llm_model
                and not is_lite
                and not llm_model in config_models.get("online", {})
                and not llm_model in config_models.get("langchain", {})
                and llm_model not in running_models):
            with st.spinner(f"Loading model: {llm_model}, do not manipulate or refresh the page"):
                prev_model = st.session_state.get("prev_llm_model")
                r = api.change_llm_model(prev_model, llm_model)
                if msg := check_error_msg(r):
                    st.error(msg)
                elif msg := check_success_msg(r):
                    st.success(msg)
                    st.session_state["prev_llm_model"] = llm_model

        index_prompt = {
            "LLM Conversation": "llm_chat",
            "Custom Agent Q&A": "agent_chat",
            "Search Engine Q&A": "search_engine_chat",
            Knowledge Base Q&A: knowledge_base_chat,
            File Conversations: knowledge_base_chat,
        }
        prompt_templates_kb_list = list(PROMPT_TEMPLATES[index_prompt[dialogue_mode]].keys())
        prompt_template_name = prompt_templates_kb_list[0]
        if "prompt_template_select" not in st.session_state:
            st.session_state.prompt_template_select = prompt_templates_kb_list[0]

        def prompt_change():
            text = f" has been switched to a {prompt_template_name} template. "
            st.toast(text)

        prompt_template_select = st.selectbox(
            "Please select a Prompt template:",
            prompt_templates_kb_list,
            index=0,
            on_change=prompt_change,
            key="prompt_template_select",
        )
        prompt_template_name = st.session_state.prompt_template_select
        temperature = st.slider("Temperature：", 0.0, 2.0, TEMPERATURE, 0.05)
        history_len = st.number_input("Number of rounds of historical dialogue:", 0, 20, HISTORY_LEN)

        def on_kb_change():
            st.toast(f"Loaded KB: {st.session_state.selected_kb}")

        if dialogue_mode == "Knowledge Base Q&A":
            with st.expander("Knowledge Base Configuration", True):
                kb_list = api.list_knowledge_bases()
                index = 0
                if DEFAULT_KNOWLEDGE_BASE in kb_list:
                    index = kb_list.index(DEFAULT_KNOWLEDGE_BASE)
                selected_kb = st.selectbox(
                    Please select a knowledge base: ,
                    kb_list,
                    index=index,
                    on_change=on_kb_change,
                    key="selected_kb",
                )
                kb_top_k = st.number_input("Number of matching knowledge:", 1, 20, VECTOR_SEARCH_TOP_K)

                ## The BGE model will exceed 1
                score_threshold = st.slider("Knowledge Matching Score Threshold:", 0.0, 2.0, float(SCORE_THRESHOLD), 0.01)
        elif dialogue_mode == "File Conversation":
            with st.expander("File dialog configuration", True):
                files = st.file_uploader("Upload knowledge file:",
                                         [i for ls in LOADER_DICT.values() for i in ls],
                                         accept_multiple_files=True,
                                         )
                kb_top_k = st.number_input("Number of matching knowledge:", 1, 20, VECTOR_SEARCH_TOP_K)

                ## The BGE model will exceed 1
                score_threshold = st.slider("Knowledge Matching Score Threshold:", 0.0, 2.0, float(SCORE_THRESHOLD), 0.01)
                if st.button("Start upload", disabled=len(files) == 0):
                    st.session_state["file_chat_id"] = upload_temp_docs(files, api)
        elif dialogue_mode == "Search Engine Q&A":
            search_engine_list = api.list_search_engines()
            if DEFAULT_SEARCH_ENGINE in search_engine_list:
                index = search_engine_list.index(DEFAULT_SEARCH_ENGINE)
            else:
                index = search_engine_list.index("duckduckgo") if "duckduckgo" in search_engine_list else 0
            with st.expander("Search Engine Configuration", True):
                search_engine = st.selectbox(
                    label="Please select a search engine",
                    options=search_engine_list,
                    index=index,
                )
                se_top_k = st.number_input("Number of matching search results:", 1, 20, SEARCH_ENGINE_TOP_K)

    # Display chat messages from history on app rerun
    chat_box.output_messages()

    chat_input_placeholder = "Please enter the dialogue, use Shift+Enter for line breaks." Enter /help to view the custom command "

    def on_feedback(
            feedback,
            message_id: str = "",
            history_index: int = -1,
    ):
        reason = feedback["text"]
        score_int = chat_box.set_feedback(feedback=feedback, history_index=history_index)
        api.chat_feedback(message_id=message_id,
                          score=score_int,
                          reason=reason)
        st.session_state["need_rerun"] = True

    feedback_kwargs = {
        "feedback_type": "thumbs",
        "optional_text_label": "Feedback on the reasons for your rating",
    }

    if prompt := st.chat_input(chat_input_placeholder, key="prompt"):
        if parse_command(text=prompt, modal=modal): # The user enters a custom command
            st.rerun()
        else:
            history = get_messages_history(history_len)
            chat_box.user_say(prompt)
            if dialogue_mode == "LLM Conversation":
                chat_box.ai_say("Thinking...")
                text = ""
                message_id = ""
                r = api.chat_chat(prompt,
                                  history=history,
                                  conversation_id=conversation_id,
                                  model=llm_model,
                                  prompt_name=prompt_template_name,
                                  temperature=temperature)
                for t in r:
                    if error_msg := check_error_msg(t):  # check whether error occured
                        st.error(error_msg)
                        break
                    text += t.get("text", "")
                    chat_box.update_msg(text)
                    message_id = t.get("message_id", "")

                metadata = {
                    "message_id": message_id,
                }
                chat_box.update_msg(text, streaming=False, metadata=metadata) # Update the final string and remove the cursor
                chat_box.show_feedback(**feedback_kwargs,
                                       key=message_id,
                                       on_submit=on_feedback,
                                       kwargs={"message_id": message_id, "history_index": len(chat_box.history) - 1})

            elif dialogue_mode == "Custom Agent Q&A":
                if not any(agent in llm_model for agent in SUPPORT_AGENT_MODEL):
                    chat_box.ai_say([
                        f"Thinking... \n\n <span style='color:red'> This model is not Agent aligned, please change the model that supports Agent for a better experience! </span>\n\n\n",
                        Markdown("...", in_expander=True, title="Thought Process", state="complete"),

                    ])
                else:
                    chat_box.ai_say([
                        f "Thinking ...",
                        Markdown("...", in_expander=True, title="Thought Process", state="complete"),

                    ])
                text = ""
                ans = ""
                for d in api.agent_chat(prompt,
                                        history=history,
                                        model=llm_model,
                                        prompt_name=prompt_template_name,
                                        temperature=temperature,
                                        ):
                    try:
                        d = json.loads(d)
                    except:
                        pass
                    if error_msg := check_error_msg(d):  # check whether error occured
                        st.error(error_msg)
                    if chunk := d.get("answer"):
                        text += chunk
                        chat_box.update_msg(text, element_index=1)
                    if chunk := d.get("final_answer"):
                        ans += chunk
                        chat_box.update_msg(ans, element_index=0)
                    if chunk := d.get("tools"):
                        text += "\n\n".join(d.get("tools", []))
                        chat_box.update_msg(text, element_index=1)
                chat_box.update_msg(ans, element_index=0, streaming=False)
                chat_box.update_msg(text, element_index=1, streaming=False)
            elif dialogue_mode == "Knowledge Base Q&A":
                chat_box.ai_say([
                    f"Querying knowledge base '{selected_kb}' ...",
                    Markdown("...", in_expander=True, title="Knowledge Base Matching Result", state="complete"),
                ])
                text = ""
                for d in api.knowledge_base_chat(prompt,
                                                 knowledge_base_name=selected_kb,
                                                 top_k=kb_top_k,
                                                 score_threshold=score_threshold,
                                                 history=history,
                                                 model=llm_model,
                                                 prompt_name=prompt_template_name,
                                                 temperature=temperature):
                    if error_msg := check_error_msg(d):  # check whether error occured
                        st.error(error_msg)
                    elif chunk := d.get("answer"):
                        text += chunk
                        chat_box.update_msg(text, element_index=0)
                chat_box.update_msg(text, element_index=0, streaming=False)
                chat_box.update_msg("\n\n".join(d.get("docs", [])), element_index=1, streaming=False)
            elif dialogue_mode == "File Conversation":
                if st.session_state["file_chat_id"] is None:
                    st.error("Please upload the file before having a conversation")
                    st.stop()
                chat_box.ai_say([
                    f"Querying file '{st.session_state['file_chat_id']}' ...",
                    Markdown("...", in_expander=True, title="File Matching Result", state="complete"),
                ])
                text = ""
                for d in api.file_chat(prompt,
                                       knowledge_id=st.session_state["file_chat_id"],
                                       top_k=kb_top_k,
                                       score_threshold=score_threshold,
                                       history=history,
                                       model=llm_model,
                                       prompt_name=prompt_template_name,
                                       temperature=temperature):
                    if error_msg := check_error_msg(d):  # check whether error occured
                        st.error(error_msg)
                    elif chunk := d.get("answer"):
                        text += chunk
                        chat_box.update_msg(text, element_index=0)
                chat_box.update_msg(text, element_index=0, streaming=False)
                chat_box.update_msg("\n\n".join(d.get("docs", [])), element_index=1, streaming=False)
            elif dialogue_mode == "Search Engine Q&A":
                chat_box.ai_say([
                    f"Performing '{search_engine}' search...",
                    Markdown("...", in_expander=True, title="Web Search Results", state="complete"),
                ])
                text = ""
                for d in api.search_engine_chat(prompt,
                                                search_engine_name=search_engine,
                                                top_k=se_top_k,
                                                history=history,
                                                model=llm_model,
                                                prompt_name=prompt_template_name,
                                                temperature=temperature,
                                                split_result=se_top_k > 1):
                    if error_msg := check_error_msg(d):  # check whether error occured
                        st.error(error_msg)
                    elif chunk := d.get("answer"):
                        text += chunk
                        chat_box.update_msg(text, element_index=0)
                chat_box.update_msg(text, element_index=0, streaming=False)
                chat_box.update_msg("\n\n".join(d.get("docs", [])), element_index=1, streaming=False)

    if st.session_state.get("need_rerun"):
        st.session_state["need_rerun"] = False
        st.rerun()

    now = datetime.now()
    with st.sidebar:

        cols = st.columns(2)
        export_btn = cols[0]
        if cols[1].button(
                "Clear Conversation",
                use_container_width=True,
        ):
            chat_box.reset_history()
            st.rerun()

    export_btn.download_button(
        Export Records,
        "".join(chat_box.export2md()),
        file_name=f"{now:%Y-%m-%d %H.%M}_Conversation log.md",
        mime="text/markdown",
        use_container_width=True,
    )

import streamlit as st
from webui_pages.utils import *
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
from server.knowledge_base.utils import get_file_path, LOADER_DICT
from server.knowledge_base.kb_service.base import get_kb_details, get_kb_file_details
from typing import Literal, Dict, Tuple
from configs import (kbs_config,
                     EMBEDDING_MODEL, DEFAULT_VS_TYPE,
                     CHUNK_SIZE, OVERLAP_SIZE, ZH_TITLE_ENHANCE)
from server.utils import list_embed_models, list_online_embed_models
import os
import time

cell_renderer = JsCode("""function(params) {if(params.value==true){return '✓'}else{return 'x'}}""")


def config_aggrid(
        df: pd. DataFrame,
        columns: Dict[Tuple[str, str], Dict] = {},
        selection_mode: Literal["single", "multiple", "disabled"] = "single",
        use_checkbox: bool = False,
) -> GridOptionsBuilder:
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_column("No", width=40)
    for (col, header), kw in columns.items():
        gb.configure_column(col, header, wrapHeaderText=True, **kw)
    gb.configure_selection(
        selection_mode=selection_mode,
        use_checkbox=use_checkbox,
        pre_selected_rows=st.session_state.get("selected_rows", [0]),
    )
    gb.configure_pagination(
        enabled=True,
        paginationAutoPageSize=False,
        paginationPageSize=10
    )
    return gb


def file_exists(kb: str, selected_rows: List) -> Tuple[str, str]:
    """
    check whether a doc file exists in local knowledge base folder.
    return the file's name and path if it exists.
    """
    if selected_rows:
        file_name = selected_rows[0]["file_name"]
        file_path = get_file_path(kb, file_name)
        if os.path.isfile(file_path):
            return file_name, file_path
    return "", ""


def knowledge_base_page(api: ApiRequest, is_lite: bool = None):
    try:
        kb_list = {x["kb_name"]: x for x in get_kb_details()}
    except Exception as e:
        st.error(
            "Getting knowledge base information error, please check whether the initialization or migration has been completed according to the '4 Knowledge Base Initialization and Migration' step in 'README.md', or whether it is a database connection error." )
        st.stop()
    kb_names = list(kb_list.keys())

    if "selected_kb_name" in st.session_state and st.session_state["selected_kb_name"] in kb_names:
        selected_kb_index = kb_names.index(st.session_state["selected_kb_name"])
    else:
        selected_kb_index = 0

    if "selected_kb_info" not in st.session_state:
        st.session_state["selected_kb_info"] = ""

    def format_selected_kb(kb_name: str) -> str:
        if kb := kb_list.get(kb_name):
            return f"{kb_name} ({kb['vs_type']} @ {kb['embed_model']})"
        else:
            return kb_name

    selected_kb = st.selectbox(
        "Please select or create a new knowledge base: ",
        kb_names + ["NewKnowledgeBase"],
        format_func=format_selected_kb,
        index=selected_kb_index
    )

    if selected_kb == "New Knowledge Base":
        with st.form("New Knowledge Base"):

            kb_name = st.text_input(
                "NewKnowledgeBaseName",
                placeholder="New knowledge base name, Chinese naming is not supported",
                key="kb_name",
            )
            kb_info = st.text_input(
                "Introduction to the Knowledge Base",
                placeholder="Introduction to the knowledge base, easy for the agent to find",
                key="kb_info",
            )

            cols = st.columns(2)

            vs_types = list(kbs_config.keys())
            vs_type = cols[0].selectbox(
                "Vector Library Type",
                vs_types,
                index=vs_types.index(DEFAULT_VS_TYPE),
                key="vs_type",
            )

            if is_lite:
                embed_models = list_online_embed_models()
                if EMBEDDING_MODEL not in embed_models:
                    embed_models.append(EMBEDDING_MODEL)
            else:
                embed_models = list_embed_models() + list_online_embed_models()

            embed_model = cols[1].selectbox(
                "Embedding Model",
                embed_models,
                index=embed_models.index(EMBEDDING_MODEL),
                key="embed_model",
            )

            submit_create_kb = st.form_submit_button(
                "New",
                # disabled=not bool(kb_name),
                use_container_width=True,
            )

        if submit_create_kb:
            if not kb_name or not kb_name.strip():
                st.error(f"The knowledge base name cannot be empty!) ")
            elif kb_name in kb_list:
                st.error(f"The knowledge base named {kb_name} already exists! ")
            else:
                ret = api.create_knowledge_base(
                    knowledge_base_name=kb_name,
                    vector_store_type=vs_type,
                    embed_model=embed_model,
                )
                st.toast(ret.get("msg", " "))
                st.session_state["selected_kb_name"] = kb_name
                st.session_state["selected_kb_info"] = kb_info
                st.rerun()

    elif selected_kb:
        kb = selected_kb
        st.session_state["selected_kb_info"] = kb_list[kb]['kb_info']
        # Upload the file
        files = st.file_uploader("Upload knowledge file:",
                                 [i for ls in LOADER_DICT.values() for i in ls],
                                 accept_multiple_files=True,
                                 )
        kb_info = st.text_area("Please enter a knowledge base introduction:", value=st.session_state["selected_kb_info"], max_chars=None,
                               key=None,
                               help=None, on_change=None, args=None, kwargs=None)

        if kb_info != st.session_state["selected_kb_info"]:
            st.session_state["selected_kb_info"] = kb_info
            api.update_kb_info(kb, kb_info)

        # with st.sidebar:
        with st.expander(
                "File Handling Configuration",
                expanded=True,
        ):
            cols = st.columns(3)
            chunk_size = cols[0].number_input("Maximum length of a single paragraph of text:", 1, 1000, CHUNK_SIZE)
            chunk_overlap = cols[1].number_input("Adjacent text coincident length:", 0, chunk_size, OVERLAP_SIZE)
            cols[2].write("")
            cols[2].write("")
            zh_title_enhance = cols[2].checkbox("Turn on Chinese header strengthening", ZH_TITLE_ENHANCE)

        if st.button(
                "Add files to the knowledge base",
                # use_container_width=True,
                disabled=len(files) == 0,
        ):
            ret = api.upload_kb_docs(files,
                                     knowledge_base_name=kb,
                                     override=True,
                                     chunk_size=chunk_size,
                                     chunk_overlap=chunk_overlap,
                                     zh_title_enhance=zh_title_enhance)
            if msg := check_success_msg(ret):
                st.toast(msg, icon="✔")
            elif msg := check_error_msg(ret):
                st.toast(msg, icon="✖")

        st.divider()


        # st.info ("Please select the file and click the button to operate.") 
        doc_details = pd. DataFrame(get_kb_file_details(kb))
        selected_rows = []
        if not len(doc_details):
            st.info (f"No files in knowledge base '{kb}'")
        else:
            st.write(f"There is already a file in the knowledge base '{kb}':")
            st.info ("The knowledge base contains source files and vector libraries, please select the files from the following table and do the action")
            doc_details.drop(columns=["kb_name"], inplace=True)
            doc_details = doc_details[[
                "No", "file_name", "document_loader", "text_splitter", "docs_count", "in_folder", "in_db",
            ]]
            doc_details["in_folder"] = doc_details["in_folder"].replace(True, "✓").replace(False, "x")
            doc_details["in_db"] = doc_details["in_db"].replace(True, "✓").replace(False, "x")
            gb = config_aggrid(
                doc_details,
                {
                    ("No", "Serial Number"): {},
                    ("file_name", "DocumentName"): {},
                    # ("file_ext", "Document Type"): {},
                    # ("file_version", "Document Version"): {},
                    ("document_loader", "Document Loader"): {},
                    ("docs_count", "Number of Documents"): {},
                    ("text_splitter", "tokenizer"): {},
                    # ("create_time", "Created"): {},
                    ("in_folder", "source file"): {"cellRenderer": cell_renderer},
                    ("in_db", "Vector Library"): {"cellRenderer": cell_renderer},
                },
                "multiple",
            )

            doc_grid = AgGrid(
                doc_details,
                gb.build(),
                columns_auto_size_mode="FIT_CONTENTS",
                theme="alpine",
                custom_css={
                    "#gridToolBar": {"display": "none"},
                },
                allow_unsafe_jscode=True,
                enable_enterprise_modules=False
            )

            selected_rows = doc_grid.get("selected_rows", [])

            cols = st.columns(4)
            file_name, file_path = file_exists(kb, selected_rows)
            if file_path:
                with open(file_path, "rb") as fp:
                    cols[0].download_button(
                        "Download selected Chinese file",
                        fp,
                        file_name=file_name,
                        use_container_width=True, )
            else:
                cols[0].download_button(
                    "Download selected Chinese file",
                    "",
                    disabled=True,
                    use_container_width=True, )

            st.write()
            # Tokenize the file and load it into the vector library
            if cols[1].button(
                    "Re-add to vector library" if selected_rows and (
                            pd. DataFrame(selected_rows)["in_db"]).any() else "Add to Vector Library",
                    disabled=not file_exists(kb, selected_rows)[0],
                    use_container_width=True,
            ):
                file_names = [row["file_name"] for row in selected_rows]
                api.update_kb_docs(kb,
                                   file_names=file_names,
                                   chunk_size=chunk_size,
                                   chunk_overlap=chunk_overlap,
                                   zh_title_enhance=zh_title_enhance)
                st.rerun()

            # Delete the file from the vector library, but not the file itself.
            if cols[2].button(
                    "Remove from Vector Library",
                    disabled=not (selected_rows and selected_rows[0]["in_db"]),
                    use_container_width=True,
            ):
                file_names = [row["file_name"] for row in selected_rows]
                api.delete_kb_docs(kb, file_names=file_names)
                st.rerun()

            if cols[3].button(
                    "Remove from Knowledge Base",
                    type="primary",
                    use_container_width=True,
            ):
                file_names = [row["file_name"] for row in selected_rows]
                api.delete_kb_docs(kb, file_names=file_names, delete_content=True)
                st.rerun()

        st.divider()

        cols = st.columns(3)

        if cols[0].button(
                "Reconstructing the vector library from the source file",
                help="You don't need to upload a file, copy the document to the content directory of the corresponding knowledge base by other means, and click this button to rebuild the knowledge base. ",
                use_container_width=True,
                type="primary",
        ):
            with st.spinner("Vector library refactoring, please be patient, do not refresh or close the page."):
                empty = st.empty()
                empty.progress(0.0, "")
                for d in api.recreate_vector_store(kb,
                                                   chunk_size=chunk_size,
                                                   chunk_overlap=chunk_overlap,
                                                   zh_title_enhance=zh_title_enhance):
                    if msg := check_error_msg(d):
                        st.toast(msg)
                    else:
                        empty.progress(d["finished"] / d["total"], d["msg"])
                st.rerun()

        if cols[2].button(
                "Delete Knowledge Base",
                use_container_width=True,
        ):
            ret = api.delete_knowledge_base(kb)
            st.toast(ret.get("msg", " "))
            time.sleep(1)
            st.rerun()

        with st.sidebar:
            keyword = st.text_input("query keyword")
            top_k = st.slider("Number of matches", 1, 100, 3)

        st.write("A list of documents within a file. Double-click to modify, and fill in Y in the delete column to delete the corresponding row. ")
        docs = []
        df = pd. DataFrame([], columns=["seq", "id", "content", "source"])
        if selected_rows:
            file_name = selected_rows[0]["file_name"]
            docs = api.search_kb_docs(knowledge_base_name=selected_kb, file_name=file_name)
            data = [
                {"seq": i + 1, "id": x["id"], "page_content": x["page_content"], "source": x["metadata"].get("source"),
                 "type": x["type"],
                 "metadata": json.dumps(x["metadata"], ensure_ascii=False),
                 "to_del": "",
                 } for i, x in enumerate(docs)]
            df = pd. DataFrame(data)

            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_columns(["id", "source", "type", "metadata"], hide=True)
            gb.configure_column("seq", "No.", width=50)
            gb.configure_column("page_content", "content", editable=True, autoHeight=True, wrapText=True, flex=1,
                                cellEditor="agLargeTextCellEditor", cellEditorPopup=True)
            gb.configure_column("to_del", "Delete", editable=True, width=50, wrapHeaderText=True,
                                cellEditor="agCheckboxCellEditor", cellRender="agCheckboxCellRenderer")
            gb.configure_selection()
            edit_docs = AgGrid(df, gb.build())

            if st.button("Save Changes"):
                origin_docs = {
                    x["id"]: {"page_content": x["page_content"], "type": x["type"], "metadata": x["metadata"]} for x in
                    docs}
                changed_docs = []
                for index, row in edit_docs.data.iterrows():
                    origin_doc = origin_docs[row["id"]]
                    if row["page_content"] != origin_doc["page_content"]:
                        if row["to_del"] not in ["Y", "y", 1]:
                            changed_docs.append({
                                "page_content": row["page_content"],
                                "type": row["type"],
                                "metadata": json.loads(row["metadata"]),
                            })

                if changed_docs:
                    if api.update_kb_docs(knowledge_base_name=selected_kb,
                                          file_names=[file_name],
                                          docs={file_name: changed_docs}):
                        st.toast("Update document successful")
                    else:
                        st.toast("Failed to update document")

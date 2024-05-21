from langchain.text_splitter import CharacterTextSplitter
import re
from typing import List


class AliTextSplitter(CharacterTextSplitter):
    def __init__(self, pdf: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.pdf = pdf

    def split_text(self, text: str) -> List[str]:
        # use_document_segmentation parameter specifies whether to use semantic segmentation to segment the document, and the document semantic segmentation model adopted here is the open source nlp_bert_document-segmentation_Chinese-base of the Damo Academy, see https://arxiv.org/abs/2107.09278 for the paper
        # If you use a model for document semantic segmentation, you need to install ModelScope[nlp]:p ip install "Modelscope[nlp]" -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html
        # Considering that three models are used, it may not be very friendly to low-configuration GPUs, so here the model is loaded into the CPU calculation, and the device can be replaced with your own graphics card ID if necessary
        if self.pdf:
            text = re.sub(r"\n{3,}", r"\n", text)
            text = re.sub('\s', " ", text)
            text = re.sub("\n\n", "", text)
        try:
            from modelscope.pipelines import pipeline
        except ImportError:
            raise ImportError(
                "Could not import modelscope python package. "
                "Please install modelscope with `pip install modelscope`. "
            )


        p = pipeline(
            task="document-segmentation",
            model='damo/nlp_bert_document-segmentation_Chinese-base',
            device="cpu")
        result = p(documents=text)
        sent_list = [i for i in result["text"].split("\n\t") if i]
        return sent_list

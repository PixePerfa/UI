import re
from typing import List, Optional, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)


def _split_text_with_regex_from_end(
        text: str, separator: str, keep_separator: bool
) -> List[str]:
    # Now that we have the separator, split the text
    if separator:
        if keep_separator:
            # The parentheses in the pattern keep the delimiters in the result.
            _splits = re.split(f"({separator})", text)
            splits = ["".join(i) for i in zip(_splits[0::2], _splits[1::2])]
            if len(_splits) % 2 == 1:
                splits += _splits[-1:]
            # splits = [_splits[0]] + splits
        else:
            splits = re.split(separator, text)
    else:
        splits = list(text)
    return [s for s in splits if s != ""]


class ChineseRecursiveTextSplitter(RecursiveCharacterTextSplitter):
    def __init__(
            self,
            separators: Optional[List[str]] = None,
            keep_separator: bool = True,
            is_separator_regex: bool = True,
            **kwargs: Any,
    ) -> None:
        """Create a new TextSplitter."""
        super().__init__(keep_separator=keep_separator, **kwargs)
        self._separators = separators or [
            "\n\n",
            "\n",
            "。|！|？",
            "\.\s|\!\s|\?\s",
            "；|; \s",
            "，|,\s"
        ]
        self._is_separator_regex = is_separator_regex

    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        """Split incoming text and return chunks."""
        final_chunks = []
        # Get appropriate separator to use
        separator = separators[-1]
        new_separators = []
        for i, _s in enumerate(separators):
            _separator = _s if self._is_separator_regex else re.escape(_s)
            if _s == "":
                separator = _s
                break
            if re.search(_separator, text):
                separator = _s
                new_separators = separators[i + 1:]
                break

        _separator = separator if self._is_separator_regex else re.escape(separator)
        splits = _split_text_with_regex_from_end(text, _separator, self._keep_separator)

        # Now go merging things, recursively splitting longer texts.
        _good_splits = []
        _separator = "" if self._keep_separator else separator
        for s in splits:
            if self._length_function(s) < self._chunk_size:
                _good_splits.append(s)
            else:
                if _good_splits:
                    merged_text = self._merge_splits(_good_splits, _separator)
                    final_chunks.extend(merged_text)
                    _good_splits = []
                if not new_separators:
                    final_chunks.append(s)
                else:
                    other_info = self._split_text(s, new_separators)
                    final_chunks.extend(other_info)
        if _good_splits:
            merged_text = self._merge_splits(_good_splits, _separator)
            final_chunks.extend(merged_text)
        return [re.sub(r"\n{2,}", "\n", chunk.strip()) for chunk in final_chunks if chunk.strip()!=""]


if __name__ == "__main__":
    text_splitter = ChineseRecursiveTextSplitter(
        keep_separator=True,
        is_separator_regex=True,
        chunk_size=50,
        chunk_overlap=0
    )
    ls = [ 
        "Report on Chinas Foreign Trade Situation (75 pages). In the first 10 months, the import and export of general trade was 19.5 trillion yuan, an increase of 25.1 percent, 2.9 percentage points higher than the overall import and export growth rate, accounting for 61.7 percent of the total import and export value, an increase of 1.6 percentage points over the same period last year. Among them, general trade exports were 10.6 trillion yuan, an increase of 25.3%, accounting for 60.9percent of total exports, an increase of 1.5 percentage points; imports were 8.9 trillion yuan, an increase of 24.9 percent, accounting for 62.7 percent of total imports, an increase of 1.8 percentage points. The import and export of processing trade was 6.8 trillion yuan, an increase of 11.8 percent, accounting for 21.5 percent of the total import and export, a decrease of 2.0 percentage points. Among them, exports increased by 10.4 percent, accounting for 24.3 percent of total exports, a decrease of 2.6 percentage points; Imports increased by 14.2 percent, accounting for 18.0 percent of total imports, down by 1.2 percentage points. In addition, imports and exports in the form of bonded logistics amounted to 3.96 trillion yuan, an increase of 27.9%. Among them, exports were 1.47 trillion yuan, an increase of 38.9%; imports were 2.49 trillion yuan, an increase of 22.2%. In the first three quarters, Chinas trade in services continued to maintain a rapid growth trend. the total import and export value of services was 3,783.43 billion yuan, up by 11.6 percent; Among them, the export of services was 1,782.09 billion yuan, an increase of 27.3 percent; Imports reached 2,001.34 billion yuan, an increase of 0.5 percent, and the growth rate of imports turned positive for the first time since the epidemic. Exports of services grew by 26.8 percentage points faster than imports, driving the deficit in trade in services down by 62.9% to RMB219.25 billion. The structure of trade in services continued to be optimized, with the import and export of knowledge-intensive services reaching 1,691.77 billion yuan, an increase of 13.3 percent, accounting for 44.7 percent of the total import and export of services, an increase of 0.7 percentage points. 2. Analysis and outlook of Chinas foreign trade development environment The global epidemic has been up and down, the economic recovery has intensified and diverged, and risks such as rising commodity prices, energy shortages, tight transportation capacity, and spillover from policy adjustments in advanced economies are intertwined and superimposed. At the same time, it should also be noted that the long-term trend of Chinas economy has not changed, the resilience and vitality of foreign trade enterprises have been continuously enhanced, the development of new forms and new models has been accelerated, and the pace of innovation and transformation has accelerated. The industrial chain and supply chain are facing challenges. The United States and Europe have accelerated the introduction of manufacturing relocation plans, accelerated the local layout of the industrial chain and supply chain, multinational companies have adjusted the supply chain of the industrial chain, and the global dual chain is facing a new round of restructuring, and the trend of regionalization, near-shoring, localization and short chain is prominent. The supply of vaccines is insufficient, the manufacturing industry is short of cores, logistics is limited, and freight rates are high, and the global industrial and supply chain is under pressure. Global inflation continues to run at high levels. Rising energy prices have increased inflationary pressures in major economies and increased uncertainty about the global economic recovery. The World Banks Commodity Markets Outlook, released in October, noted that energy prices surged by more than 80 percent in 2021 and will continue to rise modestly in 2022. The IMF pointed out that the upside risks to global inflation have intensified, and there is great uncertainty about the inflation outlook",
        ]
    for inum, text in enumerate(ls):
        print(inum)
        chunks = text_splitter.split_text(text)
        for chunk in chunks:
            print(chunk)

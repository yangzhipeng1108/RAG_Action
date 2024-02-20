from langchain.document_loaders import TextLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter
from typing import  List, Optional, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
from typing import List

path = 'E:/python/yovole/NLP/pre-train/ai_project/yovole/'

#文本加载
loader = TextLoader(path + "source/ai/ai/html/file_storage.md",encoding='UTF-8')
# loader = UnstructuredMarkdownLoader("source/ai/ai/html/activate.md",encoding='UTF-8')
result = loader.load()


#md分割
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)
md_header_splits = markdown_splitter.split_text(result[0].page_content)

result_dict = {}
for i in md_header_splits:
    key = ' '.join(i.metadata.values())
    a=r'\{.*?\}'
    value = re.sub(a, '', i.page_content)
    a=r'\}\}'
    value = re.sub(a, '', value)
    a = r'<[^>]+>'
    result_dict[key] = re.sub(a, '', value)



#更细粒度分割  RecursiveCharacterTextSplitter
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
            "；|;\s",
            "，|,\s",
            "- ",
            # "**",
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

crts = ChineseRecursiveTextSplitter(chunk_size=10 ,chunk_overlap=1)

for key in result_dict.keys():
    value = result_dict[key]
    text_inter_list = crts.split_text(value)
    text_inter = ''.join(list(filter(lambda x: False if x == '-'  else True,text_inter_list)))
    result_dict[key] = text_inter



Subdocument_result_dict = {}
for key in result_dict.keys():

    Subdocument_result_dict[key] = result_dict[key]

    ##处理表格
    if '||' in result_dict[key]:
        text_inter_list = result_dict[key].split('||')

        # sentence_inter_list = [' '.join(i.split('|'))  if '---' not  in i else False  for i in text_inter_list]

        sentence_inter_list = []
        centent_list = [i.strip() for i in text_inter_list[0].split('|')]

        for i in text_inter_list[1:]:
            if '--' in i :
                continue
            text_list = i.split('|')
            sentence_inter_list.append('    '.join([' '.join([i,j.strip()]) for i,j in zip(centent_list[1:],text_list)]))

        Subdocument_result_dict[key] = sentence_inter_list

print(Subdocument_result_dict)

from urlextract import URLExtract
import unicodedata
import re

extractor = URLExtract()


class TextFilter:

    def __init__(self, skip_word=None, skip_line="", skip_prefix="",
                 remove_punctuation=True, remove_number=True, remove_link=True):
        if skip_word is None:
            skip_word = []
        self.text = None
        self.keyword_skip_word = skip_word
        self.keyword_skip_line = skip_line
        self.keyword_skip_prefix = skip_prefix
        self._remove_punctuation = remove_punctuation
        self._remove_number = remove_number
        self._remove_link = remove_link

    @classmethod
    def remove_link(cls, text) -> str:
        urls = extractor.find_urls(text)
        if len(urls) > 0:
            for link in urls:
                text = text.replace(link, "[链接]")
        return text

    @classmethod
    def remove_numbers(cls, text) -> str:
        nums = re.findall(r'-?\d+\.?\d*', text)
        nums = sorted(nums, key=len, reverse=True)
        if len(nums) > 0:
            for num in nums:
                text = text.replace(num, "[数字]")
        return text

    @classmethod
    def skip_word(cls, text, words) -> str:
        for word in words:
            if type(word) is list:
                assert len(word) > 1, "Too few keywords in list."
                assert len(word) == 2, "Too many keywords in one skip."
                if word[0] in text and word[1] in text:
                    text = text.split(word[0])[0] + text.split(word[0])[1].split(word[1])[1]
            elif type(word) is str:
                assert len(word) > 0, "Cannot skip empty string."
                if word in text:
                    segments = text.split(word)
                    text = ''
                    for segment in segments:
                        text += segment
            else:
                raise Exception('Unsupported skip words.')
        return text

    def fit_transform(self, text):
        cur = unicodedata.normalize('NFKC', text)
        if not self.keyword_skip_line != "" and self.keyword_skip_line in cur:
            return ""
        if self._remove_link:
            cur = self.remove_link(cur)
        if self._remove_number:
            cur = self.remove_numbers(cur)
        if len(self.keyword_skip_word) > 0:
            cur = self.skip_word(cur, self.keyword_skip_word)
        cur = re.sub(r'\[.*?\]', " ", cur)
        if self.keyword_skip_prefix != "" and self.keyword_skip_prefix in cur:
            cur = cur.split(self.keyword_skip_prefix)[1]
        if self._remove_punctuation:
            cur = re.sub(r'''[][【】“”‘’"'、,.。:;@#?!&$/()%~`-―〈〉「」・@+_*=《》^…￥-]+\ *''',
                         " ", cur, flags=re.VERBOSE)
        return cur

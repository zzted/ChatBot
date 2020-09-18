from xpinyin import Pinyin
import re

p = Pinyin()


class Conversation:

    def __init__(self, include_question: list, exclude_question: list,
                 include_answer: list, exclude_answer: list,
                 include_skip_section: list, exclude_skip_section: list,
                 text_filter=None):

        self.text_filter = text_filter
        self.include_question = include_question
        self.exclude_question = exclude_question
        self.include_answer = include_answer
        self.exclude_answer = exclude_answer
        self.include_skip_section = include_skip_section
        self.exclude_skip_section = exclude_skip_section
        self.text_length = None
        self.data = []

    @classmethod
    def skip_section(cls, text, line):
        line += 1
        while "-------" not in text[line]:
            line += 1
        line += 1
        return line

    @classmethod
    def is_wanted(cls, text, includes, excludes):
        for include in includes:
            if include not in text:
                return False
        for exclude in excludes:
            if exclude in text:
                return False
        return True

    def transform(self, text):
        self.text_length = len(text)
        line = 0
        while line < self.text_length:
            Q = ""
            A = ""
            if self.is_wanted(text[line], self.include_question, self.exclude_question):
                while line < self.text_length:
                    Q += self.text_filter.fit_transform(text[line])
                    line += 1
                    if line < self.text_length and self.is_wanted(text[line], self.include_skip_section, self.exclude_skip_section):
                        line = self.skip_section(text, line)
                        continue
                    if line < self.text_length and self.is_wanted(text[line], self.include_answer, self.exclude_answer):
                        break
            if self.is_wanted(text[line], self.include_answer, self.exclude_answer):
                while line < self.text_length:
                    A += self.text_filter.fit_transform(text[line])
                    line += 1
                    if line < self.text_length and self.is_wanted(text[line], self.include_skip_section, self.exclude_skip_section):
                        line = self.skip_section(text, line)
                        continue
                    if line < self.text_length and self.is_wanted(text[line], self.include_question, self.exclude_question):
                        Q = re.sub(r"\s+", " ", Q)
                        Q_p = p.get_pinyin(Q, '')
                        Q_p = re.sub(r"\s+", "", Q_p)
                        A = re.sub(r"\s+", " ", A)
                        A_p = p.get_pinyin(A, '')
                        A_p = re.sub(r"\s+", "", A_p)
                        self.data.append([Q, A, Q_p, A_p])
                        break
            else:
                line += 1

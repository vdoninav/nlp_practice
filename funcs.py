import regex as re


def strip_me(input_string):
    newline_pos = input_string.find('\n')

    if newline_pos == -1:
        return ""

    sub_string = input_string[newline_pos + 1:]
    match = re.search(r'[:;.]', sub_string)

    if not match:
        if len(sub_string) > 20:
            cyr_match = re.search(r'[А-Яа-яЁё]', sub_string)
            if cyr_match:
                sub_string = sub_string[cyr_match.start():]
        else:
            return sub_string

    if match:
        start_pos = match.end()
        sub_string = sub_string[start_pos:].strip()

    cyr_match = re.search(r'\p{IsCyrillic}', sub_string)

    if not cyr_match:
        return "что?"

    sub_string = sub_string[cyr_match.start():]

    punc_match = re.search(r'[.!?]', sub_string)

    if not punc_match:
        b = re.search(r'[А-Яа-яЁё]', sub_string)
        if not b:
            return "что?"
        return re.sub(r'\s+', ' ', sub_string).strip()

    sub_string = sub_string[:punc_match.end()].strip()
    sub_string = re.sub(r'\s+', ' ', sub_string)

    b = re.search(r'[А-Яа-яЁё]', sub_string)
    if not b:
        return "что?"

    return sub_string

def split_text(text: str, length: int) -> list:
    text_list = []
    new_text = ''

    for idx, _ in enumerate(text):
        new_text += _
        if idx != 0 and (idx + 1 != len(text)):
            # Protection for '...' only cut from real '.'
            if text[idx-1] != '.' and text[idx+1] != '.':

                if _ == '.' and len(new_text) > length:
                    text_list.append(new_text)
                    new_text = ''
    return text_list

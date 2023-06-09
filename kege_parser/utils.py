def align_text(text: str, max_length: int = 79):
    lines = text.split('\n')

    i = 0
    while i < len(lines):
        if len(lines[i]) > max_length:
            last_space_index = lines[i][:max_length].rfind(" ")
            if last_space_index == -1:
                last_space_index = max_length

            lines[i+1:i+1] = [str(lines[i][last_space_index+1:])]
            lines[i] = lines[i][:last_space_index]

        i += 1

    return "\n".join(lines)


def comment_text(text: str):
    out = ""

    for l in text.split("\n"):
        if l:
            out += f"# {l}\n"
        else:
            out += "#\n"

    return out


def clean_unicode_text(text):
    """Remove some strange chars"""

    text = text.replace("\xa0", " ")

    text = text.replace("\xe2\x80\x89", " ")
    text = text.replace("\xe2\x80\xaf", " ")

    text = text.replace("\u2009", " ")
    text = text.replace("\u202f\u202f", "\u202f").replace("\u202f", " ")

    # text = text.replace(u'—', '-')

    return text


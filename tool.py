def text_drober_naked(self, text):
    tokens = text.split(' ')
    tokens_len = len(tokens)
    result = []
    if tokens_len > 20:
        parts = text.split('\n')
        for part in parts:
            part_token = part.split()
            if len(part_token) > 20:
                result.extend([t for t in part.split('.') if t])
            elif len(part_token) < 5:
                if part:
                    result[-1] += part
            else:
                result.append(part)
    else:
        result = [text]
    return result
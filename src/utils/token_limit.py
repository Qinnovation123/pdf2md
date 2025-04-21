def limit_tokens(text: str, max_tokens: int):
    from promptools.openai.tokenize import cached_get_encoding

    enc = cached_get_encoding("cl100k_base")

    tokens = enc.encode(text, disallowed_special=())

    if len(tokens) < max_tokens:
        return text

    while True:
        try:
            return enc.decode(tokens[:max_tokens], errors="strict")
        except UnicodeDecodeError:
            max_tokens += 1

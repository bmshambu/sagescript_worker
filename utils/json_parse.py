import re, json

# def clean_llm_json(raw_output: str) -> str:
#     # Remove JS-like expressions (.repeat, + concatenation)
#     raw_output = raw_output.replace(".repeat(", "_repeat_")  # quick guard
#     raw_output = raw_output.replace("+", "_concat_")         # prevent concat
#     return raw_output
def clean_llm_json_safe(raw_output: str) -> str:
    # 1. Replace `.repeat(N)` with a truncated placeholder
    def repeat_replacer(match):
        char = match.group(1)
        num = int(match.group(2))
        return f"{char}[{num}_chars_truncated]"

    raw_output = re.sub(r'"?([A-Za-z0-9])"\.repeat\((\d+)\)', repeat_replacer, raw_output)
    
    # 2. Remove '+' concatenations
    raw_output = raw_output.replace('+', '')

    # 3. Escape backslashes
    raw_output = raw_output.replace('\\', '\\\\')

    # 4. Escape quotes inside strings (except JSON string quotes)
    def escape_inner_quotes(match):
        inner = match.group(1)
        inner_escaped = inner.replace('"', '\\"')
        return f'"{inner_escaped}"'
    
    raw_output = re.sub(r'"(.*?)"', escape_inner_quotes, raw_output)

    # 5. Truncate very long URLs
    raw_output = re.sub(r'https://example\.com/[^"]{100,}', 'https://example.com/[truncated]', raw_output)

    # 6. Remove JS-style comments
    raw_output = re.sub(r'//.*?$', '', raw_output, flags=re.MULTILINE)

    # 7. Remove trailing commas before } or ]
    raw_output = re.sub(r',(\s*[}\]])', r'\1', raw_output)

    return raw_output

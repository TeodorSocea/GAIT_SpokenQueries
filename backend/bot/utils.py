import re


def extract_links(text):
    url_pattern = r'https?://(?:www\.)?\S+[^\.\s]|www\.\S+[^\.\s]'
    return re.findall(url_pattern, text)
JOTOBA_URL = "https://jotoba.de"
#JOTOBA_URL = "http://127.0.0.1:8080"

JOTOBA_API = JOTOBA_URL + "/api"
COMPLETIONS = JOTOBA_API+ "/suggestion"

ST_WORD = 0
ST_KANJI = 1
ST_SENTENCE = 2
ST_NAME = 3

def search_url(query, search_target):
    return JOTOBA_URL + "/search/{}?t={}".format(query,search_target)

def st_to_name(st) -> str:
    if st == ST_SENTENCE:
        return "Sentence"
    if st == ST_NAME:
        return "Name"
    if st == ST_KANJI:
        return "Kanji"
    return "Word"

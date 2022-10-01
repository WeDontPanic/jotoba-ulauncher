from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.client.EventListener import EventListener
import logging
import completion
import jotoba

logger = logging.getLogger(__name__)

KW_WORD = "word_kw"
KW_KANJI = "kanji_kw"
KW_SENTENCE = "sentence_kw"
KW_NAME = "name_kw"

OP_LANGUAGE = "language"
OP_SHOW_EN = "show_en"
OP_RES_LIMIT = "res_limit"

class JotobaExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

def kw_matches(kevent, extension, keyword):
    return extension.preferences.get(keyword) == kevent.get_keyword()

def format_word_item(item):
    prim = item['primary']

    if 'secondary' in item:
        sec = item['secondary']
        return "{} ({})".format(sec, prim)

    return prim

def try_secondary(item):
    if 'secondary' in item:
        return item['secondary']
    return item['primary']

def make_item(name, on_enter):
    return ExtensionResultItem(icon='images/icon.png',
                    name=name,
                    on_enter=on_enter)
    
class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        search_type = jotoba.ST_WORD

        if kw_matches(event, extension, KW_WORD):
            search_type = jotoba.ST_WORD
        elif kw_matches(event, extension, KW_KANJI):
            search_type = jotoba.ST_KANJI
        elif kw_matches(event, extension, KW_SENTENCE):
            search_type = jotoba.ST_SENTENCE
        elif kw_matches(event, extension, KW_NAME):
            search_type = jotoba.ST_NAME

        if event.get_argument() is None or not str(event.get_argument().strip()):
            txt = "Search in {}s".format(jotoba.st_to_name(search_type).lower())
            return RenderResultListAction([make_item(txt, DoNothingAction())])

        query_str = str(event.get_argument())

        search_lang = extension.preferences.get(OP_LANGUAGE)
        res_limit = int(extension.preferences.get(OP_RES_LIMIT) or 10)
        #show_en = extension.preferences.get(OP_SHOW_EN)

        payload = completion.payload(query_str, search_type, search_lang)
        comp_res = completion.request(payload)['suggestions']
        end = min(res_limit, len(comp_res))
        comp_res = comp_res[:end]

        items = []
        for item in comp_res:
            fmt = format_word_item(item)
            url = jotoba.search_url(try_secondary(item), search_type)
            items.append(make_item(fmt, OpenUrlAction(url)))

        return RenderResultListAction(items)

if __name__ == '__main__':
    JotobaExtension().run()

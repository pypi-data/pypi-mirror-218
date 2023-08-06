from math import ceil

from pyrogram.types import InlineKeyboardButton

from haidar import *


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


# def basic_medium_modules(user_id, datadict, prefix, chat=None):
    
#     data = {}
#     if user_id in BASICID:
#         filter_set = {'limit', 'broadcast', 'help'}
#         for key, value in datadict.items():
#             if key in filter_set:
#                 data[key] = value
            
#     elif user_id in MEDIUMID:
#         filter_set = {'limit', 'broadcast', 'pilter', 'help', 'afk', 'antipm', 'botlog'}
#         for key, value in datadict.items():
#             if key in filter_set:
#                 data[key] = value

#     if not chat:
#         modules = sorted(
#             [
#                 EqInlineKeyboardButton(
#                     x.__MODULE__,
#                     callback_data="{}_module({})".format(
#                         prefix, x.__MODULE__.replace(" ", "_").lower()
#                     ),
#                 )
#                 for x in data.values()
#             ]
#         )
#     else:
#         modules = sorted(
#             [
#                 EqInlineKeyboardButton(
#                     x.__MODULE__,
#                     callback_data="{}_module({},{})".format(
#                         prefix, chat, x.__MODULE__.replace(" ", "_").lower()
#                     ),
#                 )
#                 for x in data.values()
#             ]
#         )
        
#     pairs = list(zip(modules[::2], modules[1::2]))
#     i = 0
#     for m in pairs:
#         for _ in m:
#             i += 1
#     if len(modules) - i == 1:
#         pairs.append((modules[-1],))
#     elif len(modules) - i == 2:
#         pairs.append(
#             (
#                 modules[-2],
#                 modules[-1],
#             )
#         )
        
#     return pairs


def prem_modules(user_id, page_n, module_dict, prefix, chat=None):
    if user_id in BASICID:
        filter_set = {'limit', 'broadcast', 'help'}
        filtered_data = {key: value for key, value in data.items() if key in filter_set}
            
    elif user_id in MEDIUMID:
        filter_set = {'limit', 'broadcast', 'pilter', 'help', 'afk', 'antipm', 'botlog'}
        filtered_data = {key: value for key, value in data.items() if key in filter_set}
                
    elif user_id in PREMIUMID:
        filtered_data = module_dict
        
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({})".format(
                        prefix, x.__MODULE__.replace(" ", "_").lower()
                    ),
                )
                for x in filtered_data.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__MODULE__.replace(" ", "_").lower()
                    ),
                )
                for x in filtered_data.values()
            ]
        )
    pairs = list(zip(modules[::2], modules[1::2]))
                
    if user_id in PREMIUMID:
        line = 4
        pairs = list(zip(modules[::2], modules[1::2]))
        max_num_pages = ceil(len(pairs) / line)
        modulo_page = page_n % max_num_pages

        if len(pairs) > line:
            pairs = pairs[modulo_page * line : line * (modulo_page + 1)] + [
                (
                    EqInlineKeyboardButton(
                        "❮",
                        callback_data="{}_prev({})".format(prefix, modulo_page),
                    ),
                    EqInlineKeyboardButton(
                        "❯",
                        callback_data="{}_next({})".format(prefix, modulo_page),
                    ),
                )
            ]

        return pairs
    else:
        return pairs

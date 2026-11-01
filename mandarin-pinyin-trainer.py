#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Treino de vocabulário em Hanyu Pinyin com números e repetição espaçada.

Funciona com Python 3.9+ e tkinter da biblioteca padrão.
Cada cartão corresponde a uma PALAVRA/UNIDADE de vocabulário, não a uma frase.
O banco combina as frases do estudante, os slides e o livro da aula 16.
Blocos contêm sessões de até 100 caracteres chineses, sem dividir palavras.
"""
from __future__ import annotations

import json
import random
import re
import sys
import tkinter as tk
import unicodedata
from pathlib import Path
from tkinter import messagebox, ttk

CORPUS = [
    ("01 · Afirmação", """
我喜欢游泳。
他喜欢打篮球。
你喜欢骑车。
大家喜欢踢足球。
她喜欢跑步。
我们喜欢打乒乓球。
"""),
    ("02 · Negação", """
我不喜欢打棒球。
他不喜欢游泳。
大家不经常跑步。
她不会打网球。
我没去公园跑步。
我不太喜欢踢足球。
"""),
    ("03 · Perguntas com 吗", """
你喜欢打网球吗？
你也喜欢跑步吗？
他最喜欢游泳吗？
她经常骑车吗？
你每周去健身房吗？
你们会打棒球吗？
"""),
    ("04 · Perguntas com 什么", """
你喜欢什么运动？
他最喜欢什么运动？
你下课以后做什么？
你每周做什么运动？
你想学什么运动？
你觉得什么运动最好玩儿？
"""),
    ("05 · Perguntas com 谁", """
谁最喜欢跑步？
谁每周打篮球？
你和谁一起去公园？
谁会打乒乓球？
谁经常去游泳馆？
这是谁的网球？
"""),
    ("06 · Perguntas de lugar", """
你去哪儿跑步？
他在哪儿游泳？
你在哪个公园散步？
他们下课以后去哪里？
你最喜欢哪个游泳馆？
那个篮球场在哪儿？
"""),
    ("07 · Perguntas de tempo", """
你什么时候去公园跑步？
你星期几打网球？
你明天几点去健身房？
他今天游泳吗？
你早上喜欢跑步吗？
大家周末去公园吗？
"""),
    ("08 · Superlativo", """
我最喜欢游泳。
他最喜欢打网球。
你最喜欢什么运动？
大家最喜欢哪种运动？
你最喜欢哪个公园？
她最喜欢骑车吗？
"""),
    ("09 · Comparação de preferências", """
我喜欢跑步，但是更喜欢游泳。
他喜欢打篮球，但是更喜欢打乒乓球。
她喜欢游泳，但是更喜欢骑车。
你喜欢踢足球，但是更喜欢打网球吗？
我不喜欢打棒球，但是更喜欢打篮球。
大家喜欢去健身房，但是更喜欢去公园。
"""),
    ("10 · Frequência", """
我每周跑步三次。
他每周打网球两次。
你一周游泳几次？
大家每天散步一次。
她一般每周骑车一次。
你一个月打几次篮球？
"""),
    ("11 · Duração", """
我每次跑步半个小时。
他每次游泳一个小时。
你每次打篮球多长时间？
她每次骑车两个小时。
你每次去健身房健身多久？
大家每次打乒乓球十五分钟。
"""),
    ("12 · Ordem da frase", """
我每周去公园跑步。
他下课以后去篮球场打篮球。
我们每周去足球场踢足球。
你今天去游泳馆游泳吗？
大家下课以后去公园散步。
她星期六去健身房健身。
"""),
    ("13 · Além de", """
除了跑步，我还喜欢游泳。
除了打篮球，他还会打乒乓球。
除了游泳，你还喜欢什么运动？
除了踢足球，大家还喜欢打网球吗？
除了骑车，她还经常散步。
除了打棒球，你还会做什么？
"""),
    ("14 · Perguntas de motivo", """
你为什么喜欢跑步？
他为什么不喜欢游泳？
你为什么最喜欢打网球？
她为什么每周去健身房？
大家为什么去公园散步？
你为什么觉得打乒乓球好玩儿？
"""),
    ("15 · Como e avaliação", """
你怎么去公园？
他怎么去游泳馆？
你怎么学游泳？
从学校到公园怎么走？
你觉得打棒球怎么样？
你觉得这个健身房怎么样？
"""),
    ("16 · Escolha e A不A", """
你喜欢跑步还是游泳？
他最喜欢打篮球还是踢足球？
你喜欢不喜欢打网球？
你会不会骑车？
你下课以后去不去公园？
你想去游泳馆还是健身房？
"""),
    ("17 · Outros interrogativos", """
你有几个网球？
游泳馆的票多少钱？
你几岁开始游泳？
公园离你家多远？
篮球场有多少人？
你每周花多少时间运动？
"""),
    ("18 · Atividades e hobbies", """
我喜欢去电影院看电影。
他喜欢去酒吧喝酒。
你喜欢唱卡拉OK吗？
我不喜欢打麻将。
你什么时候跟朋友聊天？
你跟谁去电影院看电影？
他今天去酒吧喝酒吗？
她喜欢唱卡拉OK，但是不喜欢打麻将。
你周末喜欢做什么？
你在哪儿唱卡拉OK？
你为什么不喜欢去电影院看电影？
你喜欢打麻将还是跟朋友聊天？
我晚上喜欢跟朋友聊天。
他们不喜欢去酒吧喝酒。
"""),
    ("19 · Interesses e exemplos", """
我有很多兴趣和爱好，比如游泳、跑步和打麻将。
他有很多爱好，比如打网球、打乒乓球和看电影。
中国人有很多兴趣和爱好，比如打麻将和唱卡拉OK。
我有很多兴趣，比如跟朋友聊天和看电影。
你有什么兴趣和爱好？
你的爱好有哪些？
你喜欢什么运动？
你有很多兴趣和爱好吗？
她有很多爱好，比如跑步和唱卡拉OK。
我没有很多爱好，只喜欢游泳。
他有很多兴趣，但是他不喜欢打麻将。
你有别的兴趣和爱好吗？
你的朋友有什么爱好？
你可以说三个你的爱好吗？
"""),
    ("20 · Adição de interesses", """
除了跑步，我还喜欢游泳。
除了打麻将，我还喜欢看电影。
我除了喜欢运动，还有别的爱好。
他除了打棒球，还喜欢唱卡拉OK。
你除了游泳，还喜欢做什么？
你除了去电影院，还喜欢去哪儿？
她除了喜欢跑步，还喜欢别的运动，比如打网球。
我除了喜欢唱卡拉OK，还喜欢跟朋友聊天。
你除了跟朋友聊天，还会打麻将吗？
他除了喜欢跑步，还喜欢别的运动，比如游泳。
除了打网球，我还喜欢打乒乓球。
我除了喜欢运动，还有别的爱好，比如看电影。
你除了打麻将，还有别的爱好吗？
中国人除了打棒球，还有别的爱好，比如打麻将和唱卡拉OK。
"""),
    ("21 · Preferências", """
你最喜欢做什么？
我最喜欢打麻将。
他最喜欢去电影院看电影。
你最喜欢什么运动？
你的朋友最喜欢做什么？
你最喜欢唱卡拉OK吗？
你最喜欢哪种运动？
她最喜欢跟朋友聊天。
谁最喜欢打网球？
你为什么最喜欢游泳？
你最喜欢打麻将还是看电影？
他不喜欢跑步，他最喜欢打乒乓球。
我最喜欢的运动是游泳。
你现在最喜欢做什么？
"""),
    ("22 · 一样 / 不一样", """
我的爱好和你的不一样。
他的爱好和我的不一样。
我的爱好和你的不一样，比如我喜欢打麻将，你喜欢唱卡拉OK。
你的爱好和你的朋友的一样吗？
她的爱好和我的不一样。
我的爱好和他的一样。
你喜欢游泳，我也喜欢游泳，我们的爱好一样。
中国人的爱好和美国人的一样吗？
我喜欢看电影，他喜欢打麻将，我们的爱好不一样。
你和你的朋友的爱好一样吗？
谁的爱好和你的不一样？
为什么你的爱好和我的不一样？
我们的爱好不一样，但是我们都喜欢唱卡拉OK。
我喜欢跑步，你喜欢游泳，可是我们都喜欢运动。
"""),
    ("23 · 我发现", """
我发现我的爱好和你的不一样。
我发现他喜欢打麻将，你喜欢看电影。
我发现中国人的爱好和美国人的不一样。
我发现我的朋友喜欢唱卡拉OK。
你发现你的爱好和我的不一样吗？
你发现谁喜欢打麻将？
你发现中国人喜欢什么运动？
我发现他不喜欢去酒吧喝酒。
我发现她除了喜欢跑步，还喜欢游泳。
我们发现你最喜欢跟朋友聊天。
你怎么发现他喜欢打网球？
你什么时候发现他喜欢看电影？
我发现我的朋友喜欢打麻将，但是我不喜欢。
我没发现他的爱好和我的不一样。
"""),
]

PINYIN_CHAR = """
一 yi1 三 san1 上 shang4 下 xia4 不 bu4 两 liang3 个 ge 中 zhong1
为 wei4 久 jiu3 么 me 乒 ping1 乓 pang1 也 ye3 了 le 五 wu3
些 xie1 人 ren2 什 shen2 今 jin1 从 cong2 他 ta1 以 yi3 们 men
会 hui4 但 dan4 你 ni3 候 hou 做 zuo4 健 jian4 儿 r
公 gong1 六 liu4 兴 xing4 几 ji3 分 fen1 别 bie2 到 dao4 动 dong4
十 shi2 半 ban4 卡 ka3 去 qu4 友 you3 发 fa1 只 zhi3 可 ke3 后 hou4
吗 ma 吧 ba 周 zhou1 和 he2 哪 na3 唱 chang4 喜 xi3 喝 he1
园 yuan2 国 guo2 在 zai4 场 chang3 多 duo1 大 da4 天 tian1 太 tai4
她 ta1 好 hao3 如 ru2 始 shi3 学 xue2 家 jia1 将 jiang4 小 xiao3
少 shao 岁 sui4 常 chang2 开 kai1 影 ying3 很 hen3 得 de 怎 zen3
想 xiang3 我 wo3 房 fang2 打 da3 拉 la1 散 san4 早 zao3 时 shi2
明 ming2 星 xing1 是 shi4 晚 wan3 更 geng4 最 zui4 月 yue4
有 you3 朋 peng2 期 qi1 末 mo4 校 xiao4 样 yang4 棒 bang4 次 ci4
欢 huan 步 bu4 每 mei3 比 bi3 没 mei2 泳 yong3 游 you2 点 dian3
爱 ai4 玩 wan2 现 xian4 球 qiu2 电 dian4 的 de 看 kan4 票 piao4
离 li2 种 zhong3 篮 lan2 经 jing1 网 wang3 美 mei3 聊 liao2 般 ban1
花 hua1 觉 jue2 说 shuo1 课 ke4 谁 shei2 走 zou3 起 qi3 趣 qu4
足 zu2 跑 pao3 跟 gen1 踢 ti1 身 shen1 车 che1 运 yun4 还 hai2
这 zhe4 远 yuan3 那 na4 都 dou1 酒 jiu3 里 li3 钟 zhong1 钱 qian2
长 chang2 间 jian1 院 yuan4 除 chu2 馆 guan3 骑 qi2 麻 ma2
"""


# Itens de mais de um caractere são palavras do vocabulário. O algoritmo
# usa correspondência mais longa e, quando necessário, um único caractere.
# A escrita esperada usa tons NUMÉRICOS (1-4, 5 ou ausente para tom neutro).
# Importante: o tom das palavras é conferido; não basta acertar as letras.
WORD_PINYIN = {
    # Pronomes, perguntas, expressões
    "我们": "wo3men", "你们": "ni3men", "他们": "ta1men",
    "大家": "da4jia1", "什么": "shen2me", "什么时候": "shen2meshi2hou",
    "为什么": "wei4shen2me", "怎么": "zen3me", "怎么样": "zen3meyang4",
    "哪儿": "na3r", "哪里": "na3li3", "哪个": "na3ge", "那个": "na4ge",
    "这个": "zhe4ge", "多少": "duo1shao", "几个": "ji3ge",
    "几点": "ji3dian3", "多长": "duo1chang2", "多久": "duo1jiu3",
    "多远": "duo1yuan3", "别的": "bie2de", "一样": "yi2yang4",
    "一起": "yi4qi3", "一般": "yi4ban1",
    "但是": "dan4shi4", "可是": "ke3shi4", "比如": "bi3ru2",
    "除了": "chu2le", "以后": "yi3hou4", "发现": "fa1xian4",
    "可以": "ke3yi3", "开始": "kai1shi3",
    "会不会": "hui4buhui4", "去不去": "qu4buqu4",
    "喜欢不喜欢": "xi3huanbuxi3huan",
    # Verbos e ações
    "喜欢": "xi3huan", "游泳": "you2yong3", "骑车": "qi2che1",
    "跑步": "pao3bu4", "散步": "san4bu4", "健身": "jian4shen1",
    "运动": "yun4dong4", "聊天": "liao2tian1",
    "喝酒": "he1jiu3", "唱歌": "chang4ge1",
    "觉得": "jue2de", "好玩儿": "hao3wan2r",
    "没有": "mei2you3", "不会": "bu2hui4", "不太": "bu2tai4",
    "不去": "bu2qu4", "下课": "xia4ke4", "说话": "shuo1hua4",
    # Esportes, lazer e lugares
    "篮球": "lan2qiu2", "篮球场": "lan2qiu2chang3", "足球": "zu2qiu2",
    "足球场": "zu2qiu2chang3", "棒球": "bang4qiu2", "网球": "wang3qiu2",
    "乒乓球": "ping1pang1qiu2", "麻将": "ma2jiang4",
    "电影院": "dian4ying3yuan4", "电影": "dian4ying3",
    "游泳馆": "you2yong3guan3", "健身房": "jian4shen1fang2",
    "公园": "gong1yuan2", "学校": "xue2xiao4",
    "酒吧": "jiu3ba", "卡拉OK": "ka3la1ok",
    # Pessoas e interesses
    "朋友": "peng2you", "兴趣": "xing4qu4", "爱好": "ai4hao4",
    "中国人": "zhong1guo2ren2", "美国人": "mei3guo2ren2",
    "中国": "zhong1guo2", "美国": "mei3guo2",
    # Tempo, quantidade e frequência
    "经常": "jing1chang2", "每周": "mei3zhou1", "每次": "mei3ci4",
    "每天": "mei3tian1", "一周": "yi4zhou1", "一次": "yi2ci4",
    "一个": "yi2ge", "两个": "liang3ge", "三个": "san1ge",
    "十五": "shi2wu3", "星期": "xing1qi1", "星期六": "xing1qi1liu4",
    "今天": "jin1tian1", "明天": "ming2tian1", "现在": "xian4zai4",
    "周末": "zhou1mo4", "早上": "zao3shang", "晚上": "wan3shang",
    "小时": "xiao3shi2", "分钟": "fen1zhong1", "时间": "shi2jian1",

    # Demais palavras comuns
    "很多": "hen3duo1",
}


# Complementos conferidos visualmente nas páginas dos dois PDFs.
# Termos originalmente ausentes e expressões de frequência escritas nos slides.
# Formato: hanzi -> (pinyin numerico, tradução pt-BR, exemplo, tradução do exemplo, PDF, página).
SLIDE_ADDITIONS = {
    "大部分": ("da4bu4fen", "a maior parte; a maioria", "大部分人喜欢运动。", "A maioria das pessoas gosta de praticar esportes.", "16.1", 3),
    "美式": ("mei3shi4", "estilo americano; americano (estilo)", "美式足球很有趣。", "O futebol americano é interessante.", "16.1", 3),
    "有趣": ("you3qu4", "interessante; curioso", "游泳很有趣。", "Nadar é interessante.", "16.1", 3),
    "棒球场": ("bang4qiu2chang3", "campo de beisebol", "他在棒球场打棒球。", "Ele joga beisebol no campo de beisebol.", "16.1", 14),
    "中文": ("zhong1wen2", "língua chinesa; chinês", "除了中文以外，我还会说英语。", "Além do chinês, também sei falar inglês.", "16.1", 17),
    "英语": ("ying1yu3", "língua inglesa; inglês", "除了中文以外，我还会说英语。", "Além do chinês, também sei falar inglês.", "16.1", 17),
    "以外": ("yi3wai4", "além de; fora de; exceto", "除了中文以外，我还会说英语。", "Além do chinês, também sei falar inglês.", "16.1", 17),
    "一天": ("yi4tian1", "um dia; por dia", "我一天跑步一次。", "Eu corro uma vez por dia.", "16.1", 9),
    "一星期": ("yi4xing1qi1", "uma semana; por semana", "我一星期打两次网球。", "Eu jogo tênis duas vezes por semana.", "16.1", 11),
    "一天一次": ("yi4tian1yi2ci4", "uma vez por dia", "我一天跑步一次。", "Eu corro uma vez por dia.", "16.1", 9),
    "一周两次": ("yi4zhou1liang3ci4", "duas vezes por semana", "他一周打两次网球。", "Ele joga tênis duas vezes por semana.", "16.1", 11),
    "一星期两次": ("yi4xing1qi1liang3ci4", "duas vezes por semana", "我一星期打两次网球。", "Eu jogo tênis duas vezes por semana.", "16.1", 11),
    "每周两次": ("mei3zhou1liang3ci4", "duas vezes toda semana", "他每周打两次网球。", "Ele joga tênis duas vezes por semana.", "16.1", 11),
    "更喜欢": ("geng4xi3huan", "gostar ainda mais; preferir", "我喜欢跑步，但是更喜欢游泳。", "Eu gosto de correr, mas gosto ainda mais de nadar.", "16.1", 7),
    "最喜欢": ("zui4xi3huan", "gostar mais de; favorito", "你最喜欢什么运动？", "De qual esporte você mais gosta?", "16.1", 8),
}

# Amostragem de TODO o conteúdo chinês visível das páginas com texto em mandarim;
# as figuras puramente ilustrativas e os exercícios só em inglês não têm palavras extras.
# A coluna é PDF, página, texto exibido na imagem. Pontos suspensivos foram omitidos.
SLIDE_SOURCES = [
    ("16.1",1,"你也喜欢跑步吗"),
    ("16.1",3,"更|小时|最|大家|棒球|但是|大部分|美式|有趣|好玩儿|除了|一般|经常|公园|篮球场"),
    ("16.1",4,"打网球|打乒乓球|打棒球|踢足球|打篮球|游泳"),
    ("16.1",5,"你喜欢什么运动"),
    ("16.1",6,"他喜欢什么运动|跑步|骑车|踢足球|打网球"),
    ("16.1",7,"喜欢|但是|更喜欢"),
    ("16.1",8,"你最喜欢什么运动"),
    ("16.1",9,"一天一次"),
    ("16.1",10,"每次两个小时|每次一个小时|每次半个小时|每次十五分钟"),
    ("16.1",11,"你一周打几次网球|一周两次|一星期两次|每周两次"),
    ("16.1",12,"他每周打一次网球"),
    ("16.1",14,"健身房|足球场|公园|游泳馆|篮球场|棒球场"),
    ("16.1",15,"他们下课以后做什么|去健身房健身|去公园跑步|去公园散步|去游泳馆游泳|去足球场踢足球|去篮球场打篮球"),
    ("16.1",16,"除了跑步我还喜欢骑车|除了打篮球我还会打乒乓球"),
    ("16.1",17,"除了游泳我还喜欢散步|除了中文以外我还会说英语|除了打棒球我还喜欢打网球"),
    ("16.1",18,"除了|还"),
    ("16.2",1,"你也喜欢跑步吗"),
    ("16.2",2,"去电影院看电影|去酒吧喝酒|唱卡拉OK|跟朋友聊天|打麻将"),
    ("16.2",3,"我有很多兴趣和爱好比如|中国人有很多兴趣和爱好比如"),
    ("16.2",4,"我除了喜欢运动还有别的爱好比如"),
    ("16.2",5,"他除了喜欢跑步还喜欢别的运动比如"),
    ("16.2",6,"中国人除了打棒球还有别的爱好比如"),
    ("16.2",7,"你最喜欢做什么"),
    ("16.2",8,"和|不一样|我的爱好和你的不一样比如我喜欢打麻将你喜欢去酒吧喝酒"),
    # Na página 9, 'country' é um espaço em inglês a completar, NÃO pinyin.
    ("16.2",9,"我发现中国人的爱好和|人的不一样|中国人喜欢|人喜欢"),
]

# As frases de reforço dos slides são exemplos, NÃO cartões de frases inteiras.
for _w, (_pin, _pt, _ex, _ex_pt, _lesson, _page) in SLIDE_ADDITIONS.items():
    # Preservar como cartões separados 更, 最 e 喜欢 que já existiam.
    # Estas 2 combinações são acrescentadas como cartões extras sem mudar
    # a segmentação do material anterior.
    if _w not in {"更喜欢", "最喜欢"}:
        WORD_PINYIN[_w] = _pin

# As frases de entrada são usadas SOMENTE para extrair palavras e para mostrar
# um exemplo opcional após a resposta. Jamais são usadas como cartão inteiro.
TOKENS = PINYIN_CHAR.split()
assert len(TOKENS) % 2 == 0, "Dicionário de caracteres incompleto"
CHAR_PINYIN = dict(zip(TOKENS[::2], TOKENS[1::2]))
# Correções do dicionário-base (nos raros casos de caractere isolado).
CHAR_PINYIN.update({"少": "shao3", "候": "hou", "得": "de"})
WORD_KEYS = sorted(WORD_PINYIN, key=len, reverse=True)
PUNCTUATION = set("。，！？、；：,.!?;:()（）\"'“”‘’ ")


def segment(sentence: str) -> list[str]:
    """Segmentação por vocabulário fechado, sem dependências externas."""
    result = []
    idx = 0
    while idx < len(sentence):
        char = sentence[idx]
        if char in PUNCTUATION:
            idx += 1
            continue
        chosen = next((w for w in WORD_KEYS if sentence.startswith(w, idx)), None)
        if chosen is not None:
            result.append(chosen)
            idx += len(chosen)
        elif char in CHAR_PINYIN:
            result.append(char)
            idx += 1
        else:
            raise ValueError(f"Caractere não cadastrado {char!r} em {sentence!r}")
    return result


def pinyin_of(word: str) -> str:
    if word in WORD_PINYIN:
        return WORD_PINYIN[word]
    if len(word) == 1 and word in CHAR_PINYIN:
        return CHAR_PINYIN[word]
    raise KeyError(f"Palavra sem romanização: {word}")


def build_cards():
    cards: dict[str, dict] = {}
    sentence_count = 0
    token_count = 0
    for category, body in CORPUS:
        for sentence in (s.strip() for s in body.splitlines()):
            if not sentence:
                continue
            sentence_count += 1
            for word in segment(sentence):
                token_count += 1
                if word not in cards:
                    cards[word] = {
                        "word": word,
                        "answer": pinyin_of(word),
                        "categories": [category],
                        "examples": [sentence],
                        "occurrences": 1,
                    }
                else:
                    item = cards[word]
                    item["occurrences"] += 1
                    if category not in item["categories"]:
                        item["categories"].append(category)
                    if sentence not in item["examples"] and len(item["examples"]) < 4:
                        item["examples"].append(sentence)
    return cards, sentence_count, token_count


CARDS, TOTAL_SENTENCES, TOTAL_TOKENS = build_cards()

# Palavras novas dos PDFs entram uma vez cada, preservando os cartões antigos.
WORD_PINYIN.update({w: data[0] for w, data in SLIDE_ADDITIONS.items()})
for _word, (_pin, _pt, _ex, _ex_pt, _lesson, _page) in SLIDE_ADDITIONS.items():
    if _word not in CARDS:
        CARDS[_word] = {"word": _word, "answer": _pin,
                        "categories": [f"Slides {_lesson} · pág. {_page}"],
                        "examples": [_ex], "occurrences": 1}

# Checagem estrutural: cada unidade textual dos slides precisa ter cartões.
# Não é uma extração via OCR: o índice foi transcrito/conferido das imagens.
def audit_slide_coverage() -> list[dict]:
    rows = []
    for lesson, page, content in SLIDE_SOURCES:
        for chunk in content.split("|"):
            units = segment(chunk)
            missing = [w for w in units if w not in CARDS]
            rows.append({"lesson": lesson, "page": page, "text": chunk,
                         "terms": " / ".join(units), "missing": missing})
    return rows

SLIDE_COVERAGE = audit_slide_coverage()
if any(row["missing"] for row in SLIDE_COVERAGE):
    raise RuntimeError("Há palavras dos PDFs faltando: " + str([
        row for row in SLIDE_COVERAGE if row["missing"]]))

# 100 CARACTERES CHINESES por sessão (não 100 palavras), sem dividir cartões.
# Programação dinâmica mantém as primeiras palavras na ordem original sempre
# que possível, e completa exatamente 100 sem sacrificar nenhuma palavra.
def hanzi_count(s: str) -> int:
    return sum(('\u3400' <= c <= '\u9fff') or ('\uf900' <= c <= '\ufaff')
               for c in s)

def make_sessions(cards: dict, cap: int = 100) -> dict[str, list[str]]:
    remaining = list(cards)
    result = {}
    while remaining:
        total = sum(hanzi_count(w) for w in remaining)
        target = min(cap, total)
        dp: dict[int, tuple[str, ...]] = {0: ()}
        for word in remaining:
            size = hanzi_count(word)
            if not 0 < size <= cap:
                raise ValueError(f"Cartão não cabe numa sessão: {word}")
            for subtotal, selected in sorted(list(dp.items()), reverse=True):
                nxt = subtotal + size
                if nxt <= target and nxt not in dp:
                    dp[nxt] = selected + (word,)
            if target in dp and len(remaining) > 70:
                # Otimização opcional: prioriza primeiro conjunto exato.
                break
        # Até 100 caracteres: não dividir uma palavra para preencher o limite.
        target = max(dp)
        chosen = list(dp[target])
        name = (f"Sessão {len(result)+1:02d} · {target} caracteres · "
                f"{len(chosen)} cartões")
        result[name] = chosen
        selected_set = set(chosen)
        remaining = [w for w in remaining if w not in selected_set]
    return result

LEGACY_SESSIONS = make_sessions(CARDS)
LEGACY_WORD_SESSION = {w: name for name, words in LEGACY_SESSIONS.items() for w in words}
ORIGINAL_WORDS = tuple(CARDS)


# Traduções em português brasileiro do vocabulário (incluindo partículas).
# A tradução está ligada à palavra, e não à resposta digitada pelo aluno.
WORD_TRANSLATIONS = {
    "我": "eu", "喜欢": "gostar de", "游泳": "nadar; natação",
    "他": "ele", "打": "praticar (esporte com bola); jogar", "篮球": "basquete",
    "你": "você", "骑车": "andar de bicicleta", "大家": "todos; todo mundo",
    "踢": "chutar; jogar (futebol)", "足球": "futebol", "她": "ela",
    "跑步": "correr; corrida", "我们": "nós", "乒乓球": "tênis de mesa",
    "不": "não (negação)", "棒球": "beisebol", "经常": "frequentemente",
    "不会": "não saber; não conseguir (fazer)", "网球": "tênis",
    "没": "não (passado ou ausência)", "去": "ir", "公园": "parque",
    "不太": "não muito", "吗": "partícula de pergunta (sim/não)",
    "也": "também", "最": "mais; o mais (superlativo)",
    "每周": "toda semana; semanalmente", "健身房": "academia",
    "你们": "vocês", "会": "saber fazer; conseguir; poder",
    "什么": "o quê; que", "运动": "esporte; atividade física",
    "下课": "terminar a aula; depois da aula", "以后": "depois; após",
    "做": "fazer", "想": "querer; ter vontade de", "学": "aprender; estudar",
    "觉得": "achar; considerar", "好玩儿": "divertido; interessante",
    "谁": "quem", "和": "e; com", "一起": "junto(s)",
    "游泳馆": "piscina pública; centro de natação",
    "这": "este; esta; isto", "是": "ser; estar", "的": "partícula de posse/atribuição",
    "哪儿": "onde", "在": "estar em; em", "哪个": "qual (dentre opções)",
    "散步": "caminhar; passear", "他们": "eles; elas", "哪里": "onde",
    "那个": "aquele; aquela", "篮球场": "quadra de basquete",
    "什么时候": "quando", "星期": "semana; dia da semana",
    "几": "quantos; qual (número pequeno)", "明天": "amanhã",
    "几点": "que horas", "今天": "hoje", "早上": "de manhã",
    "周末": "fim de semana", "哪": "qual", "种": "tipo; espécie",
    "但是": "mas; porém", "更": "mais; ainda mais",
    "三": "três", "次": "vez; vezes", "两": "dois; duas (antes de classificador)",
    "一周": "uma semana; por semana", "每天": "todos os dias",
    "一次": "uma vez", "一般": "geralmente; em geral",
    "一个": "um; uma (com classificador)", "月": "mês",
    "每次": "cada vez; todas as vezes", "半": "meio; metade",
    "个": "classificador geral", "小时": "hora (duração)",
    "多长": "quanto tempo; quão comprido", "时间": "tempo",
    "两个": "dois; duas (com classificador)", "健身": "fazer exercícios; condicionamento físico",
    "多久": "quanto tempo (duração)", "十五": "quinze",
    "分钟": "minuto(s)", "足球场": "campo de futebol",
    "星期六": "sábado", "除了": "além de; exceto",
    "还": "ainda; além disso; também", "为什么": "por quê",
    "怎么": "como; de que maneira", "从": "de; a partir de",
    "学校": "escola", "到": "até; chegar a", "走": "andar; caminhar; ir",
    "怎么样": "como é; o que acha de", "这个": "este; esta",
    "喜欢不喜欢": "gosta ou não gosta", "会不会": "sabe ou não sabe (fazer)",
    "去不去": "vai ou não vai", "有": "ter; haver; existir",
    "几个": "quantos (poucos)", "票": "ingresso; bilhete",
    "多少": "quanto(s)", "钱": "dinheiro", "岁": "anos de idade",
    "开始": "começar", "离": "estar a certa distância de",
    "家": "casa; lar; família", "多远": "a que distância",
    "人": "pessoa(s)", "花": "gastar (tempo/dinheiro)",
    "电影院": "cinema", "看": "ver; assistir; olhar",
    "电影": "filme", "酒吧": "bar", "喝酒": "beber álcool",
    "唱": "cantar", "卡拉OK": "karaokê", "麻将": "mahjong",
    "跟": "com; junto com", "朋友": "amigo(a)",
    "聊天": "conversar; bater papo", "晚上": "à noite",
    "很多": "muitos; muitas", "兴趣": "interesse(s)",
    "爱好": "hobby; passatempo", "比如": "por exemplo",
    "中国人": "chinês; chineses", "些": "alguns; algumas",
    "没有": "não ter; não haver", "只": "somente; apenas",
    "别的": "outro(s); outra(s)", "可以": "poder; ter permissão para",
    "说": "dizer; falar", "三个": "três (com classificador)",
    "现在": "agora; atualmente", "一样": "igual; da mesma maneira",
    "美国人": "americano(s); estadunidense(s)", "都": "todos; ambos",
    "可是": "mas; porém", "发现": "perceber; descobrir",
}

WORD_TRANSLATIONS.update({w: data[1] for w, data in SLIDE_ADDITIONS.items()})

# Traduções das frases usadas como exemplos dos cartões.
# O banco exige cobertura completa: nenhuma palavra pode ter exemplo sem tradução.
EXAMPLE_TRANSLATIONS = {
    "我喜欢游泳。": "Eu gosto de nadar.",
    "他喜欢打篮球。": "Ele gosta de jogar basquete.",
    "你喜欢骑车。": "Você gosta de andar de bicicleta.",
    "大家喜欢踢足球。": "Todo mundo gosta de jogar futebol.",
    "她喜欢跑步。": "Ela gosta de correr.",
    "我们喜欢打乒乓球。": "Nós gostamos de jogar tênis de mesa.",
    "我不喜欢打棒球。": "Eu não gosto de jogar beisebol.",
    "大家不经常跑步。": "O pessoal não corre com frequência.",
    "她不会打网球。": "Ela não sabe jogar tênis.",
    "我没去公园跑步。": "Eu não fui correr no parque.",
    "我不太喜欢踢足球。": "Eu não gosto muito de jogar futebol.",
    "你喜欢打网球吗？": "Você gosta de jogar tênis?",
    "你也喜欢跑步吗？": "Você também gosta de correr?",
    "他最喜欢游泳吗？": "Nadar é o que ele mais gosta de fazer?",
    "你每周去健身房吗？": "Você vai à academia toda semana?",
    "你们会打棒球吗？": "Vocês sabem jogar beisebol?",
    "你喜欢什么运动？": "De qual esporte você gosta?",
    "你下课以后做什么？": "O que você faz depois da aula?",
    "你想学什么运动？": "Qual esporte você quer aprender?",
    "你觉得什么运动最好玩儿？": "Qual esporte você acha mais divertido?",
    "谁最喜欢跑步？": "Quem mais gosta de correr?",
    "你和谁一起去公园？": "Com quem você vai ao parque?",
    "谁经常去游泳馆？": "Quem costuma ir à piscina?",
    "这是谁的网球？": "De quem é esta bola de tênis?",
    "你去哪儿跑步？": "Onde você vai correr?",
    "他在哪儿游泳？": "Onde ele nada?",
    "你在哪个公园散步？": "Em qual parque você caminha?",
    "他们下课以后去哪里？": "Aonde eles vão depois da aula?",
    "那个篮球场在哪儿？": "Onde fica aquela quadra de basquete?",
    "你什么时候去公园跑步？": "Quando você vai correr no parque?",
    "你星期几打网球？": "Em qual dia da semana você joga tênis?",
    "你明天几点去健身房？": "A que horas você vai à academia amanhã?",
    "他今天游泳吗？": "Ele vai nadar hoje?",
    "你早上喜欢跑步吗？": "Você gosta de correr de manhã?",
    "大家周末去公园吗？": "Todo mundo vai ao parque no fim de semana?",
    "大家最喜欢哪种运动？": "De qual tipo de esporte todo mundo mais gosta?",
    "我喜欢跑步，但是更喜欢游泳。": "Eu gosto de correr, mas gosto ainda mais de nadar.",
    "我每周跑步三次。": "Eu corro três vezes por semana.",
    "他每周打网球两次。": "Ele joga tênis duas vezes por semana.",
    "你一周游泳几次？": "Quantas vezes por semana você nada?",
    "大家每天散步一次。": "Todo mundo caminha uma vez por dia.",
    "她一般每周骑车一次。": "Ela geralmente anda de bicicleta uma vez por semana.",
    "你一个月打几次篮球？": "Quantas vezes por mês você joga basquete?",
    "我每次跑步半个小时。": "Toda vez que corro, corro por meia hora.",
    "你每次打篮球多长时间？": "Por quanto tempo você joga basquete a cada vez?",
    "她每次骑车两个小时。": "Ela anda de bicicleta por duas horas a cada vez.",
    "你每次去健身房健身多久？": "Quanto tempo você se exercita na academia a cada visita?",
    "大家每次打乒乓球十五分钟。": "Todo mundo joga tênis de mesa por quinze minutos a cada vez.",
    "我们每周去足球场踢足球。": "Nós vamos ao campo jogar futebol toda semana.",
    "她星期六去健身房健身。": "Ela vai à academia se exercitar no sábado.",
    "除了跑步，我还喜欢游泳。": "Além de correr, também gosto de nadar.",
    "你为什么喜欢跑步？": "Por que você gosta de correr?",
    "你怎么去公园？": "Como você vai ao parque?",
    "从学校到公园怎么走？": "Como se vai da escola até o parque?",
    "你觉得打棒球怎么样？": "O que você acha de jogar beisebol?",
    "你觉得这个健身房怎么样？": "O que você acha desta academia?",
    "你喜欢不喜欢打网球？": "Você gosta de jogar tênis ou não?",
    "你会不会骑车？": "Você sabe andar de bicicleta?",
    "你下课以后去不去公园？": "Você vai ao parque depois da aula ou não?",
    "你有几个网球？": "Quantas bolas de tênis você tem?",
    "游泳馆的票多少钱？": "Quanto custa a entrada da piscina?",
    "你几岁开始游泳？": "Com quantos anos você começou a nadar?",
    "公园离你家多远？": "A que distância da sua casa fica o parque?",
    "篮球场有多少人？": "Quantas pessoas há na quadra de basquete?",
    "你每周花多少时间运动？": "Quanto tempo você dedica a exercícios físicos por semana?",
    "我喜欢去电影院看电影。": "Eu gosto de ir ao cinema assistir a filmes.",
    "他喜欢去酒吧喝酒。": "Ele gosta de ir ao bar beber.",
    "你喜欢唱卡拉OK吗？": "Você gosta de cantar karaokê?",
    "我不喜欢打麻将。": "Eu não gosto de jogar mahjong.",
    "你什么时候跟朋友聊天？": "Quando você conversa com os amigos?",
    "我晚上喜欢跟朋友聊天。": "Eu gosto de conversar com os amigos à noite.",
    "我有很多兴趣和爱好，比如游泳、跑步和打麻将。": "Tenho muitos interesses e hobbies, como nadar, correr e jogar mahjong.",
    "中国人有很多兴趣和爱好，比如打麻将和唱卡拉OK。": "Os chineses têm muitos interesses e hobbies, como jogar mahjong e cantar karaokê.",
    "你的爱好有哪些？": "Quais são seus hobbies?",
    "我没有很多爱好，只喜欢游泳。": "Eu não tenho muitos hobbies; só gosto de nadar.",
    "你有别的兴趣和爱好吗？": "Você tem outros interesses e hobbies?",
    "你可以说三个你的爱好吗？": "Você consegue citar três hobbies seus?",
    "你现在最喜欢做什么？": "O que você mais gosta de fazer atualmente?",
    "我的爱好和你的不一样。": "Meus hobbies são diferentes dos seus.",
    "中国人的爱好和美国人的一样吗？": "Os hobbies dos chineses são iguais aos dos americanos?",
    "我们的爱好不一样，但是我们都喜欢唱卡拉OK。": "Nossos hobbies são diferentes, mas todos gostamos de cantar karaokê.",
    "我喜欢跑步，你喜欢游泳，可是我们都喜欢运动。": "Eu gosto de correr, você gosta de nadar, mas nós dois gostamos de praticar esportes.",
    "我发现我的爱好和你的不一样。": "Percebi que meus hobbies são diferentes dos seus.",
}



EXAMPLE_TRANSLATIONS.update({data[2]: data[3] for data in SLIDE_ADDITIONS.values()})

# Vocabulário conferido nas páginas visíveis do livro, sem importar a aula 17
# oculta fora do recorte da última página. Exemplos curtos são adaptações didáticas.
# Palavra | pinyin numérico | tradução | exemplo | pinyin do exemplo | tradução | página PDF
BOOK_ROWS = '''
知道|zhi1dao|saber; ter conhecimento|你知道吗？|nǐ zhīdao ma?|Você sabe?|1
美国|mei3guo2|Estados Unidos|你们在美国喜欢什么运动？|nǐmen zài Měiguó xǐhuan shénme yùndòng?|De quais esportes vocês gostam nos Estados Unidos?|3
但|dan4|mas; porém|我喜欢唱歌，但我更喜欢跳舞。|wǒ xǐhuan chànggē, dàn wǒ gèng xǐhuan tiàowǔ.|Eu gosto de cantar, mas gosto ainda mais de dançar.|3
唱歌|chang4ge1|cantar|我喜欢唱歌，但我更喜欢跳舞。|wǒ xǐhuan chànggē, dàn wǒ gèng xǐhuan tiàowǔ.|Eu gosto de cantar, mas gosto ainda mais de dançar.|3
跳舞|tiao4wu3|dançar|我喜欢唱歌，但我更喜欢跳舞。|wǒ xǐhuan chànggē, dàn wǒ gèng xǐhuan tiàowǔ.|Eu gosto de cantar, mas gosto ainda mais de dançar.|3
体育馆|ti3yu4guan3|ginásio esportivo|我去学校的体育馆打球。|wǒ qù xuéxiào de tǐyùguǎn dǎqiú.|Eu vou jogar bola no ginásio da escola.|3
市中心|shi4zhong1xin1|centro da cidade|我去市中心的游泳馆游泳。|wǒ qù shìzhōngxīn de yóuyǒngguǎn yóuyǒng.|Eu vou nadar na piscina do centro da cidade.|3
马克|ma3ke4|Mark (nome próprio)|马克喜欢打篮球。|Mǎkè xǐhuan dǎ lánqiú.|Mark gosta de jogar basquete.|4
李佳|li3jia1|Li Jia (nome próprio)|李佳喜欢跑步。|Lǐ Jiā xǐhuan pǎobù.|Li Jia gosta de correr.|4
你好|ni3hao3|olá|你好，李佳！|nǐ hǎo, Lǐ Jiā!|Olá, Li Jia!|4
啊|a|partícula de exclamação|你也在跑步啊！|nǐ yě zài pǎobù a!|Você também está correndo!|4
来|lai2|vir|我每天都来跑步。|wǒ měitiān dōu lái pǎobù.|Eu venho correr todos os dias.|4
对|dui4|certo; correto; sim|对，我喜欢运动。|duì, wǒ xǐhuan yùndòng.|Sim, eu gosto de esportes.|4
等等|deng3deng3|etcétera; e assim por diante|我喜欢篮球、棒球等等。|wǒ xǐhuan lánqiú, bàngqiú děngděng.|Eu gosto de basquete, beisebol etc.|4
游|you2|nadar (parte verbal de 游泳)|我每周游两次泳。|wǒ měizhōu yóu liǎng cì yǒng.|Eu nado duas vezes por semana.|4
泳|yong3|natação (elemento de 游泳)|我每周游两次泳。|wǒ měizhōu yóu liǎng cì yǒng.|Eu nado duas vezes por semana.|4
还是|hai2shi|ainda; mesmo assim; ou (em perguntas)|我还是喜欢打篮球。|wǒ háishi xǐhuan dǎ lánqiú.|Eu ainda prefiro jogar basquete.|5
打球|da3qiu2|jogar bola|我去学校的体育馆打球。|wǒ qù xuéxiào de tǐyùguǎn dǎqiú.|Eu vou jogar bola no ginásio da escola.|5
里|li3|dentro; em|我在公园里跑步。|wǒ zài gōngyuán lǐ pǎobù.|Eu corro no parque.|5
图书馆|tu2shu1guan3|biblioteca|我去图书馆看书。|wǒ qù túshūguǎn kànshū.|Eu vou ler na biblioteca.|6
看书|kan4shu1|ler (livros)|我去图书馆看书。|wǒ qù túshūguǎn kànshū.|Eu vou ler na biblioteca.|6
海边|hai3bian1|beira-mar; litoral|我去海边游泳。|wǒ qù hǎibiān yóuyǒng.|Eu vou nadar no mar.|6
超市|chao1shi4|supermercado|我去超市买东西。|wǒ qù chāoshì mǎi dōngxi.|Eu vou fazer compras no supermercado.|7
买|mai3|comprar|我去超市买东西。|wǒ qù chāoshì mǎi dōngxi.|Eu vou fazer compras no supermercado.|7
东西|dong1xi|coisa(s); objetos|我去超市买东西。|wǒ qù chāoshì mǎi dōngxi.|Eu vou fazer compras no supermercado.|7
香蕉|xiang1jiao1|banana|我喜欢吃香蕉。|wǒ xǐhuan chī xiāngjiāo.|Eu gosto de comer banana.|7
吃|chi1|comer|我喜欢吃香蕉。|wǒ xǐhuan chī xiāngjiāo.|Eu gosto de comer banana.|7
日记|ri4ji4|diário|这是马克的日记。|zhè shì Mǎkè de rìjì.|Este é o diário de Mark.|8
告诉|gao4su|contar; informar; dizer a alguém|老师告诉我，学汉语很有趣。|lǎoshī gàosu wǒ, xué Hànyǔ hěn yǒuqù.|O professor me disse que aprender chinês é interessante.|8
年轻|nian2qing1|jovem|我的朋友很年轻。|wǒ de péngyou hěn niánqīng.|Meu amigo é muito jovem.|8
不过|bu2guo4|porém; no entanto|我喜欢跑步，不过我更喜欢游泳。|wǒ xǐhuan pǎobù, búguò wǒ gèng xǐhuan yóuyǒng.|Eu gosto de correr, porém gosto ainda mais de nadar.|8
有时|you3shi2|às vezes|我们有时一起打麻将。|wǒmen yǒushí yìqǐ dǎ májiàng.|Às vezes jogamos mahjong juntos.|8
聚|ju4|reunir-se|朋友们聚在一起聊天。|péngyoumen jù zài yìqǐ liáotiān.|Os amigos se reúnem para conversar.|8
了解|liao3jie3|conhecer; compreender|我想了解中国人的生活。|wǒ xiǎng liǎojiě Zhōngguórén de shēnghuó.|Eu quero conhecer a vida dos chineses.|8
生活|sheng1huo2|vida; viver|我想了解中国人的生活。|wǒ xiǎng liǎojiě Zhōngguórén de shēnghuó.|Eu quero conhecer a vida dos chineses.|8
中国|zhong1guo2|China|中国的年轻人也喜欢运动。|Zhōngguó de niánqīngrén yě xǐhuan yùndòng.|Os jovens da China também gostam de esportes.|9
年轻人|nian2qing1ren2|jovem; pessoa jovem|中国的年轻人也喜欢运动。|Zhōngguó de niánqīngrén yě xǐhuan yùndòng.|Os jovens da China também gostam de esportes.|9
老师|lao3shi1|professor(a)|老师告诉我，学汉语很有趣。|lǎoshī gàosu wǒ, xué Hànyǔ hěn yǒuqù.|O professor me disse que aprender chinês é interessante.|9
汉语|han4yu3|língua chinesa; mandarim|老师告诉我，学汉语很有趣。|lǎoshī gàosu wǒ, xué Hànyǔ hěn yǒuqù.|O professor me disse que aprender chinês é interessante.|9
很|hen3|muito|我的朋友很年轻。|wǒ de péngyou hěn niánqīng.|Meu amigo é muito jovem.|9
了|le|partícula de ação concluída ou mudança|我买了两双鞋。|wǒ mǎi le liǎng shuāng xié.|Eu comprei dois pares de sapatos.|9
一|yi1|um|我买了一件衣服。|wǒ mǎi le yí jiàn yīfu.|Eu comprei uma peça de roupa.|9
件|jian4|classificador de roupas e objetos|我买了一件衣服。|wǒ mǎi le yí jiàn yīfu.|Eu comprei uma peça de roupa.|9
衣服|yi1fu|roupa(s)|我买了一件衣服。|wǒ mǎi le yí jiàn yīfu.|Eu comprei uma peça de roupa.|9
双|shuang1|par; classificador de pares|我买了两双鞋。|wǒ mǎi le liǎng shuāng xié.|Eu comprei dois pares de sapatos.|9
鞋|xie2|sapato(s)|我买了两双鞋。|wǒ mǎi le liǎng shuāng xié.|Eu comprei dois pares de sapatos.|9
有点儿|you3dian3r|um pouco|我们的爱好有点儿不一样。|wǒmen de àihào yǒudiǎnr bù yíyàng.|Nossos hobbies são um pouco diferentes.|10
不一样|bu4yi2yang4|diferente; não igual|我们的爱好有点儿不一样。|wǒmen de àihào yǒudiǎnr bù yíyàng.|Nossos hobbies são um pouco diferentes.|10
希望|xi1wang4|esperar; desejar; esperança|我希望以后可以去中国。|wǒ xīwàng yǐhòu kěyǐ qù Zhōngguó.|Eu espero poder ir à China no futuro.|10
多|duo1|muito(s); mais|我想更多地了解中国。|wǒ xiǎng gèng duō de liǎojiě Zhōngguó.|Eu quero conhecer mais a China.|10
地|de|partícula que liga um modificador ao verbo|我想更多地了解中国。|wǒ xiǎng gèng duō de liǎojiě Zhōngguó.|Eu quero conhecer mais a China.|10
苹果|ping2guo3|maçã|除了苹果，我还喜欢吃香蕉。|chúle píngguǒ, wǒ hái xǐhuan chī xiāngjiāo.|Além de maçã, também gosto de comer banana.|11
旅游|lv3you2|viajar; turismo|我喜欢旅游。|wǒ xǐhuan lǚyóu.|Eu gosto de viajar.|12
法语|fa3yu3|língua francesa; francês|除了汉语，我还会说法语。|chúle Hànyǔ, wǒ hái huì shuō Fǎyǔ.|Além do chinês, também sei falar francês.|12
羽毛球|yu3mao2qiu2|badminton|我每周打两个小时羽毛球。|wǒ měizhōu dǎ liǎng ge xiǎoshí yǔmáoqiú.|Eu jogo badminton duas horas por semana.|12
玩|wan2|brincar; jogar; divertir-se|他喜欢玩电脑。|tā xǐhuan wán diànnǎo.|Ele gosta de se divertir no computador.|13
电脑|dian4nao3|computador|他喜欢玩电脑。|tā xǐhuan wán diànnǎo.|Ele gosta de se divertir no computador.|13
歌|ge1|canção; música|我喜欢唱歌。|wǒ xǐhuan chàng gē.|Eu gosto de cantar.|13
四十|si4shi2|quarenta|我每次跑步四十分钟。|wǒ měicì pǎobù sìshí fēnzhōng.|Eu corro quarenta minutos a cada vez.|13
那|na4|aquele; então|那你喜欢什么运动？|nà nǐ xǐhuan shénme yùndòng?|Então, de qual esporte você gosta?|13
瑜伽|yu2jia1|ioga|我喜欢瑜伽。|wǒ xǐhuan yújiā.|Eu gosto de ioga.|13
中国菜|zhong1guo2cai4|comida chinesa|你最喜欢吃什么中国菜？|nǐ zuì xǐhuan chī shénme Zhōngguócài?|Qual prato chinês você mais gosta de comer?|14
害怕|hai4pa4|ter medo de|你最害怕什么？|nǐ zuì hàipà shénme?|Do que você tem mais medo?|14
语言|yu3yan2|língua; idioma|你还会说什么语言？|nǐ hái huì shuō shénme yǔyán?|Que outros idiomas você sabe falar?|14
运|yun4|transportar; elemento de 运动 (esporte)|我喜欢运动。|wǒ xǐhuan yùndòng.|Eu gosto de esportes.|15
动|dong4|mover; movimento|我喜欢运动。|wǒ xǐhuan yùndòng.|Eu gosto de esportes.|15
部|bu4|parte; seção|大部分人喜欢运动。|dàbùfen rén xǐhuan yùndòng.|A maioria das pessoas gosta de esportes.|15
足|zu2|pé; elemento de 足球 (futebol)|我喜欢踢足球。|wǒ xǐhuan tī zúqiú.|Eu gosto de jogar futebol.|15
趣|qu4|interesse; elemento de 有趣 (interessante)|游泳很有趣。|yóuyǒng hěn yǒuqù.|Nadar é interessante.|15
除|chu2|remover; excetuar; elemento de 除了|除了跑步，我还喜欢游泳。|chúle pǎobù, wǒ hái xǐhuan yóuyǒng.|Além de correr, também gosto de nadar.|15
般|ban1|tipo; espécie; elemento de 一般|我一般去公园跑步。|wǒ yìbān qù gōngyuán pǎobù.|Eu geralmente vou correr no parque.|15
园|yuan2|jardim; parque|我去公园跑步。|wǒ qù gōngyuán pǎobù.|Eu vou correr no parque.|15
日|ri4|dia; sol|这是我的日记。|zhè shì wǒ de rìjì.|Este é o meu diário.|15
告|gao4|informar; elemento de 告诉|老师告诉我，学汉语很有趣。|lǎoshī gàosu wǒ, xué Hànyǔ hěn yǒuqù.|O professor me disse que aprender chinês é interessante.|15
诉|su4|contar; elemento de 告诉 (sílaba neutra na palavra)|老师告诉我，学汉语很有趣。|lǎoshī gàosu wǒ, xué Hànyǔ hěn yǒuqù.|O professor me disse que aprender chinês é interessante.|15
'''

BOOK_ADDITIONS = {}
BOOK_EXAMPLE_PINYIN = {}
for _row in BOOK_ROWS.strip().splitlines():
    _word, _pin, _pt, _ex, _ex_pin, _ex_pt, _page = _row.split('|')
    BOOK_ADDITIONS[_word] = (_pin, _pt, _ex, _ex_pt, int(_page))
    BOOK_EXAMPLE_PINYIN[_ex] = _ex_pin


# Acrescentar cartões sem alterar a segmentação ou as respostas dos antigos.
for _word, (_pin, _pt, _ex, _ex_pt, _page) in BOOK_ADDITIONS.items():
    if _word not in CARDS:
        WORD_PINYIN[_word] = _pin
        CARDS[_word] = {"word": _word, "answer": _pin,
                        "categories": [f"Livro 16 · pág. {_page}"],
                        "examples": [_ex], "occurrences": 1}
        WORD_TRANSLATIONS[_word] = _pt
    EXAMPLE_TRANSLATIONS.setdefault(_ex, _ex_pt)

# IDs estáveis: o tamanho exibido da sessão não faz parte da chave salva.
BLOCK_WORDS = {"16": list(CARDS)}
BLOCK_LABELS = {"16": "Bloco 16"}
BLOCKS = {}
SESSIONS = {}
SESSION_LABELS = {}
SESSION_BLOCK = {}
for _block, _words in BLOCK_WORDS.items():
    BLOCKS[_block] = []
    for _number, (_label, _batch) in enumerate(
            make_sessions(dict.fromkeys(_words)).items(), start=1):
        _sid = f"{_block}:{_number:02d}"
        BLOCKS[_block].append(_sid)
        SESSIONS[_sid] = _batch
        SESSION_LABELS[_sid] = _label
        SESSION_BLOCK[_sid] = _block
WORD_SESSION = {w: sid for sid, words in SESSIONS.items() for w in words}
WORD_BLOCK = {w: SESSION_BLOCK[sid] for w, sid in WORD_SESSION.items()}
assert len(WORD_SESSION) == len(CARDS)

# O próximo cartão fica elegível depois de N OUTRAS respostas avaliadas.
# Exemplo: erro na resposta 10, intervalo 3, elegível após a resposta 13.
CORRECT_INTERVALS = ((5, 10), (15, 20), (25, 50), (50, 100))
# Cada erro histórico aumenta a exigência de TODAS as etapas seguintes.
# A última faixa é de manutenção: não volta ao início após acertos.
BASE_REPETITIONS = (1, 2, 3, 4)
STATE_VERSION = 4
ERROR_INTERVAL = (3, 7)
SAVE_PATH = Path.home() / ".treino_pinyin_sessoes_progresso.json"
LEGACY_SAVE_PATH = Path.home() / ".treino_pinyin_palavras_progresso.json"

ACCENT_CHARS = {
    "a": "āáǎà", "e": "ēéěè", "i": "īíǐì",
    "o": "ōóǒò", "u": "ūúǔù", "v": "ǖǘǚǜ",
}
ACCENT_TO_BASE = {mark: (vowel, i + 1)
                  for vowel, marks in ACCENT_CHARS.items()
                  for i, mark in enumerate(marks)}


def normalize_pinyin(text: str) -> str:
    """Normaliza entradas numéricas e com diacríticos, sem ignorar tons.

    Para neutro, `5`, `0` ou nenhum dígito são equivalentes.
    Ex.: xue2xi2 -> xue2xi2; xi3huan5 -> xi3huan.
    """
    text = unicodedata.normalize("NFC", text.strip().lower())
    text = text.replace("u:", "v").replace("ü", "v")
    if not text:
        return ""

    # Para o formato numérico, não modificar números 1 a 4.
    if not any(c in ACCENT_TO_BASE for c in text):
        cleaned = re.sub(r"[\s\-_'.,!?;:，。？！、/]+", "", text)
        cleaned = re.sub(r"(?<=[a-zv])[50](?=[a-z]|$)", "", cleaned)
        return cleaned if re.fullmatch(r"[a-zv0-4]+", cleaned) else ""

    # Marcas diacríticas: cada sílaba é fechada após vogais e finais n/ng/r.
    out = []
    syllable = []
    tone = None
    for i, c in enumerate(text):
        next_c = text[i+1] if i+1 < len(text) else ""
        if c in ACCENT_TO_BASE:
            base, new_tone = ACCENT_TO_BASE[c]
            if tone is not None:
                out.extend(syllable + [str(tone)])
                syllable, tone = [], None
            syllable.append(base)
            tone = new_tone
        elif c in "abcdefghijklmnopqrstuvwxyz":
            if tone is not None and c not in "aeiouv":
                # n/ng/r finais pertencem à sílaba anterior, a menos que
                # a próxima letra seja vogal (aí já é início de sílaba).
                next_is_vowel = next_c in "aeiouvü" or next_c in ACCENT_TO_BASE
                ends_with_n = bool(syllable and syllable[-1] == "n")
                if c == "n" and not next_is_vowel:
                    pass
                elif c == "g" and ends_with_n and not next_is_vowel:
                    pass
                elif c == "r" and not next_is_vowel:
                    pass
                else:
                    out.extend(syllable + [str(tone)])
                    syllable, tone = [], None
            syllable.append(c)
        elif c in "1234":
            out.extend(syllable + ([str(tone)] if tone else []) + [c])
            syllable, tone = [], None
        elif c in "50 \t\r\n-'_.,!?;:，。？！、/":
            if syllable:
                out.extend(syllable + ([str(tone)] if tone else []))
                syllable, tone = [], None
        else:
            return ""
    out.extend(syllable + ([str(tone)] if tone else []))
    return "".join(out)


def accented_pinyin(numbered: str) -> str:
    """Exibe uma leitura adicional com sinais de tom (somente para feedback)."""
    chunks = re.findall(r"[a-zv]+[1-4]?", numbered.lower())
    pretty = []
    for chunk in chunks:
        match = re.fullmatch(r"([a-zv]+)([1-4])?", chunk)
        if not match:
            continue
        syllable, digit = match.groups()
        if digit:
            # Prioridade Hanyu Pinyin: a > e > ou > vogal final.
            if "a" in syllable:
                vowel_position = syllable.index("a")
            elif "e" in syllable:
                vowel_position = syllable.index("e")
            elif "ou" in syllable:
                vowel_position = syllable.index("o")
            else:
                vowel_position = max((j for j, x in enumerate(syllable)
                                      if x in "aeiouv"), default=-1)
            if vowel_position >= 0:
                v = syllable[vowel_position]
                syllable = (syllable[:vowel_position] +
                            ACCENT_CHARS[v][int(digit)-1] +
                            syllable[vowel_position+1:])
        pretty.append(syllable.replace("v", "ü"))
    return "".join(pretty)


# Casos com sílabas neutras NO MEIO e um nome misto chinês/latim.
# Não é correto converter "zen3meyang4" como se "me" tivesse tom 3.
PRETTY_OVERRIDES = {
    "什么时候": "shénme shíhou",
    "怎么样": "zěnme yàng",
    "会不会": "huì bu huì",
    "去不去": "qù bu qù",
    "喜欢不喜欢": "xǐhuan bu xǐhuan",
    "卡拉OK": "kǎlā OK",
}


def pretty_word(word: str) -> str:
    """Pinyin com acentos, separando corretamente sílabas neutras."""
    if word in PRETTY_OVERRIDES:
        return PRETTY_OVERRIDES[word]
    return accented_pinyin(pinyin_of(word))


def pinyin_sentence(sentence: str) -> str:
    """Romaniza a frase EXEMPLO inteira, respeitando palavras e pontuação.

    Regras ilustrativas: 不 + quarto tom se torna bú; os números cobrados
    no cartão continuam sendo os tons próprios do item de vocabulário.
    """
    if sentence in BOOK_EXAMPLE_PINYIN:
        return BOOK_EXAMPLE_PINYIN[sentence]
    punctuation = {"，": ",", "、": ",", "。": ".", "？": "?", "！": "!",
                   "；": ";", "：": ":"}
    chunks = []
    for part in re.findall(r"[^，、。？！；：]+|[，、。？！；：]", sentence):
        if part in punctuation:
            if chunks:
                chunks[-1] += punctuation[part]
            continue
        words = segment(part)
        for i, word in enumerate(words):
            if word == "不" and i + 1 < len(words):
                next_pinyin = pinyin_of(words[i + 1])
                match = re.match(r"^[a-zv]+([1-4])", next_pinyin)
                p = "bú" if match and match.group(1) == "4" else "bù"
            else:
                p = pretty_word(word)
            chunks.append(p)
    return " ".join(chunks)


def accepted_answers(word: str) -> set[str]:
    """Variantes reais da mesma palavra; NUNCA ignoramos números de tom."""
    main = CARDS[word]["answer"]
    variants = {main}
    if word == "谁":
        variants.add("shui2")   # 谁: shéi ou shuí
    return {normalize_pinyin(v) for v in variants}


def fresh_record() -> dict:
    return {"hits": 0, "misses": 0, "total_misses": 0,
            "stage": 0, "stage_repetitions": 0,
            "due": 0, "last_interval": None}


def initial_state() -> dict:
    default = next(iter(SESSIONS))
    return {"version": STATE_VERSION, "completed": 0,
            "session_counts": {sid: 0 for sid in SESSIONS},
            "cards": {w: fresh_record() for w in CARDS},
            "current": None, "graded": False, "feedback": "",
            "was_correct": False, "early": False,
            "block": SESSION_BLOCK[default], "session": default}


def repetitions_required(record: dict) -> int:
    return BASE_REPETITIONS[record["stage"]] + record["total_misses"]


def advance_stage(record: dict):
    record["stage_repetitions"] += 1
    if record["stage_repetitions"] >= repetitions_required(record):
        record["stage_repetitions"] = 0
        record["stage"] = min(record["stage"] + 1, len(CORRECT_INTERVALS) - 1)


def migrate_state(data: dict) -> dict:
    """Preserva histórico, cartão aberto e prazos ao introduzir blocos.

    v2/v3 guardavam erros acumulados, sem sequência completa de respostas.
    Conservamos esses erros como pendentes e históricos; acertos futuros
    quitam os pendentes. A etapa antiga permite reconstruir no máximo os
    acertos desde o último reinício, sem conceder promoções indevidas.
    """
    state = initial_state()
    version = data.get("version")
    if version not in (2, 3, STATE_VERSION):
        return state
    state["completed"] = max(0, int(data.get("completed", 0)))
    old_counts = data.get("session_counts", {})
    old_cards = data.get("cards", {})
    legacy_ids = {name: f"16:{i:02d}" for i, name in enumerate(LEGACY_SESSIONS, 1)}
    for old_sid, count in old_counts.items():
        sid = old_sid if version == STATE_VERSION else legacy_ids.get(old_sid)
        if sid in SESSIONS:
            state["session_counts"][sid] = max(0, int(count))
    for word, rec in state["cards"].items():
        old = old_cards.get(word)
        if not isinstance(old, dict):
            continue
        rec["hits"] = max(0, int(old.get("hits", 0)))
        rec["misses"] = max(0, int(old.get("misses", 0)))
        rec["total_misses"] = max(rec["misses"], int(old.get("total_misses", rec["misses"])))
        if version == STATE_VERSION:
            rec["stage"] = max(0, min(len(CORRECT_INTERVALS)-1, int(old.get("stage", 0))))
            rec["stage_repetitions"] = max(0, min(repetitions_required(rec)-1,
                                                   int(old.get("stage_repetitions", 0))))
            old_clock = int(old_counts.get(WORD_SESSION[word], 0))
        else:
            for _ in range(min(6, rec["hits"], max(0, int(old.get("stage", 0))))):
                advance_stage(rec)
            old_clock = (int(old_counts.get(LEGACY_WORD_SESSION.get(word), 0))
                         if version == 3 else state["completed"])
        remaining = min(CORRECT_INTERVALS[-1][1], int(old.get("due", 0)) - old_clock)
        rec["due"] = max(0, state["session_counts"][WORD_SESSION[word]] + remaining)
        last = old.get("last_interval")
        rec["last_interval"] = min(100, max(0, int(last))) if last is not None else None
    old_sid = data.get("session")
    sid = old_sid if version == STATE_VERSION else legacy_ids.get(old_sid)
    if sid in SESSIONS:
        state["session"] = sid
    current = data.get("current")
    if current in CARDS:
        state["session"] = WORD_SESSION[current]
        for key in ("current", "graded", "was_correct", "early"):
            if key in data:
                state[key] = data[key]
        if state["graded"]:
            state["feedback"] = ("✓ Correto!" if state["was_correct"]
                                 else "✗ Incorreto! Revise o pinyin e os tons.")
    state["block"] = SESSION_BLOCK[state["session"]]
    return state


def load_state() -> dict:
    source_path = SAVE_PATH if SAVE_PATH.exists() else LEGACY_SAVE_PATH
    if source_path.exists():
        try:
            return migrate_state(json.loads(source_path.read_text(encoding="utf-8")))
        except (OSError, ValueError, TypeError, KeyError, AttributeError):
            print("Aviso: progresso anterior ilegível. Nova sessão iniciada.", file=sys.stderr)
    return initial_state()


def save_state(state: dict):
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = SAVE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(SAVE_PATH)


def choose_word(state: dict, candidates: list[str], previous: str | None = None):
    """Vencidos > novos > antecipados, contando respostas só da sessão ativa."""
    if not candidates:
        return None, False
    now = state["session_counts"][state["session"]]
    recs = state["cards"]
    due = [w for w in candidates if (recs[w]["hits"] or recs[w]["misses"])
           and recs[w]["due"] <= now]
    if due:
        best_due = min(recs[w]["due"] for w in due)
        group = [w for w in due if recs[w]["due"] <= best_due + 2]
        if previous in group and len(group) > 1:
            group.remove(previous)
        weights = [1 + min(recs[w]["misses"], 10)*0.2 for w in group]
        return random.choices(group, weights=weights)[0], False
    new = [w for w in candidates if not (recs[w]["hits"] or recs[w]["misses"])]
    if new:
        if previous in new and len(new) > 1:
            new.remove(previous)
        return random.choice(new), False
    upcoming = min(recs[w]["due"] for w in candidates)
    group = [w for w in candidates if recs[w]["due"] == upcoming]
    if previous in group and len(group) > 1:
        group.remove(previous)
    return random.choice(group), True


def record_answer(state: dict, word: str, correct: bool) -> int:
    rec = state["cards"][word]
    state["completed"] += 1
    session_name = WORD_SESSION[word]
    state["session_counts"][session_name] += 1
    if correct:
        low, high = CORRECT_INTERVALS[rec["stage"]]
        rec["hits"] += 1
        rec["misses"] = max(0, rec["misses"] - 1)
        advance_stage(rec)
    else:
        low, high = ERROR_INTERVAL
        rec["misses"] += 1
        rec["total_misses"] += 1
        rec["stage"] = 0
        rec["stage_repetitions"] = 0
    delay = random.randint(low, high)
    rec["due"] = state["session_counts"][session_name] + delay
    rec["last_interval"] = delay
    return delay


class PinyinTrainer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Treino de Pinyin · Blocos e sessões")
        self.geometry("1000x810")
        self.minsize(780, 680)
        self.configure(bg="#eff3f9")
        self.data = load_state()
        self.block_var = tk.StringVar(value=BLOCK_LABELS[self.data["block"]])
        self.sessions = list(BLOCKS[self.data["block"]])
        self.session_var = tk.StringVar(value=SESSION_LABELS[self.data["session"]])
        self.input_var = tk.StringVar()
        self.feedback_var = tk.StringVar()
        self.answer_var = tk.StringVar()
        self.translation_var = tk.StringVar()
        self.example_hanzi_var = tk.StringVar()
        self.example_pinyin_var = tk.StringVar()
        self.example_translation_var = tk.StringVar()
        self.info_var = tk.StringVar()
        self.footer_var = tk.StringVar()
        self.current = self.data["current"]
        self._build_ui()
        if self.current is None or self.current not in self._filtered():
            self.data["graded"] = True
            self._next_card()
        else:
            self._render()
        self.bind("<Return>", self._on_enter)
        self.protocol("WM_DELETE_WINDOW", self._close)

    def _build_ui(self):
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("TCombobox", padding=6, font=("Arial", 10))
        style.configure("Horizontal.TProgressbar", troughcolor="#dce5f0",
                        background="#276ed1")
        # O conteúdo pode ser rolado em telas menores, sem ocultar os botões.
        scroll_shell = tk.Frame(self, bg="#eff3f9")
        scroll_shell.pack(expand=True, fill="both")
        canvas = tk.Canvas(scroll_shell, bg="#eff3f9", highlightthickness=0,
                           borderwidth=0)
        scrollbar = ttk.Scrollbar(scroll_shell, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        root = tk.Frame(canvas, bg="#eff3f9", padx=24, pady=19)
        window_id = canvas.create_window((0, 0), window=root, anchor="nw")
        root.bind("<Configure>",
                  lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self._responsive_labels = []
        canvas.bind("<Configure>",
                    lambda e: self._resize_text(canvas, window_id, e.width))
        tk.Label(root, text="Treino de Pinyin · Blocos e sessões", font=("Arial", 22, "bold"),
                 fg="#14273d", bg="#eff3f9").pack(anchor="w")
        tk.Label(root, text="Escolha o bloco e a sessão (até 100 caracteres). Use os tons: xi3huan, xue2xi2.",
                 fg="#55677f", bg="#eff3f9", font=("Arial", 11)).pack(anchor="w", pady=(3, 14))

        row = tk.Frame(root, bg="#eff3f9")
        row.pack(fill="x")
        self.stats = {}
        for key, label in (("total", "PALAVRAS"), ("seen", "ESTUDADAS"),
                           ("hits", "ACERTOS"), ("misses", "ERROS PENDENTES"),
                           ("rate", "TAXA DE ACERTO")):
            box = tk.Frame(row, bg="white", padx=11, pady=8,
                           highlightthickness=1, highlightbackground="#e0e6f0")
            box.pack(side="left", fill="both", expand=True, padx=(0, 7))
            tk.Label(box, text=label, font=("Arial", 8, "bold"),
                     fg="#73829a", bg="white").pack(anchor="w")
            stat = tk.Label(box, text="0", font=("Arial", 19, "bold"),
                            fg="#15283d", bg="white")
            stat.pack(anchor="w")
            self.stats[key] = stat

        block_row = tk.Frame(root, bg="#eff3f9")
        block_row.pack(fill="x", pady=(14, 0))
        tk.Label(block_row, text="Bloco:", bg="#eff3f9", font=("Arial", 11, "bold"),
                 fg="#23364f").pack(side="left", padx=(0, 8))
        self.block_combo = ttk.Combobox(block_row, textvariable=self.block_var,
                                        values=list(BLOCK_LABELS.values()),
                                        state="readonly", width=15)
        self.block_combo.pack(side="left")
        self.block_combo.bind("<<ComboboxSelected>>", self._block_changed)

        filter_box = tk.Frame(root, bg="#eff3f9")
        filter_box.pack(fill="x", pady=(16, 8))
        tk.Label(filter_box, text="Sessão:", bg="#eff3f9", font=("Arial", 11, "bold"),
                 fg="#23364f").pack(side="left", padx=(0, 8))
        self.session_combo = ttk.Combobox(filter_box, textvariable=self.session_var,
                                          values=[SESSION_LABELS[s] for s in self.sessions],
                                          state="readonly", width=42)
        self.session_combo.pack(side="left")
        self.session_combo.bind("<<ComboboxSelected>>", self._filter_changed)
        tk.Button(filter_box, text="◀", command=lambda: self._change_session(-1),
                  relief="flat", bg="#dfe8f5", padx=7).pack(side="left", padx=(6, 3))
        tk.Button(filter_box, text="▶", command=lambda: self._change_session(1),
                  relief="flat", bg="#dfe8f5", padx=7).pack(side="left")
        tk.Button(filter_box, text="Zerar tudo", command=self._reset,
                  relief="flat", bg="#fee6e7", fg="#a52731", padx=9, pady=6).pack(side="right", padx=(0, 8))

        panel = tk.Frame(root, bg="white", padx=24, pady=18,
                         highlightbackground="#dde6f1", highlightthickness=1)
        panel.pack(fill="both", expand=True)
        self.info_label = tk.Label(panel, textvariable=self.info_var,
                                   font=("Arial", 10), fg="#6f7e90", bg="white",
                                   justify="left", wraplength=780)
        self.info_label.pack(anchor="w")
        self.word_label = tk.Label(panel, text="", font=("Microsoft YaHei", 46),
                                   bg="white", fg="#0f2544", wraplength=730)
        self.word_label.pack(fill="x", pady=(9, 18))
        tk.Label(panel, text="Digite o pinyin NUMÉRICO (incluindo cada tom):",
                 font=("Arial", 11, "bold"), fg="#223955", bg="white").pack(anchor="w")
        self.entry = tk.Entry(panel, textvariable=self.input_var, font=("Arial", 18),
                              relief="solid", bd=1)
        self.entry.pack(fill="x", ipady=9, pady=(6, 12))
        self.feedback_label = tk.Label(panel, textvariable=self.feedback_var,
                                       font=("Arial", 11, "bold"), bg="white",
                                       fg="#137c48", anchor="w", justify="left",
                                       wraplength=770)
        self.feedback_label.pack(fill="x", pady=(0, 4))
        self.details = tk.Frame(panel, bg="#f2f7fd", padx=13, pady=10,
                                highlightbackground="#dde6f1", highlightthickness=1)
        answer_label = tk.Label(self.details, textvariable=self.answer_var,
                                font=("Arial", 12, "bold"), bg="#f2f7fd",
                                fg="#194f8b", anchor="w", justify="left")
        answer_label.pack(fill="x")
        translation_label = tk.Label(self.details, textvariable=self.translation_var,
                                     font=("Arial", 11), bg="#f2f7fd",
                                     fg="#194f8b", anchor="w", justify="left")
        translation_label.pack(fill="x", pady=(3, 8))
        tk.Label(self.details, text="EXEMPLO DE USO", font=("Arial", 9, "bold"),
                 bg="#f2f7fd", fg="#586c85", anchor="w").pack(fill="x")
        example_label = tk.Label(self.details, textvariable=self.example_hanzi_var,
                                 font=("Microsoft YaHei", 12), bg="#f2f7fd",
                                 fg="#213a58", anchor="w", justify="left")
        example_label.pack(fill="x", pady=(3, 1))
        pinyin_label = tk.Label(self.details, textvariable=self.example_pinyin_var,
                                font=("Arial", 11, "italic"), bg="#f2f7fd",
                                fg="#194f8b", anchor="w", justify="left")
        pinyin_label.pack(fill="x", pady=(2, 1))
        example_translation_label = tk.Label(
            self.details, textvariable=self.example_translation_var,
            font=("Arial", 11), bg="#f2f7fd", fg="#334d68",
            anchor="w", justify="left")
        example_translation_label.pack(fill="x", pady=(2, 0))
        self._responsive_labels.extend((answer_label, translation_label,
                                         example_label, pinyin_label,
                                         example_translation_label,
                                         self.info_label, self.word_label,
                                         self.feedback_label))
        action_row = tk.Frame(panel, bg="white")
        action_row.pack(fill="x", pady=(4, 0))
        self.check_btn = tk.Button(action_row, text="Verificar  ↵", command=self._check,
                                   bg="#276ed1", fg="white", relief="flat",
                                   font=("Arial", 11, "bold"), padx=16, pady=10)
        self.check_btn.pack(side="left", padx=(0, 8))
        self.give_up_btn = tk.Button(action_row, text="Não sei (erro)", command=self._give_up,
                                     bg="#e7edf6", fg="#354965", relief="flat",
                                     font=("Arial", 11), padx=13, pady=10)
        self.give_up_btn.pack(side="left")
        self.next_btn = tk.Button(action_row, text="Próxima palavra  →", command=self._next_card,
                                  bg="#276ed1", fg="white", relief="flat",
                                  font=("Arial", 11, "bold"), padx=16, pady=10)
        self.progress = ttk.Progressbar(root, maximum=100, value=0,
                                        style="Horizontal.TProgressbar")
        self.progress.pack(fill="x", pady=(14, 6))
        tk.Label(root, textvariable=self.footer_var, fg="#4d617c", bg="#eff3f9",
                 font=("Arial", 10), wraplength=850, justify="left").pack(anchor="w")
        tk.Label(root, text=(f"{len(CARDS)} cartões únicos · {len(BLOCKS)} bloco(s) · {len(SESSIONS)} sessões"),
                 fg="#7d899a", bg="#eff3f9", font=("Arial", 9)).pack(anchor="w", pady=(5, 0))

    def _resize_text(self, canvas: tk.Canvas, window_id: int, width: int):
        canvas.itemconfigure(window_id, width=width)
        wrap = max(280, width - 155)
        for label in self._responsive_labels:
            label.configure(wraplength=wrap)

    def _filtered(self) -> list[str]:
        return SESSIONS[self.data["session"]]

    def _stats(self):
        words = self._filtered()
        records = [self.data["cards"][w] for w in words]
        seen = sum(1 for x in records if x["hits"] or x["misses"])
        hits = sum(x["hits"] for x in records)
        misses = sum(x["misses"] for x in records)
        total_misses = sum(x["total_misses"] for x in records)
        values = {"total": len(words), "seen": seen, "hits": hits,
                  "misses": misses,
                  "rate": f"{100*hits/(hits+total_misses):.1f}%" if hits+total_misses else "—"}
        for k, val in values.items():
            self.stats[k].config(text=str(val))
        self.progress["value"] = 100*seen/len(words) if words else 0
        local_count = self.data["session_counts"][self.data["session"]]
        due = sum(1 for x in records if x["hits"]+x["misses"] > 0
                  and x["due"] <= local_count)
        chars = sum(hanzi_count(w) for w in words)
        covered_chars = sum(hanzi_count(w) for w, x in zip(words, records)
                            if x["hits"] or x["misses"])
        global_seen = sum(1 for r in self.data["cards"].values()
                          if r["hits"] or r["misses"])
        self.footer_var.set(
            f"Esta sessão: {chars} caracteres chineses · {covered_chars} vistos · "
            f"{len(words)-seen} cartões novos · {due} revisões pendentes · "
            f"{local_count} respostas locais\n"
            f"Geral: {global_seen}/{len(CARDS)} cartões vistos · "
            f"{self.data['completed']} respostas em {len(SESSIONS)} sessões"
        )

    def _next_card(self):
        if self.current is not None and not self.data["graded"]:
            return
        previous = self.current
        self.current, self.data["early"] = choose_word(
            self.data, self._filtered(), previous)
        self.data["current"] = self.current
        self.data["graded"] = False
        self.data["feedback"] = ""
        self.data["was_correct"] = False
        self.input_var.set("")
        self._render()
        save_state(self.data)

    def _render(self):
        self._stats()
        if not self.current:
            self.word_label.config(text="Sem palavras nesta sessão", font=("Arial", 19))
            self.info_var.set("Escolha outra sessão")
            self.feedback_var.set("")
            self.answer_var.set("")
            self.details.pack_forget()
            self.entry.config(state="disabled")
            self.check_btn.pack_forget()
            self.give_up_btn.pack_forget()
            self.next_btn.pack_forget()
            return
        card = CARDS[self.current]
        record = self.data["cards"][self.current]
        self.word_label.config(text=self.current, font=("Microsoft YaHei", 46))
        early = " · Revisão antecipada (sem itens disponíveis)" if self.data["early"] else ""
        self.info_var.set(f"{record['hits']} acerto(s) · {record['misses']} erro(s) pendente(s) nesta palavra" + early)
        self.check_btn.pack_forget()
        self.give_up_btn.pack_forget()
        self.next_btn.pack_forget()
        if self.data["graded"]:
            self.entry.config(state="disabled")
            self.feedback_var.set(self.data["feedback"])
            self.feedback_label.config(fg="#137c48" if self.data["was_correct"] else "#b33434")
            example = card["examples"][0]
            self.answer_var.set(
                f"Resposta: {card['answer']}    ({pretty_word(self.current)})")
            self.translation_var.set(f"Tradução: {WORD_TRANSLATIONS[self.current]}")
            self.example_hanzi_var.set(example)
            self.example_pinyin_var.set(f"Pinyin: {pinyin_sentence(example)}")
            self.example_translation_var.set(
                f"Tradução: {EXAMPLE_TRANSLATIONS[example]}")
            self.details.pack(fill="x", pady=(0, 10), before=self.check_btn.master)
            self.next_btn.pack(side="left")
            self.next_btn.focus_set()
        else:
            self.entry.config(state="normal")
            self.feedback_var.set("")
            self.answer_var.set("")
            self.details.pack_forget()
            self.check_btn.pack(side="left", padx=(0, 8))
            self.give_up_btn.pack(side="left")
            self.entry.focus_set()

    def _grade(self, correct):
        if self.current is None or self.data["graded"]:
            return
        record_answer(self.data, self.current, correct)
        self.data["graded"] = True
        self.data["was_correct"] = correct
        if correct:
            self.data["feedback"] = "✓ Correto!"
        else:
            self.data["feedback"] = "✗ Incorreto! Revise o pinyin e os tons."
        self._render()
        save_state(self.data)

    def _check(self):
        if self.current is None or self.data["graded"]:
            return
        raw = self.input_var.get().strip()
        if not raw:
            messagebox.showinfo("Resposta vazia", "Digite o pinyin numérico ou clique em 'Não sei'.")
            return
        answer = normalize_pinyin(raw)
        if not answer:
            messagebox.showwarning("Entrada inválida", "Use pinyin com letras e números 1–4 (5 opcional para neutro).")
            return
        self._grade(answer in accepted_answers(self.current))

    def _give_up(self):
        self._grade(False)

    def _on_enter(self, _event=None):
        if self.data["graded"]:
            self._next_card()
        else:
            self._check()

    def _change_session(self, delta: int):
        current = self.sessions.index(self.data["session"])
        new_idx = max(0, min(len(self.sessions)-1, current + delta))
        if new_idx != current:
            self.session_var.set(SESSION_LABELS[self.sessions[new_idx]])
            self._filter_changed()

    def _block_changed(self, _event=None):
        block = next(b for b, label in BLOCK_LABELS.items() if label == self.block_var.get())
        self.data["block"] = block
        self.sessions = list(BLOCKS[block])
        self.session_combo.configure(values=[SESSION_LABELS[s] for s in self.sessions])
        self.session_var.set(SESSION_LABELS[self.sessions[0]])
        self._filter_changed()

    def _filter_changed(self, _event=None):
        self.data["session"] = next(s for s in self.sessions
                                    if SESSION_LABELS[s] == self.session_var.get())
        self.data["block"] = SESSION_BLOCK[self.data["session"]]
        if self.current is None or self.current not in self._filtered():
            self.data["graded"] = True
            self._next_card()
        else:
            self._render()
            save_state(self.data)

    def _reset(self):
        if not messagebox.askyesno("Zerar progresso", "Apagar o histórico de acertos, erros e revisões de TODAS as sessões?"):
            return
        session = self.data["session"]
        self.data = initial_state()
        self.data["session"] = session
        self.data["block"] = SESSION_BLOCK[session]
        self.current = None
        self.data["graded"] = True
        self._next_card()

    def _close(self):
        save_state(self.data)
        self.destroy()


def test_logic():
    assert len(CARDS) > 150, f"Poucas palavras: {len(CARDS)}"
    assert set(CARDS) == set(WORD_TRANSLATIONS), (
        "Palavras sem tradução: " + str(set(CARDS) - set(WORD_TRANSLATIONS)))
    assert {c["examples"][0] for c in CARDS.values()} <= set(EXAMPLE_TRANSLATIONS), (
        "Exemplos sem tradução: " + str({c["examples"][0] for c in CARDS.values()} - set(EXAMPLE_TRANSLATIONS)))
    assert pinyin_sentence("我没去公园跑步。") == "wǒ méi qù gōngyuán pǎobù."
    assert pinyin_sentence("她不会打网球。") == "tā búhuì dǎ wǎngqiú."
    assert pinyin_sentence("他不喜欢游泳。") == "tā bù xǐhuan yóuyǒng."
    assert pretty_word("什么时候") == "shénme shíhou"
    assert pretty_word("怎么样") == "zěnme yàng"
    assert sum(x["occurrences"] for x in CARDS.values()) == (
        TOTAL_TOKENS + len(SLIDE_ADDITIONS) + len(CARDS) - len(ORIGINAL_WORDS))
    assert all(card["answer"] for card in CARDS.values())
    # Verifica que a normalização NÃO perde os tons.
    assert normalize_pinyin("xue2xi2") == "xue2xi2"
    assert normalize_pinyin("xue3xi2") != normalize_pinyin("xue2xi2")
    assert normalize_pinyin("xuéxí") == "xue2xi2"
    assert normalize_pinyin("peng2you5") == "peng2you"
    assert normalize_pinyin("xi3huan") == "xi3huan"
    assert normalize_pinyin("xǐhuan") == "xi3huan"
    assert accepted_answers("喜欢") == {"xi3huan"}
    assert "xi2huan" not in accepted_answers("喜欢")
    assert accepted_answers("会不会") == {"hui4buhui4"}
    assert "hui4bu4hui4" not in accepted_answers("会不会")
    assert CARDS["游泳"]["answer"] == "you2yong3"
    assert CARDS["不会"]["answer"] == "bu2hui4"
    assert CARDS["谁"]["answer"] == "shei2"
    assert CARDS["一样"]["answer"] == "yi2yang4"
    # Progressão sem erros: 1, 2, 3, 4 ocorrências e manutenção em 50–100.
    for errors in (0, 1, 2, 5):
        state = initial_state()
        word = "喜欢"
        for _ in range(errors):
            assert 3 <= record_answer(state, word, False) <= 7
        ranges = [interval for stage, interval in enumerate(CORRECT_INTERVALS)
                  for _ in range(BASE_REPETITIONS[stage] + errors)]
        ranges += [(50, 100)] * 12
        for turn, (lo, hi) in enumerate(ranges, 1):
            prev = state["session_counts"][WORD_SESSION[word]]
            delay = record_answer(state, word, True)
            rec = state["cards"][word]
            assert lo <= delay <= hi, (errors, turn, delay, lo, hi)
            assert rec["due"] == prev + 1 + delay
            assert rec["misses"] == max(0, errors - turn)
            assert rec["total_misses"] == errors
        record_answer(state, word, False)
        assert state["cards"][word]["stage"] == 0
        assert state["cards"][word]["stage_repetitions"] == 0
        assert state["cards"][word]["total_misses"] == errors + 1
    assert set(ORIGINAL_WORDS) <= set(CARDS)
    assert all(WORD_BLOCK[w] == "16" for w in CARDS)
    for word in BOOK_ADDITIONS:
        assert word in CARDS
        assert pinyin_sentence(CARDS[word]["examples"][0])
    for word, card in CARDS.items():
        assert normalize_pinyin(card["answer"]) in accepted_answers(word)
        assert WORD_TRANSLATIONS[word] and EXAMPLE_TRANSLATIONS[card["examples"][0]]
    assert migrate_state(state) == state
    assert len(choose_word(initial_state(), list(CARDS))[0]) >= 1
    assert all(not row["missing"] for row in SLIDE_COVERAGE)
    assert len(SLIDE_COVERAGE) >= 50
    assert sum(len(words) for words in SESSIONS.values()) == len(CARDS)
    assert sum(hanzi_count(w) for words in SESSIONS.values() for w in words) == sum(hanzi_count(w) for w in CARDS)
    assert all(sum(hanzi_count(w) for w in words) == 100 for words in list(SESSIONS.values())[:-1])
    assert all(0 < sum(hanzi_count(w) for w in words) <= 100 for words in SESSIONS.values())
    for word in SLIDE_ADDITIONS:
        assert word in CARDS and word in WORD_SESSION
        assert word in WORD_TRANSLATIONS and EXAMPLE_TRANSLATIONS[CARDS[word]["examples"][0]]
    assert normalize_pinyin("da4bu4fen") == "da4bu4fen"
    assert "da4bu4fen4" not in accepted_answers("大部分")  # fiel ao slide (tom neutro)
    # Turnos de uma outra sessão NÃO adiantam as revisões desta.
    if len(SESSIONS) >= 2:
        first, second = list(SESSIONS)[:2]
        state2 = initial_state()
        a, b = SESSIONS[first][0], SESSIONS[second][0]
        record_answer(state2, a, False)
        due_before = state2["cards"][a]["due"]
        for _ in range(15):
            record_answer(state2, b, True)
        assert state2["cards"][a]["due"] == due_before
        assert state2["session_counts"][first] == 1
        assert state2["session_counts"][second] == 15
    print(f"TESTES OK | {TOTAL_SENTENCES} frases fonte | {TOTAL_TOKENS} tokens originais | "
          f"{len(CARDS)} cartões únicos | {len(SESSIONS)} sessões | "
          f"{len(CARDS) - len(ORIGINAL_WORDS)} cartões novos do livro")
    print("SESSÕES:", [(n, sum(hanzi_count(w) for w in words)) for n,words in SESSIONS.items()])
    print("Exemplos:", {w: CARDS[w]["answer"] for w in
                         ("喜欢", "游泳", "打", "篮球", "不会", "会不会", "朋友")})


def main():
    if "--self-test" in sys.argv:
        test_logic()
        return
    app = PinyinTrainer()
    app.mainloop()


if __name__ == "__main__":
    main()

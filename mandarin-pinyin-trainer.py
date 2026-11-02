#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Treino de vocabulário em Hanyu Pinyin com números e repetição espaçada.

Funciona com Python 3.9+ e tkinter da biblioteca padrão.
Cada cartão corresponde a uma PALAVRA/UNIDADE de vocabulário, não a uma frase.
O banco combina as frases do estudante, os slides e os livros das aulas 16, 17, 18, 19 e 20.
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

# Preservar a ordem e os IDs do Bloco 16 mantém todas as sessões existentes.
BLOCK16_WORDS = list(CARDS)

# Aula 17: vocabulário conferido nas páginas visíveis do livro e dos slides.
# Os exemplos são frases curtas do material ou adaptações didáticas em português.
# As instruções dos exercícios são conteúdo da fonte, não comandos do aplicativo.
LESSON17_EXAMPLE_ROWS = '''
calligraphy|我最近在学书法。|wǒ zuìjìn zài xué shūfǎ.|Ultimamente estou aprendendo caligrafia.
difficult|书法很难，但是我学得还可以。|shūfǎ hěn nán, dànshì wǒ xué de hái kěyǐ.|Caligrafia é difícil, mas estou aprendendo razoavelmente bem.
practice|我经常听着音乐练书法。|wǒ jīngcháng tīng zhe yīnyuè liàn shūfǎ.|Costumo praticar caligrafia enquanto ouço música.
great|真好，我们下次可以一起写。|zhēn hǎo, wǒmen xiàcì kěyǐ yìqǐ xiě.|Que bom! Da próxima vez podemos escrever juntos.
western|我在学做西餐，做得也不错。|wǒ zài xué zuò xīcān, zuò de yě búcuò.|Estou aprendendo a preparar comida ocidental e estou me saindo bem.
photo|这是朋友给我拍的照片。|zhè shì péngyou gěi wǒ pāi de zhàopiàn.|Esta é a foto que meu amigo tirou de mim.
steak|我当时正看着菜谱做牛排呢。|wǒ dāngshí zhèng kàn zhe càipǔ zuò niúpái ne.|Naquele momento eu estava preparando um bife enquanto consultava a receita.
sure|哇，肯定很好吃吧？|wā, kěndìng hěn hǎochī ba?|Uau, deve estar muito gostoso, não é?
happy|挺好吃的，我们吃得很开心。|tǐng hǎochī de, wǒmen chī de hěn kāixīn.|Estava bem gostoso; ficamos muito felizes com a refeição.
taste|什么时候能尝尝你的手艺？|shénme shíhou néng chángchang nǐ de shǒuyì?|Quando poderemos experimentar sua comida?
guest|这个周末来我家做客吧，我给大家做牛排。|zhè ge zhōumò lái wǒ jiā zuòkè ba, wǒ gěi dàjiā zuò niúpái.|Venham me visitar em casa neste fim de semana; vou preparar bifes para todos.
tv|电视开着，窗也开着。|diànshì kāi zhe, chuāng yě kāi zhe.|A televisão está ligada e a janela também está aberta.
wall|墙上挂着一张全家福。|qiáng shàng guà zhe yì zhāng quánjiāfú.|Há uma foto de família pendurada na parede.
lounge|客厅里摆着沙发和桌子。|kètīng lǐ bǎi zhe shāfā hé zhuōzi.|Há um sofá e uma mesa na sala de estar.
neat|桌子上整整齐齐地放着书和毛笔。|zhuōzi shàng zhěngzhěngqíqí de fàng zhe shū hé máobǐ.|Os livros e os pincéis de caligrafia estão bem arrumados sobre a mesa.
writing|她在椅子上坐着，正在写书法。|tā zài yǐzi shàng zuò zhe, zhèngzài xiě shūfǎ.|Ela está sentada na cadeira, escrevendo caligrafia.
husband|她的丈夫在客厅里喝着咖啡看电视。|tā de zhàngfu zài kètīng lǐ hē zhe kāfēi kàn diànshì.|O marido dela está na sala assistindo à televisão enquanto toma café.
toy|杰克在地板上坐着玩玩具。|Jiékè zài dìbǎn shàng zuò zhe wán wánjù.|Jack está sentado no chão brincando com brinquedos.
room|丽莎在自己的房间里听音乐。|Lìshā zài zìjǐ de fángjiān lǐ tīng yīnyuè.|Lisa está ouvindo música em seu próprio quarto.
dog|小狗在窗台上啃着骨头。|xiǎo gǒu zài chuāngtái shàng kěn zhe gǔtou.|O cachorrinho está roendo um osso no peitoril da janela.
news|他在客厅喝着茶看报纸。|tā zài kètīng hē zhe chá kàn bàozhǐ.|Ele está lendo o jornal na sala enquanto toma chá.
dictionary|桌子上放着汉语词典。|zhuōzi shàng fàng zhe Hànyǔ cídiǎn.|Há um dicionário de chinês sobre a mesa.
wear|她穿得很少。|tā chuān de hěn shǎo.|Ela está usando pouca roupa.
light|他开着灯睡觉。|tā kāi zhe dēng shuìjiào.|Ele dorme com a luz acesa.
picture|墙上挂着一幅画。|qiáng shàng guà zhe yì fú huà.|Há um quadro pendurado na parede.
recording|我听着录音学汉语。|wǒ tīng zhe lùyīn xué Hànyǔ.|Eu estudo chinês ouvindo uma gravação.
child|椅子上坐着一个小孩子。|yǐzi shàng zuò zhe yí ge xiǎo háizi.|Há uma criança sentada na cadeira.
greeting|好久不见，你最近怎么样？|hǎojiǔ bújiàn, nǐ zuìjìn zěnme yàng?|Há quanto tempo! Como você tem passado?
busy|我最近非常忙。|wǒ zuìjìn fēicháng máng.|Ultimamente estou muito ocupado.
doing|你最近在干什么呢？|nǐ zuìjìn zài gàn shénme ne?|O que você tem feito ultimamente?
fluent|我说中文说得很流利。|wǒ shuō Zhōngwén shuō de hěn liúlì.|Eu falo chinês com muita fluência.
cooking|她看着菜谱做饭。|tā kàn zhe càipǔ zuòfàn.|Ela cozinha enquanto consulta a receita.
chinese_food|我最近在学做中国菜。|wǒ zuìjìn zài xué zuò Zhōngguócài.|Ultimamente estou aprendendo a preparar comida chinesa.
early|他睡觉得早，她睡觉得晚。|tā shuìjiào de zǎo, tā shuìjiào de wǎn.|Ele vai dormir cedo; ela vai dormir tarde.
wake|周末你起得早吗？|zhōumò nǐ qǐ de zǎo ma?|Você se levanta cedo no fim de semana?
run|我跑得不快。|wǒ pǎo de bú kuài.|Eu não corro rápido.
hanzi|你汉字写得怎么样？|nǐ Hànzì xiě de zěnme yàng?|Como você escreve os caracteres chineses?
sing|我唱得不太好。|wǒ chàng de bú tài hǎo.|Eu não canto muito bem.
cat|猫在沙发上。|māo zài shāfā shàng.|O gato está no sofá.
window|窗户开着。|chuānghu kāi zhe.|A janela está aberta.
chat|他们在客厅聊天儿。|tāmen zài kètīng liáotiānr.|Eles estão conversando na sala.
milk|他喝着牛奶看书。|tā hē zhe niúnǎi kànshū.|Ele lê enquanto toma leite.
durian|我喜欢吃榴莲。|wǒ xǐhuan chī liúlián.|Eu gosto de comer durião.
door|门开着。|mén kāi zhe.|A porta está aberta.
hello|嗨，艾米丽！|hāi, Àimǐlì!|Oi, Emily!
haoming|王浩明在学做西餐。|Wáng Hàomíng zài xué zuò xīcān.|Wang Haoming está aprendendo a preparar comida ocidental.
mark|马克听着音乐。|Mǎkè tīng zhe yīnyuè.|Mark está ouvindo música.
polite|您好，老师！|nín hǎo, lǎoshī!|Olá, professor!
swim|我会游泳，游得很好。|wǒ huì yóuyǒng, yóu de hěn hǎo.|Eu sei nadar e nado muito bem.
dance|她听着音乐跳舞。|tā tīng zhe yīnyuè tiàowǔ.|Ela dança enquanto ouve música.
walk|他听着音乐散步。|tā tīng zhe yīnyuè sànbù.|Ele caminha enquanto ouve música.
mahjong|你打麻将打得怎么样？|nǐ dǎ májiàng dǎ de zěnme yàng?|Como você joga mahjong?
fine|我很好。|wǒ hěn hǎo.|Eu estou bem.
bad|我学得不好。|wǒ xué de bù hǎo.|Eu não estou aprendendo bem.
much|他吃得多，我吃得少。|tā chī de duō, wǒ chī de shǎo.|Ele come muito; eu como pouco.
song|你会唱中文歌吗？|nǐ huì chàng Zhōngwén gē ma?|Você sabe cantar músicas em chinês?
piano|你会弹钢琴吗？|nǐ huì tán gāngqín ma?|Você sabe tocar piano?
basketball|你会打篮球吗？打得怎么样？|nǐ huì dǎ lánqiú ma? dǎ de zěnme yàng?|Você sabe jogar basquete? Como você joga?
'''

LESSON17_EXAMPLES = {}
for _line in LESSON17_EXAMPLE_ROWS.strip().splitlines():
    _key, _hanzi, _pin, _pt = _line.split('|')
    LESSON17_EXAMPLES[_key] = (_hanzi, _pin, _pt)

# Palavra | sílabas com tons (5 = neutro) | tradução | exemplo | fonte/página PDF
LESSON17_ROWS = '''
书法|shu1 fa3|caligrafia chinesa|calligraphy|Livro 17 p.2; Aula 17.1 p.3
难|nan2|difícil|difficult|Livro 17 p.2
但是|dan4 shi4|mas; porém|difficult|Livro 17 p.2
经常|jing1 chang2|frequentemente; com frequência|practice|Livro 17 p.2; Aula 17.1 p.11
练|lian4|praticar; treinar|practice|Livro 17 p.2; Aula 17.1 p.3
真好|zhen1 hao3|muito bom; que bom|great|Livro 17 p.2
做|zuo4|fazer; preparar (comida)|western|Livro 17 p.2; Aula 17.1 p.4
西餐|xi1 can1|comida ocidental|western|Livro 17 p.2; Aula 17.1 p.4
拍|pai1|tirar (fotografia); bater levemente|photo|Livro 17 p.2; Aula 17.1 p.4
照片|zhao4 pian4|fotografia; foto|photo|Livro 17 p.2; Aula 17.1 p.4
当时|dang1 shi2|naquele momento; naquela época|steak|Livro 17 p.2
菜谱|cai4 pu3|receita; livro de receitas|steak|Livro 17 p.2; Aula 17.1 p.11
牛排|niu2 pai2|bife de carne bovina|steak|Livro 17 p.2
肯定|ken3 ding4|certamente; com certeza|sure|Livro 17 p.2
开心|kai1 xin1|feliz; contente|happy|Livro 17 p.2
尝尝|chang2 chang5|provar; experimentar um pouco|taste|Livro 17 p.2
手艺|shou3 yi4|habilidade manual; habilidade culinária|taste|Livro 17 p.2
做客|zuo4 ke4|visitar alguém como convidado|guest|Livro 17 p.2
电视|dian4 shi4|televisão|tv|Livro 17 p.8; Aula 17.2 p.6
窗|chuang1|janela|tv|Livro 17 p.8; Aula 17.2 p.6
开|kai1|abrir; ligar|tv|Livro 17 p.8; Aula 17.2 p.6
墙|qiang2|parede|wall|Livro 17 p.8; Aula 17.2 p.3
张|zhang1|classificador de fotos, folhas e objetos planos|wall|Livro 17 p.8; Aula 17.2 p.3
全家福|quan2 jia1 fu2|foto de família|wall|Livro 17 p.8; Aula 17.2 p.3
客厅|ke4 ting1|sala de estar|lounge|Livro 17 p.8; Aula 17.2 p.2
摆|bai3|colocar; dispor; arrumar|lounge|Livro 17 p.8; Aula 17.2 p.4
整整齐齐|zheng3 zheng3 qi2 qi2|bem arrumado; em perfeita ordem|neat|Livro 17 p.8
毛笔|mao2 bi3|pincel de caligrafia|neat|Livro 17 p.8; Aula 17.2 p.5
正在|zheng4 zai4|estar fazendo algo neste momento|writing|Livro 17 p.8
丈夫|zhang4 fu5|marido|husband|Livro 17 p.8
玩具|wan2 ju4|brinquedo|toy|Livro 17 p.8
音乐|yin1 yue4|música|practice|Livro 17 p.8; Aula 17.1 p.4
狗|gou3|cachorro; cão|dog|Livro 17 p.8
窗台|chuang1 tai2|peitoril da janela|dog|Livro 17 p.8; Aula 17.2 p.2
啃|ken3|roer; mordiscar|dog|Livro 17 p.8
骨头|gu3 tou5|osso|dog|Livro 17 p.8
报纸|bao4 zhi3|jornal|news|Livro 17 p.17
词典|ci2 dian3|dicionário|dictionary|Livro 17 p.17
穿|chuan1|vestir; usar (roupa)|wear|Livro 17 p.17
灯|deng1|luz; lâmpada|light|Livro 17 p.17
幅|fu2|classificador de pinturas e quadros|picture|Livro 17 p.17
录音|lu4 yin1|gravação de áudio; gravar áudio|recording|Livro 17 p.17
小孩子|xiao3 hai2 zi5|criança|child|Livro 17 p.17
最近|zui4 jin4|recentemente; ultimamente|calligraphy|Livro 17 p.17; Aula 17.1 p.2
门|men2|porta|door|Livro 17 p.1,11
桌子|zhuo1 zi5|mesa|lounge|Livro 17 p.1; Aula 17.2 p.2
椅子|yi3 zi5|cadeira|writing|Livro 17 p.1; Aula 17.2 p.2
沙发|sha1 fa1|sofá|lounge|Livro 17 p.1; Aula 17.2 p.4
地板|di4 ban3|piso; chão|toy|Livro 17 p.1; Aula 17.2 p.2
得|de5|partícula que liga o verbo à avaliação da ação|difficult|Livro 17 p.3; Aula 17.1 p.7
着|zhe5|partícula que indica ação ou estado em continuidade|practice|Livro 17 p.3; Aula 17.1 p.11
听|ting1|ouvir; escutar|practice|Livro 17 p.3; Aula 17.1 p.4
呢|ne5|partícula de pergunta ou de ação em curso|doing|Livro 17 p.3,4; Aula 17.1 p.5
好久不见|hao3 jiu3 bu2 jian4|há quanto tempo; quanto tempo sem nos ver|greeting|Livro 17 p.4; Aula 17.1 p.2
好|hao3|bom; bem|fine|Livro 17 p.4; Aula 17.1 p.2
还可以|hai2 ke3 yi3|razoável; até que vai bem|difficult|Livro 17 p.4; Aula 17.1 p.7
下次|xia4 ci4|próxima vez|great|Livro 17 p.4
写|xie3|escrever|great|Livro 17 p.4
干|gan4|fazer; ocupar-se de uma atividade|doing|Livro 17 p.4; Aula 17.1 p.5
不错|bu2 cuo4|bom; nada mal|western|Livro 17 p.3,4
给|gei3|dar; para; em benefício de|photo|Livro 17 p.4
正|zheng4|justamente; estar em pleno ato de|steak|Livro 17 p.4
嗨|hai1|oi; olá|hello|Livro 17 p.4
哇|wa1|uau; nossa (surpresa)|sure|Livro 17 p.5
好吃|hao3 chi1|gostoso; delicioso|sure|Livro 17 p.5
吧|ba5|partícula de sugestão ou suposição|sure|Livro 17 p.5
挺|ting3|bastante; bem (intensidade)|happy|Livro 17 p.5
能|neng2|poder; conseguir; ser capaz de|taste|Livro 17 p.5
睡觉|shui4 jiao4|dormir|early|Livro 17 p.6
早|zao3|cedo|early|Livro 17 p.6
晚|wan3|tarde (horário)|early|Livro 17 p.6
少|shao3|pouco; poucos|wear|Livro 17 p.6
挂|gua4|pendurar; estar pendurado|wall|Livro 17 p.9; Aula 17.2 p.3
放|fang4|colocar; pôr|neat|Livro 17 p.10; Aula 17.2 p.5
书|shu1|livro|neat|Livro 17 p.10; Aula 17.2 p.5
坐|zuo4|sentar; estar sentado|writing|Livro 17 p.10
喝|he1|beber|husband|Livro 17 p.9,10
茶|cha2|chá|news|Livro 17 p.9
咖啡|ka1 fei1|café|husband|Livro 17 p.10
自己|zi4 ji3|si mesmo; próprio|room|Livro 17 p.10
房间|fang2 jian1|quarto; cômodo|room|Livro 17 p.10
小|xiao3|pequeno|dog|Livro 17 p.10
上|shang4|sobre; em cima de|wall|Livro 17 p.9; Aula 17.2 p.3
您好|nin2 hao3|olá (forma respeitosa)|polite|Livro 17 p.12
画|hua4|pintura; quadro; desenhar|picture|Livro 17 p.12
起|qi3|levantar-se; erguer-se|wake|Livro 17 p.13
跑|pao3|correr|run|Livro 17 p.13
快|kuai4|rápido; depressa|run|Livro 17 p.13
汉字|han4 zi4|caracteres chineses|hanzi|Livro 17 p.13
猫|mao1|gato|cat|Livro 17 p.14
窗户|chuang1 hu5|janela|window|Livro 17 p.14
聊天儿|liao2 tian1 r|conversar; bater papo (com erhua)|chat|Livro 17 p.14
牛奶|niu2 nai3|leite|milk|Livro 17 p.14 (exercício de pinyin)
榴莲|liu2 lian2|durião (fruta)|durian|Livro 17 p.14 (exercício de pinyin)
忙|mang2|ocupado|busy|Aula 17.1 p.2
非常|fei1 chang2|muito; extremamente|busy|Aula 17.1 p.2
流利|liu2 li4|fluente; com fluência|fluent|Aula 17.1 p.8
做饭|zuo4 fan4|cozinhar; preparar uma refeição|cooking|Aula 17.1 p.11
王浩明|wang2 hao4 ming2|Wang Haoming (nome próprio)|haoming|Livro 17 p.4
艾米丽|ai4 mi3 li4|Emily (nome próprio)|hello|Livro 17 p.4
杰克|jie2 ke4|Jack (nome próprio)|toy|Livro 17 p.10
丽莎|li4 sha1|Lisa (nome próprio)|room|Livro 17 p.10
近|jin4|perto; recente; elemento de 最近|calligraphy|Livro 17 p.15
样|yang4|modo; aparência; elemento de 怎么样|greeting|Livro 17 p.15
法|fa3|método; elemento de 书法|calligraphy|Livro 17 p.15
经|jing1|elemento de 经常 (frequentemente)|practice|Livro 17 p.15
常|chang2|frequente; elemento de 经常|practice|Livro 17 p.15
音|yin1|som; elemento de 音乐|practice|Livro 17 p.15
乐|yue4|música (leitura em 音乐)|practice|Livro 17 p.15
西|xi1|oeste; ocidental|western|Livro 17 p.15
餐|can1|refeição|western|Livro 17 p.15
学|xue2|aprender; estudar|calligraphy|Livro 17 p.4; Aula 17.1 p.3
中文|zhong1 wen2|língua chinesa; chinês|fluent|Aula 17.1 p.8
汉语|han4 yu3|língua chinesa; mandarim|recording|Livro 17 p.12
中国菜|zhong1 guo2 cai4|comida chinesa|chinese_food|Aula 17.1 p.5
怎么样|zen3 me5 yang4|como; de que maneira; como vai|greeting|Livro 17 p.4; Aula 17.1 p.2
说|shuo1|falar; dizer|fluent|Livro 17 p.13; Aula 17.1 p.8
游泳|you2 yong3|nadar; natação|swim|Livro 17 p.3
游|you2|nadar (verbo em 游泳)|swim|Livro 17 p.3
散步|san4 bu4|caminhar; passear|walk|Aula 17.1 p.11
麻将|ma2 jiang4|mahjong|mahjong|Aula 17.1 p.9
打|da3|jogar; praticar (esporte ou jogo)|mahjong|Aula 17.1 p.9
跳舞|tiao4 wu3|dançar|dance|Livro 17 p.12
玩|wan2|brincar; jogar|toy|Livro 17 p.10
看书|kan4 shu1|ler (livros)|milk|Livro 17 p.10
唱|chang4|cantar|sing|Livro 17 p.13
吃|chi1|comer|happy|Livro 17 p.5
多|duo1|muito; muitos|much|Livro 17 p.6
里|li3|dentro; em|lounge|Livro 17 p.9; Aula 17.2 p.4
地|de5|partícula que liga um modificador ao verbo|neat|Livro 17 p.10
一|yi1|um; uma|wall|Livro 17 p.9; Aula 17.2 p.3
和|he2|e; com|lounge|Livro 17 p.9; Aula 17.2 p.4
在|zai4|estar em; estar fazendo|calligraphy|Livro 17 p.4; Aula 17.1 p.5
我|wo3|eu|calligraphy|Livro 17 p.4; Aula 17.1 p.5
你|ni3|você|greeting|Livro 17 p.4; Aula 17.1 p.2
他|ta1|ele|news|Livro 17 p.9
她|ta1|ela|writing|Livro 17 p.10
的|de5|partícula de posse ou atribuição|photo|Livro 17 p.4
很|hen3|muito|difficult|Livro 17 p.4; Aula 17.1 p.2
也|ye3|também|tv|Livro 17 p.10; Aula 17.2 p.6
不|bu4|não|bad|Livro 17 p.7; Aula 17.1 p.7
可以|ke3 yi3|poder; ser possível|great|Livro 17 p.4
一起|yi4 qi3|junto(s)|great|Livro 17 p.4
我们|wo3 men5|nós|great|Livro 17 p.4
什么|shen2 me5|o que; que|doing|Livro 17 p.4; Aula 17.1 p.5
是|shi4|ser; estar|photo|Livro 17 p.4
这|zhe4|isto; este; esta|photo|Livro 17 p.4
朋友|peng2 you5|amigo(a)|photo|Livro 17 p.4
什么时候|shen2 me5 shi2 hou5|quando|taste|Livro 17 p.5
这个|zhe4 ge5|este; esta|guest|Livro 17 p.5
周末|zhou1 mo4|fim de semana|guest|Livro 17 p.5
来|lai2|vir|guest|Livro 17 p.5
家|jia1|casa; lar; família|guest|Livro 17 p.5
会|hui4|saber fazer; conseguir|swim|Livro 17 p.3
他们|ta1 men5|eles; elas|chat|Livro 17 p.7
马克|ma3 ke4|Mark (nome próprio)|mark|Livro 17 p.3
喜欢|xi3 huan5|gostar de|durian|Livro 17 p.4
不好|bu4 hao3|não ser bom; não ir bem|bad|Livro 17 p.7; Aula 17.1 p.7
看|kan4|ver; olhar; assistir; ler|steak|Livro 17 p.4; Aula 17.1 p.11
大家|da4 jia1|todos; todo mundo|guest|Livro 17 p.5
不太|bu2 tai4|não muito|sing|Livro 17 p.13
歌|ge1|canção; música cantada|song|Livro 17 p.14
篮球|lan2 qiu2|basquete|basketball|Livro 17 p.14
弹|tan2|tocar (instrumentos de corda ou teclado)|piano|Livro 17 p.14
钢琴|gang1 qin2|piano|piano|Livro 17 p.14
吗|ma5|partícula de pergunta (sim/não)|wake|Livro 17 p.13
个|ge5|classificador geral|child|Livro 17 p.13
'''

LESSON17_VOCAB = {}
for _line in LESSON17_ROWS.strip().splitlines():
    _word, _syllables, _pt, _example_id, _source = _line.split('|')
    if _word in LESSON17_VOCAB:
        raise ValueError(f'Palavra duplicada no Bloco 17: {_word}')
    LESSON17_VOCAB[_word] = (_syllables, _pt, _example_id, _source)


# O ID inclui a aula; a palavra visível continua sendo apenas o hanzi.
# Assim, palavras repetidas entre aulas têm treinamento independente.
BLOCK17_WORDS = []
for _word, (_syllables, _pt, _example_id, _source) in LESSON17_VOCAB.items():
    _card_id = f"17::{_word}"
    _example, _example_pin, _example_pt = LESSON17_EXAMPLES[_example_id]
    _pin = ''.join(_syllables.split()).replace('5', '')
    BLOCK17_WORDS.append(_card_id)
    WORD_PINYIN[_card_id] = _pin
    WORD_TRANSLATIONS[_card_id] = _pt
    CARDS[_card_id] = {
        "word": _word, "answer": _pin,
        "pinyin_syllables": _syllables.split(),
        "categories": [_source], "examples": [_example], "occurrences": 1,
        "example_pinyin": _example_pin, "example_translation": _example_pt,
    }
    # Não substituir traduções nem leituras de exemplos já usados no Bloco 16.
    EXAMPLE_TRANSLATIONS.setdefault(_example, _example_pt)

# IDs estáveis: o tamanho exibido da sessão não faz parte da chave salva.

# Aula 18: IDs separados preservam o progresso de palavras comuns a outras aulas.
LESSON18_CARDS = {'18::食堂': {'word': '食堂',
            'answer': 'shi2tang2',
            'pinyin_syllables': ['shi2', 'tang2'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['食堂的肉夹馍比汉堡包好吃。'],
            'occurrences': 1,
            'example_pinyin': 'shí táng deròu jiā mó bǐ hàn bǎo bāo hǎo chī',
            'example_translation': 'O roujiamo do refeitório é mais gostoso que o hambúrguer.'},
 '18::肉夹馍': {'word': '肉夹馍',
             'answer': 'rou4jia1mo2',
             'pinyin_syllables': ['rou4', 'jia1', 'mo2'],
             'categories': ['Livro 18 e aulas 18.1 / 18.2'],
             'examples': ['食堂的肉夹馍比汉堡包好吃。'],
             'occurrences': 1,
             'example_pinyin': 'shí táng deròu jiā mó bǐ hàn bǎo bāo hǎo chī',
             'example_translation': 'O roujiamo do refeitório é mais gostoso que o hambúrguer.'},
 '18::中式': {'word': '中式',
            'answer': 'zhong1shi4',
            'pinyin_syllables': ['zhong1', 'shi4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我觉得肉夹馍是中式汉堡包。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jué deròu jiā mó shì zhōng shì hàn bǎo bāo',
            'example_translation': 'Acho que o roujiamo é um hambúrguer ao estilo chinês.'},
 '18::汉堡包': {'word': '汉堡包',
             'answer': 'han4bao3bao1',
             'pinyin_syllables': ['han4', 'bao3', 'bao1'],
             'categories': ['Livro 18 e aulas 18.1 / 18.2'],
             'examples': ['食堂的肉夹馍比汉堡包好吃。'],
             'occurrences': 1,
             'example_pinyin': 'shí táng deròu jiā mó bǐ hàn bǎo bāo hǎo chī',
             'example_translation': 'O roujiamo do refeitório é mais gostoso que o hambúrguer.'},
 '18::晚餐': {'word': '晚餐',
            'answer': 'wan3can1',
            'pinyin_syllables': ['wan3', 'can1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['你经常去哪里吃晚餐？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ jīng cháng qù nǎ lǐ chī wǎn cān',
            'example_translation': 'Onde você costuma jantar?'},
 '18::外面': {'word': '外面',
            'answer': 'wai4mian4',
            'pinyin_syllables': ['wai4', 'mian4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我有时候去外面的餐厅吃饭。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ yǒu shí hou qù wài miàn de cān tīng chī fàn',
            'example_translation': 'Às vezes vou comer em um restaurante fora de casa.'},
 '18::外卖': {'word': '外卖',
            'answer': 'wai4mai4',
            'pinyin_syllables': ['wai4', 'mai4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['在中国叫外卖很方便。'],
            'occurrences': 1,
            'example_pinyin': 'zài zhōng guó jiào wài mài hěn fāng biàn',
            'example_translation': 'É muito prático pedir comida para entrega na China.'},
 '18::方便': {'word': '方便',
            'answer': 'fang1bian4',
            'pinyin_syllables': ['fang1', 'bian4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['在中国叫外卖很方便。'],
            'occurrences': 1,
            'example_pinyin': 'zài zhōng guó jiào wài mài hěn fāng biàn',
            'example_translation': 'É muito prático pedir comida para entrega na China.'},
 '18::健康': {'word': '健康',
            'answer': 'jian4kang1',
            'pinyin_syllables': ['jian4', 'kang1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['家里的饭比外卖更健康。'],
            'occurrences': 1,
            'example_pinyin': 'jiā lǐ de fàn bǐ wài mài gèng jiàn kāng',
            'example_translation': 'A comida caseira é mais saudável que a comida entregue.'},
 '18::离': {'word': '离',
           'answer': 'li2',
           'pinyin_syllables': ['li2'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['我家离学校不远，可以走路去。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jiā lí xué xiào bù yuǎn kě yǐ zǒu lù qù',
           'example_translation': 'Minha casa não fica longe da escola; dá para ir a pé.'},
 '18::走路': {'word': '走路',
            'answer': 'zou3lu4',
            'pinyin_syllables': ['zou3', 'lu4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我家离学校不远，可以走路去。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jiā lí xué xiào bù yuǎn kě yǐ zǒu lù qù',
            'example_translation': 'Minha casa não fica longe da escola; dá para ir a pé.'},
 '18::年': {'word': '年',
           'answer': 'nian2',
           'pinyin_syllables': ['nian2'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['我来上海半年多了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ lái shàng hǎi bàn nián duō le',
           'example_translation': 'Cheguei a Xangai há mais de meio ano.'},
 '18::天气': {'word': '天气',
            'answer': 'tian1qi4',
            'pinyin_syllables': ['tian1', 'qi4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['上海的天气比洛杉矶潮湿多了。'],
            'occurrences': 1,
            'example_pinyin': 'shàng hǎi de tiān qì bǐ luò shān jī cháo shī duō le',
            'example_translation': 'O clima de Xangai é muito mais úmido que o de Los Angeles.'},
 '18::潮湿': {'word': '潮湿',
            'answer': 'chao2shi1',
            'pinyin_syllables': ['chao2', 'shi1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['上海的天气比洛杉矶潮湿多了。'],
            'occurrences': 1,
            'example_pinyin': 'shàng hǎi de tiān qì bǐ luò shān jī cháo shī duō le',
            'example_translation': 'O clima de Xangai é muito mais úmido que o de Los Angeles.'},
 '18::待': {'word': '待',
           'answer': 'dai1',
           'pinyin_syllables': ['dai1'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['周末我只能待在家里。'],
           'occurrences': 1,
           'example_pinyin': 'zhōu mò wǒ zhǐ néng dāi zài jiā lǐ',
           'example_translation': 'No fim de semana só posso ficar em casa.'},
 '18::想念': {'word': '想念',
            'answer': 'xiang3nian4',
            'pinyin_syllables': ['xiang3', 'nian4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我很想念洛杉矶的阳光。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ hěn xiǎng niàn luò shān jī de yáng guāng',
            'example_translation': 'Sinto muita falta do sol de Los Angeles.'},
 '18::阳光': {'word': '阳光',
            'answer': 'yang2guang1',
            'pinyin_syllables': ['yang2', 'guang1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我很想念洛杉矶的阳光。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ hěn xiǎng niàn luò shān jī de yáng guāng',
            'example_translation': 'Sinto muita falta do sol de Los Angeles.'},
 '18::娱乐': {'word': '娱乐',
            'answer': 'yu2le4',
            'pinyin_syllables': ['yu2', 'le4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['年轻人的娱乐生活很丰富。'],
            'occurrences': 1,
            'example_pinyin': 'nián qīngrén de yú lè shēng huó hěn fēng fù',
            'example_translation': 'A vida de lazer dos jovens é bem variada.'},
 '18::丰富': {'word': '丰富',
            'answer': 'feng1fu4',
            'pinyin_syllables': ['feng1', 'fu4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['年轻人的娱乐生活很丰富。'],
            'occurrences': 1,
            'example_pinyin': 'nián qīngrén de yú lè shēng huó hěn fēng fù',
            'example_translation': 'A vida de lazer dos jovens é bem variada.'},
 '18::逛街': {'word': '逛街',
            'answer': 'guang4jie1',
            'pinyin_syllables': ['guang4', 'jie1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我喜欢逛街。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xǐ huan guàng jiē',
            'example_translation': 'Gosto de passear pelas lojas.'},
 '18::只能': {'word': '只能',
            'answer': 'zhi3neng2',
            'pinyin_syllables': ['zhi3', 'neng2'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['周末我只能待在家里。'],
            'occurrences': 1,
            'example_pinyin': 'zhōu mò wǒ zhǐ néng dāi zài jiā lǐ',
            'example_translation': 'No fim de semana só posso ficar em casa.'},
 '18::洛杉矶': {'word': '洛杉矶',
             'answer': 'luo4shan1ji1',
             'pinyin_syllables': ['luo4', 'shan1', 'ji1'],
             'categories': ['Livro 18 e aulas 18.1 / 18.2'],
             'examples': ['上海的天气比洛杉矶潮湿多了。'],
             'occurrences': 1,
             'example_pinyin': 'shàng hǎi de tiān qì bǐ luò shān jī cháo shī duō le',
             'example_translation': 'O clima de Xangai é muito mais úmido que o de Los Angeles.'},
 '18::长': {'word': '长',
           'answer': 'chang2',
           'pinyin_syllables': ['chang2'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['小红的头发比小丽的长。'],
           'occurrences': 1,
           'example_pinyin': 'xiǎo hóng de tóu fa bǐ xiǎo lì de cháng',
           'example_translation': 'O cabelo de Xiaohong é mais comprido que o de Xiaoli.'},
 '18::地方': {'word': '地方',
            'answer': 'di4fang',
            'pinyin_syllables': ['di4', 'fang5'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['他住的地方离学校很近。'],
            'occurrences': 1,
            'example_pinyin': 'tā zhù de dì fang lí xué xiào hěn jìn',
            'example_translation': 'O lugar onde ele mora fica perto da escola.'},
 '18::气温': {'word': '气温',
            'answer': 'qi4wen1',
            'pinyin_syllables': ['qi4', 'wen1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['哈尔滨的气温比海南低。'],
            'occurrences': 1,
            'example_pinyin': 'hā ěr bīn de qì wēn bǐ hǎi nán dī',
            'example_translation': 'A temperatura de Harbin é mais baixa que a de Hainan.'},
 '18::火车': {'word': '火车',
            'answer': 'huo3che1',
            'pinyin_syllables': ['huo3', 'che1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['坐火车比坐汽车快一点儿。'],
            'occurrences': 1,
            'example_pinyin': 'zuò huǒ chē bǐ zuò qì chē kuài yì diǎnr',
            'example_translation': 'Viajar de trem é um pouco mais rápido que viajar de carro.'},
 '18::住': {'word': '住',
           'answer': 'zhu4',
           'pinyin_syllables': ['zhu4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['他住的地方离学校很近。'],
           'occurrences': 1,
           'example_pinyin': 'tā zhù de dì fang lí xué xiào hěn jìn',
           'example_translation': 'O lugar onde ele mora fica perto da escola.'},
 '18::下雨': {'word': '下雨',
            'answer': 'xia4yu3',
            'pinyin_syllables': ['xia4', 'yu3'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['这里六月经常下雨。'],
            'occurrences': 1,
            'example_pinyin': 'zhè lǐ liù yuè jīng cháng xià yǔ',
            'example_translation': 'Aqui chove frequentemente em junho.'},
 '18::下雪': {'word': '下雪',
            'answer': 'xia4xue3',
            'pinyin_syllables': ['xia4', 'xue3'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['冬天经常下雪。'],
            'occurrences': 1,
            'example_pinyin': 'dōng tiān jīng cháng xià xuě',
            'example_translation': 'No inverno neva com frequência.'},
 '18::刮风': {'word': '刮风',
            'answer': 'gua1feng1',
            'pinyin_syllables': ['gua1', 'feng1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['今天刮风，还打雷。'],
            'occurrences': 1,
            'example_pinyin': 'jīn tiān guā fēng hái dǎ léi',
            'example_translation': 'Hoje está ventando e também está trovejando.'},
 '18::打雷': {'word': '打雷',
            'answer': 'da3lei2',
            'pinyin_syllables': ['da3', 'lei2'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['今天刮风，还打雷。'],
            'occurrences': 1,
            'example_pinyin': 'jīn tiān guā fēng hái dǎ léi',
            'example_translation': 'Hoje está ventando e também está trovejando.'},
 '18::晴天': {'word': '晴天',
            'answer': 'qing2tian1',
            'pinyin_syllables': ['qing2', 'tian1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['昨天是阴天，今天是晴天。'],
            'occurrences': 1,
            'example_pinyin': 'zuó tiān shì yīn tiān jīn tiān shì qíng tiān',
            'example_translation': 'Ontem estava nublado; hoje está ensolarado.'},
 '18::阴天': {'word': '阴天',
            'answer': 'yin1tian1',
            'pinyin_syllables': ['yin1', 'tian1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['昨天是阴天，今天是晴天。'],
            'occurrences': 1,
            'example_pinyin': 'zuó tiān shì yīn tiān jīn tiān shì qíng tiān',
            'example_translation': 'Ontem estava nublado; hoje está ensolarado.'},
 '18::晴': {'word': '晴',
           'answer': 'qing2',
           'pinyin_syllables': ['qing2'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['昨天是阴天，今天是晴天。'],
           'occurrences': 1,
           'example_pinyin': 'zuó tiān shì yīn tiān jīn tiān shì qíng tiān',
           'example_translation': 'Ontem estava nublado; hoje está ensolarado.'},
 '18::阴': {'word': '阴',
           'answer': 'yin1',
           'pinyin_syllables': ['yin1'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['昨天是阴天，今天是晴天。'],
           'occurrences': 1,
           'example_pinyin': 'zuó tiān shì yīn tiān jīn tiān shì qíng tiān',
           'example_translation': 'Ontem estava nublado; hoje está ensolarado.'},
 '18::俄罗斯': {'word': '俄罗斯',
             'answer': 'e2luo2si1',
             'pinyin_syllables': ['e2', 'luo2', 'si1'],
             'categories': ['Livro 18 e aulas 18.1 / 18.2'],
             'examples': ['俄罗斯比中国大。'],
             'occurrences': 1,
             'example_pinyin': 'é luó sī bǐ zhōng guó dà',
             'example_translation': 'A Rússia é maior que a China.'},
 '18::哈尔滨': {'word': '哈尔滨',
             'answer': 'ha1er3bin1',
             'pinyin_syllables': ['ha1', 'er3', 'bin1'],
             'categories': ['Livro 18 e aulas 18.1 / 18.2'],
             'examples': ['哈尔滨的气温比海南低。'],
             'occurrences': 1,
             'example_pinyin': 'hā ěr bīn de qì wēn bǐ hǎi nán dī',
             'example_translation': 'A temperatura de Harbin é mais baixa que a de Hainan.'},
 '18::热': {'word': '热',
           'answer': 're4',
           'pinyin_syllables': ['re4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['上海的夏天比北京的夏天热。'],
           'occurrences': 1,
           'example_pinyin': 'shàng hǎi de xià tiān bǐ běi jīng de xià tiānrè',
           'example_translation': 'O verão de Xangai é mais quente que o de Pequim.'},
 '18::冷': {'word': '冷',
           'answer': 'leng3',
           'pinyin_syllables': ['leng3'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['上海没有北京那么冷。'],
           'occurrences': 1,
           'example_pinyin': 'shàng hǎi méi yǒu běi jīng nà me lěng',
           'example_translation': 'Xangai não é tão fria quanto Pequim.'},
 '18::夏天': {'word': '夏天',
            'answer': 'xia4tian1',
            'pinyin_syllables': ['xia4', 'tian1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['上海的夏天比北京的夏天热。'],
            'occurrences': 1,
            'example_pinyin': 'shàng hǎi de xià tiān bǐ běi jīng de xià tiānrè',
            'example_translation': 'O verão de Xangai é mais quente que o de Pequim.'},
 '18::冬天': {'word': '冬天',
            'answer': 'dong1tian1',
            'pinyin_syllables': ['dong1', 'tian1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['冬天经常下雪。'],
            'occurrences': 1,
            'example_pinyin': 'dōng tiān jīng cháng xià xuě',
            'example_translation': 'No inverno neva com frequência.'},
 '18::开车': {'word': '开车',
            'answer': 'kai1che1',
            'pinyin_syllables': ['kai1', 'che1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['开车比走路快多了。'],
            'occurrences': 1,
            'example_pinyin': 'kāi chē bǐ zǒu lù kuài duō le',
            'example_translation': 'Ir de carro é muito mais rápido que ir a pé.'},
 '18::比': {'word': '比',
           'answer': 'bi3',
           'pinyin_syllables': ['bi3'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['食堂的肉夹馍比汉堡包好吃。'],
           'occurrences': 1,
           'example_pinyin': 'shí táng deròu jiā mó bǐ hàn bǎo bāo hǎo chī',
           'example_translation': 'O roujiamo do refeitório é mais gostoso que o hambúrguer.'},
 '18::没有': {'word': '没有',
            'answer': 'mei2you3',
            'pinyin_syllables': ['mei2', 'you3'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['上海没有北京那么冷。'],
            'occurrences': 1,
            'example_pinyin': 'shàng hǎi méi yǒu běi jīng nà me lěng',
            'example_translation': 'Xangai não é tão fria quanto Pequim.'},
 '18::那么': {'word': '那么',
            'answer': 'na4me',
            'pinyin_syllables': ['na4', 'me5'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['上海没有北京那么冷。'],
            'occurrences': 1,
            'example_pinyin': 'shàng hǎi méi yǒu běi jīng nà me lěng',
            'example_translation': 'Xangai não é tão fria quanto Pequim.'},
 '18::高': {'word': '高',
           'answer': 'gao1',
           'pinyin_syllables': ['gao1'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['我没有马克那么高。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ méi yǒu mǎ kè nà me gāo',
           'example_translation': 'Eu não sou tão alto quanto Mark.'},
 '18::远': {'word': '远',
           'answer': 'yuan3',
           'pinyin_syllables': ['yuan3'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['我家离学校不远，可以走路去。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jiā lí xué xiào bù yuǎn kě yǐ zǒu lù qù',
           'example_translation': 'Minha casa não fica longe da escola; dá para ir a pé.'},
 '18::学校': {'word': '学校',
            'answer': 'xue2xiao4',
            'pinyin_syllables': ['xue2', 'xiao4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我家离学校不远，可以走路去。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jiā lí xué xiào bù yuǎn kě yǐ zǒu lù qù',
            'example_translation': 'Minha casa não fica longe da escola; dá para ir a pé.'},
 '18::美国': {'word': '美国',
            'answer': 'mei3guo2',
            'pinyin_syllables': ['mei3', 'guo2'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['在美国叫外卖没有在中国方便。'],
            'occurrences': 1,
            'example_pinyin': 'zài měi guó jiào wài mài méi yǒu zài zhōng guó fāng biàn',
            'example_translation': 'Pedir comida nos Estados Unidos não é tão prático quanto na China.'},
 '18::中国': {'word': '中国',
            'answer': 'zhong1guo2',
            'pinyin_syllables': ['zhong1', 'guo2'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['在中国叫外卖很方便。'],
            'occurrences': 1,
            'example_pinyin': 'zài zhōng guó jiào wài mài hěn fāng biàn',
            'example_translation': 'É muito prático pedir comida para entrega na China.'},
 '18::上海': {'word': '上海',
            'answer': 'shang4hai3',
            'pinyin_syllables': ['shang4', 'hai3'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['上海的天气比洛杉矶潮湿多了。'],
            'occurrences': 1,
            'example_pinyin': 'shàng hǎi de tiān qì bǐ luò shān jī cháo shī duō le',
            'example_translation': 'O clima de Xangai é muito mais úmido que o de Los Angeles.'},
 '18::北京': {'word': '北京',
            'answer': 'bei3jing1',
            'pinyin_syllables': ['bei3', 'jing1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['上海的夏天比北京的夏天热。'],
            'occurrences': 1,
            'example_pinyin': 'shàng hǎi de xià tiān bǐ běi jīng de xià tiānrè',
            'example_translation': 'O verão de Xangai é mais quente que o de Pequim.'},
 '18::不过': {'word': '不过',
            'answer': 'bu2guo4',
            'pinyin_syllables': ['bu2', 'guo4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['汉堡包很好吃，不过我更喜欢肉夹馍。'],
            'occurrences': 1,
            'example_pinyin': 'hàn bǎo bāo hěn hǎo chī bú guò wǒ gèng xǐ huanròu jiā mó',
            'example_translation': 'Hambúrguer é gostoso, mas prefiro roujiamo.'},
 '18::哪里': {'word': '哪里',
            'answer': 'na3li3',
            'pinyin_syllables': ['na3', 'li3'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['你经常去哪里吃晚餐？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ jīng cháng qù nǎ lǐ chī wǎn cān',
            'example_translation': 'Onde você costuma jantar?'},
 '18::有时候': {'word': '有时候',
             'answer': 'you3shi2hou',
             'pinyin_syllables': ['you3', 'shi2', 'hou5'],
             'categories': ['Livro 18 e aulas 18.1 / 18.2'],
             'examples': ['我有时候去外面的餐厅吃饭。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ yǒu shí hou qù wài miàn de cān tīng chī fàn',
             'example_translation': 'Às vezes vou comer em um restaurante fora de casa.'},
 '18::餐厅': {'word': '餐厅',
            'answer': 'can1ting1',
            'pinyin_syllables': ['can1', 'ting1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我有时候去外面的餐厅吃饭。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ yǒu shí hou qù wài miàn de cān tīng chī fàn',
            'example_translation': 'Às vezes vou comer em um restaurante fora de casa.'},
 '18::吃饭': {'word': '吃饭',
            'answer': 'chi1fan4',
            'pinyin_syllables': ['chi1', 'fan4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我有时候去外面的餐厅吃饭。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ yǒu shí hou qù wài miàn de cān tīng chī fàn',
            'example_translation': 'Às vezes vou comer em um restaurante fora de casa.'},
 '18::饭': {'word': '饭',
           'answer': 'fan4',
           'pinyin_syllables': ['fan4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['家里的饭比外卖更健康。'],
           'occurrences': 1,
           'example_pinyin': 'jiā lǐ de fàn bǐ wài mài gèng jiàn kāng',
           'example_translation': 'A comida caseira é mais saudável que a comida entregue.'},
 '18::叫': {'word': '叫',
           'answer': 'jiao4',
           'pinyin_syllables': ['jiao4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['在中国叫外卖很方便。'],
           'occurrences': 1,
           'example_pinyin': 'zài zhōng guó jiào wài mài hěn fāng biàn',
           'example_translation': 'É muito prático pedir comida para entrega na China.'},
 '18::没关系': {'word': '没关系',
             'answer': 'mei2guan1xi',
             'pinyin_syllables': ['mei2', 'guan1', 'xi5'],
             'categories': ['Livro 18 e aulas 18.1 / 18.2'],
             'examples': ['没关系，你有时间，我请你到我家吃饭。'],
             'occurrences': 1,
             'example_pinyin': 'méi guān xi nǐ yǒu shí jiān wǒ qǐng nǐ dào wǒ jiā chī fàn',
             'example_translation': 'Tudo bem; quando você tiver tempo, convido você para comer na minha '
                                    'casa.'},
 '18::时间': {'word': '时间',
            'answer': 'shi2jian1',
            'pinyin_syllables': ['shi2', 'jian1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['没关系，你有时间，我请你到我家吃饭。'],
            'occurrences': 1,
            'example_pinyin': 'méi guān xi nǐ yǒu shí jiān wǒ qǐng nǐ dào wǒ jiā chī fàn',
            'example_translation': 'Tudo bem; quando você tiver tempo, convido você para comer na minha '
                                   'casa.'},
 '18::请': {'word': '请',
           'answer': 'qing3',
           'pinyin_syllables': ['qing3'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['没关系，你有时间，我请你到我家吃饭。'],
           'occurrences': 1,
           'example_pinyin': 'méi guān xi nǐ yǒu shí jiān wǒ qǐng nǐ dào wǒ jiā chī fàn',
           'example_translation': 'Tudo bem; quando você tiver tempo, convido você para comer na minha '
                                  'casa.'},
 '18::到': {'word': '到',
           'answer': 'dao4',
           'pinyin_syllables': ['dao4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['没关系，你有时间，我请你到我家吃饭。'],
           'occurrences': 1,
           'example_pinyin': 'méi guān xi nǐ yǒu shí jiān wǒ qǐng nǐ dào wǒ jiā chī fàn',
           'example_translation': 'Tudo bem; quando você tiver tempo, convido você para comer na minha '
                                  'casa.'},
 '18::地铁站': {'word': '地铁站',
             'answer': 'di4tie3zhan4',
             'pinyin_syllables': ['di4', 'tie3', 'zhan4'],
             'categories': ['Livro 18 e aulas 18.1 / 18.2'],
             'examples': ['地铁站离这儿五百米。'],
             'occurrences': 1,
             'example_pinyin': 'dì tiě zhàn lí zhèr wǔ bǎi mǐ',
             'example_translation': 'A estação de metrô fica a quinhentos metros daqui.'},
 '18::这儿': {'word': '这儿',
            'answer': 'zhe4r',
            'pinyin_syllables': ['zhe4', 'r'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['地铁站离这儿五百米。'],
            'occurrences': 1,
            'example_pinyin': 'dì tiě zhàn lí zhèr wǔ bǎi mǐ',
            'example_translation': 'A estação de metrô fica a quinhentos metros daqui.',
            'answer_variants': ['zher4']},
 '18::百': {'word': '百',
           'answer': 'bai3',
           'pinyin_syllables': ['bai3'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['地铁站离这儿五百米。'],
           'occurrences': 1,
           'example_pinyin': 'dì tiě zhàn lí zhèr wǔ bǎi mǐ',
           'example_translation': 'A estação de metrô fica a quinhentos metros daqui.'},
 '18::米': {'word': '米',
           'answer': 'mi3',
           'pinyin_syllables': ['mi3'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['地铁站离这儿五百米。'],
           'occurrences': 1,
           'example_pinyin': 'dì tiě zhàn lí zhèr wǔ bǎi mǐ',
           'example_translation': 'A estação de metrô fica a quinhentos metros daqui.'},
 '18::飞机': {'word': '飞机',
            'answer': 'fei1ji1',
            'pinyin_syllables': ['fei1', 'ji1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['飞机比火车快。'],
            'occurrences': 1,
            'example_pinyin': 'fēi jī bǐ huǒ chē kuài',
            'example_translation': 'O avião é mais rápido que o trem.'},
 '18::大': {'word': '大',
           'answer': 'da4',
           'pinyin_syllables': ['da4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['俄罗斯比中国大。'],
           'occurrences': 1,
           'example_pinyin': 'é luó sī bǐ zhōng guó dà',
           'example_translation': 'A Rússia é maior que a China.'},
 '18::头发': {'word': '头发',
            'answer': 'tou2fa',
            'pinyin_syllables': ['tou2', 'fa5'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['小红的头发比小丽的长。'],
            'occurrences': 1,
            'example_pinyin': 'xiǎo hóng de tóu fa bǐ xiǎo lì de cháng',
            'example_translation': 'O cabelo de Xiaohong é mais comprido que o de Xiaoli.'},
 '18::小红': {'word': '小红',
            'answer': 'xiao3hong2',
            'pinyin_syllables': ['xiao3', 'hong2'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['小红的头发比小丽的长。'],
            'occurrences': 1,
            'example_pinyin': 'xiǎo hóng de tóu fa bǐ xiǎo lì de cháng',
            'example_translation': 'O cabelo de Xiaohong é mais comprido que o de Xiaoli.'},
 '18::小丽': {'word': '小丽',
            'answer': 'xiao3li4',
            'pinyin_syllables': ['xiao3', 'li4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['小红的头发比小丽的长。'],
            'occurrences': 1,
            'example_pinyin': 'xiǎo hóng de tóu fa bǐ xiǎo lì de cháng',
            'example_translation': 'O cabelo de Xiaohong é mais comprido que o de Xiaoli.'},
 '18::海南': {'word': '海南',
            'answer': 'hai3nan2',
            'pinyin_syllables': ['hai3', 'nan2'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['哈尔滨的气温比海南低。'],
            'occurrences': 1,
            'example_pinyin': 'hā ěr bīn de qì wēn bǐ hǎi nán dī',
            'example_translation': 'A temperatura de Harbin é mais baixa que a de Hainan.'},
 '18::汽车': {'word': '汽车',
            'answer': 'qi4che1',
            'pinyin_syllables': ['qi4', 'che1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['坐火车比坐汽车快一点儿。'],
            'occurrences': 1,
            'example_pinyin': 'zuò huǒ chē bǐ zuò qì chē kuài yì diǎnr',
            'example_translation': 'Viajar de trem é um pouco mais rápido que viajar de carro.'},
 '18::一点儿': {'word': '一点儿',
             'answer': 'yi4dian3r',
             'pinyin_syllables': ['yi4', 'dian3', 'r'],
             'categories': ['Livro 18 e aulas 18.1 / 18.2'],
             'examples': ['坐火车比坐汽车快一点儿。'],
             'occurrences': 1,
             'example_pinyin': 'zuò huǒ chē bǐ zuò qì chē kuài yì diǎnr',
             'example_translation': 'Viajar de trem é um pouco mais rápido que viajar de carro.',
             'answer_variants': ['yi4dianr3']},
 '18::件': {'word': '件',
           'answer': 'jian4',
           'pinyin_syllables': ['jian4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['这件毛衣比那件贵一点儿。'],
           'occurrences': 1,
           'example_pinyin': 'zhè jiàn máo yī bǐ nà jiàn guì yì diǎnr',
           'example_translation': 'Este suéter é um pouco mais caro que aquele.'},
 '18::毛衣': {'word': '毛衣',
            'answer': 'mao2yi1',
            'pinyin_syllables': ['mao2', 'yi1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['这件毛衣比那件贵一点儿。'],
            'occurrences': 1,
            'example_pinyin': 'zhè jiàn máo yī bǐ nà jiàn guì yì diǎnr',
            'example_translation': 'Este suéter é um pouco mais caro que aquele.'},
 '18::贵': {'word': '贵',
           'answer': 'gui4',
           'pinyin_syllables': ['gui4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['这件毛衣比那件贵一点儿。'],
           'occurrences': 1,
           'example_pinyin': 'zhè jiàn máo yī bǐ nà jiàn guì yì diǎnr',
           'example_translation': 'Este suéter é um pouco mais caro que aquele.'},
 '18::日记': {'word': '日记',
            'answer': 'ri4ji4',
            'pinyin_syllables': ['ri4', 'ji4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['马克每天写日记。'],
            'occurrences': 1,
            'example_pinyin': 'mǎ kè měi tiān xiěrì jì',
            'example_translation': 'Mark escreve no diário todos os dias.'},
 '18::半年': {'word': '半年',
            'answer': 'ban4nian2',
            'pinyin_syllables': ['ban4', 'nian2'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我来上海半年多了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ lái shàng hǎi bàn nián duō le',
            'example_translation': 'Cheguei a Xangai há mais de meio ano.'},
 '18::月': {'word': '月',
           'answer': 'yue4',
           'pinyin_syllables': ['yue4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['六月和七月经常下雨。'],
           'occurrences': 1,
           'example_pinyin': 'liù yuè hé qī yuè jīng cháng xià yǔ',
           'example_translation': 'Chove com frequência em junho e julho.'},
 '18::广州': {'word': '广州',
            'answer': 'guang3zhou1',
            'pinyin_syllables': ['guang3', 'zhou1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['广州比北京潮湿。'],
            'occurrences': 1,
            'example_pinyin': 'guǎng zhōu bǐ běi jīng cháo shī',
            'example_translation': 'Guangzhou é mais úmida que Pequim.'},
 '18::年轻人': {'word': '年轻人',
             'answer': 'nian2qing1ren2',
             'pinyin_syllables': ['nian2', 'qing1', 'ren2'],
             'categories': ['Livro 18 e aulas 18.1 / 18.2'],
             'examples': ['年轻人的娱乐生活很丰富。'],
             'occurrences': 1,
             'example_pinyin': 'nián qīngrén de yú lè shēng huó hěn fēng fù',
             'example_translation': 'A vida de lazer dos jovens é bem variada.'},
 '18::老年人': {'word': '老年人',
             'answer': 'lao3nian2ren2',
             'pinyin_syllables': ['lao3', 'nian2', 'ren2'],
             'categories': ['Livro 18 e aulas 18.1 / 18.2'],
             'examples': ['老年人也喜欢娱乐。'],
             'occurrences': 1,
             'example_pinyin': 'lǎo niánrén yě xǐ huan yú lè',
             'example_translation': 'Os idosos também gostam de lazer.'},
 '18::生活': {'word': '生活',
            'answer': 'sheng1huo2',
            'pinyin_syllables': ['sheng1', 'huo2'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['年轻人的娱乐生活很丰富。'],
            'occurrences': 1,
            'example_pinyin': 'nián qīngrén de yú lè shēng huó hěn fēng fù',
            'example_translation': 'A vida de lazer dos jovens é bem variada.'},
 '18::从': {'word': '从',
           'answer': 'cong2',
           'pinyin_syllables': ['cong2'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['从这里到超市只能坐公交车。'],
           'occurrences': 1,
           'example_pinyin': 'cóng zhè lǐ dào chāo shì zhǐ néng zuò gōng jiāo chē',
           'example_translation': 'Daqui ao supermercado só é possível ir de ônibus.'},
 '18::这里': {'word': '这里',
            'answer': 'zhe4li3',
            'pinyin_syllables': ['zhe4', 'li3'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['从这里到超市只能坐公交车。'],
            'occurrences': 1,
            'example_pinyin': 'cóng zhè lǐ dào chāo shì zhǐ néng zuò gōng jiāo chē',
            'example_translation': 'Daqui ao supermercado só é possível ir de ônibus.'},
 '18::超市': {'word': '超市',
            'answer': 'chao1shi4',
            'pinyin_syllables': ['chao1', 'shi4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['从这里到超市只能坐公交车。'],
            'occurrences': 1,
            'example_pinyin': 'cóng zhè lǐ dào chāo shì zhǐ néng zuò gōng jiāo chē',
            'example_translation': 'Daqui ao supermercado só é possível ir de ônibus.'},
 '18::公交车': {'word': '公交车',
             'answer': 'gong1jiao1che1',
             'pinyin_syllables': ['gong1', 'jiao1', 'che1'],
             'categories': ['Livro 18 e aulas 18.1 / 18.2'],
             'examples': ['从这里到超市只能坐公交车。'],
             'occurrences': 1,
             'example_pinyin': 'cóng zhè lǐ dào chāo shì zhǐ néng zuò gōng jiāo chē',
             'example_translation': 'Daqui ao supermercado só é possível ir de ônibus.'},
 '18::地铁': {'word': '地铁',
            'answer': 'di4tie3',
            'pinyin_syllables': ['di4', 'tie3'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['地铁站离这儿五百米。'],
            'occurrences': 1,
            'example_pinyin': 'dì tiě zhàn lí zhèr wǔ bǎi mǐ',
            'example_translation': 'A estação de metrô fica a quinhentos metros daqui.'},
 '18::昨天': {'word': '昨天',
            'answer': 'zuo2tian1',
            'pinyin_syllables': ['zuo2', 'tian1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['昨天十八度，今天二十度。'],
            'occurrences': 1,
            'example_pinyin': 'zuó tiān shí bā dù jīn tiān èr shí dù',
            'example_translation': 'Ontem fez dezoito graus; hoje faz vinte.'},
 '18::今天': {'word': '今天',
            'answer': 'jin1tian1',
            'pinyin_syllables': ['jin1', 'tian1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['昨天十八度，今天二十度。'],
            'occurrences': 1,
            'example_pinyin': 'zuó tiān shí bā dù jīn tiān èr shí dù',
            'example_translation': 'Ontem fez dezoito graus; hoje faz vinte.'},
 '18::度': {'word': '度',
           'answer': 'du4',
           'pinyin_syllables': ['du4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['昨天十八度，今天二十度。'],
           'occurrences': 1,
           'example_pinyin': 'zuó tiān shí bā dù jīn tiān èr shí dù',
           'example_translation': 'Ontem fez dezoito graus; hoje faz vinte.'},
 '18::香蕉': {'word': '香蕉',
            'answer': 'xiang1jiao1',
            'pinyin_syllables': ['xiang1', 'jiao1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['香蕉三块钱一斤，苹果六块钱一斤。'],
            'occurrences': 1,
            'example_pinyin': 'xiāng jiāo sān kuài qián yì jīn píng guǒ liù kuài qián yì jīn',
            'example_translation': 'Banana custa três yuans por meio quilo; maçã custa seis.'},
 '18::苹果': {'word': '苹果',
            'answer': 'ping2guo3',
            'pinyin_syllables': ['ping2', 'guo3'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['香蕉三块钱一斤，苹果六块钱一斤。'],
            'occurrences': 1,
            'example_pinyin': 'xiāng jiāo sān kuài qián yì jīn píng guǒ liù kuài qián yì jīn',
            'example_translation': 'Banana custa três yuans por meio quilo; maçã custa seis.'},
 '18::块': {'word': '块',
           'answer': 'kuai4',
           'pinyin_syllables': ['kuai4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['香蕉三块钱一斤，苹果六块钱一斤。'],
           'occurrences': 1,
           'example_pinyin': 'xiāng jiāo sān kuài qián yì jīn píng guǒ liù kuài qián yì jīn',
           'example_translation': 'Banana custa três yuans por meio quilo; maçã custa seis.'},
 '18::钱': {'word': '钱',
           'answer': 'qian2',
           'pinyin_syllables': ['qian2'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['香蕉三块钱一斤，苹果六块钱一斤。'],
           'occurrences': 1,
           'example_pinyin': 'xiāng jiāo sān kuài qián yì jīn píng guǒ liù kuài qián yì jīn',
           'example_translation': 'Banana custa três yuans por meio quilo; maçã custa seis.'},
 '18::斤': {'word': '斤',
           'answer': 'jin1',
           'pinyin_syllables': ['jin1'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['香蕉三块钱一斤，苹果六块钱一斤。'],
           'occurrences': 1,
           'example_pinyin': 'xiāng jiāo sān kuài qián yì jīn píng guǒ liù kuài qián yì jīn',
           'example_translation': 'Banana custa três yuans por meio quilo; maçã custa seis.'},
 '18::认识': {'word': '认识',
            'answer': 'ren4shi',
            'pinyin_syllables': ['ren4', 'shi5'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我认识一千多个汉字。'],
            'occurrences': 1,
            'example_pinyin': 'wǒrèn shi yì qiān duō ge hàn zì',
            'example_translation': 'Conheço mais de mil caracteres chineses.'},
 '18::千': {'word': '千',
           'answer': 'qian1',
           'pinyin_syllables': ['qian1'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['我认识一千多个汉字。'],
           'occurrences': 1,
           'example_pinyin': 'wǒrèn shi yì qiān duō ge hàn zì',
           'example_translation': 'Conheço mais de mil caracteres chineses.'},
 '18::国家': {'word': '国家',
            'answer': 'guo2jia1',
            'pinyin_syllables': ['guo2', 'jia1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['你国家的东西贵吗？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ guó jiā de dōng xi guì ma',
            'example_translation': 'As coisas no seu país são caras?'},
 '18::东西': {'word': '东西',
            'answer': 'dong1xi',
            'pinyin_syllables': ['dong1', 'xi5'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['你国家的东西贵吗？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ guó jiā de dōng xi guì ma',
            'example_translation': 'As coisas no seu país são caras?'},
 '18::星期五': {'word': '星期五',
             'answer': 'xing1qi1wu3',
             'pinyin_syllables': ['xing1', 'qi1', 'wu3'],
             'categories': ['Livro 18 e aulas 18.1 / 18.2'],
             'examples': ['今天是星期五。'],
             'occurrences': 1,
             'example_pinyin': 'jīn tiān shì xīng qī wǔ',
             'example_translation': 'Hoje é sexta-feira.'},
 '18::岁': {'word': '岁',
           'answer': 'sui4',
           'pinyin_syllables': ['sui4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['他十八岁。'],
           'occurrences': 1,
           'example_pinyin': 'tā shí bā suì',
           'example_translation': 'Ele tem dezoito anos.'},
 '18::便宜': {'word': '便宜',
            'answer': 'pian2yi',
            'pinyin_syllables': ['pian2', 'yi5'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['这个比那个便宜。'],
            'occurrences': 1,
            'example_pinyin': 'zhè ge bǐ nà ge pián yi',
            'example_translation': 'Este é mais barato que aquele.'},
 '18::水': {'word': '水',
           'answer': 'shui3',
           'pinyin_syllables': ['shui3'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['水比可乐健康。'],
           'occurrences': 1,
           'example_pinyin': 'shuǐ bǐ kě lè jiàn kāng',
           'example_translation': 'Água é mais saudável que refrigerante de cola.'},
 '18::可乐': {'word': '可乐',
            'answer': 'ke3le4',
            'pinyin_syllables': ['ke3', 'le4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['水比可乐健康。'],
            'occurrences': 1,
            'example_pinyin': 'shuǐ bǐ kě lè jiàn kāng',
            'example_translation': 'Água é mais saudável que refrigerante de cola.'},
 '18::面条': {'word': '面条',
            'answer': 'mian4tiao2',
            'pinyin_syllables': ['mian4', 'tiao2'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我喜欢吃面条和饺子。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xǐ huan chī miàn tiáo hé jiǎo zi',
            'example_translation': 'Gosto de comer macarrão e bolinhos chineses.'},
 '18::饺子': {'word': '饺子',
            'answer': 'jiao3zi',
            'pinyin_syllables': ['jiao3', 'zi5'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我喜欢吃面条和饺子。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xǐ huan chī miàn tiáo hé jiǎo zi',
            'example_translation': 'Gosto de comer macarrão e bolinhos chineses.'},
 '18::手机': {'word': '手机',
            'answer': 'shou3ji1',
            'pinyin_syllables': ['shou3', 'ji1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['这部手机很贵。'],
            'occurrences': 1,
            'example_pinyin': 'zhè bù shǒu jī hěn guì',
            'example_translation': 'Este celular é caro.'},
 '18::食': {'word': '食',
           'answer': 'shi2',
           'pinyin_syllables': ['shi2'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['食堂的肉夹馍比汉堡包好吃。'],
           'occurrences': 1,
           'example_pinyin': 'shí táng deròu jiā mó bǐ hàn bǎo bāo hǎo chī',
           'example_translation': 'O roujiamo do refeitório é mais gostoso que o hambúrguer.'},
 '18::堂': {'word': '堂',
           'answer': 'tang2',
           'pinyin_syllables': ['tang2'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['食堂的肉夹馍比汉堡包好吃。'],
           'occurrences': 1,
           'example_pinyin': 'shí táng deròu jiā mó bǐ hàn bǎo bāo hǎo chī',
           'example_translation': 'O roujiamo do refeitório é mais gostoso que o hambúrguer.'},
 '18::星': {'word': '星',
           'answer': 'xing1',
           'pinyin_syllables': ['xing1'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['今天是星期五。'],
           'occurrences': 1,
           'example_pinyin': 'jīn tiān shì xīng qī wǔ',
           'example_translation': 'Hoje é sexta-feira.'},
 '18::肉': {'word': '肉',
           'answer': 'rou4',
           'pinyin_syllables': ['rou4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['我喜欢吃肉。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ xǐ huan chīròu',
           'example_translation': 'Gosto de comer carne.'},
 '18::外': {'word': '外',
           'answer': 'wai4',
           'pinyin_syllables': ['wai4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['我有时候去外面的餐厅吃饭。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ yǒu shí hou qù wài miàn de cān tīng chī fàn',
           'example_translation': 'Às vezes vou comer em um restaurante fora de casa.'},
 '18::卖': {'word': '卖',
           'answer': 'mai4',
           'pinyin_syllables': ['mai4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['这里卖水果。'],
           'occurrences': 1,
           'example_pinyin': 'zhè lǐ mài shuǐ guǒ',
           'example_translation': 'Aqui se vendem frutas.'},
 '18::方': {'word': '方',
           'answer': 'fang1',
           'pinyin_syllables': ['fang1'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['在中国叫外卖很方便。'],
           'occurrences': 1,
           'example_pinyin': 'zài zhōng guó jiào wài mài hěn fāng biàn',
           'example_translation': 'É muito prático pedir comida para entrega na China.'},
 '18::便': {'word': '便',
           'answer': 'bian4',
           'pinyin_syllables': ['bian4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['在中国叫外卖很方便。'],
           'occurrences': 1,
           'example_pinyin': 'zài zhōng guó jiào wài mài hěn fāng biàn',
           'example_translation': 'É muito prático pedir comida para entrega na China.'},
 '18::太': {'word': '太',
           'answer': 'tai4',
           'pinyin_syllables': ['tai4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['今天太热了。'],
           'occurrences': 1,
           'example_pinyin': 'jīn tiān tàirè le',
           'example_translation': 'Hoje está quente demais.'},
 '18::关': {'word': '关',
           'answer': 'guan1',
           'pinyin_syllables': ['guan1'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['没关系，你有时间，我请你到我家吃饭。'],
           'occurrences': 1,
           'example_pinyin': 'méi guān xi nǐ yǒu shí jiān wǒ qǐng nǐ dào wǒ jiā chī fàn',
           'example_translation': 'Tudo bem; quando você tiver tempo, convido você para comer na minha '
                                  'casa.'},
 '18::系': {'word': '系',
           'answer': 'xi4',
           'pinyin_syllables': ['xi4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['没关系，你有时间，我请你到我家吃饭。'],
           'occurrences': 1,
           'example_pinyin': 'méi guān xi nǐ yǒu shí jiān wǒ qǐng nǐ dào wǒ jiā chī fàn',
           'example_translation': 'Tudo bem; quando você tiver tempo, convido você para comer na minha '
                                  'casa.'},
 '18::路': {'word': '路',
           'answer': 'lu4',
           'pinyin_syllables': ['lu4'],
           'categories': ['Livro 18 e aulas 18.1 / 18.2'],
           'examples': ['我家离学校不远，可以走路去。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jiā lí xué xiào bù yuǎn kě yǐ zǒu lù qù',
           'example_translation': 'Minha casa não fica longe da escola; dá para ir a pé.'},
 '18::通讯': {'word': '通讯',
            'answer': 'tong1xun4',
            'pinyin_syllables': ['tong1', 'xun4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['这篇通讯很详细。'],
            'occurrences': 1,
            'example_pinyin': 'zhè piān tōng xùn hěn xiáng xì',
            'example_translation': 'Esta reportagem é muito detalhada.'},
 '18::通信': {'word': '通信',
            'answer': 'tong1xin4',
            'pinyin_syllables': ['tong1', 'xin4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我们经常通信。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ men jīng cháng tōng xìn',
            'example_translation': 'Nós nos correspondemos com frequência.'},
 '18::药片': {'word': '药片',
            'answer': 'yao4pian4',
            'pinyin_syllables': ['yao4', 'pian4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['这是药片。'],
            'occurrences': 1,
            'example_pinyin': 'zhè shì yào piàn',
            'example_translation': 'Isto é um comprimido.'},
 '18::欠缺': {'word': '欠缺',
            'answer': 'qian4que1',
            'pinyin_syllables': ['qian4', 'que1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['他欠缺经验。'],
            'occurrences': 1,
            'example_pinyin': 'tā qiàn quē jīng yàn',
            'example_translation': 'Falta experiência a ele.'},
 '18::详细': {'word': '详细',
            'answer': 'xiang2xi4',
            'pinyin_syllables': ['xiang2', 'xi4'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['这篇通讯很详细。'],
            'occurrences': 1,
            'example_pinyin': 'zhè piān tōng xùn hěn xiáng xì',
            'example_translation': 'Esta reportagem é muito detalhada.'},
 '18::求学': {'word': '求学',
            'answer': 'qiu2xue2',
            'pinyin_syllables': ['qiu2', 'xue2'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['他去中国求学。'],
            'occurrences': 1,
            'example_pinyin': 'tā qù zhōng guó qiú xué',
            'example_translation': 'Ele vai à China para estudar.'},
 '18::一知半解': {'word': '一知半解',
              'answer': 'yi4zhi1ban4jie3',
              'pinyin_syllables': ['yi4', 'zhi1', 'ban4', 'jie3'],
              'categories': ['Livro 18 e aulas 18.1 / 18.2'],
              'examples': ['我对书法一知半解。'],
              'occurrences': 1,
              'example_pinyin': 'wǒ duì shū fǎ yì zhī bàn jiě',
              'example_translation': 'Tenho apenas um conhecimento superficial de caligrafia.'},
 '18::一言为定': {'word': '一言为定',
              'answer': 'yi4yan2wei2ding4',
              'pinyin_syllables': ['yi4', 'yan2', 'wei2', 'ding4'],
              'categories': ['Livro 18 e aulas 18.1 / 18.2'],
              'examples': ['我们一言为定。'],
              'occurrences': 1,
              'example_pinyin': 'wǒ men yì yán wéi dìng',
              'example_translation': 'Estamos combinados.'},
 '18::一致通过': {'word': '一致通过',
              'answer': 'yi2zhi4tong1guo4',
              'pinyin_syllables': ['yi2', 'zhi4', 'tong1', 'guo4'],
              'categories': ['Livro 18 e aulas 18.1 / 18.2'],
              'examples': ['大家一致通过这个计划。'],
              'occurrences': 1,
              'example_pinyin': 'dà jiā yí zhì tōng guò zhè ge jì huà',
              'example_translation': 'Todos aprovaram este plano por unanimidade.'},
 '18::看电影': {'word': '看电影',
             'answer': 'kan4dian4ying3',
             'pinyin_syllables': ['kan4', 'dian4', 'ying3'],
             'categories': ['Livro 18 e aulas 18.1 / 18.2'],
             'examples': ['我们一起去看电影。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ men yì qǐ qù kàn diàn yǐng',
             'example_translation': 'Vamos ao cinema juntos.'},
 '18::学习': {'word': '学习',
            'answer': 'xue2xi2',
            'pinyin_syllables': ['xue2', 'xi2'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['你每天学习汉语多长时间？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ měi tiān xué xí hàn yǔ duō cháng shí jiān',
            'example_translation': 'Quanto tempo você estuda chinês por dia?'},
 '18::常常': {'word': '常常',
            'answer': 'chang2chang2',
            'pinyin_syllables': ['chang2', 'chang2'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['我常常自己做饭。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ cháng cháng zì jǐ zuò fàn',
            'example_translation': 'Costumo cozinhar por conta própria.'},
 '18::李佳': {'word': '李佳',
            'answer': 'li3jia1',
            'pinyin_syllables': ['li3', 'jia1'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['李佳请马克吃饭。'],
            'occurrences': 1,
            'example_pinyin': 'lǐ jiā qǐng mǎ kè chī fàn',
            'example_translation': 'Li Jia convida Mark para comer.'},
 '18::姚明': {'word': '姚明',
            'answer': 'yao2ming2',
            'pinyin_syllables': ['yao2', 'ming2'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['姚明比马克高。'],
            'occurrences': 1,
            'example_pinyin': 'yáo míng bǐ mǎ kè gāo',
            'example_translation': 'Yao Ming é mais alto que Mark.'},
 '18::哪个': {'word': '哪个',
            'answer': 'na3ge',
            'pinyin_syllables': ['na3', 'ge5'],
            'categories': ['Livro 18 e aulas 18.1 / 18.2'],
            'examples': ['哪个更好吃？'],
            'occurrences': 1,
            'example_pinyin': 'nǎ ge gèng hǎo chī',
            'example_translation': 'Qual é mais gostoso?'},
 '18::做饭': {'word': '做饭',
            'answer': 'zuo4fan4',
            'pinyin_syllables': ['zuo4', 'fan4'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['我常常自己做饭。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ cháng cháng zì jǐ zuò fàn',
            'example_translation': 'Costumo cozinhar por conta própria.',
            'display_pinyin': 'zuò fàn'},
 '18::健身房': {'word': '健身房',
             'answer': 'jian4shen1fang2',
             'categories': ['Revisão · Aula 18'],
             'examples': ['你每周去健身房吗？', '你明天几点去健身房？', '大家喜欢去健身房，但是更喜欢去公园。', '你每次去健身房健身多久？'],
             'occurrences': 1,
             'display_pinyin': 'jiànshēnfáng'},
 '18::好吃': {'word': '好吃',
            'answer': 'hao3chi1',
            'pinyin_syllables': ['hao3', 'chi1'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['食堂的肉夹馍比汉堡包好吃。'],
            'occurrences': 1,
            'example_pinyin': 'shí táng deròu jiā mó bǐ hàn bǎo bāo hǎo chī',
            'example_translation': 'O roujiamo do refeitório é mais gostoso que o hambúrguer.',
            'display_pinyin': 'hǎo chī'},
 '18::更': {'word': '更',
           'answer': 'geng4',
           'categories': ['Revisão · Aula 18'],
           'examples': ['家里的饭比外卖更健康。'],
           'occurrences': 1,
           'display_pinyin': 'gèng',
           'example_pinyin': 'jiā lǐ de fàn bǐ wài mài gèng jiàn kāng',
           'example_translation': 'A comida caseira é mais saudável que a comida entregue.'},
 '18::觉得': {'word': '觉得',
            'answer': 'jue2de',
            'categories': ['Revisão · Aula 18'],
            'examples': ['我觉得肉夹馍是中式汉堡包。'],
            'occurrences': 1,
            'display_pinyin': 'juéde',
            'example_pinyin': 'wǒ jué deròu jiā mó shì zhōng shì hàn bǎo bāo',
            'example_translation': 'Acho que o roujiamo é um hambúrguer ao estilo chinês.'},
 '18::写': {'word': '写',
           'answer': 'xie3',
           'pinyin_syllables': ['xie3'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['马克每天写日记。'],
           'occurrences': 1,
           'example_pinyin': 'mǎ kè měi tiān xiěrì jì',
           'example_translation': 'Mark escreve no diário todos os dias.',
           'display_pinyin': 'xiě'},
 '18::书法': {'word': '书法',
            'answer': 'shu1fa3',
            'pinyin_syllables': ['shu1', 'fa3'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['我对书法一知半解。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ duì shū fǎ yì zhī bàn jiě',
            'example_translation': 'Tenho apenas um conhecimento superficial de caligrafia.',
            'display_pinyin': 'shū fǎ'},
 '18::汉字': {'word': '汉字',
            'answer': 'han4zi4',
            'pinyin_syllables': ['han4', 'zi4'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['我认识一千多个汉字。'],
            'occurrences': 1,
            'example_pinyin': 'wǒrèn shi yì qiān duō ge hàn zì',
            'example_translation': 'Conheço mais de mil caracteres chineses.',
            'display_pinyin': 'hàn zì'},
 '18::难': {'word': '难',
           'answer': 'nan2',
           'pinyin_syllables': ['nan2'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['书法很难，但是我学得还可以。'],
           'occurrences': 1,
           'example_pinyin': 'shūfǎ hěn nán, dànshì wǒ xué de hái kěyǐ.',
           'example_translation': 'Caligrafia é difícil, mas estou aprendendo razoavelmente bem.',
           'display_pinyin': 'nán'},
 '18::多': {'word': '多',
           'answer': 'duo1',
           'pinyin_syllables': ['duo1'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['我来上海半年多了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ lái shàng hǎi bàn nián duō le',
           'example_translation': 'Cheguei a Xangai há mais de meio ano.',
           'display_pinyin': 'duō'},
 '18::了': {'word': '了',
           'answer': 'le',
           'categories': ['Revisão · Aula 18'],
           'examples': ['我来上海半年多了。'],
           'occurrences': 1,
           'display_pinyin': 'le',
           'example_pinyin': 'wǒ lái shàng hǎi bàn nián duō le',
           'example_translation': 'Cheguei a Xangai há mais de meio ano.'},
 '18::经常': {'word': '经常',
            'answer': 'jing1chang2',
            'pinyin_syllables': ['jing1', 'chang2'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['你经常去哪里吃晚餐？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ jīng cháng qù nǎ lǐ chī wǎn cān',
            'example_translation': 'Onde você costuma jantar?',
            'display_pinyin': 'jīng cháng'},
 '18::有': {'word': '有',
           'answer': 'you3',
           'categories': ['Revisão · Aula 18'],
           'examples': ['我有时候去外面的餐厅吃饭。'],
           'occurrences': 1,
           'display_pinyin': 'yǒu',
           'example_pinyin': 'wǒ yǒu shí hou qù wài miàn de cān tīng chī fàn',
           'example_translation': 'Às vezes vou comer em um restaurante fora de casa.'},
 '18::什么时候': {'word': '什么时候',
              'answer': 'shen2meshi2hou',
              'pinyin_syllables': ['shen2', 'me5', 'shi2', 'hou5'],
              'categories': ['Revisão · Aula 18'],
              'examples': ['什么时候能尝尝你的手艺？'],
              'occurrences': 1,
              'example_pinyin': 'shénme shíhou néng chángchang nǐ de shǒuyì?',
              'example_translation': 'Quando poderemos experimentar sua comida?',
              'display_pinyin': 'shén me shí hou'},
 '18::做客': {'word': '做客',
            'answer': 'zuo4ke4',
            'pinyin_syllables': ['zuo4', 'ke4'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['这个周末来我家做客吧，我给大家做牛排。'],
            'occurrences': 1,
            'example_pinyin': 'zhè ge zhōumò lái wǒ jiā zuòkè ba, wǒ gěi dàjiā zuò niúpái.',
            'example_translation': 'Venham me visitar em casa neste fim de semana; vou preparar bifes para '
                                   'todos.',
            'display_pinyin': 'zuò kè'},
 '18::一起': {'word': '一起',
            'answer': 'yi4qi3',
            'pinyin_syllables': ['yi4', 'qi3'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['我们一起去看电影。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ men yì qǐ qù kàn diàn yǐng',
            'example_translation': 'Vamos ao cinema juntos.',
            'display_pinyin': 'yì qǐ'},
 '18::打': {'word': '打',
           'answer': 'da3',
           'pinyin_syllables': ['da3'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['今天刮风，还打雷。'],
           'occurrences': 1,
           'example_pinyin': 'jīn tiān guā fēng hái dǎ léi',
           'example_translation': 'Hoje está ventando e também está trovejando.',
           'display_pinyin': 'dǎ'},
 '18::网球': {'word': '网球',
            'answer': 'wang3qiu2',
            'categories': ['Revisão · Aula 18'],
            'examples': ['她不会打网球。', '你喜欢打网球吗？', '这是谁的网球？', '你星期几打网球？'],
            'occurrences': 1,
            'display_pinyin': 'wǎngqiú'},
 '18::快': {'word': '快',
           'answer': 'kuai4',
           'pinyin_syllables': ['kuai4'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['坐火车比坐汽车快一点儿。'],
           'occurrences': 1,
           'example_pinyin': 'zuò huǒ chē bǐ zuò qì chē kuài yì diǎnr',
           'example_translation': 'Viajar de trem é um pouco mais rápido que viajar de carro.',
           'display_pinyin': 'kuài'},
 '18::家': {'word': '家',
           'answer': 'jia1',
           'pinyin_syllables': ['jia1'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['家里的饭比外卖更健康。'],
           'occurrences': 1,
           'example_pinyin': 'jiā lǐ de fàn bǐ wài mài gèng jiàn kāng',
           'example_translation': 'A comida caseira é mais saudável que a comida entregue.',
           'display_pinyin': 'jiā'},
 '18::里': {'word': '里',
           'answer': 'li3',
           'pinyin_syllables': ['li3'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['你经常去哪里吃晚餐？'],
           'occurrences': 1,
           'example_pinyin': 'nǐ jīng cháng qù nǎ lǐ chī wǎn cān',
           'example_translation': 'Onde você costuma jantar?',
           'display_pinyin': 'lǐ'},
 '18::和': {'word': '和',
           'answer': 'he2',
           'pinyin_syllables': ['he2'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['六月和七月经常下雨。'],
           'occurrences': 1,
           'example_pinyin': 'liù yuè hé qī yuè jīng cháng xià yǔ',
           'example_translation': 'Chove com frequência em junho e julho.',
           'display_pinyin': 'hé'},
 '18::我': {'word': '我',
           'answer': 'wo3',
           'pinyin_syllables': ['wo3'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['我觉得肉夹馍是中式汉堡包。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jué deròu jiā mó shì zhōng shì hàn bǎo bāo',
           'example_translation': 'Acho que o roujiamo é um hambúrguer ao estilo chinês.',
           'display_pinyin': 'wǒ'},
 '18::你': {'word': '你',
           'answer': 'ni3',
           'pinyin_syllables': ['ni3'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['你经常去哪里吃晚餐？'],
           'occurrences': 1,
           'example_pinyin': 'nǐ jīng cháng qù nǎ lǐ chī wǎn cān',
           'example_translation': 'Onde você costuma jantar?',
           'display_pinyin': 'nǐ'},
 '18::他': {'word': '他',
           'answer': 'ta1',
           'pinyin_syllables': ['ta1'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['他住的地方离学校很近。'],
           'occurrences': 1,
           'example_pinyin': 'tā zhù de dì fang lí xué xiào hěn jìn',
           'example_translation': 'O lugar onde ele mora fica perto da escola.',
           'display_pinyin': 'tā'},
 '18::她': {'word': '她',
           'answer': 'ta1',
           'pinyin_syllables': ['ta1'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['她在椅子上坐着，正在写书法。'],
           'occurrences': 1,
           'example_pinyin': 'tā zài yǐzi shàng zuò zhe, zhèngzài xiě shūfǎ.',
           'example_translation': 'Ela está sentada na cadeira, escrevendo caligrafia.',
           'display_pinyin': 'tā'},
 '18::我们': {'word': '我们',
            'answer': 'wo3men',
            'pinyin_syllables': ['wo3', 'men5'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['我们经常通信。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ men jīng cháng tōng xìn',
            'example_translation': 'Nós nos correspondemos com frequência.',
            'display_pinyin': 'wǒ men'},
 '18::的': {'word': '的',
           'answer': 'de',
           'pinyin_syllables': ['de5'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['食堂的肉夹馍比汉堡包好吃。'],
           'occurrences': 1,
           'example_pinyin': 'shí táng deròu jiā mó bǐ hàn bǎo bāo hǎo chī',
           'example_translation': 'O roujiamo do refeitório é mais gostoso que o hambúrguer.',
           'display_pinyin': 'de'},
 '18::是': {'word': '是',
           'answer': 'shi4',
           'pinyin_syllables': ['shi4'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['我觉得肉夹馍是中式汉堡包。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jué deròu jiā mó shì zhōng shì hàn bǎo bāo',
           'example_translation': 'Acho que o roujiamo é um hambúrguer ao estilo chinês.',
           'display_pinyin': 'shì'},
 '18::不': {'word': '不',
           'answer': 'bu4',
           'pinyin_syllables': ['bu4'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['我家离学校不远，可以走路去。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jiā lí xué xiào bù yuǎn kě yǐ zǒu lù qù',
           'example_translation': 'Minha casa não fica longe da escola; dá para ir a pé.',
           'display_pinyin': 'bù'},
 '18::也': {'word': '也',
           'answer': 'ye3',
           'pinyin_syllables': ['ye3'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['老年人也喜欢娱乐。'],
           'occurrences': 1,
           'example_pinyin': 'lǎo niánrén yě xǐ huan yú lè',
           'example_translation': 'Os idosos também gostam de lazer.',
           'display_pinyin': 'yě'},
 '18::很': {'word': '很',
           'answer': 'hen3',
           'pinyin_syllables': ['hen3'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['在中国叫外卖很方便。'],
           'occurrences': 1,
           'example_pinyin': 'zài zhōng guó jiào wài mài hěn fāng biàn',
           'example_translation': 'É muito prático pedir comida para entrega na China.',
           'display_pinyin': 'hěn'},
 '18::去': {'word': '去',
           'answer': 'qu4',
           'categories': ['Revisão · Aula 18'],
           'examples': ['你经常去哪里吃晚餐？'],
           'occurrences': 1,
           'display_pinyin': 'qù',
           'example_pinyin': 'nǐ jīng cháng qù nǎ lǐ chī wǎn cān',
           'example_translation': 'Onde você costuma jantar?'},
 '18::来': {'word': '来',
           'answer': 'lai2',
           'pinyin_syllables': ['lai2'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['我来上海半年多了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ lái shàng hǎi bàn nián duō le',
           'example_translation': 'Cheguei a Xangai há mais de meio ano.',
           'display_pinyin': 'lái'},
 '18::可以': {'word': '可以',
            'answer': 'ke3yi3',
            'pinyin_syllables': ['ke3', 'yi3'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['我家离学校不远，可以走路去。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jiā lí xué xiào bù yuǎn kě yǐ zǒu lù qù',
            'example_translation': 'Minha casa não fica longe da escola; dá para ir a pé.',
            'display_pinyin': 'kě yǐ'},
 '18::喜欢': {'word': '喜欢',
            'answer': 'xi3huan',
            'pinyin_syllables': ['xi3', 'huan5'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['我喜欢逛街。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xǐ huan guàng jiē',
            'example_translation': 'Gosto de passear pelas lojas.',
            'display_pinyin': 'xǐ huan'},
 '18::吃': {'word': '吃',
           'answer': 'chi1',
           'pinyin_syllables': ['chi1'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['食堂的肉夹馍比汉堡包好吃。'],
           'occurrences': 1,
           'example_pinyin': 'shí táng deròu jiā mó bǐ hàn bǎo bāo hǎo chī',
           'example_translation': 'O roujiamo do refeitório é mais gostoso que o hambúrguer.',
           'display_pinyin': 'chī'},
 '18::周末': {'word': '周末',
            'answer': 'zhou1mo4',
            'pinyin_syllables': ['zhou1', 'mo4'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['周末我只能待在家里。'],
            'occurrences': 1,
            'example_pinyin': 'zhōu mò wǒ zhǐ néng dāi zài jiā lǐ',
            'example_translation': 'No fim de semana só posso ficar em casa.',
            'display_pinyin': 'zhōu mò'},
 '18::看书': {'word': '看书',
            'answer': 'kan4shu1',
            'pinyin_syllables': ['kan4', 'shu1'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['他喝着牛奶看书。'],
            'occurrences': 1,
            'example_pinyin': 'tā hē zhe niúnǎi kànshū.',
            'example_translation': 'Ele lê enquanto toma leite.',
            'display_pinyin': 'kàn shū'},
 '18::听': {'word': '听',
           'answer': 'ting1',
           'pinyin_syllables': ['ting1'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['我经常听着音乐练书法。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jīngcháng tīng zhe yīnyuè liàn shūfǎ.',
           'example_translation': 'Costumo praticar caligrafia enquanto ouço música.',
           'display_pinyin': 'tīng'},
 '18::音乐': {'word': '音乐',
            'answer': 'yin1yue4',
            'pinyin_syllables': ['yin1', 'yue4'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['我经常听着音乐练书法。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jīngcháng tīng zhe yīnyuè liàn shūfǎ.',
            'example_translation': 'Costumo praticar caligrafia enquanto ouço música.',
            'display_pinyin': 'yīn yuè'},
 '18::自己': {'word': '自己',
            'answer': 'zi4ji3',
            'pinyin_syllables': ['zi4', 'ji3'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['我常常自己做饭。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ cháng cháng zì jǐ zuò fàn',
            'example_translation': 'Costumo cozinhar por conta própria.',
            'display_pinyin': 'zì jǐ'},
 '18::近': {'word': '近',
           'answer': 'jin4',
           'pinyin_syllables': ['jin4'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['他住的地方离学校很近。'],
           'occurrences': 1,
           'example_pinyin': 'tā zhù de dì fang lí xué xiào hěn jìn',
           'example_translation': 'O lugar onde ele mora fica perto da escola.',
           'display_pinyin': 'jìn'},
 '18::每天': {'word': '每天',
            'answer': 'mei3tian1',
            'categories': ['Revisão · Aula 18'],
            'examples': ['马克每天写日记。'],
            'occurrences': 1,
            'display_pinyin': 'měitiān',
            'example_pinyin': 'mǎ kè měi tiān xiěrì jì',
            'example_translation': 'Mark escreve no diário todos os dias.'},
 '18::汉语': {'word': '汉语',
            'answer': 'han4yu3',
            'pinyin_syllables': ['han4', 'yu3'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['你每天学习汉语多长时间？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ měi tiān xué xí hàn yǔ duō cháng shí jiān',
            'example_translation': 'Quanto tempo você estuda chinês por dia?',
            'display_pinyin': 'hàn yǔ'},
 '18::小时': {'word': '小时',
            'answer': 'xiao3shi2',
            'categories': ['Revisão · Aula 18'],
            'examples': ['我每次跑步半个小时。', '他每次游泳一个小时。', '她每次骑车两个小时。'],
            'occurrences': 1,
            'display_pinyin': 'xiǎoshí'},
 '18::朋友': {'word': '朋友',
            'answer': 'peng2you',
            'pinyin_syllables': ['peng2', 'you5'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['这是朋友给我拍的照片。'],
            'occurrences': 1,
            'example_pinyin': 'zhè shì péngyou gěi wǒ pāi de zhàopiàn.',
            'example_translation': 'Esta é a foto que meu amigo tirou de mim.',
            'display_pinyin': 'péng you'},
 '18::你们': {'word': '你们',
            'answer': 'ni3men',
            'categories': ['Revisão · Aula 18'],
            'examples': ['你们会打棒球吗？'],
            'occurrences': 1,
            'display_pinyin': 'nǐmen'},
 '18::几': {'word': '几',
           'answer': 'ji3',
           'categories': ['Revisão · Aula 18'],
           'examples': ['你星期几打网球？', '你一周游泳几次？', '你一个月打几次篮球？', '你几岁开始游泳？'],
           'occurrences': 1,
           'display_pinyin': 'jǐ'},
 '18::什么': {'word': '什么',
            'answer': 'shen2me',
            'pinyin_syllables': ['shen2', 'me5'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['你最近在干什么呢？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ zuìjìn zài gàn shénme ne?',
            'example_translation': 'O que você tem feito ultimamente?',
            'display_pinyin': 'shén me'},
 '18::想': {'word': '想',
           'answer': 'xiang3',
           'categories': ['Revisão · Aula 18'],
           'examples': ['我很想念洛杉矶的阳光。'],
           'occurrences': 1,
           'display_pinyin': 'xiǎng',
           'example_pinyin': 'wǒ hěn xiǎng niàn luò shān jī de yáng guāng',
           'example_translation': 'Sinto muita falta do sol de Los Angeles.'},
 '18::为什么': {'word': '为什么',
             'answer': 'wei4shen2me',
             'categories': ['Revisão · Aula 18'],
             'examples': ['你为什么喜欢跑步？', '他为什么不喜欢游泳？', '你为什么最喜欢打网球？', '她为什么每周去健身房？'],
             'occurrences': 1,
             'display_pinyin': 'wèishénme'},
 '18::哪儿': {'word': '哪儿',
            'answer': 'na3r',
            'categories': ['Revisão · Aula 18'],
            'examples': ['你去哪儿跑步？', '他在哪儿游泳？', '那个篮球场在哪儿？', '你在哪儿唱卡拉OK？'],
            'occurrences': 1,
            'display_pinyin': 'nǎr',
            'answer_variants': ['nar3']},
 '18::坐': {'word': '坐',
           'answer': 'zuo4',
           'pinyin_syllables': ['zuo4'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['坐火车比坐汽车快一点儿。'],
           'occurrences': 1,
           'example_pinyin': 'zuò huǒ chē bǐ zuò qì chē kuài yì diǎnr',
           'example_translation': 'Viajar de trem é um pouco mais rápido que viajar de carro.',
           'display_pinyin': 'zuò'},
 '18::还': {'word': '还',
           'answer': 'hai2',
           'categories': ['Revisão · Aula 18'],
           'examples': ['今天刮风，还打雷。'],
           'occurrences': 1,
           'display_pinyin': 'hái',
           'example_pinyin': 'jīn tiān guā fēng hái dǎ léi',
           'example_translation': 'Hoje está ventando e também está trovejando.'},
 '18::不太': {'word': '不太',
            'answer': 'bu2tai4',
            'pinyin_syllables': ['bu2', 'tai4'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['我唱得不太好。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ chàng de bú tài hǎo.',
            'example_translation': 'Eu não canto muito bem.',
            'display_pinyin': 'bú tài'},
 '18::会': {'word': '会',
           'answer': 'hui4',
           'pinyin_syllables': ['hui4'],
           'categories': ['Revisão · Aula 18'],
           'examples': ['我会游泳，游得很好。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ huì yóuyǒng, yóu de hěn hǎo.',
           'example_translation': 'Eu sei nadar e nado muito bem.',
           'display_pinyin': 'huì'},
 '18::马克': {'word': '马克',
            'answer': 'ma3ke4',
            'pinyin_syllables': ['ma3', 'ke4'],
            'categories': ['Revisão · Aula 18'],
            'examples': ['我没有马克那么高。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ méi yǒu mǎ kè nà me gāo',
            'example_translation': 'Eu não sou tão alto quanto Mark.',
            'display_pinyin': 'mǎ kè'},
 '18::艾米丽': {'word': '艾米丽',
             'answer': 'ai4mi3li4',
             'pinyin_syllables': ['ai4', 'mi3', 'li4'],
             'categories': ['Revisão · Aula 18'],
             'examples': ['嗨，艾米丽！'],
             'occurrences': 1,
             'example_pinyin': 'hāi, Àimǐlì!',
             'example_translation': 'Oi, Emily!',
             'display_pinyin': 'ài mǐ lì'},
 '18::王浩明': {'word': '王浩明',
             'answer': 'wang2hao4ming2',
             'pinyin_syllables': ['wang2', 'hao4', 'ming2'],
             'categories': ['Revisão · Aula 18'],
             'examples': ['王浩明在学做西餐。'],
             'occurrences': 1,
             'example_pinyin': 'Wáng Hàomíng zài xué zuò xīcān.',
             'example_translation': 'Wang Haoming está aprendendo a preparar comida ocidental.',
             'display_pinyin': 'wáng hào míng'}}
LESSON18_TRANSLATIONS = {'18::食堂': 'refeitório; cantina',
 '18::肉夹馍': 'roujiamo; pão chinês recheado com carne',
 '18::中式': 'ao estilo chinês',
 '18::汉堡包': 'hambúrguer',
 '18::晚餐': 'jantar',
 '18::外面': 'fora; do lado de fora',
 '18::外卖': 'comida para viagem ou entrega',
 '18::方便': 'prático; conveniente',
 '18::健康': 'saudável; saúde',
 '18::离': 'estar a uma distância de',
 '18::走路': 'andar a pé; caminhar',
 '18::年': 'ano',
 '18::天气': 'tempo; clima',
 '18::潮湿': 'úmido',
 '18::待': 'ficar; permanecer',
 '18::想念': 'sentir saudade de',
 '18::阳光': 'luz do sol',
 '18::娱乐': 'entretenimento; lazer',
 '18::丰富': 'rico; abundante; variado',
 '18::逛街': 'passear pelas lojas; fazer compras',
 '18::只能': 'só poder; apenas conseguir',
 '18::洛杉矶': 'Los Angeles',
 '18::长': 'comprido; longo',
 '18::地方': 'lugar',
 '18::气温': 'temperatura do ar',
 '18::火车': 'trem',
 '18::住': 'morar; residir',
 '18::下雨': 'chover',
 '18::下雪': 'nevar',
 '18::刮风': 'ventar',
 '18::打雷': 'trovejar',
 '18::晴天': 'dia ensolarado',
 '18::阴天': 'dia nublado',
 '18::晴': 'ensolarado; tempo aberto',
 '18::阴': 'nublado',
 '18::俄罗斯': 'Rússia',
 '18::哈尔滨': 'Harbin',
 '18::热': 'quente; calor',
 '18::冷': 'frio',
 '18::夏天': 'verão',
 '18::冬天': 'inverno',
 '18::开车': 'dirigir; ir de carro',
 '18::比': 'que; em comparação com',
 '18::没有': 'não ter; não ser tão... quanto',
 '18::那么': 'tão; daquela maneira',
 '18::高': 'alto',
 '18::远': 'longe; distante',
 '18::学校': 'escola',
 '18::美国': 'Estados Unidos',
 '18::中国': 'China',
 '18::上海': 'Xangai',
 '18::北京': 'Pequim',
 '18::不过': 'mas; porém',
 '18::哪里': 'onde',
 '18::有时候': 'às vezes',
 '18::餐厅': 'restaurante',
 '18::吃饭': 'comer; fazer uma refeição',
 '18::饭': 'comida; refeição; arroz cozido',
 '18::叫': 'chamar; pedir (comida)',
 '18::没关系': 'não tem problema; tudo bem',
 '18::时间': 'tempo; horário',
 '18::请': 'por favor; convidar',
 '18::到': 'chegar; até; para',
 '18::地铁站': 'estação de metrô',
 '18::这儿': 'aqui',
 '18::百': 'cem',
 '18::米': 'metro (unidade de comprimento)',
 '18::飞机': 'avião',
 '18::大': 'grande',
 '18::头发': 'cabelo',
 '18::小红': 'Xiaohong (nome próprio)',
 '18::小丽': 'Xiaoli (nome próprio)',
 '18::海南': 'Hainan',
 '18::汽车': 'automóvel; carro',
 '18::一点儿': 'um pouco',
 '18::件': 'classificador de roupas e assuntos',
 '18::毛衣': 'suéter; blusa de lã',
 '18::贵': 'caro',
 '18::日记': 'diário pessoal',
 '18::半年': 'meio ano',
 '18::月': 'mês; lua',
 '18::广州': 'Guangzhou; Cantão',
 '18::年轻人': 'jovem; pessoa jovem',
 '18::老年人': 'idoso; pessoa idosa',
 '18::生活': 'vida; viver',
 '18::从': 'de; a partir de',
 '18::这里': 'aqui; este lugar',
 '18::超市': 'supermercado',
 '18::公交车': 'ônibus urbano',
 '18::地铁': 'metrô',
 '18::昨天': 'ontem',
 '18::今天': 'hoje',
 '18::度': 'grau (temperatura)',
 '18::香蕉': 'banana',
 '18::苹果': 'maçã',
 '18::块': 'yuan (forma coloquial); pedaço',
 '18::钱': 'dinheiro',
 '18::斤': 'jin; meio quilo',
 '18::认识': 'conhecer; reconhecer',
 '18::千': 'mil',
 '18::国家': 'país',
 '18::东西': 'coisa; objeto',
 '18::星期五': 'sexta-feira',
 '18::岁': 'ano de idade',
 '18::便宜': 'barato',
 '18::水': 'água',
 '18::可乐': 'refrigerante de cola',
 '18::面条': 'macarrão',
 '18::饺子': 'jiaozi; bolinho chinês recheado',
 '18::手机': 'celular',
 '18::食': 'comida; elemento de 食堂',
 '18::堂': 'salão; elemento de 食堂',
 '18::星': 'estrela; elemento de 星期',
 '18::肉': 'carne',
 '18::外': 'fora; exterior',
 '18::卖': 'vender',
 '18::方': 'direção; elemento de 方便',
 '18::便': 'conveniente; elemento de 方便',
 '18::太': 'demais; muito',
 '18::关': 'elemento de 关系 (relação)',
 '18::系': 'ligação; elemento de 关系',
 '18::路': 'rua; caminho',
 '18::通讯': 'comunicação; reportagem',
 '18::通信': 'corresponder-se; comunicação',
 '18::药片': 'comprimido',
 '18::欠缺': 'faltar; carecer de',
 '18::详细': 'detalhado',
 '18::求学': 'buscar formação; estudar',
 '18::一知半解': 'conhecimento superficial; compreensão parcial',
 '18::一言为定': 'combinado; está decidido',
 '18::一致通过': 'aprovar por unanimidade',
 '18::看电影': 'assistir a um filme; ir ao cinema',
 '18::学习': 'estudar; aprender',
 '18::常常': 'frequentemente; com frequência',
 '18::李佳': 'Li Jia (nome próprio)',
 '18::姚明': 'Yao Ming (nome próprio)',
 '18::哪个': 'qual',
 '18::做饭': 'cozinhar; preparar uma refeição',
 '18::健身房': 'academia',
 '18::好吃': 'gostoso; delicioso',
 '18::更': 'mais; ainda mais',
 '18::觉得': 'achar; considerar',
 '18::写': 'escrever',
 '18::书法': 'caligrafia chinesa',
 '18::汉字': 'caracteres chineses',
 '18::难': 'difícil',
 '18::多': 'muito; muitos',
 '18::了': 'partícula de ação concluída ou mudança',
 '18::经常': 'frequentemente; com frequência',
 '18::有': 'ter; haver; existir',
 '18::什么时候': 'quando',
 '18::做客': 'visitar alguém como convidado',
 '18::一起': 'junto(s)',
 '18::打': 'jogar; praticar (esporte ou jogo)',
 '18::网球': 'tênis',
 '18::快': 'rápido; depressa',
 '18::家': 'casa; lar; família',
 '18::里': 'dentro; em',
 '18::和': 'e; com',
 '18::我': 'eu',
 '18::你': 'você',
 '18::他': 'ele',
 '18::她': 'ela',
 '18::我们': 'nós',
 '18::的': 'partícula de posse ou atribuição',
 '18::是': 'ser; estar',
 '18::不': 'não',
 '18::也': 'também',
 '18::很': 'muito',
 '18::去': 'ir',
 '18::来': 'vir',
 '18::可以': 'poder; ser possível',
 '18::喜欢': 'gostar de',
 '18::吃': 'comer',
 '18::周末': 'fim de semana',
 '18::看书': 'ler (livros)',
 '18::听': 'ouvir; escutar',
 '18::音乐': 'música',
 '18::自己': 'si mesmo; próprio',
 '18::近': 'perto; recente; elemento de 最近',
 '18::每天': 'todos os dias',
 '18::汉语': 'língua chinesa; mandarim',
 '18::小时': 'hora (duração)',
 '18::朋友': 'amigo(a)',
 '18::你们': 'vocês',
 '18::几': 'quantos; qual (número pequeno)',
 '18::什么': 'o que; que',
 '18::想': 'querer; ter vontade de',
 '18::为什么': 'por quê',
 '18::哪儿': 'onde',
 '18::坐': 'sentar; estar sentado',
 '18::还': 'ainda; além disso; também',
 '18::不太': 'não muito',
 '18::会': 'saber fazer; conseguir',
 '18::马克': 'Mark (nome próprio)',
 '18::艾米丽': 'Emily (nome próprio)',
 '18::王浩明': 'Wang Haoming (nome próprio)'}
BLOCK18_WORDS = list(LESSON18_CARDS)
CARDS.update(LESSON18_CARDS)
WORD_TRANSLATIONS.update(LESSON18_TRANSLATIONS)
for _cid, _card in LESSON18_CARDS.items():
    WORD_PINYIN[_cid] = _card['answer']
    if 'example_translation' in _card:
        EXAMPLE_TRANSLATIONS.setdefault(_card['examples'][0], _card['example_translation'])


# Aula 19: IDs separados preservam o progresso de palavras comuns a outras aulas.
LESSON19_CARDS = {'19::倒霉': {'word': '倒霉',
            'answer': 'dao3mei2',
            'pinyin_syllables': ['dao3', 'mei2'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我今天真是太倒霉了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jīn tiān zhēn shì tài dǎo méi le',
            'example_translation': 'Hoje eu realmente tive muito azar.'},
 '19::丢': {'word': '丢',
           'answer': 'diu1',
           'pinyin_syllables': ['diu1'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我新买的手机丢了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ xīn mǎi de shǒu jī diū le',
           'example_translation': 'Perdi o celular que comprei recentemente.'},
 '19::不见': {'word': '不见',
            'answer': 'bu2jian4',
            'pinyin_syllables': ['bu2', 'jian4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我发现手机不见了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ fā xiàn shǒu jī bú jiàn le',
            'example_translation': 'Percebi que meu celular tinha desaparecido.'},
 '19::小偷': {'word': '小偷',
            'answer': 'xiao3tou1',
            'pinyin_syllables': ['xiao3', 'tou1'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['小偷偷走了我的手机。'],
            'occurrences': 1,
            'example_pinyin': 'xiǎo tōu tōu zǒu le wǒ de shǒu jī',
            'example_translation': 'O ladrão levou meu celular.'},
 '19::偷走': {'word': '偷走',
            'answer': 'tou1zou3',
            'pinyin_syllables': ['tou1', 'zou3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['小偷偷走了我的手机。'],
            'occurrences': 1,
            'example_pinyin': 'xiǎo tōu tōu zǒu le wǒ de shǒu jī',
            'example_translation': 'O ladrão levou meu celular.'},
 '19::应该': {'word': '应该',
            'answer': 'ying1gai1',
            'pinyin_syllables': ['ying1', 'gai1'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我现在应该怎么办？'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xiàn zài yīng gāi zěn me bàn',
            'example_translation': 'O que devo fazer agora?'},
 '19::怎么办': {'word': '怎么办',
             'answer': 'zen3meban4',
             'pinyin_syllables': ['zen3', 'me5', 'ban4'],
             'categories': ['Livro 19 e aulas 19.1 / 19.2'],
             'examples': ['我现在应该怎么办？'],
             'occurrences': 1,
             'example_pinyin': 'wǒ xiàn zài yīng gāi zěn me bàn',
             'example_translation': 'O que devo fazer agora?'},
 '19::自认倒霉': {'word': '自认倒霉',
              'answer': 'zi4ren4dao3mei2',
              'pinyin_syllables': ['zi4', 'ren4', 'dao3', 'mei2'],
              'categories': ['Livro 19 e aulas 19.1 / 19.2'],
              'examples': ['他只能自认倒霉。'],
              'occurrences': 1,
              'example_pinyin': 'tā zhǐ néng zìrèn dǎo méi',
              'example_translation': 'Ele só pode se conformar com o azar.'},
 '19::即使': {'word': '即使',
            'answer': 'ji2shi3',
            'pinyin_syllables': ['ji2', 'shi3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['即使明天下雨，我也要去上课。'],
            'occurrences': 1,
            'example_pinyin': 'jí shǐ míng tiān xià yǔ wǒ yě yào qù shàng kè',
            'example_translation': 'Mesmo que chova amanhã, vou à aula.'},
 '19::报警': {'word': '报警',
            'answer': 'bao4jing3',
            'pinyin_syllables': ['bao4', 'jing3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['他报警以后，警察来了。'],
            'occurrences': 1,
            'example_pinyin': 'tā bào jǐng yǐ hòu jǐng chá lái le',
            'example_translation': 'Depois que ele chamou a polícia, os policiais chegaram.'},
 '19::警察': {'word': '警察',
            'answer': 'jing3cha2',
            'pinyin_syllables': ['jing3', 'cha2'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['他报警以后，警察来了。'],
            'occurrences': 1,
            'example_pinyin': 'tā bào jǐng yǐ hòu jǐng chá lái le',
            'example_translation': 'Depois que ele chamou a polícia, os policiais chegaram.'},
 '19::骑': {'word': '骑',
           'answer': 'qi2',
           'pinyin_syllables': ['qi2'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我骑自行车出去玩。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ qí zì xíng chē chū qù wán',
           'example_translation': 'Saí de bicicleta para passear.'},
 '19::出去': {'word': '出去',
            'answer': 'chu1qu4',
            'pinyin_syllables': ['chu1', 'qu4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我骑自行车出去玩。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ qí zì xíng chē chū qù wán',
            'example_translation': 'Saí de bicicleta para passear.'},
 '19::辆': {'word': '辆',
           'answer': 'liang4',
           'pinyin_syllables': ['liang4'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['一辆车把我撞晕了。'],
           'occurrences': 1,
           'example_pinyin': 'yí liàng chē bǎ wǒ zhuàng yūn le',
           'example_translation': 'Um carro me atingiu e me fez perder a consciência.'},
 '19::撞晕': {'word': '撞晕',
            'answer': 'zhuang4yun1',
            'pinyin_syllables': ['zhuang4', 'yun1'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['一辆车把我撞晕了。'],
            'occurrences': 1,
            'example_pinyin': 'yí liàng chē bǎ wǒ zhuàng yūn le',
            'example_translation': 'Um carro me atingiu e me fez perder a consciência.'},
 '19::吓坏': {'word': '吓坏',
            'answer': 'xia4huai4',
            'pinyin_syllables': ['xia4', 'huai4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我的朋友当时吓坏了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de péng you dāng shí xià huài le',
            'example_translation': 'Meu amigo ficou apavorado naquele momento.'},
 '19::路人': {'word': '路人',
            'answer': 'lu4ren2',
            'pinyin_syllables': ['lu4', 'ren2'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['热心的路人叫了救护车。'],
            'occurrences': 1,
            'example_pinyin': 'rè xīn de lùrén jiào le jiù hù chē',
            'example_translation': 'Um pedestre prestativo chamou uma ambulância.'},
 '19::救护车': {'word': '救护车',
             'answer': 'jiu4hu4che1',
             'pinyin_syllables': ['jiu4', 'hu4', 'che1'],
             'categories': ['Livro 19 e aulas 19.1 / 19.2'],
             'examples': ['热心的路人叫了救护车。'],
             'occurrences': 1,
             'example_pinyin': 'rè xīn de lùrén jiào le jiù hù chē',
             'example_translation': 'Um pedestre prestativo chamou uma ambulância.'},
 '19::醒来': {'word': '醒来',
            'answer': 'xing3lai2',
            'pinyin_syllables': ['xing3', 'lai2'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我醒来的时候，在医院的床上躺着。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xǐng lái de shí hou zài yī yuàn de chuáng shàng tǎng zhe',
            'example_translation': 'Quando acordei, estava deitado em uma cama do hospital.'},
 '19::床': {'word': '床',
           'answer': 'chuang2',
           'pinyin_syllables': ['chuang2'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我醒来的时候，在医院的床上躺着。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ xǐng lái de shí hou zài yī yuàn de chuáng shàng tǎng zhe',
           'example_translation': 'Quando acordei, estava deitado em uma cama do hospital.'},
 '19::躺': {'word': '躺',
           'answer': 'tang3',
           'pinyin_syllables': ['tang3'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我醒来的时候，在医院的床上躺着。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ xǐng lái de shí hou zài yī yuàn de chuáng shàng tǎng zhe',
           'example_translation': 'Quando acordei, estava deitado em uma cama do hospital.'},
 '19::腿': {'word': '腿',
           'answer': 'tui3',
           'pinyin_syllables': ['tui3'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我的腿受伤了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ de tuǐ shòu shāng le',
           'example_translation': 'Minha perna ficou machucada.'},
 '19::受伤': {'word': '受伤',
            'answer': 'shou4shang1',
            'pinyin_syllables': ['shou4', 'shang1'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我的腿受伤了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de tuǐ shòu shāng le',
            'example_translation': 'Minha perna ficou machucada.'},
 '19::女': {'word': '女',
           'answer': 'nv3',
           'pinyin_syllables': ['nv3'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['警察把女司机带走了。'],
           'occurrences': 1,
           'example_pinyin': 'jǐng chá bǎ nǚ sī jī dài zǒu le',
           'example_translation': 'A polícia levou a motorista.'},
 '19::司机': {'word': '司机',
            'answer': 'si1ji1',
            'pinyin_syllables': ['si1', 'ji1'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['警察把女司机带走了。'],
            'occurrences': 1,
            'example_pinyin': 'jǐng chá bǎ nǚ sī jī dài zǒu le',
            'example_translation': 'A polícia levou a motorista.'},
 '19::带走': {'word': '带走',
            'answer': 'dai4zou3',
            'pinyin_syllables': ['dai4', 'zou3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['警察把女司机带走了。'],
            'occurrences': 1,
            'example_pinyin': 'jǐng chá bǎ nǚ sī jī dài zǒu le',
            'example_translation': 'A polícia levou a motorista.'},
 '19::严重': {'word': '严重',
            'answer': 'yan2zhong4',
            'pinyin_syllables': ['yan2', 'zhong4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['这次交通事故很严重。'],
            'occurrences': 1,
            'example_pinyin': 'zhè cì jiāo tōng shì gù hěn yán zhòng',
            'example_translation': 'Este acidente de trânsito foi grave.'},
 '19::愿意': {'word': '愿意',
            'answer': 'yuan4yi4',
            'pinyin_syllables': ['yuan4', 'yi4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我愿意跟她和解。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ yuàn yì gēn tā hé jiě',
            'example_translation': 'Estou disposto a me reconciliar com ela.'},
 '19::和解': {'word': '和解',
            'answer': 'he2jie3',
            'pinyin_syllables': ['he2', 'jie3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我愿意跟她和解。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ yuàn yì gēn tā hé jiě',
            'example_translation': 'Estou disposto a me reconciliar com ela.'},
 '19::华山路': {'word': '华山路',
             'answer': 'hua4shan1lu4',
             'pinyin_syllables': ['hua4', 'shan1', 'lu4'],
             'categories': ['Livro 19 e aulas 19.1 / 19.2'],
             'examples': ['我们骑到华山路的路口。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ men qí dào huà shān lù de lù kǒu',
             'example_translation': 'Fomos de bicicleta até o cruzamento da Rua Huashan.'},
 '19::警察局': {'word': '警察局',
             'answer': 'jing3cha2ju2',
             'pinyin_syllables': ['jing3', 'cha2', 'ju2'],
             'categories': ['Livro 19 e aulas 19.1 / 19.2'],
             'examples': ['警察局和派出所在哪里？'],
             'occurrences': 1,
             'example_pinyin': 'jǐng chá jú hé pài chū suǒ zài nǎ lǐ',
             'example_translation': 'Onde ficam a delegacia e o posto policial?'},
 '19::派出所': {'word': '派出所',
             'answer': 'pai4chu1suo3',
             'pinyin_syllables': ['pai4', 'chu1', 'suo3'],
             'categories': ['Livro 19 e aulas 19.1 / 19.2'],
             'examples': ['警察局和派出所在哪里？'],
             'occurrences': 1,
             'example_pinyin': 'jǐng chá jú hé pài chū suǒ zài nǎ lǐ',
             'example_translation': 'Onde ficam a delegacia e o posto policial?'},
 '19::消防队': {'word': '消防队',
             'answer': 'xiao1fang2dui4',
             'pinyin_syllables': ['xiao1', 'fang2', 'dui4'],
             'categories': ['Livro 19 e aulas 19.1 / 19.2'],
             'examples': ['消防队的消防员来了。'],
             'occurrences': 1,
             'example_pinyin': 'xiāo fáng duì de xiāo fáng yuán lái le',
             'example_translation': 'Os bombeiros do corpo de bombeiros chegaram.'},
 '19::消防员': {'word': '消防员',
             'answer': 'xiao1fang2yuan2',
             'pinyin_syllables': ['xiao1', 'fang2', 'yuan2'],
             'categories': ['Livro 19 e aulas 19.1 / 19.2'],
             'examples': ['消防队的消防员来了。'],
             'occurrences': 1,
             'example_pinyin': 'xiāo fáng duì de xiāo fáng yuán lái le',
             'example_translation': 'Os bombeiros do corpo de bombeiros chegaram.'},
 '19::失物招领处': {'word': '失物招领处',
               'answer': 'shi1wu4zhao1ling3chu4',
               'pinyin_syllables': ['shi1', 'wu4', 'zhao1', 'ling3', 'chu4'],
               'categories': ['Livro 19 e aulas 19.1 / 19.2'],
               'examples': ['我去失物招领处找手机。'],
               'occurrences': 1,
               'example_pinyin': 'wǒ qù shī wù zhāo lǐng chù zhǎo shǒu jī',
               'example_translation': 'Vou aos achados e perdidos procurar meu celular.'},
 '19::急诊': {'word': '急诊',
            'answer': 'ji2zhen3',
            'pinyin_syllables': ['ji2', 'zhen3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['这家医院有急诊和门诊。'],
            'occurrences': 1,
            'example_pinyin': 'zhè jiā yī yuàn yǒu jí zhěn hé mén zhěn',
            'example_translation': 'Este hospital tem pronto-socorro e atendimento ambulatorial.'},
 '19::门诊': {'word': '门诊',
            'answer': 'men2zhen3',
            'pinyin_syllables': ['men2', 'zhen3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['这家医院有急诊和门诊。'],
            'occurrences': 1,
            'example_pinyin': 'zhè jiā yī yuàn yǒu jí zhěn hé mén zhěn',
            'example_translation': 'Este hospital tem pronto-socorro e atendimento ambulatorial.'},
 '19::比赛': {'word': '比赛',
            'answer': 'bi3sai4',
            'pinyin_syllables': ['bi3', 'sai4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我们去看篮球比赛。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ men qù kàn lán qiú bǐ sài',
            'example_translation': 'Vamos assistir a uma partida de basquete.'},
 '19::出发': {'word': '出发',
            'answer': 'chu1fa1',
            'pinyin_syllables': ['chu1', 'fa1'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['即使现在出发，你也会迟到。'],
            'occurrences': 1,
            'example_pinyin': 'jí shǐ xiàn zài chū fā nǐ yě huì chí dào',
            'example_translation': 'Mesmo saindo agora, você vai se atrasar.'},
 '19::迟到': {'word': '迟到',
            'answer': 'chi2dao4',
            'pinyin_syllables': ['chi2', 'dao4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['即使现在出发，你也会迟到。'],
            'occurrences': 1,
            'example_pinyin': 'jí shǐ xiàn zài chū fā nǐ yě huì chí dào',
            'example_translation': 'Mesmo saindo agora, você vai se atrasar.'},
 '19::认真': {'word': '认真',
            'answer': 'ren4zhen1',
            'pinyin_syllables': ['ren4', 'zhen1'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['即使很难，我也要认真学。'],
            'occurrences': 1,
            'example_pinyin': 'jí shǐ hěn nán wǒ yě yàorèn zhēn xué',
            'example_translation': 'Mesmo sendo difícil, vou estudar com dedicação.'},
 '19::条': {'word': '条',
           'answer': 'tiao2',
           'pinyin_syllables': ['tiao2'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['这条裤子是在商店买的。'],
           'occurrences': 1,
           'example_pinyin': 'zhè tiáo kù zi shì zài shāng diàn mǎi de',
           'example_translation': 'Esta calça foi comprada na loja.'},
 '19::南京': {'word': '南京',
            'answer': 'nan2jing1',
            'pinyin_syllables': ['nan2', 'jing1'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我是坐火车去南京的。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ shì zuò huǒ chē qù nán jīng de',
            'example_translation': 'Fui a Nanquim de trem.'},
 '19::开始': {'word': '开始',
            'answer': 'kai1shi3',
            'pinyin_syllables': ['kai1', 'shi3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['你是什么时候开始学习汉语的？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ shì shén me shí hou kāi shǐ xué xí hàn yǔ de',
            'example_translation': 'Quando você começou a estudar chinês?'},
 '19::裤子': {'word': '裤子',
            'answer': 'ku4zi',
            'pinyin_syllables': ['ku4', 'zi5'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['这条裤子是在商店买的。'],
            'occurrences': 1,
            'example_pinyin': 'zhè tiáo kù zi shì zài shāng diàn mǎi de',
            'example_translation': 'Esta calça foi comprada na loja.'},
 '19::图书馆': {'word': '图书馆',
             'answer': 'tu2shu1guan3',
             'pinyin_syllables': ['tu2', 'shu1', 'guan3'],
             'categories': ['Livro 19 e aulas 19.1 / 19.2'],
             'examples': ['我是从图书馆回来的时候发现的。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ shì cóng tú shū guǎn huí lái de shí hou fā xiàn de',
             'example_translation': 'Percebi quando estava voltando da biblioteca.'},
 '19::新': {'word': '新',
           'answer': 'xin1',
           'pinyin_syllables': ['xin1'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我新买的手机丢了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ xīn mǎi de shǒu jī diū le',
           'example_translation': 'Perdi o celular que comprei recentemente.'},
 '19::买': {'word': '买',
           'answer': 'mai3',
           'pinyin_syllables': ['mai3'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我新买的手机丢了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ xīn mǎi de shǒu jī diū le',
           'example_translation': 'Perdi o celular que comprei recentemente.'},
 '19::商场': {'word': '商场',
            'answer': 'shang1chang3',
            'pinyin_syllables': ['shang1', 'chang3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['是在商场买东西的时候丢的。'],
            'occurrences': 1,
            'example_pinyin': 'shì zài shāng chǎng mǎi dōng xi de shí hou diū de',
            'example_translation': 'Perdi quando estava fazendo compras no shopping.'},
 '19::商店': {'word': '商店',
            'answer': 'shang1dian4',
            'pinyin_syllables': ['shang1', 'dian4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['这条裤子是在商店买的。'],
            'occurrences': 1,
            'example_pinyin': 'zhè tiáo kù zi shì zài shāng diàn mǎi de',
            'example_translation': 'Esta calça foi comprada na loja.'},
 '19::银行': {'word': '银行',
            'answer': 'yin2hang2',
            'pinyin_syllables': ['yin2', 'hang2'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我去银行取钱。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ qù yín háng qǔ qián',
            'example_translation': 'Vou ao banco sacar dinheiro.'},
 '19::回来': {'word': '回来',
            'answer': 'hui2lai2',
            'pinyin_syllables': ['hui2', 'lai2'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我是从图书馆回来的时候发现的。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ shì cóng tú shū guǎn huí lái de shí hou fā xiàn de',
            'example_translation': 'Percebi quando estava voltando da biblioteca.'},
 '19::发现': {'word': '发现',
            'answer': 'fa1xian4',
            'pinyin_syllables': ['fa1', 'xian4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我发现手机不见了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ fā xiàn shǒu jī bú jiàn le',
            'example_translation': 'Percebi que meu celular tinha desaparecido.'},
 '19::时候': {'word': '时候',
            'answer': 'shi2hou',
            'pinyin_syllables': ['shi2', 'hou5'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我是从图书馆回来的时候发现的。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ shì cóng tú shū guǎn huí lái de shí hou fā xiàn de',
            'example_translation': 'Percebi quando estava voltando da biblioteca.'},
 '19::交通事故': {'word': '交通事故',
              'answer': 'jiao1tong1shi4gu4',
              'pinyin_syllables': ['jiao1', 'tong1', 'shi4', 'gu4'],
              'categories': ['Livro 19 e aulas 19.1 / 19.2'],
              'examples': ['这次交通事故很严重。'],
              'occurrences': 1,
              'example_pinyin': 'zhè cì jiāo tōng shì gù hěn yán zhòng',
              'example_translation': 'Este acidente de trânsito foi grave.'},
 '19::撞': {'word': '撞',
           'answer': 'zhuang4',
           'pinyin_syllables': ['zhuang4'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['一辆车把我撞晕了。'],
           'occurrences': 1,
           'example_pinyin': 'yí liàng chē bǎ wǒ zhuàng yūn le',
           'example_translation': 'Um carro me atingiu e me fez perder a consciência.'},
 '19::把': {'word': '把',
           'answer': 'ba3',
           'pinyin_syllables': ['ba3'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['警察把女司机带走了。'],
           'occurrences': 1,
           'example_pinyin': 'jǐng chá bǎ nǚ sī jī dài zǒu le',
           'example_translation': 'A polícia levou a motorista.'},
 '19::医院': {'word': '医院',
            'answer': 'yi1yuan4',
            'pinyin_syllables': ['yi1', 'yuan4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我醒来的时候，在医院的床上躺着。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xǐng lái de shí hou zài yī yuàn de chuáng shàng tǎng zhe',
            'example_translation': 'Quando acordei, estava deitado em uma cama do hospital.'},
 '19::医生': {'word': '医生',
            'answer': 'yi1sheng1',
            'pinyin_syllables': ['yi1', 'sheng1'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['医生在医院工作。'],
            'occurrences': 1,
            'example_pinyin': 'yī shēng zài yī yuàn gōng zuò',
            'example_translation': 'O médico trabalha no hospital.'},
 '19::明天': {'word': '明天',
            'answer': 'ming2tian1',
            'pinyin_syllables': ['ming2', 'tian1'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['即使明天下雨，我也要去上课。'],
            'occurrences': 1,
            'example_pinyin': 'jí shǐ míng tiān xià yǔ wǒ yě yào qù shàng kè',
            'example_translation': 'Mesmo que chova amanhã, vou à aula.'},
 '19::上课': {'word': '上课',
            'answer': 'shang4ke4',
            'pinyin_syllables': ['shang4', 'ke4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['即使明天下雨，我也要去上课。'],
            'occurrences': 1,
            'example_pinyin': 'jí shǐ míng tiān xià yǔ wǒ yě yào qù shàng kè',
            'example_translation': 'Mesmo que chova amanhã, vou à aula.'},
 '19::打算': {'word': '打算',
            'answer': 'da3suan4',
            'pinyin_syllables': ['da3', 'suan4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我打算再买一个手机。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ dǎ suàn zài mǎi yí ge shǒu jī',
            'example_translation': 'Pretendo comprar outro celular.'},
 '19::记得': {'word': '记得',
            'answer': 'ji4de',
            'pinyin_syllables': ['ji4', 'de5'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我不记得了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ bú jì de le',
            'example_translation': 'Não me lembro mais.'},
 '19::怎么': {'word': '怎么',
            'answer': 'zen3me',
            'pinyin_syllables': ['zen3', 'me5'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['你是怎么去的？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ shì zěn me qù de',
            'example_translation': 'Como você foi?'},
 '19::一个人': {'word': '一个人',
             'answer': 'yi2geren2',
             'pinyin_syllables': ['yi2', 'ge5', 'ren2'],
             'categories': ['Livro 19 e aulas 19.1 / 19.2'],
             'examples': ['我是自己一个人去的。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ shì zì jǐ yí gerén qù de',
             'example_translation': 'Fui sozinho.'},
 '19::打电话': {'word': '打电话',
             'answer': 'da3dian4hua4',
             'pinyin_syllables': ['da3', 'dian4', 'hua4'],
             'categories': ['Livro 19 e aulas 19.1 / 19.2'],
             'examples': ['我想打电话请朋友吃饭。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ xiǎng dǎ diàn huà qǐng péng you chī fàn',
             'example_translation': 'Quero telefonar para convidar um amigo para comer.'},
 '19::可能': {'word': '可能',
            'answer': 'ke3neng2',
            'pinyin_syllables': ['ke3', 'neng2'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['小偷可能在地铁上偷走了手机。'],
            'occurrences': 1,
            'example_pinyin': 'xiǎo tōu kě néng zài dì tiě shàng tōu zǒu le shǒu jī',
            'example_translation': 'Talvez o ladrão tenha levado o celular no metrô.'},
 '19::现在': {'word': '现在',
            'answer': 'xian4zai4',
            'pinyin_syllables': ['xian4', 'zai4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我现在应该怎么办？'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xiàn zài yīng gāi zěn me bàn',
            'example_translation': 'O que devo fazer agora?'},
 '19::再': {'word': '再',
           'answer': 'zai4',
           'pinyin_syllables': ['zai4'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我打算再买一个手机。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ dǎ suàn zài mǎi yí ge shǒu jī',
           'example_translation': 'Pretendo comprar outro celular.'},
 '19::知道': {'word': '知道',
            'answer': 'zhi1dao4',
            'pinyin_syllables': ['zhi1', 'dao4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我不知道是谁偷走的。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ bù zhī dào shì shéi tōu zǒu de',
            'example_translation': 'Não sei quem o levou.'},
 '19::帮': {'word': '帮',
           'answer': 'bang1',
           'pinyin_syllables': ['bang1'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我愿意帮你复习。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ yuàn yì bāng nǐ fù xí',
           'example_translation': 'Estou disposto a ajudar você a revisar.'},
 '19::复习': {'word': '复习',
            'answer': 'fu4xi2',
            'pinyin_syllables': ['fu4', 'xi2'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我愿意帮你复习。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ yuàn yì bāng nǐ fù xí',
            'example_translation': 'Estou disposto a ajudar você a revisar.'},
 '19::旅行': {'word': '旅行',
            'answer': 'lv3xing2',
            'pinyin_syllables': ['lv3', 'xing2'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我愿意跟你一起去旅行。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ yuàn yì gēn nǐ yì qǐ qù lǚ xíng',
            'example_translation': 'Estou disposto a viajar com você.'},
 '19::路口': {'word': '路口',
            'answer': 'lu4kou3',
            'pinyin_syllables': ['lu4', 'kou3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我们骑到华山路的路口。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ men qí dào huà shān lù de lù kǒu',
            'example_translation': 'Fomos de bicicleta até o cruzamento da Rua Huashan.'},
 '19::热心': {'word': '热心',
            'answer': 're4xin1',
            'pinyin_syllables': ['re4', 'xin1'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['热心的路人叫了救护车。'],
            'occurrences': 1,
            'example_pinyin': 'rè xīn de lùrén jiào le jiù hù chē',
            'example_translation': 'Um pedestre prestativo chamou uma ambulância.'},
 '19::告诉': {'word': '告诉',
            'answer': 'gao4su',
            'pinyin_syllables': ['gao4', 'su5'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['路人告诉他应该怎么办。'],
            'occurrences': 1,
            'example_pinyin': 'lùrén gào su tā yīng gāi zěn me bàn',
            'example_translation': 'O pedestre disse a ele o que deveria fazer.'},
 '19::听说': {'word': '听说',
            'answer': 'ting1shuo1',
            'pinyin_syllables': ['ting1', 'shuo1'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['听说她是新司机，所以我愿意和解。'],
            'occurrences': 1,
            'example_pinyin': 'tīng shuō tā shì xīn sī jī suǒ yǐ wǒ yuàn yì hé jiě',
            'example_translation': 'Ouvi dizer que ela é motorista iniciante, por isso estou disposto a '
                                   'fazer as pazes.'},
 '19::所以': {'word': '所以',
            'answer': 'suo3yi3',
            'pinyin_syllables': ['suo3', 'yi3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['听说她是新司机，所以我愿意和解。'],
            'occurrences': 1,
            'example_pinyin': 'tīng shuō tā shì xīn sī jī suǒ yǐ wǒ yuàn yì hé jiě',
            'example_translation': 'Ouvi dizer que ela é motorista iniciante, por isso estou disposto a '
                                   'fazer as pazes.'},
 '19::书店': {'word': '书店',
            'answer': 'shu1dian4',
            'pinyin_syllables': ['shu1', 'dian4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['这本书是在书店买的。'],
            'occurrences': 1,
            'example_pinyin': 'zhè běn shū shì zài shū diàn mǎi de',
            'example_translation': 'Este livro foi comprado na livraria.'},
 '19::本': {'word': '本',
           'answer': 'ben3',
           'pinyin_syllables': ['ben3'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['这本书是在书店买的。'],
           'occurrences': 1,
           'example_pinyin': 'zhè běn shū shì zài shū diàn mǎi de',
           'example_translation': 'Este livro foi comprado na livraria.'},
 '19::大学': {'word': '大学',
            'answer': 'da4xue2',
            'pinyin_syllables': ['da4', 'xue2'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我的汉语是在大学学的。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de hàn yǔ shì zài dà xué xué de',
            'example_translation': 'Aprendi chinês na universidade.'},
 '19::博物馆': {'word': '博物馆',
             'answer': 'bo2wu4guan3',
             'pinyin_syllables': ['bo2', 'wu4', 'guan3'],
             'categories': ['Livro 19 e aulas 19.1 / 19.2'],
             'examples': ['我是坐地铁去博物馆的。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ shì zuò dì tiě qù bó wù guǎn de',
             'example_translation': 'Fui ao museu de metrô.'},
 '19::自行车': {'word': '自行车',
             'answer': 'zi4xing2che1',
             'pinyin_syllables': ['zi4', 'xing2', 'che1'],
             'categories': ['Livro 19 e aulas 19.1 / 19.2'],
             'examples': ['我骑自行车出去玩。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ qí zì xíng chē chū qù wán',
             'example_translation': 'Saí de bicicleta para passear.'},
 '19::害怕': {'word': '害怕',
            'answer': 'hai4pa4',
            'pinyin_syllables': ['hai4', 'pa4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我很害怕蛇。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ hěn hài pà shé',
            'example_translation': 'Tenho muito medo de cobras.'},
 '19::蛇': {'word': '蛇',
           'answer': 'she2',
           'pinyin_syllables': ['she2'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我很害怕蛇。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ hěn hài pà shé',
           'example_translation': 'Tenho muito medo de cobras.'},
 '19::看到': {'word': '看到',
            'answer': 'kan4dao4',
            'pinyin_syllables': ['kan4', 'dao4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['他看到小偷，于是马上报警了。'],
            'occurrences': 1,
            'example_pinyin': 'tā kàn dào xiǎo tōu yú shì mǎ shàng bào jǐng le',
            'example_translation': 'Ele viu o ladrão e então avisou a polícia imediatamente.'},
 '19::偷': {'word': '偷',
           'answer': 'tou1',
           'pinyin_syllables': ['tou1'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['小偷偷走了我的手机。'],
           'occurrences': 1,
           'example_pinyin': 'xiǎo tōu tōu zǒu le wǒ de shǒu jī',
           'example_translation': 'O ladrão levou meu celular.'},
 '19::于是': {'word': '于是',
            'answer': 'yu2shi4',
            'pinyin_syllables': ['yu2', 'shi4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['他看到小偷，于是马上报警了。'],
            'occurrences': 1,
            'example_pinyin': 'tā kàn dào xiǎo tōu yú shì mǎ shàng bào jǐng le',
            'example_translation': 'Ele viu o ladrão e então avisou a polícia imediatamente.'},
 '19::马上': {'word': '马上',
            'answer': 'ma3shang4',
            'pinyin_syllables': ['ma3', 'shang4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['他看到小偷，于是马上报警了。'],
            'occurrences': 1,
            'example_pinyin': 'tā kàn dào xiǎo tōu yú shì mǎ shàng bào jǐng le',
            'example_translation': 'Ele viu o ladrão e então avisou a polícia imediatamente.'},
 '19::早上': {'word': '早上',
            'answer': 'zao3shang',
            'pinyin_syllables': ['zao3', 'shang5'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['你今天早上是怎么来学校的？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ jīn tiān zǎo shang shì zěn me lái xué xiào de',
            'example_translation': 'Como você veio para a escola hoje de manhã?'},
 '19::中午': {'word': '中午',
            'answer': 'zhong1wu3',
            'pinyin_syllables': ['zhong1', 'wu3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['中午吃了午饭以后，他就去银行了。'],
            'occurrences': 1,
            'example_pinyin': 'zhōng wǔ chī le wǔ fàn yǐ hòu tā jiù qù yín háng le',
            'example_translation': 'Depois do almoço, ao meio-dia, ele foi ao banco.'},
 '19::午饭': {'word': '午饭',
            'answer': 'wu3fan4',
            'pinyin_syllables': ['wu3', 'fan4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['中午吃了午饭以后，他就去银行了。'],
            'occurrences': 1,
            'example_pinyin': 'zhōng wǔ chī le wǔ fàn yǐ hòu tā jiù qù yín háng le',
            'example_translation': 'Depois do almoço, ao meio-dia, ele foi ao banco.'},
 '19::取钱': {'word': '取钱',
            'answer': 'qu3qian2',
            'pinyin_syllables': ['qu3', 'qian2'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我去银行取钱。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ qù yín háng qǔ qián',
            'example_translation': 'Vou ao banco sacar dinheiro.'},
 '19::然后': {'word': '然后',
            'answer': 'ran2hou4',
            'pinyin_syllables': ['ran2', 'hou4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['然后他到了教室，发现钱包没有了。'],
            'occurrences': 1,
            'example_pinyin': 'rán hòu tā dào le jiào shì fā xiàn qián bāo méi yǒu le',
            'example_translation': 'Depois chegou à sala de aula e percebeu que a carteira havia sumido.'},
 '19::教室': {'word': '教室',
            'answer': 'jiao4shi4',
            'pinyin_syllables': ['jiao4', 'shi4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['然后他到了教室，发现钱包没有了。'],
            'occurrences': 1,
            'example_pinyin': 'rán hòu tā dào le jiào shì fā xiàn qián bāo méi yǒu le',
            'example_translation': 'Depois chegou à sala de aula e percebeu que a carteira havia sumido.'},
 '19::钱包': {'word': '钱包',
            'answer': 'qian2bao1',
            'pinyin_syllables': ['qian2', 'bao1'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['然后他到了教室，发现钱包没有了。'],
            'occurrences': 1,
            'example_pinyin': 'rán hòu tā dào le jiào shì fā xiàn qián bāo méi yǒu le',
            'example_translation': 'Depois chegou à sala de aula e percebeu que a carteira havia sumido.'},
 '19::幸亏': {'word': '幸亏',
            'answer': 'xing4kui1',
            'pinyin_syllables': ['xing4', 'kui1'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['幸亏你来帮忙。'],
            'occurrences': 1,
            'example_pinyin': 'xìng kuī nǐ lái bāng máng',
            'example_translation': 'Ainda bem que você veio ajudar.'},
 '19::麻烦': {'word': '麻烦',
            'answer': 'ma2fan',
            'pinyin_syllables': ['ma2', 'fan5'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['这件事很麻烦。'],
            'occurrences': 1,
            'example_pinyin': 'zhè jiàn shì hěn má fan',
            'example_translation': 'Este assunto é complicado.'},
 '19::岂有此理': {'word': '岂有此理',
              'answer': 'qi3you3ci3li3',
              'pinyin_syllables': ['qi3', 'you3', 'ci3', 'li3'],
              'categories': ['Livro 19 e aulas 19.1 / 19.2'],
              'examples': ['岂有此理！'],
              'occurrences': 1,
              'example_pinyin': 'qǐ yǒu cǐ lǐ',
              'example_translation': 'Isso é um absurdo!'},
 '19::彼此': {'word': '彼此',
            'answer': 'bi3ci3',
            'pinyin_syllables': ['bi3', 'ci3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我们彼此了解。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ men bǐ cǐ liǎo jiě',
            'example_translation': 'Nós nos entendemos mutuamente.'},
 '19::了解': {'word': '了解',
            'answer': 'liao3jie3',
            'pinyin_syllables': ['liao3', 'jie3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我们彼此了解。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ men bǐ cǐ liǎo jiě',
            'example_translation': 'Nós nos entendemos mutuamente.'},
 '19::恋恋不舍': {'word': '恋恋不舍',
              'answer': 'lian4lian4bu4she3',
              'pinyin_syllables': ['lian4', 'lian4', 'bu4', 'she3'],
              'categories': ['Livro 19 e aulas 19.1 / 19.2'],
              'examples': ['离开的时候，我恋恋不舍。'],
              'occurrences': 1,
              'example_pinyin': 'lí kāi de shí hou wǒ liàn liàn bù shě',
              'example_translation': 'Na hora de partir, relutei em ir embora.'},
 '19::倒': {'word': '倒',
           'answer': 'dao3',
           'pinyin_syllables': ['dao3'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我今天真是太倒霉了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jīn tiān zhēn shì tài dǎo méi le',
           'example_translation': 'Hoje eu realmente tive muito azar.'},
 '19::霉': {'word': '霉',
           'answer': 'mei2',
           'pinyin_syllables': ['mei2'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我今天真是太倒霉了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jīn tiān zhēn shì tài dǎo méi le',
           'example_translation': 'Hoje eu realmente tive muito azar.'},
 '19::图': {'word': '图',
           'answer': 'tu2',
           'pinyin_syllables': ['tu2'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我是从图书馆回来的时候发现的。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ shì cóng tú shū guǎn huí lái de shí hou fā xiàn de',
           'example_translation': 'Percebi quando estava voltando da biblioteca.'},
 '19::馆': {'word': '馆',
           'answer': 'guan3',
           'pinyin_syllables': ['guan3'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我是从图书馆回来的时候发现的。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ shì cóng tú shū guǎn huí lái de shí hou fā xiàn de',
           'example_translation': 'Percebi quando estava voltando da biblioteca.'},
 '19::应': {'word': '应',
           'answer': 'ying1',
           'pinyin_syllables': ['ying1'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我现在应该怎么办？'],
           'occurrences': 1,
           'example_pinyin': 'wǒ xiàn zài yīng gāi zěn me bàn',
           'example_translation': 'O que devo fazer agora?'},
 '19::该': {'word': '该',
           'answer': 'gai1',
           'pinyin_syllables': ['gai1'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我现在应该怎么办？'],
           'occurrences': 1,
           'example_pinyin': 'wǒ xiàn zài yīng gāi zěn me bàn',
           'example_translation': 'O que devo fazer agora?'},
 '19::末': {'word': '末',
           'answer': 'mo4',
           'pinyin_syllables': ['mo4'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['上个周末，我们骑车出去玩。'],
           'occurrences': 1,
           'example_pinyin': 'shàng ge zhōu mò wǒ men qí chē chū qù wán',
           'example_translation': 'No fim de semana passado saímos de bicicleta para passear.'},
 '19::车': {'word': '车',
           'answer': 'che1',
           'pinyin_syllables': ['che1'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['一辆车把我撞晕了。'],
           'occurrences': 1,
           'example_pinyin': 'yí liàng chē bǎ wǒ zhuàng yūn le',
           'example_translation': 'Um carro me atingiu e me fez perder a consciência.'},
 '19::自': {'word': '自',
           'answer': 'zi4',
           'pinyin_syllables': ['zi4'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我是自己一个人去的。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ shì zì jǐ yí gerén qù de',
           'example_translation': 'Fui sozinho.'},
 '19::己': {'word': '己',
           'answer': 'ji3',
           'pinyin_syllables': ['ji3'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我是自己一个人去的。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ shì zì jǐ yí gerén qù de',
           'example_translation': 'Fui sozinho.'},
 '19::只': {'word': '只',
           'answer': 'zhi3',
           'pinyin_syllables': ['zhi3'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['他只能自认倒霉。'],
           'occurrences': 1,
           'example_pinyin': 'tā zhǐ néng zìrèn dǎo méi',
           'example_translation': 'Ele só pode se conformar com o azar.'},
 '19::护照': {'word': '护照',
            'answer': 'hu4zhao4',
            'pinyin_syllables': ['hu4', 'zhao4'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我的护照丢了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de hù zhào diū le',
            'example_translation': 'Perdi meu passaporte.'},
 '19::银行卡': {'word': '银行卡',
             'answer': 'yin2hang2ka3',
             'pinyin_syllables': ['yin2', 'hang2', 'ka3'],
             'categories': ['Livro 19 e aulas 19.1 / 19.2'],
             'examples': ['我的银行卡不见了。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ de yín háng kǎ bú jiàn le',
             'example_translation': 'Meu cartão bancário desapareceu.'},
 '19::出租车': {'word': '出租车',
             'answer': 'chu1zu1che1',
             'pinyin_syllables': ['chu1', 'zu1', 'che1'],
             'categories': ['Livro 19 e aulas 19.1 / 19.2'],
             'examples': ['我是坐出租车去机场的。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ shì zuò chū zū chē qù jī chǎng de',
             'example_translation': 'Fui ao aeroporto de táxi.'},
 '19::机场': {'word': '机场',
            'answer': 'ji1chang3',
            'pinyin_syllables': ['ji1', 'chang3'],
            'categories': ['Livro 19 e aulas 19.1 / 19.2'],
            'examples': ['我是坐出租车去机场的。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ shì zuò chū zū chē qù jī chǎng de',
            'example_translation': 'Fui ao aeroporto de táxi.'},
 '19::要': {'word': '要',
           'answer': 'yao4',
           'pinyin_syllables': ['yao4'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['即使明天下雨，我也要去上课。'],
           'occurrences': 1,
           'example_pinyin': 'jí shǐ míng tiān xià yǔ wǒ yě yào qù shàng kè',
           'example_translation': 'Mesmo que chova amanhã, vou à aula.'},
 '19::真': {'word': '真',
           'answer': 'zhen1',
           'pinyin_syllables': ['zhen1'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['我今天真是太倒霉了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jīn tiān zhēn shì tài dǎo méi le',
           'example_translation': 'Hoje eu realmente tive muito azar.'},
 '19::就': {'word': '就',
           'answer': 'jiu4',
           'pinyin_syllables': ['jiu4'],
           'categories': ['Livro 19 e aulas 19.1 / 19.2'],
           'examples': ['中午吃了午饭以后，他就去银行了。'],
           'occurrences': 1,
           'example_pinyin': 'zhōng wǔ chī le wǔ fàn yǐ hòu tā jiù qù yín háng le',
           'example_translation': 'Depois do almoço, ao meio-dia, ele foi ao banco.'},
 '19::自己': {'word': '自己',
            'answer': 'zi4ji3',
            'pinyin_syllables': ['zi4', 'ji3'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['我是自己一个人去的。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ shì zì jǐ yí gerén qù de',
            'example_translation': 'Fui sozinho.',
            'display_pinyin': 'zì jǐ'},
 '19::请': {'word': '请',
           'answer': 'qing3',
           'pinyin_syllables': ['qing3'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['我想打电话请朋友吃饭。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ xiǎng dǎ diàn huà qǐng péng you chī fàn',
           'example_translation': 'Quero telefonar para convidar um amigo para comer.',
           'display_pinyin': 'qǐng'},
 '19::到': {'word': '到',
           'answer': 'dao4',
           'pinyin_syllables': ['dao4'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['我们骑到华山路的路口。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ men qí dào huà shān lù de lù kǒu',
           'example_translation': 'Fomos de bicicleta até o cruzamento da Rua Huashan.',
           'display_pinyin': 'dào'},
 '19::忙': {'word': '忙',
           'answer': 'mang2',
           'pinyin_syllables': ['mang2'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['幸亏你来帮忙。'],
           'occurrences': 1,
           'example_pinyin': 'xìng kuī nǐ lái bāng máng',
           'example_translation': 'Ainda bem que você veio ajudar.',
           'display_pinyin': 'máng'},
 '19::手机': {'word': '手机',
            'answer': 'shou3ji1',
            'pinyin_syllables': ['shou3', 'ji1'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['我新买的手机丢了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xīn mǎi de shǒu jī diū le',
            'example_translation': 'Perdi o celular que comprei recentemente.',
            'display_pinyin': 'shǒu jī'},
 '19::地铁': {'word': '地铁',
            'answer': 'di4tie3',
            'pinyin_syllables': ['di4', 'tie3'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['小偷可能在地铁上偷走了手机。'],
            'occurrences': 1,
            'example_pinyin': 'xiǎo tōu kě néng zài dì tiě shàng tōu zǒu le shǒu jī',
            'example_translation': 'Talvez o ladrão tenha levado o celular no metrô.',
            'display_pinyin': 'dì tiě'},
 '19::从': {'word': '从',
           'answer': 'cong2',
           'pinyin_syllables': ['cong2'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['我是从图书馆回来的时候发现的。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ shì cóng tú shū guǎn huí lái de shí hou fā xiàn de',
           'example_translation': 'Percebi quando estava voltando da biblioteca.',
           'display_pinyin': 'cóng'},
 '19::公交车': {'word': '公交车',
             'answer': 'gong1jiao1che1',
             'pinyin_syllables': ['gong1', 'jiao1', 'che1'],
             'categories': ['Revisão · Aula 19'],
             'examples': ['从这里到超市只能坐公交车。'],
             'occurrences': 1,
             'example_pinyin': 'cóng zhè lǐ dào chāo shì zhǐ néng zuò gōng jiāo chē',
             'example_translation': 'Daqui ao supermercado só é possível ir de ônibus.',
             'display_pinyin': 'gōng jiāo chē'},
 '19::东西': {'word': '东西',
            'answer': 'dong1xi',
            'pinyin_syllables': ['dong1', 'xi5'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['是在商场买东西的时候丢的。'],
            'occurrences': 1,
            'example_pinyin': 'shì zài shāng chǎng mǎi dōng xi de shí hou diū de',
            'example_translation': 'Perdi quando estava fazendo compras no shopping.',
            'display_pinyin': 'dōng xi'},
 '19::今天': {'word': '今天',
            'answer': 'jin1tian1',
            'pinyin_syllables': ['jin1', 'tian1'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['我今天真是太倒霉了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jīn tiān zhēn shì tài dǎo méi le',
            'example_translation': 'Hoje eu realmente tive muito azar.',
            'display_pinyin': 'jīn tiān'},
 '19::哪儿': {'word': '哪儿',
            'answer': 'na3r',
            'categories': ['Revisão · Aula 19'],
            'examples': ['你去哪儿跑步？', '他在哪儿游泳？', '那个篮球场在哪儿？', '你在哪儿唱卡拉OK？'],
            'occurrences': 1,
            'display_pinyin': 'nǎr',
            'answer_variants': ['nar3']},
 '19::什么': {'word': '什么',
            'answer': 'shen2me',
            'pinyin_syllables': ['shen2', 'me5'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['你是什么时候开始学习汉语的？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ shì shén me shí hou kāi shǐ xué xí hàn yǔ de',
            'example_translation': 'Quando você começou a estudar chinês?',
            'display_pinyin': 'shén me'},
 '19::什么时候': {'word': '什么时候',
              'answer': 'shen2meshi2hou',
              'pinyin_syllables': ['shen2', 'me5', 'shi2', 'hou5'],
              'categories': ['Revisão · Aula 19'],
              'examples': ['你是什么时候开始学习汉语的？'],
              'occurrences': 1,
              'example_pinyin': 'nǐ shì shén me shí hou kāi shǐ xué xí hàn yǔ de',
              'example_translation': 'Quando você começou a estudar chinês?',
              'display_pinyin': 'shén me shí hou'},
 '19::谁': {'word': '谁',
           'answer': 'shei2',
           'categories': ['Revisão · Aula 19'],
           'examples': ['我不知道是谁偷走的。'],
           'occurrences': 1,
           'display_pinyin': 'shéi',
           'example_pinyin': 'wǒ bù zhī dào shì shéi tōu zǒu de',
           'example_translation': 'Não sei quem o levou.'},
 '19::跟': {'word': '跟',
           'answer': 'gen1',
           'categories': ['Revisão · Aula 19'],
           'examples': ['我愿意跟她和解。'],
           'occurrences': 1,
           'display_pinyin': 'gēn',
           'example_pinyin': 'wǒ yuàn yì gēn tā hé jiě',
           'example_translation': 'Estou disposto a me reconciliar com ela.'},
 '19::一起': {'word': '一起',
            'answer': 'yi4qi3',
            'pinyin_syllables': ['yi4', 'qi3'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['我愿意跟你一起去旅行。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ yuàn yì gēn nǐ yì qǐ qù lǚ xíng',
            'example_translation': 'Estou disposto a viajar com você.',
            'display_pinyin': 'yì qǐ'},
 '19::朋友': {'word': '朋友',
            'answer': 'peng2you',
            'pinyin_syllables': ['peng2', 'you5'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['我的朋友当时吓坏了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de péng you dāng shí xià huài le',
            'example_translation': 'Meu amigo ficou apavorado naquele momento.',
            'display_pinyin': 'péng you'},
 '19::是': {'word': '是',
           'answer': 'shi4',
           'pinyin_syllables': ['shi4'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['我今天真是太倒霉了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jīn tiān zhēn shì tài dǎo méi le',
           'example_translation': 'Hoje eu realmente tive muito azar.',
           'display_pinyin': 'shì'},
 '19::的': {'word': '的',
           'answer': 'de',
           'pinyin_syllables': ['de5'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['我新买的手机丢了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ xīn mǎi de shǒu jī diū le',
           'example_translation': 'Perdi o celular que comprei recentemente.',
           'display_pinyin': 'de'},
 '19::在': {'word': '在',
           'answer': 'zai4',
           'pinyin_syllables': ['zai4'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['我现在应该怎么办？'],
           'occurrences': 1,
           'example_pinyin': 'wǒ xiàn zài yīng gāi zěn me bàn',
           'example_translation': 'O que devo fazer agora?',
           'display_pinyin': 'zài'},
 '19::了': {'word': '了',
           'answer': 'le',
           'categories': ['Revisão · Aula 19'],
           'examples': ['我今天真是太倒霉了。'],
           'occurrences': 1,
           'display_pinyin': 'le',
           'example_pinyin': 'wǒ jīn tiān zhēn shì tài dǎo méi le',
           'example_translation': 'Hoje eu realmente tive muito azar.'},
 '19::我': {'word': '我',
           'answer': 'wo3',
           'pinyin_syllables': ['wo3'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['我今天真是太倒霉了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jīn tiān zhēn shì tài dǎo méi le',
           'example_translation': 'Hoje eu realmente tive muito azar.',
           'display_pinyin': 'wǒ'},
 '19::你': {'word': '你',
           'answer': 'ni3',
           'pinyin_syllables': ['ni3'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['即使现在出发，你也会迟到。'],
           'occurrences': 1,
           'example_pinyin': 'jí shǐ xiàn zài chū fā nǐ yě huì chí dào',
           'example_translation': 'Mesmo saindo agora, você vai se atrasar.',
           'display_pinyin': 'nǐ'},
 '19::他': {'word': '他',
           'answer': 'ta1',
           'pinyin_syllables': ['ta1'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['他只能自认倒霉。'],
           'occurrences': 1,
           'example_pinyin': 'tā zhǐ néng zìrèn dǎo méi',
           'example_translation': 'Ele só pode se conformar com o azar.',
           'display_pinyin': 'tā'},
 '19::她': {'word': '她',
           'answer': 'ta1',
           'pinyin_syllables': ['ta1'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['我愿意跟她和解。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ yuàn yì gēn tā hé jiě',
           'example_translation': 'Estou disposto a me reconciliar com ela.',
           'display_pinyin': 'tā'},
 '19::我们': {'word': '我们',
            'answer': 'wo3men',
            'pinyin_syllables': ['wo3', 'men5'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['我们骑到华山路的路口。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ men qí dào huà shān lù de lù kǒu',
            'example_translation': 'Fomos de bicicleta até o cruzamento da Rua Huashan.',
            'display_pinyin': 'wǒ men'},
 '19::都': {'word': '都',
           'answer': 'dou1',
           'categories': ['Revisão · Aula 19'],
           'examples': ['我们的爱好不一样，但是我们都喜欢唱卡拉OK。', '我喜欢跑步，你喜欢游泳，可是我们都喜欢运动。'],
           'occurrences': 1,
           'display_pinyin': 'dōu'},
 '19::一': {'word': '一',
           'answer': 'yi1',
           'pinyin_syllables': ['yi1'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['一辆车把我撞晕了。'],
           'occurrences': 1,
           'example_pinyin': 'yí liàng chē bǎ wǒ zhuàng yūn le',
           'example_translation': 'Um carro me atingiu e me fez perder a consciência.',
           'display_pinyin': 'yī'},
 '19::个': {'word': '个',
           'answer': 'ge',
           'pinyin_syllables': ['ge5'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['我是自己一个人去的。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ shì zì jǐ yí gerén qù de',
           'example_translation': 'Fui sozinho.',
           'display_pinyin': 'ge'},
 '19::人': {'word': '人',
           'answer': 'ren2',
           'categories': ['Revisão · Aula 19'],
           'examples': ['热心的路人叫了救护车。'],
           'occurrences': 1,
           'display_pinyin': 'rén',
           'example_pinyin': 'rè xīn de lùrén jiào le jiù hù chē',
           'example_translation': 'Um pedestre prestativo chamou uma ambulância.'},
 '19::不': {'word': '不',
           'answer': 'bu4',
           'pinyin_syllables': ['bu4'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['我发现手机不见了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ fā xiàn shǒu jī bú jiàn le',
           'example_translation': 'Percebi que meu celular tinha desaparecido.',
           'display_pinyin': 'bù'},
 '19::也': {'word': '也',
           'answer': 'ye3',
           'pinyin_syllables': ['ye3'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['即使明天下雨，我也要去上课。'],
           'occurrences': 1,
           'example_pinyin': 'jí shǐ míng tiān xià yǔ wǒ yě yào qù shàng kè',
           'example_translation': 'Mesmo que chova amanhã, vou à aula.',
           'display_pinyin': 'yě'},
 '19::很': {'word': '很',
           'answer': 'hen3',
           'pinyin_syllables': ['hen3'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['这次交通事故很严重。'],
           'occurrences': 1,
           'example_pinyin': 'zhè cì jiāo tōng shì gù hěn yán zhòng',
           'example_translation': 'Este acidente de trânsito foi grave.',
           'display_pinyin': 'hěn'},
 '19::太': {'word': '太',
           'answer': 'tai4',
           'pinyin_syllables': ['tai4'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['我今天真是太倒霉了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jīn tiān zhēn shì tài dǎo méi le',
           'example_translation': 'Hoje eu realmente tive muito azar.',
           'display_pinyin': 'tài'},
 '19::只能': {'word': '只能',
            'answer': 'zhi3neng2',
            'pinyin_syllables': ['zhi3', 'neng2'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['他只能自认倒霉。'],
            'occurrences': 1,
            'example_pinyin': 'tā zhǐ néng zìrèn dǎo méi',
            'example_translation': 'Ele só pode se conformar com o azar.',
            'display_pinyin': 'zhǐ néng'},
 '19::贵': {'word': '贵',
           'answer': 'gui4',
           'pinyin_syllables': ['gui4'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['这件毛衣比那件贵一点儿。'],
           'occurrences': 1,
           'example_pinyin': 'zhè jiàn máo yī bǐ nà jiàn guì yì diǎnr',
           'example_translation': 'Este suéter é um pouco mais caro que aquele.',
           'display_pinyin': 'guì'},
 '19::下雨': {'word': '下雨',
            'answer': 'xia4yu3',
            'pinyin_syllables': ['xia4', 'yu3'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['即使明天下雨，我也要去上课。'],
            'occurrences': 1,
            'example_pinyin': 'jí shǐ míng tiān xià yǔ wǒ yě yào qù shàng kè',
            'example_translation': 'Mesmo que chova amanhã, vou à aula.',
            'display_pinyin': 'xià yǔ'},
 '19::去': {'word': '去',
           'answer': 'qu4',
           'categories': ['Revisão · Aula 19'],
           'examples': ['即使明天下雨，我也要去上课。'],
           'occurrences': 1,
           'display_pinyin': 'qù',
           'example_pinyin': 'jí shǐ míng tiān xià yǔ wǒ yě yào qù shàng kè',
           'example_translation': 'Mesmo que chova amanhã, vou à aula.'},
 '19::来': {'word': '来',
           'answer': 'lai2',
           'pinyin_syllables': ['lai2'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['他报警以后，警察来了。'],
           'occurrences': 1,
           'example_pinyin': 'tā bào jǐng yǐ hòu jǐng chá lái le',
           'example_translation': 'Depois que ele chamou a polícia, os policiais chegaram.',
           'display_pinyin': 'lái'},
 '19::吃饭': {'word': '吃饭',
            'answer': 'chi1fan4',
            'pinyin_syllables': ['chi1', 'fan4'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['我想打电话请朋友吃饭。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xiǎng dǎ diàn huà qǐng péng you chī fàn',
            'example_translation': 'Quero telefonar para convidar um amigo para comer.',
            'display_pinyin': 'chī fàn'},
 '19::和': {'word': '和',
           'answer': 'he2',
           'pinyin_syllables': ['he2'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['我愿意跟她和解。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ yuàn yì gēn tā hé jiě',
           'example_translation': 'Estou disposto a me reconciliar com ela.',
           'display_pinyin': 'hé'},
 '19::王浩明': {'word': '王浩明',
             'answer': 'wang2hao4ming2',
             'pinyin_syllables': ['wang2', 'hao4', 'ming2'],
             'categories': ['Revisão · Aula 19'],
             'examples': ['王浩明在学做西餐。'],
             'occurrences': 1,
             'example_pinyin': 'Wáng Hàomíng zài xué zuò xīcān.',
             'example_translation': 'Wang Haoming está aprendendo a preparar comida ocidental.',
             'display_pinyin': 'wáng hào míng'},
 '19::马克': {'word': '马克',
            'answer': 'ma3ke4',
            'pinyin_syllables': ['ma3', 'ke4'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['我没有马克那么高。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ méi yǒu mǎ kè nà me gāo',
            'example_translation': 'Eu não sou tão alto quanto Mark.',
            'display_pinyin': 'mǎ kè'},
 '19::想': {'word': '想',
           'answer': 'xiang3',
           'categories': ['Revisão · Aula 19'],
           'examples': ['我想打电话请朋友吃饭。'],
           'occurrences': 1,
           'display_pinyin': 'xiǎng',
           'example_pinyin': 'wǒ xiǎng dǎ diàn huà qǐng péng you chī fàn',
           'example_translation': 'Quero telefonar para convidar um amigo para comer.'},
 '19::上': {'word': '上',
           'answer': 'shang4',
           'pinyin_syllables': ['shang4'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['即使明天下雨，我也要去上课。'],
           'occurrences': 1,
           'example_pinyin': 'jí shǐ míng tiān xià yǔ wǒ yě yào qù shàng kè',
           'example_translation': 'Mesmo que chova amanhã, vou à aula.',
           'display_pinyin': 'shàng'},
 '19::周末': {'word': '周末',
            'answer': 'zhou1mo4',
            'pinyin_syllables': ['zhou1', 'mo4'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['上个周末，我们骑车出去玩。'],
            'occurrences': 1,
            'example_pinyin': 'shàng ge zhōu mò wǒ men qí chē chū qù wán',
            'example_translation': 'No fim de semana passado saímos de bicicleta para passear.',
            'display_pinyin': 'zhōu mò'},
 '19::骑车': {'word': '骑车',
            'answer': 'qi2che1',
            'categories': ['Revisão · Aula 19'],
            'examples': ['上个周末，我们骑车出去玩。'],
            'occurrences': 1,
            'display_pinyin': 'qíchē',
            'example_pinyin': 'shàng ge zhōu mò wǒ men qí chē chū qù wán',
            'example_translation': 'No fim de semana passado saímos de bicicleta para passear.'},
 '19::玩': {'word': '玩',
           'answer': 'wan2',
           'pinyin_syllables': ['wan2'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['我骑自行车出去玩。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ qí zì xíng chē chū qù wán',
           'example_translation': 'Saí de bicicleta para passear.',
           'display_pinyin': 'wán'},
 '19::当时': {'word': '当时',
            'answer': 'dang1shi2',
            'pinyin_syllables': ['dang1', 'shi2'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['我的朋友当时吓坏了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de péng you dāng shí xià huài le',
            'example_translation': 'Meu amigo ficou apavorado naquele momento.',
            'display_pinyin': 'dāng shí'},
 '19::说': {'word': '说',
           'answer': 'shuo1',
           'pinyin_syllables': ['shuo1'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['听说她是新司机，所以我愿意和解。'],
           'occurrences': 1,
           'example_pinyin': 'tīng shuō tā shì xīn sī jī suǒ yǐ wǒ yuàn yì hé jiě',
           'example_translation': 'Ouvi dizer que ela é motorista iniciante, por isso estou disposto a fazer '
                                  'as pazes.',
           'display_pinyin': 'shuō'},
 '19::叫': {'word': '叫',
           'answer': 'jiao4',
           'pinyin_syllables': ['jiao4'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['热心的路人叫了救护车。'],
           'occurrences': 1,
           'example_pinyin': 'rè xīn de lùrén jiào le jiù hù chē',
           'example_translation': 'Um pedestre prestativo chamou uma ambulância.',
           'display_pinyin': 'jiào'},
 '19::还': {'word': '还',
           'answer': 'hai2',
           'categories': ['Revisão · Aula 19'],
           'examples': ['今天刮风，还打雷。'],
           'occurrences': 1,
           'display_pinyin': 'hái',
           'example_pinyin': 'jīn tiān guā fēng hái dǎ léi',
           'example_translation': 'Hoje está ventando e também está trovejando.'},
 '19::学': {'word': '学',
           'answer': 'xue2',
           'pinyin_syllables': ['xue2'],
           'categories': ['Revisão · Aula 19'],
           'examples': ['即使很难，我也要认真学。'],
           'occurrences': 1,
           'example_pinyin': 'jí shǐ hěn nán wǒ yě yàorèn zhēn xué',
           'example_translation': 'Mesmo sendo difícil, vou estudar com dedicação.',
           'display_pinyin': 'xué'},
 '19::汉语': {'word': '汉语',
            'answer': 'han4yu3',
            'pinyin_syllables': ['han4', 'yu3'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['你是什么时候开始学习汉语的？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ shì shén me shí hou kāi shǐ xué xí hàn yǔ de',
            'example_translation': 'Quando você começou a estudar chinês?',
            'display_pinyin': 'hàn yǔ'},
 '19::电影': {'word': '电影',
            'answer': 'dian4ying3',
            'categories': ['Revisão · Aula 19'],
            'examples': ['我喜欢去电影院看电影。', '你跟谁去电影院看电影？', '你为什么不喜欢去电影院看电影？', '他有很多爱好，比如打网球、打乒乓球和看电影。'],
            'occurrences': 1,
            'display_pinyin': 'diànyǐng'},
 '19::电影院': {'word': '电影院',
             'answer': 'dian4ying3yuan4',
             'categories': ['Revisão · Aula 19'],
             'examples': ['我喜欢去电影院看电影。', '你跟谁去电影院看电影？', '你为什么不喜欢去电影院看电影？', '你除了去电影院，还喜欢去哪儿？'],
             'occurrences': 1,
             'display_pinyin': 'diànyǐngyuàn'},
 '19::北京': {'word': '北京',
            'answer': 'bei3jing1',
            'pinyin_syllables': ['bei3', 'jing1'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['上海的夏天比北京的夏天热。'],
            'occurrences': 1,
            'example_pinyin': 'shàng hǎi de xià tiān bǐ běi jīng de xià tiānrè',
            'example_translation': 'O verão de Xangai é mais quente que o de Pequim.',
            'display_pinyin': 'běi jīng'},
 '19::飞机': {'word': '飞机',
            'answer': 'fei1ji1',
            'pinyin_syllables': ['fei1', 'ji1'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['飞机比火车快。'],
            'occurrences': 1,
            'example_pinyin': 'fēi jī bǐ huǒ chē kuài',
            'example_translation': 'O avião é mais rápido que o trem.',
            'display_pinyin': 'fēi jī'},
 '19::火车': {'word': '火车',
            'answer': 'huo3che1',
            'pinyin_syllables': ['huo3', 'che1'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['我是坐火车去南京的。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ shì zuò huǒ chē qù nán jīng de',
            'example_translation': 'Fui a Nanquim de trem.',
            'display_pinyin': 'huǒ chē'},
 '19::学校': {'word': '学校',
            'answer': 'xue2xiao4',
            'pinyin_syllables': ['xue2', 'xiao4'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['你今天早上是怎么来学校的？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ jīn tiān zǎo shang shì zěn me lái xué xiào de',
            'example_translation': 'Como você veio para a escola hoje de manhã?',
            'display_pinyin': 'xué xiào'},
 '19::走路': {'word': '走路',
            'answer': 'zou3lu4',
            'pinyin_syllables': ['zou3', 'lu4'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['我家离学校不远，可以走路去。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jiā lí xué xiào bù yuǎn kě yǐ zǒu lù qù',
            'example_translation': 'Minha casa não fica longe da escola; dá para ir a pé.',
            'display_pinyin': 'zǒu lù'},
 '19::学习': {'word': '学习',
            'answer': 'xue2xi2',
            'pinyin_syllables': ['xue2', 'xi2'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['你是什么时候开始学习汉语的？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ shì shén me shí hou kāi shǐ xué xí hàn yǔ de',
            'example_translation': 'Quando você começou a estudar chinês?',
            'display_pinyin': 'xué xí'},
 '19::国家': {'word': '国家',
            'answer': 'guo2jia1',
            'pinyin_syllables': ['guo2', 'jia1'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['你国家的东西贵吗？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ guó jiā de dōng xi guì ma',
            'example_translation': 'As coisas no seu país são caras?',
            'display_pinyin': 'guó jiā'},
 '19::哪个': {'word': '哪个',
            'answer': 'na3ge',
            'pinyin_syllables': ['na3', 'ge5'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['哪个更好吃？'],
            'occurrences': 1,
            'example_pinyin': 'nǎ ge gèng hǎo chī',
            'example_translation': 'Qual é mais gostoso?',
            'display_pinyin': 'nǎ ge'},
 '19::昨天': {'word': '昨天',
            'answer': 'zuo2tian1',
            'pinyin_syllables': ['zuo2', 'tian1'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['昨天十八度，今天二十度。'],
            'occurrences': 1,
            'example_pinyin': 'zuó tiān shí bā dù jīn tiān èr shí dù',
            'example_translation': 'Ontem fez dezoito graus; hoje faz vinte.',
            'display_pinyin': 'zuó tiān'},
 '19::踢': {'word': '踢',
           'answer': 'ti1',
           'categories': ['Revisão · Aula 19'],
           'examples': ['大家喜欢踢足球。', '我不太喜欢踢足球。', '你喜欢踢足球，但是更喜欢打网球吗？', '我们每周去足球场踢足球。'],
           'occurrences': 1,
           'display_pinyin': 'tī'},
 '19::足球': {'word': '足球',
            'answer': 'zu2qiu2',
            'categories': ['Revisão · Aula 19'],
            'examples': ['大家喜欢踢足球。', '我不太喜欢踢足球。', '你喜欢踢足球，但是更喜欢打网球吗？', '我们每周去足球场踢足球。'],
            'occurrences': 1,
            'display_pinyin': 'zúqiú'},
 '19::正在': {'word': '正在',
            'answer': 'zheng4zai4',
            'pinyin_syllables': ['zheng4', 'zai4'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['她在椅子上坐着，正在写书法。'],
            'occurrences': 1,
            'example_pinyin': 'tā zài yǐzi shàng zuò zhe, zhèngzài xiě shūfǎ.',
            'example_translation': 'Ela está sentada na cadeira, escrevendo caligrafia.',
            'display_pinyin': 'zhèng zài'},
 '19::以后': {'word': '以后',
            'answer': 'yi3hou4',
            'categories': ['Revisão · Aula 19'],
            'examples': ['他报警以后，警察来了。'],
            'occurrences': 1,
            'display_pinyin': 'yǐhòu',
            'example_pinyin': 'tā bào jǐng yǐ hòu jǐng chá lái le',
            'example_translation': 'Depois que ele chamou a polícia, os policiais chegaram.'},
 '19::但是': {'word': '但是',
            'answer': 'dan4shi4',
            'pinyin_syllables': ['dan4', 'shi4'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['书法很难，但是我学得还可以。'],
            'occurrences': 1,
            'example_pinyin': 'shūfǎ hěn nán, dànshì wǒ xué de hái kěyǐ.',
            'example_translation': 'Caligrafia é difícil, mas estou aprendendo razoavelmente bem.',
            'display_pinyin': 'dàn shì'},
 '19::老师': {'word': '老师',
            'answer': 'lao3shi1',
            'categories': ['Revisão · Aula 19'],
            'examples': ['老师告诉我，学汉语很有趣。'],
            'occurrences': 1,
            'display_pinyin': 'lǎoshī'},
 '19::没有': {'word': '没有',
            'answer': 'mei2you3',
            'pinyin_syllables': ['mei2', 'you3'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['然后他到了教室，发现钱包没有了。'],
            'occurrences': 1,
            'example_pinyin': 'rán hòu tā dào le jiào shì fā xiàn qián bāo méi yǒu le',
            'example_translation': 'Depois chegou à sala de aula e percebeu que a carteira havia sumido.',
            'display_pinyin': 'méi yǒu'},
 '19::李佳': {'word': '李佳',
            'answer': 'li3jia1',
            'pinyin_syllables': ['li3', 'jia1'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['李佳请马克吃饭。'],
            'occurrences': 1,
            'example_pinyin': 'lǐ jiā qǐng mǎ kè chī fàn',
            'example_translation': 'Li Jia convida Mark para comer.',
            'display_pinyin': 'lǐ jiā'},
 '19::日记': {'word': '日记',
            'answer': 'ri4ji4',
            'pinyin_syllables': ['ri4', 'ji4'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['马克每天写日记。'],
            'occurrences': 1,
            'example_pinyin': 'mǎ kè měi tiān xiěrì jì',
            'example_translation': 'Mark escreve no diário todos os dias.',
            'display_pinyin': 'rì jì'},
 '19::篮球': {'word': '篮球',
            'answer': 'lan2qiu2',
            'pinyin_syllables': ['lan2', 'qiu2'],
            'categories': ['Revisão · Aula 19'],
            'examples': ['我们去看篮球比赛。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ men qù kàn lán qiú bǐ sài',
            'example_translation': 'Vamos assistir a uma partida de basquete.',
            'display_pinyin': 'lán qiú'},
 '19::怎么样': {'word': '怎么样',
             'answer': 'zen3meyang4',
             'pinyin_syllables': ['zen3', 'me5', 'yang4'],
             'categories': ['Revisão · Aula 19'],
             'examples': ['好久不见，你最近怎么样？'],
             'occurrences': 1,
             'example_pinyin': 'hǎojiǔ bújiàn, nǐ zuìjìn zěnme yàng?',
             'example_translation': 'Há quanto tempo! Como você tem passado?',
             'display_pinyin': 'zěn me yàng'}}
LESSON19_TRANSLATIONS = {'19::倒霉': 'ter azar; azarado',
 '19::丢': 'perder (um objeto)',
 '19::不见': 'desaparecer; sumir',
 '19::小偷': 'ladrão',
 '19::偷走': 'furtar; levar escondido',
 '19::应该': 'dever; ser recomendável',
 '19::怎么办': 'o que fazer',
 '19::自认倒霉': 'conformar-se com o próprio azar',
 '19::即使': 'mesmo que; ainda que',
 '19::报警': 'avisar a polícia; chamar a polícia',
 '19::警察': 'policial; polícia',
 '19::骑': 'andar montado; andar de bicicleta',
 '19::出去': 'sair; ir para fora',
 '19::辆': 'classificador de veículos',
 '19::撞晕': 'atingir e deixar inconsciente',
 '19::吓坏': 'assustar muito; apavorar',
 '19::路人': 'pedestre; transeunte',
 '19::救护车': 'ambulância',
 '19::醒来': 'acordar; recobrar a consciência',
 '19::床': 'cama',
 '19::躺': 'deitar; estar deitado',
 '19::腿': 'perna',
 '19::受伤': 'machucar-se; ficar ferido',
 '19::女': 'mulher; feminino',
 '19::司机': 'motorista',
 '19::带走': 'levar embora',
 '19::严重': 'grave; sério',
 '19::愿意': 'estar disposto a; querer',
 '19::和解': 'reconciliar-se; chegar a um acordo',
 '19::华山路': 'Rua Huashan',
 '19::警察局': 'delegacia de polícia',
 '19::派出所': 'posto policial; delegacia local',
 '19::消防队': 'corpo de bombeiros',
 '19::消防员': 'bombeiro',
 '19::失物招领处': 'setor de achados e perdidos',
 '19::急诊': 'pronto-socorro; atendimento de urgência',
 '19::门诊': 'atendimento ambulatorial',
 '19::比赛': 'partida; competição',
 '19::出发': 'partir; sair em viagem',
 '19::迟到': 'chegar atrasado',
 '19::认真': 'atento; sério; dedicado',
 '19::条': 'classificador de objetos compridos, como calças',
 '19::南京': 'Nanquim',
 '19::开始': 'começar',
 '19::裤子': 'calça',
 '19::图书馆': 'biblioteca',
 '19::新': 'novo; recentemente',
 '19::买': 'comprar',
 '19::商场': 'shopping; centro comercial',
 '19::商店': 'loja',
 '19::银行': 'banco (instituição financeira)',
 '19::回来': 'voltar; retornar',
 '19::发现': 'descobrir; perceber',
 '19::时候': 'momento; ocasião',
 '19::交通事故': 'acidente de trânsito',
 '19::撞': 'bater; colidir; atingir',
 '19::把': 'partícula que antepõe o objeto à ação',
 '19::医院': 'hospital',
 '19::医生': 'médico',
 '19::明天': 'amanhã',
 '19::上课': 'ter aula; assistir à aula',
 '19::打算': 'planejar; pretender',
 '19::记得': 'lembrar-se',
 '19::怎么': 'como; de que maneira',
 '19::一个人': 'uma pessoa; sozinho',
 '19::打电话': 'telefonar',
 '19::可能': 'talvez; possível',
 '19::现在': 'agora',
 '19::再': 'de novo; outra vez',
 '19::知道': 'saber',
 '19::帮': 'ajudar',
 '19::复习': 'revisar; recapitular',
 '19::旅行': 'viajar; viagem',
 '19::路口': 'cruzamento; interseção',
 '19::热心': 'prestativo; solícito',
 '19::告诉': 'dizer; contar; informar',
 '19::听说': 'ouvir dizer',
 '19::所以': 'por isso; portanto',
 '19::书店': 'livraria',
 '19::本': 'classificador de livros',
 '19::大学': 'universidade',
 '19::博物馆': 'museu',
 '19::自行车': 'bicicleta',
 '19::害怕': 'ter medo',
 '19::蛇': 'cobra; serpente',
 '19::看到': 'ver; avistar',
 '19::偷': 'furtar; roubar às escondidas',
 '19::于是': 'então; em consequência',
 '19::马上': 'imediatamente',
 '19::早上': 'de manhã; manhã',
 '19::中午': 'meio-dia',
 '19::午饭': 'almoço',
 '19::取钱': 'sacar dinheiro',
 '19::然后': 'depois; em seguida',
 '19::教室': 'sala de aula',
 '19::钱包': 'carteira',
 '19::幸亏': 'ainda bem que; felizmente',
 '19::麻烦': 'complicado; incômodo; problema',
 '19::岂有此理': 'isso é um absurdo',
 '19::彼此': 'um ao outro; mutuamente',
 '19::了解': 'entender; conhecer',
 '19::恋恋不舍': 'relutar em se separar; não querer partir',
 '19::倒': 'cair; elemento de 倒霉',
 '19::霉': 'mofo; elemento de 倒霉 (azar)',
 '19::图': 'imagem; elemento de 图书馆',
 '19::馆': 'edifício ou estabelecimento; elemento de 图书馆',
 '19::应': 'dever; elemento de 应该',
 '19::该': 'dever; elemento de 应该',
 '19::末': 'fim; elemento de 周末',
 '19::车': 'veículo; carro',
 '19::自': 'próprio; elemento de 自己',
 '19::己': 'si mesmo; elemento de 自己',
 '19::只': 'somente; apenas',
 '19::护照': 'passaporte',
 '19::银行卡': 'cartão bancário',
 '19::出租车': 'táxi',
 '19::机场': 'aeroporto',
 '19::要': 'querer; precisar; ir fazer',
 '19::真': 'realmente; de fato',
 '19::就': 'então; logo; já',
 '19::自己': 'si mesmo; próprio',
 '19::请': 'por favor; convidar',
 '19::到': 'chegar; até; para',
 '19::忙': 'ocupado',
 '19::手机': 'celular',
 '19::地铁': 'metrô',
 '19::从': 'de; a partir de',
 '19::公交车': 'ônibus urbano',
 '19::东西': 'coisa; objeto',
 '19::今天': 'hoje',
 '19::哪儿': 'onde',
 '19::什么': 'o que; que',
 '19::什么时候': 'quando',
 '19::谁': 'quem',
 '19::跟': 'com; junto com',
 '19::一起': 'junto(s)',
 '19::朋友': 'amigo(a)',
 '19::是': 'ser; estar',
 '19::的': 'partícula de posse ou atribuição',
 '19::在': 'estar em; estar fazendo',
 '19::了': 'partícula de ação concluída ou mudança',
 '19::我': 'eu',
 '19::你': 'você',
 '19::他': 'ele',
 '19::她': 'ela',
 '19::我们': 'nós',
 '19::都': 'todos; ambos',
 '19::一': 'um; uma',
 '19::个': 'classificador geral',
 '19::人': 'pessoa(s)',
 '19::不': 'não',
 '19::也': 'também',
 '19::很': 'muito',
 '19::太': 'demais; muito',
 '19::只能': 'só poder; apenas conseguir',
 '19::贵': 'caro',
 '19::下雨': 'chover',
 '19::去': 'ir',
 '19::来': 'vir',
 '19::吃饭': 'comer; fazer uma refeição',
 '19::和': 'e; com',
 '19::王浩明': 'Wang Haoming (nome próprio)',
 '19::马克': 'Mark (nome próprio)',
 '19::想': 'querer; ter vontade de',
 '19::上': 'sobre; em cima de',
 '19::周末': 'fim de semana',
 '19::骑车': 'andar de bicicleta',
 '19::玩': 'brincar; jogar',
 '19::当时': 'naquele momento; naquela época',
 '19::说': 'falar; dizer',
 '19::叫': 'chamar; pedir (comida)',
 '19::还': 'ainda; além disso; também',
 '19::学': 'aprender; estudar',
 '19::汉语': 'língua chinesa; mandarim',
 '19::电影': 'filme',
 '19::电影院': 'cinema',
 '19::北京': 'Pequim',
 '19::飞机': 'avião',
 '19::火车': 'trem',
 '19::学校': 'escola',
 '19::走路': 'andar a pé; caminhar',
 '19::学习': 'estudar; aprender',
 '19::国家': 'país',
 '19::哪个': 'qual',
 '19::昨天': 'ontem',
 '19::踢': 'chutar; jogar (futebol)',
 '19::足球': 'futebol',
 '19::正在': 'estar fazendo algo neste momento',
 '19::以后': 'depois; após',
 '19::但是': 'mas; porém',
 '19::老师': 'professor(a)',
 '19::没有': 'não ter; não ser tão... quanto',
 '19::李佳': 'Li Jia (nome próprio)',
 '19::日记': 'diário pessoal',
 '19::篮球': 'basquete',
 '19::怎么样': 'como; de que maneira; como vai'}
BLOCK19_WORDS = list(LESSON19_CARDS)
CARDS.update(LESSON19_CARDS)
WORD_TRANSLATIONS.update(LESSON19_TRANSLATIONS)
for _cid, _card in LESSON19_CARDS.items():
    WORD_PINYIN[_cid] = _card['answer']
    if 'example_translation' in _card:
        EXAMPLE_TRANSLATIONS.setdefault(_card['examples'][0], _card['example_translation'])


# Aula 20: IDs separados preservam o progresso de palavras comuns a outras aulas.
LESSON20_CARDS = {'20::面试': {'word': '面试',
            'answer': 'mian4shi4',
            'pinyin_syllables': ['mian4', 'shi4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我明天去面试。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ míng tiān qù miàn shì',
            'example_translation': 'Amanhã vou a uma entrevista.'},
 '20::交流': {'word': '交流',
            'answer': 'jiao1liu2',
            'pinyin_syllables': ['jiao1', 'liu2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我经常跟中国朋友交流。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jīng cháng gēn zhōng guó péng you jiāo liú',
            'example_translation': 'Costumo conversar com amigos chineses.'},
 '20::以前': {'word': '以前',
            'answer': 'yi3qian2',
            'pinyin_syllables': ['yi3', 'qian2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['你以前教过英语吗？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ yǐ qián jiāo guò yīng yǔ ma',
            'example_translation': 'Você já ensinou inglês antes?'},
 '20::教': {'word': '教',
           'answer': 'jiao1',
           'pinyin_syllables': ['jiao1'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['你以前教过英语吗？'],
           'occurrences': 1,
           'example_pinyin': 'nǐ yǐ qián jiāo guò yīng yǔ ma',
           'example_translation': 'Você já ensinou inglês antes?'},
 '20::发音': {'word': '发音',
            'answer': 'fa1yin1',
            'pinyin_syllables': ['fa1', 'yin1'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的发音很清楚，说得很慢。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de fā yīn hěn qīng chu shuō de hěn màn',
            'example_translation': 'Minha pronúncia é clara e falo devagar.'},
 '20::清楚': {'word': '清楚',
            'answer': 'qing1chu',
            'pinyin_syllables': ['qing1', 'chu5'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的发音很清楚，说得很慢。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de fā yīn hěn qīng chu shuō de hěn màn',
            'example_translation': 'Minha pronúncia é clara e falo devagar.'},
 '20::慢': {'word': '慢',
           'answer': 'man4',
           'pinyin_syllables': ['man4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我的发音很清楚，说得很慢。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ de fā yīn hěn qīng chu shuō de hěn màn',
           'example_translation': 'Minha pronúncia é clara e falo devagar.'},
 '20::懂': {'word': '懂',
           'answer': 'dong3',
           'pinyin_syllables': ['dong3'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['小朋友都能听懂。'],
           'occurrences': 1,
           'example_pinyin': 'xiǎo péng you dōu néng tīng dǒng',
           'example_translation': 'Todas as crianças conseguem entender o que ouvem.'},
 '20::如果': {'word': '如果',
            'answer': 'ru2guo3',
            'pinyin_syllables': ['ru2', 'guo3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['如果你没听懂，我会再讲一遍。'],
            'occurrences': 1,
            'example_pinyin': 'rú guǒ nǐ méi tīng dǒng wǒ huì zài jiǎng yí biàn',
            'example_translation': 'Se você não entendeu, vou explicar mais uma vez.'},
 '20::讲': {'word': '讲',
           'answer': 'jiang3',
           'pinyin_syllables': ['jiang3'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我会再讲一遍，或者换一个方法。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ huì zài jiǎng yí biàn huò zhě huàn yí ge fāng fǎ',
           'example_translation': 'Vou explicar outra vez ou mudar de método.'},
 '20::或者': {'word': '或者',
            'answer': 'huo4zhe3',
            'pinyin_syllables': ['huo4', 'zhe3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我会再讲一遍，或者换一个方法。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ huì zài jiǎng yí biàn huò zhě huàn yí ge fāng fǎ',
            'example_translation': 'Vou explicar outra vez ou mudar de método.'},
 '20::方法': {'word': '方法',
            'answer': 'fang1fa3',
            'pinyin_syllables': ['fang1', 'fa3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我会再讲一遍，或者换一个方法。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ huì zài jiǎng yí biàn huò zhě huàn yí ge fāng fǎ',
            'example_translation': 'Vou explicar outra vez ou mudar de método.'},
 '20::优点': {'word': '优点',
            'answer': 'you1dian3',
            'pinyin_syllables': ['you1', 'dian3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['你还有别的优点吗？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ hái yǒu bié de yōu diǎn ma',
            'example_translation': 'Você tem outras qualidades?'},
 '20::幽默': {'word': '幽默',
            'answer': 'you1mo4',
            'pinyin_syllables': ['you1', 'mo4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我很幽默，学生们都很喜欢我。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ hěn yōu mò xué sheng men dōu hěn xǐ huan wǒ',
            'example_translation': 'Sou bem-humorado e todos os alunos gostam de mim.'},
 '20::故事': {'word': '故事',
            'answer': 'gu4shi',
            'pinyin_syllables': ['gu4', 'shi5'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我会给学生讲英文故事。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ huì gěi xué sheng jiǎng yīng wén gù shi',
            'example_translation': 'Vou contar histórias em inglês aos alunos.'},
 '20::当然': {'word': '当然',
            'answer': 'dang1ran2',
            'pinyin_syllables': ['dang1', 'ran2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['当然，我能准备好明天的面试。'],
            'occurrences': 1,
            'example_pinyin': 'dāngrán wǒ néng zhǔn bèi hǎo míng tiān de miàn shì',
            'example_translation': 'Claro, consigo me preparar bem para a entrevista de amanhã.'},
 '20::准备': {'word': '准备',
            'answer': 'zhun3bei4',
            'pinyin_syllables': ['zhun3', 'bei4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['当然，我能准备好明天的面试。'],
            'occurrences': 1,
            'example_pinyin': 'dāngrán wǒ néng zhǔn bèi hǎo míng tiān de miàn shì',
            'example_translation': 'Claro, consigo me preparar bem para a entrevista de amanhã.'},
 '20::已经': {'word': '已经',
            'answer': 'yi3jing1',
            'pinyin_syllables': ['yi3', 'jing1'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我来中国已经很久了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ lái zhōng guó yǐ jīng hěn jiǔ le',
            'example_translation': 'Já faz muito tempo que cheguei à China.'},
 '20::久': {'word': '久',
           'answer': 'jiu3',
           'pinyin_syllables': ['jiu3'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我来中国已经很久了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ lái zhōng guó yǐ jīng hěn jiǔ le',
           'example_translation': 'Já faz muito tempo que cheguei à China.'},
 '20::份': {'word': '份',
           'answer': 'fen4',
           'pinyin_syllables': ['fen4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我找到了一份兼职工作。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ zhǎo dào le yí fèn jiān zhí gōng zuò',
           'example_translation': 'Consegui um emprego de meio período.'},
 '20::兼职': {'word': '兼职',
            'answer': 'jian1zhi2',
            'pinyin_syllables': ['jian1', 'zhi2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我找到了一份兼职工作。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ zhǎo dào le yí fèn jiān zhí gōng zuò',
            'example_translation': 'Consegui um emprego de meio período.'},
 '20::曾经': {'word': '曾经',
            'answer': 'ceng2jing1',
            'pinyin_syllables': ['ceng2', 'jing1'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我曾经教过中国学生。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ céng jīng jiāo guò zhōng guó xué sheng',
            'example_translation': 'Já ensinei alunos chineses.'},
 '20::对…来说': {'word': '对…来说',
              'answer': 'dui4lai2shuo1',
              'pinyin_syllables': ['dui4', 'lai2', 'shuo1'],
              'categories': ['Livro 20 e aulas 20.1 / 20.2'],
              'examples': ['对我来说，这份工作不太容易。'],
              'occurrences': 1,
              'example_pinyin': 'duì wǒ lái shuō zhè fèn gōng zuò bú tàiróng yì',
              'example_translation': 'Para mim, esse trabalho não é muito fácil.'},
 '20::容易': {'word': '容易',
            'answer': 'rong2yi4',
            'pinyin_syllables': ['rong2', 'yi4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['对我来说，这份工作不太容易。'],
            'occurrences': 1,
            'example_pinyin': 'duì wǒ lái shuō zhè fèn gōng zuò bú tàiróng yì',
            'example_translation': 'Para mim, esse trabalho não é muito fácil.'},
 '20::信心': {'word': '信心',
            'answer': 'xin4xin1',
            'pinyin_syllables': ['xin4', 'xin1'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的老板对我很有信心。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de lǎo bǎn duì wǒ hěn yǒu xìn xīn',
            'example_translation': 'Meu chefe tem muita confiança em mim.'},
 '20::虽然': {'word': '虽然',
            'answer': 'sui1ran2',
            'pinyin_syllables': ['sui1', 'ran2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['虽然时间很紧，不过我一个晚上就能准备好。'],
            'occurrences': 1,
            'example_pinyin': 'suīrán shí jiān hěn jǐn bú guò wǒ yí ge wǎn shang jiù néng zhǔn bèi hǎo',
            'example_translation': 'Embora o tempo seja curto, consigo me preparar em uma noite.'},
 '20::紧': {'word': '紧',
           'answer': 'jin3',
           'pinyin_syllables': ['jin3'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['虽然时间很紧，不过我一个晚上就能准备好。'],
           'occurrences': 1,
           'example_pinyin': 'suīrán shí jiān hěn jǐn bú guò wǒ yí ge wǎn shang jiù néng zhǔn bèi hǎo',
           'example_translation': 'Embora o tempo seja curto, consigo me preparar em uma noite.'},
 '20::有意思': {'word': '有意思',
             'answer': 'you3yi4si',
             'pinyin_syllables': ['you3', 'yi4', 'si5'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['教英语很有意思。'],
             'occurrences': 1,
             'example_pinyin': 'jiāo yīng yǔ hěn yǒu yì si',
             'example_translation': 'Ensinar inglês é muito interessante.'},
 '20::家人': {'word': '家人',
            'answer': 'jia1ren2',
            'pinyin_syllables': ['jia1', 'ren2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的家人很包容，也很体贴。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de jiārén hěn bāoróng yě hěn tǐ tiē',
            'example_translation': 'Minha família é tolerante e atenciosa.'},
 '20::包容': {'word': '包容',
            'answer': 'bao1rong2',
            'pinyin_syllables': ['bao1', 'rong2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的家人很包容，也很体贴。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de jiārén hěn bāoróng yě hěn tǐ tiē',
            'example_translation': 'Minha família é tolerante e atenciosa.'},
 '20::体贴': {'word': '体贴',
            'answer': 'ti3tie1',
            'pinyin_syllables': ['ti3', 'tie1'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的家人很包容，也很体贴。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de jiārén hěn bāoróng yě hěn tǐ tiē',
            'example_translation': 'Minha família é tolerante e atenciosa.'},
 '20::孝心': {'word': '孝心',
            'answer': 'xiao4xin1',
            'pinyin_syllables': ['xiao4', 'xin1'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['他很有孝心。'],
            'occurrences': 1,
            'example_pinyin': 'tā hěn yǒu xiào xīn',
            'example_translation': 'Ele é muito dedicado aos pais.'},
 '20::真诚': {'word': '真诚',
            'answer': 'zhen1cheng2',
            'pinyin_syllables': ['zhen1', 'cheng2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的朋友真诚、善良、热情。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de péng you zhēn chéng shàn liángrè qíng',
            'example_translation': 'Meu amigo é sincero, bondoso e caloroso.'},
 '20::善良': {'word': '善良',
            'answer': 'shan4liang2',
            'pinyin_syllables': ['shan4', 'liang2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的朋友真诚、善良、热情。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de péng you zhēn chéng shàn liángrè qíng',
            'example_translation': 'Meu amigo é sincero, bondoso e caloroso.'},
 '20::热情': {'word': '热情',
            'answer': 're4qing2',
            'pinyin_syllables': ['re4', 'qing2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的朋友真诚、善良、热情。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de péng you zhēn chéng shàn liángrè qíng',
            'example_translation': 'Meu amigo é sincero, bondoso e caloroso.'},
 '20::勤奋': {'word': '勤奋',
            'answer': 'qin2fen4',
            'pinyin_syllables': ['qin2', 'fen4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的同事认真、勤奋、有责任心。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de tóng shìrèn zhēn qín fèn yǒu zérèn xīn',
            'example_translation': 'Meu colega é dedicado, esforçado e responsável.'},
 '20::责任心': {'word': '责任心',
             'answer': 'ze2ren4xin1',
             'pinyin_syllables': ['ze2', 'ren4', 'xin1'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['我的同事认真、勤奋、有责任心。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ de tóng shìrèn zhēn qín fèn yǒu zérèn xīn',
             'example_translation': 'Meu colega é dedicado, esforçado e responsável.'},
 '20::渴': {'word': '渴',
           'answer': 'ke3',
           'pinyin_syllables': ['ke3'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我很渴，想喝水。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ hěn kě xiǎng hē shuǐ',
           'example_translation': 'Estou com muita sede e quero beber água.'},
 '20::累': {'word': '累',
           'answer': 'lei4',
           'pinyin_syllables': ['lei4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['如果我很累，我会休息。'],
           'occurrences': 1,
           'example_pinyin': 'rú guǒ wǒ hěn lèi wǒ huì xiū xi',
           'example_translation': 'Se eu estiver muito cansado, vou descansar.'},
 '20::手表': {'word': '手表',
            'answer': 'shou3biao3',
            'pinyin_syllables': ['shou3', 'biao3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['这块手表很重。'],
            'occurrences': 1,
            'example_pinyin': 'zhè kuài shǒu biǎo hěn zhòng',
            'example_translation': 'Este relógio de pulso é pesado.'},
 '20::重': {'word': '重',
           'answer': 'zhong4',
           'pinyin_syllables': ['zhong4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['这块手表很重。'],
           'occurrences': 1,
           'example_pinyin': 'zhè kuài shǒu biǎo hěn zhòng',
           'example_translation': 'Este relógio de pulso é pesado.'},
 '20::简单': {'word': '简单',
            'answer': 'jian3dan1',
            'pinyin_syllables': ['jian3', 'dan1'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['这个方法很简单。'],
            'occurrences': 1,
            'example_pinyin': 'zhè ge fāng fǎ hěn jiǎn dān',
            'example_translation': 'Este método é simples.'},
 '20::房子': {'word': '房子',
            'answer': 'fang2zi',
            'pinyin_syllables': ['fang2', 'zi5'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我看见山上的房子了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ kàn jiàn shān shàng de fáng zi le',
            'example_translation': 'Vi a casa que fica na montanha.'},
 '20::找工作': {'word': '找工作',
             'answer': 'zhao3gong1zuo4',
             'pinyin_syllables': ['zhao3', 'gong1', 'zuo4'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['我正在找工作。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ zhèng zài zhǎo gōng zuò',
             'example_translation': 'Estou procurando emprego.'},
 '20::工作': {'word': '工作',
            'answer': 'gong1zuo4',
            'pinyin_syllables': ['gong1', 'zuo4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我正在找工作。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ zhèng zài zhǎo gōng zuò',
            'example_translation': 'Estou procurando emprego.'},
 '20::找': {'word': '找',
           'answer': 'zhao3',
           'pinyin_syllables': ['zhao3'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我正在找工作。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ zhèng zài zhǎo gōng zuò',
           'example_translation': 'Estou procurando emprego.'},
 '20::当': {'word': '当',
           'answer': 'dang1',
           'pinyin_syllables': ['dang1'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我以前当过工程师。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ yǐ qián dāng guò gōng chéng shī',
           'example_translation': 'Já trabalhei como engenheiro.'},
 '20::工程师': {'word': '工程师',
             'answer': 'gong1cheng2shi1',
             'pinyin_syllables': ['gong1', 'cheng2', 'shi1'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['我以前当过工程师。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ yǐ qián dāng guò gōng chéng shī',
             'example_translation': 'Já trabalhei como engenheiro.'},
 '20::过': {'word': '过',
           'answer': 'guo4',
           'pinyin_syllables': ['guo4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['你以前教过英语吗？'],
           'occurrences': 1,
           'example_pinyin': 'nǐ yǐ qián jiāo guò yīng yǔ ma',
           'example_translation': 'Você já ensinou inglês antes?',
           'answer_variants': ['guo']},
 '20::学过': {'word': '学过',
            'answer': 'xue2guo4',
            'pinyin_syllables': ['xue2', 'guo4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我学过书法。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xué guò shū fǎ',
            'example_translation': 'Já estudei caligrafia.',
            'answer_variants': ['xue2guo']},
 '20::教过': {'word': '教过',
            'answer': 'jiao1guo4',
            'pinyin_syllables': ['jiao1', 'guo4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['你以前教过英语吗？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ yǐ qián jiāo guò yīng yǔ ma',
            'example_translation': 'Você já ensinou inglês antes?',
            'answer_variants': ['jiao1guo']},
 '20::去过': {'word': '去过',
            'answer': 'qu4guo4',
            'pinyin_syllables': ['qu4', 'guo4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我去过中国。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ qù guò zhōng guó',
            'example_translation': 'Já fui à China.',
            'answer_variants': ['qu4guo']},
 '20::做过': {'word': '做过',
            'answer': 'zuo4guo4',
            'pinyin_syllables': ['zuo4', 'guo4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['考官问我以前做过什么工作。'],
            'occurrences': 1,
            'example_pinyin': 'kǎo guān wèn wǒ yǐ qián zuò guò shén me gōng zuò',
            'example_translation': 'O entrevistador perguntou que trabalhos eu já fiz.',
            'answer_variants': ['zuo4guo']},
 '20::适合': {'word': '适合',
            'answer': 'shi4he2',
            'pinyin_syllables': ['shi4', 'he2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我很适合做老师。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ hěn shì hé zuò lǎo shī',
            'example_translation': 'Tenho perfil para ser professor.'},
 '20::小朋友': {'word': '小朋友',
             'answer': 'xiao3peng2you',
             'pinyin_syllables': ['xiao3', 'peng2', 'you5'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['小朋友都能听懂。'],
             'occurrences': 1,
             'example_pinyin': 'xiǎo péng you dōu néng tīng dǒng',
             'example_translation': 'Todas as crianças conseguem entender o que ouvem.'},
 '20::听懂': {'word': '听懂',
            'answer': 'ting1dong3',
            'pinyin_syllables': ['ting1', 'dong3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['小朋友都能听懂。'],
            'occurrences': 1,
            'example_pinyin': 'xiǎo péng you dōu néng tīng dǒng',
            'example_translation': 'Todas as crianças conseguem entender o que ouvem.'},
 '20::没听懂': {'word': '没听懂',
             'answer': 'mei2ting1dong3',
             'pinyin_syllables': ['mei2', 'ting1', 'dong3'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['如果你没听懂，我会再讲一遍。'],
             'occurrences': 1,
             'example_pinyin': 'rú guǒ nǐ méi tīng dǒng wǒ huì zài jiǎng yí biàn',
             'example_translation': 'Se você não entendeu, vou explicar mais uma vez.'},
 '20::准备好': {'word': '准备好',
             'answer': 'zhun3bei4hao3',
             'pinyin_syllables': ['zhun3', 'bei4', 'hao3'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['当然，我能准备好明天的面试。'],
             'occurrences': 1,
             'example_pinyin': 'dāngrán wǒ néng zhǔn bèi hǎo míng tiān de miàn shì',
             'example_translation': 'Claro, consigo me preparar bem para a entrevista de amanhã.'},
 '20::有信心': {'word': '有信心',
             'answer': 'you3xin4xin1',
             'pinyin_syllables': ['you3', 'xin4', 'xin1'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['我的老板对我很有信心。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ de lǎo bǎn duì wǒ hěn yǒu xìn xīn',
             'example_translation': 'Meu chefe tem muita confiança em mim.'},
 '20::有孝心': {'word': '有孝心',
             'answer': 'you3xiao4xin1',
             'pinyin_syllables': ['you3', 'xiao4', 'xin1'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['他很有孝心。'],
             'occurrences': 1,
             'example_pinyin': 'tā hěn yǒu xiào xīn',
             'example_translation': 'Ele é muito dedicado aos pais.'},
 '20::有责任心': {'word': '有责任心',
              'answer': 'you3ze2ren4xin1',
              'pinyin_syllables': ['you3', 'ze2', 'ren4', 'xin1'],
              'categories': ['Livro 20 e aulas 20.1 / 20.2'],
              'examples': ['我的同事认真、勤奋、有责任心。'],
              'occurrences': 1,
              'example_pinyin': 'wǒ de tóng shìrèn zhēn qín fèn yǒu zérèn xīn',
              'example_translation': 'Meu colega é dedicado, esforçado e responsável.'},
 '20::同事': {'word': '同事',
            'answer': 'tong2shi4',
            'pinyin_syllables': ['tong2', 'shi4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的同事认真、勤奋、有责任心。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de tóng shìrèn zhēn qín fèn yǒu zérèn xīn',
            'example_translation': 'Meu colega é dedicado, esforçado e responsável.'},
 '20::考官': {'word': '考官',
            'answer': 'kao3guan1',
            'pinyin_syllables': ['kao3', 'guan1'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['考官问我以前做过什么工作。'],
            'occurrences': 1,
            'example_pinyin': 'kǎo guān wèn wǒ yǐ qián zuò guò shén me gōng zuò',
            'example_translation': 'O entrevistador perguntou que trabalhos eu já fiz.'},
 '20::谢谢': {'word': '谢谢',
            'answer': 'xie4xie',
            'pinyin_syllables': ['xie4', 'xie5'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['谢谢，我很喜欢教英语。'],
            'occurrences': 1,
            'example_pinyin': 'xiè xie wǒ hěn xǐ huan jiāo yīng yǔ',
            'example_translation': 'Obrigado, gosto muito de ensinar inglês.'},
 '20::而且': {'word': '而且',
            'answer': 'er2qie3',
            'pinyin_syllables': ['er2', 'qie3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我教过小朋友，而且很喜欢做老师。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jiāo guò xiǎo péng you ér qiě hěn xǐ huan zuò lǎo shī',
            'example_translation': 'Já ensinei crianças e, além disso, gosto muito de ser professor.'},
 '20::学生': {'word': '学生',
            'answer': 'xue2sheng',
            'pinyin_syllables': ['xue2', 'sheng5'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我会给学生讲英文故事。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ huì gěi xué sheng jiǎng yīng wén gù shi',
            'example_translation': 'Vou contar histórias em inglês aos alunos.',
            'answer_variants': ['xue2sheng1']},
 '20::学生们': {'word': '学生们',
             'answer': 'xue2shengmen',
             'pinyin_syllables': ['xue2', 'sheng5', 'men5'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['我很幽默，学生们都很喜欢我。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ hěn yōu mò xué sheng men dōu hěn xǐ huan wǒ',
             'example_translation': 'Sou bem-humorado e todos os alunos gostam de mim.',
             'answer_variants': ['xue2sheng1men']},
 '20::遍': {'word': '遍',
           'answer': 'bian4',
           'pinyin_syllables': ['bian4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我会再讲一遍，或者换一个方法。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ huì zài jiǎng yí biàn huò zhě huàn yí ge fāng fǎ',
           'example_translation': 'Vou explicar outra vez ou mudar de método.'},
 '20::换': {'word': '换',
           'answer': 'huan4',
           'pinyin_syllables': ['huan4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我会再讲一遍，或者换一个方法。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ huì zài jiǎng yí biàn huò zhě huàn yí ge fāng fǎ',
           'example_translation': 'Vou explicar outra vez ou mudar de método.'},
 '20::英文': {'word': '英文',
            'answer': 'ying1wen2',
            'pinyin_syllables': ['ying1', 'wen2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我会给学生讲英文故事。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ huì gěi xué sheng jiǎng yīng wén gù shi',
            'example_translation': 'Vou contar histórias em inglês aos alunos.'},
 '20::希望': {'word': '希望',
            'answer': 'xi1wang4',
            'pinyin_syllables': ['xi1', 'wang4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我希望可以做好这份工作。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xī wàng kě yǐ zuò hǎo zhè fèn gōng zuò',
            'example_translation': 'Espero conseguir fazer bem este trabalho.'},
 '20::老板': {'word': '老板',
            'answer': 'lao3ban3',
            'pinyin_syllables': ['lao3', 'ban3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的老板对我很有信心。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de lǎo bǎn duì wǒ hěn yǒu xìn xīn',
            'example_translation': 'Meu chefe tem muita confiança em mim.'},
 '20::让': {'word': '让',
           'answer': 'rang4',
           'pinyin_syllables': ['rang4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['老板让我明天去上班。'],
           'occurrences': 1,
           'example_pinyin': 'lǎo bǎnràng wǒ míng tiān qù shàng bān',
           'example_translation': 'O chefe pediu que eu vá trabalhar amanhã.'},
 '20::上班': {'word': '上班',
            'answer': 'shang4ban1',
            'pinyin_syllables': ['shang4', 'ban1'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['老板让我明天去上班。'],
            'occurrences': 1,
            'example_pinyin': 'lǎo bǎnràng wǒ míng tiān qù shàng bān',
            'example_translation': 'O chefe pediu que eu vá trabalhar amanhã.'},
 '20::晚上': {'word': '晚上',
            'answer': 'wan3shang',
            'pinyin_syllables': ['wan3', 'shang5'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['虽然时间很紧，不过我一个晚上就能准备好。'],
            'occurrences': 1,
            'example_pinyin': 'suīrán shí jiān hěn jǐn bú guò wǒ yí ge wǎn shang jiù néng zhǔn bèi hǎo',
            'example_translation': 'Embora o tempo seja curto, consigo me preparar em uma noite.'},
 '20::第二': {'word': '第二',
            'answer': 'di4er4',
            'pinyin_syllables': ['di4', 'er4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['这是我找到的第二份兼职工作。'],
            'occurrences': 1,
            'example_pinyin': 'zhè shì wǒ zhǎo dào de dì èr fèn jiān zhí gōng zuò',
            'example_translation': 'Este é o segundo emprego de meio período que consegui.'},
 '20::找到': {'word': '找到',
            'answer': 'zhao3dao4',
            'pinyin_syllables': ['zhao3', 'dao4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我找到了一份兼职工作。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ zhǎo dào le yí fèn jiān zhí gōng zuò',
            'example_translation': 'Consegui um emprego de meio período.'},
 '20::还是': {'word': '还是',
            'answer': 'hai2shi4',
            'pinyin_syllables': ['hai2', 'shi4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['这份工作还是不太容易。'],
            'occurrences': 1,
            'example_pinyin': 'zhè fèn gōng zuò hái shì bú tàiróng yì',
            'example_translation': 'Este trabalho ainda não é muito fácil.'},
 '20::做好': {'word': '做好',
            'answer': 'zuo4hao3',
            'pinyin_syllables': ['zuo4', 'hao3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我希望可以做好这份工作。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xī wàng kě yǐ zuò hǎo zhè fèn gōng zuò',
            'example_translation': 'Espero conseguir fazer bem este trabalho.'},
 '20::学好': {'word': '学好',
            'answer': 'xue2hao3',
            'pinyin_syllables': ['xue2', 'hao3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我能学好英语。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ néng xué hǎo yīng yǔ',
            'example_translation': 'Consigo aprender inglês bem.'},
 '20::教好': {'word': '教好',
            'answer': 'jiao1hao3',
            'pinyin_syllables': ['jiao1', 'hao3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我会教好英语的。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ huì jiāo hǎo yīng yǔ de',
            'example_translation': 'Vou ensinar inglês bem.'},
 '20::送到': {'word': '送到',
            'answer': 'song4dao4',
            'pinyin_syllables': ['song4', 'dao4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['外卖会很快送到的。'],
            'occurrences': 1,
            'example_pinyin': 'wài mài huì hěn kuài sòng dào de',
            'example_translation': 'A comida vai chegar logo.'},
 '20::送': {'word': '送',
           'answer': 'song4',
           'pinyin_syllables': ['song4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['外卖会很快送到的。'],
           'occurrences': 1,
           'example_pinyin': 'wài mài huì hěn kuài sòng dào de',
           'example_translation': 'A comida vai chegar logo.'},
 '20::写得完': {'word': '写得完',
             'answer': 'xie3dewan2',
             'pinyin_syllables': ['xie3', 'de5', 'wan2'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['我今天写得完作业。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ jīn tiān xiě de wán zuò yè',
             'example_translation': 'Consigo terminar de escrever a lição hoje.'},
 '20::写不完': {'word': '写不完',
             'answer': 'xie3bu4wan2',
             'pinyin_syllables': ['xie3', 'bu4', 'wan2'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['我今天写不完作业。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ jīn tiān xiě bù wán zuò yè',
             'example_translation': 'Não consigo terminar de escrever a lição hoje.',
             'answer_variants': ['xie3buwan2']},
 '20::写完': {'word': '写完',
            'answer': 'xie3wan2',
            'pinyin_syllables': ['xie3', 'wan2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的作业写完了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de zuò yè xiě wán le',
            'example_translation': 'Terminei de escrever minha lição.'},
 '20::写对': {'word': '写对',
            'answer': 'xie3dui4',
            'pinyin_syllables': ['xie3', 'dui4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['这个字写对了。'],
            'occurrences': 1,
            'example_pinyin': 'zhè ge zì xiě duì le',
            'example_translation': 'Este caractere foi escrito corretamente.'},
 '20::写错': {'word': '写错',
            'answer': 'xie3cuo4',
            'pinyin_syllables': ['xie3', 'cuo4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['这个字写错了。'],
            'occurrences': 1,
            'example_pinyin': 'zhè ge zì xiě cuò le',
            'example_translation': 'Este caractere foi escrito errado.'},
 '20::听得懂': {'word': '听得懂',
             'answer': 'ting1dedong3',
             'pinyin_syllables': ['ting1', 'de5', 'dong3'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['他说的话我听得懂。'],
             'occurrences': 1,
             'example_pinyin': 'tā shuō de huà wǒ tīng de dǒng',
             'example_translation': 'Consigo entender o que ele diz.'},
 '20::听不懂': {'word': '听不懂',
             'answer': 'ting1bu4dong3',
             'pinyin_syllables': ['ting1', 'bu4', 'dong3'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['他说的话我听不懂。'],
             'occurrences': 1,
             'example_pinyin': 'tā shuō de huà wǒ tīng bù dǒng',
             'example_translation': 'Não consigo entender o que ele diz.',
             'answer_variants': ['ting1budong3']},
 '20::听清楚': {'word': '听清楚',
             'answer': 'ting1qing1chu',
             'pinyin_syllables': ['ting1', 'qing1', 'chu5'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['我听清楚了。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ tīng qīng chu le',
             'example_translation': 'Ouvi com clareza.'},
 '20::听见': {'word': '听见',
            'answer': 'ting1jian4',
            'pinyin_syllables': ['ting1', 'jian4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['你听见了吗？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ tīng jiàn le ma',
            'example_translation': 'Você ouviu?'},
 '20::卖完': {'word': '卖完',
            'answer': 'mai4wan2',
            'pinyin_syllables': ['mai4', 'wan2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['水果都卖完了。'],
            'occurrences': 1,
            'example_pinyin': 'shuǐ guǒ dōu mài wán le',
            'example_translation': 'Todas as frutas foram vendidas.'},
 '20::吃完': {'word': '吃完',
            'answer': 'chi1wan2',
            'pinyin_syllables': ['chi1', 'wan2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我吃完了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ chī wán le',
            'example_translation': 'Terminei de comer.'},
 '20::说完': {'word': '说完',
            'answer': 'shuo1wan2',
            'pinyin_syllables': ['shuo1', 'wan2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['他说完了。'],
            'occurrences': 1,
            'example_pinyin': 'tā shuō wán le',
            'example_translation': 'Ele terminou de falar.'},
 '20::完': {'word': '完',
           'answer': 'wan2',
           'pinyin_syllables': ['wan2'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我的作业写完了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ de zuò yè xiě wán le',
           'example_translation': 'Terminei de escrever minha lição.'},
 '20::对': {'word': '对',
           'answer': 'dui4',
           'pinyin_syllables': ['dui4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['这个字写对了。'],
           'occurrences': 1,
           'example_pinyin': 'zhè ge zì xiě duì le',
           'example_translation': 'Este caractere foi escrito corretamente.'},
 '20::错': {'word': '错',
           'answer': 'cuo4',
           'pinyin_syllables': ['cuo4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['这个字写错了。'],
           'occurrences': 1,
           'example_pinyin': 'zhè ge zì xiě cuò le',
           'example_translation': 'Este caractere foi escrito errado.'},
 '20::作业': {'word': '作业',
            'answer': 'zuo4ye4',
            'pinyin_syllables': ['zuo4', 'ye4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的作业写完了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de zuò yè xiě wán le',
            'example_translation': 'Terminei de escrever minha lição.'},
 '20::学会': {'word': '学会',
            'answer': 'xue2hui4',
            'pinyin_syllables': ['xue2', 'hui4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['这个汉字我学会了。'],
            'occurrences': 1,
            'example_pinyin': 'zhè ge hàn zì wǒ xué huì le',
            'example_translation': 'Aprendi este caractere chinês.'},
 '20::电话号码': {'word': '电话号码',
              'answer': 'dian4hua4hao4ma3',
              'pinyin_syllables': ['dian4', 'hua4', 'hao4', 'ma3'],
              'categories': ['Livro 20 e aulas 20.1 / 20.2'],
              'examples': ['这个电话号码你记住了吗？'],
              'occurrences': 1,
              'example_pinyin': 'zhè ge diàn huà hào mǎ nǐ jì zhù le ma',
              'example_translation': 'Você memorizou este número de telefone?'},
 '20::记住': {'word': '记住',
            'answer': 'ji4zhu4',
            'pinyin_syllables': ['ji4', 'zhu4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['这个电话号码你记住了吗？'],
            'occurrences': 1,
            'example_pinyin': 'zhè ge diàn huà hào mǎ nǐ jì zhù le ma',
            'example_translation': 'Você memorizou este número de telefone?'},
 '20::滑': {'word': '滑',
           'answer': 'hua2',
           'pinyin_syllables': ['hua2'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['他滑倒了。'],
           'occurrences': 1,
           'example_pinyin': 'tā huá dǎo le',
           'example_translation': 'Ele escorregou e caiu.'},
 '20::滑倒': {'word': '滑倒',
            'answer': 'hua2dao3',
            'pinyin_syllables': ['hua2', 'dao3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['他滑倒了。'],
            'occurrences': 1,
            'example_pinyin': 'tā huá dǎo le',
            'example_translation': 'Ele escorregou e caiu.'},
 '20::饱': {'word': '饱',
           'answer': 'bao3',
           'pinyin_syllables': ['bao3'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['她吃饱了。'],
           'occurrences': 1,
           'example_pinyin': 'tā chī bǎo le',
           'example_translation': 'Ela comeu até ficar satisfeita.'},
 '20::吃饱': {'word': '吃饱',
            'answer': 'chi1bao3',
            'pinyin_syllables': ['chi1', 'bao3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['她吃饱了。'],
            'occurrences': 1,
            'example_pinyin': 'tā chī bǎo le',
            'example_translation': 'Ela comeu até ficar satisfeita.'},
 '20::买到': {'word': '买到',
            'answer': 'mai3dao4',
            'pinyin_syllables': ['mai3', 'dao4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['他买到票了。'],
            'occurrences': 1,
            'example_pinyin': 'tā mǎi dào piào le',
            'example_translation': 'Ele conseguiu comprar a passagem.'},
 '20::票': {'word': '票',
           'answer': 'piao4',
           'pinyin_syllables': ['piao4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['他买到票了。'],
           'occurrences': 1,
           'example_pinyin': 'tā mǎi dào piào le',
           'example_translation': 'Ele conseguiu comprar a passagem.'},
 '20::看懂': {'word': '看懂',
            'answer': 'kan4dong3',
            'pinyin_syllables': ['kan4', 'dong3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['他看懂这本书了。'],
            'occurrences': 1,
            'example_pinyin': 'tā kàn dǒng zhè běn shū le',
            'example_translation': 'Ele entendeu este livro.'},
 '20::看见': {'word': '看见',
            'answer': 'kan4jian4',
            'pinyin_syllables': ['kan4', 'jian4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我看见山上的房子了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ kàn jiàn shān shàng de fáng zi le',
            'example_translation': 'Vi a casa que fica na montanha.'},
 '20::借': {'word': '借',
           'answer': 'jie4',
           'pinyin_syllables': ['jie4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我借到钱了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jiè dào qián le',
           'example_translation': 'Consegui dinheiro emprestado.'},
 '20::借到': {'word': '借到',
            'answer': 'jie4dao4',
            'pinyin_syllables': ['jie4', 'dao4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我借到钱了。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jiè dào qián le',
            'example_translation': 'Consegui dinheiro emprestado.'},
 '20::舒服': {'word': '舒服',
            'answer': 'shu1fu',
            'pinyin_syllables': ['shu1', 'fu5'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我今天不舒服。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jīn tiān bù shū fu',
            'example_translation': 'Hoje não estou me sentindo bem.'},
 '20::不舒服': {'word': '不舒服',
             'answer': 'bu4shu1fu',
             'pinyin_syllables': ['bu4', 'shu1', 'fu5'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['我今天不舒服。'],
             'occurrences': 1,
             'example_pinyin': 'wǒ jīn tiān bù shū fu',
             'example_translation': 'Hoje não estou me sentindo bem.'},
 '20::电脑': {'word': '电脑',
            'answer': 'dian4nao3',
            'pinyin_syllables': ['dian4', 'nao3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['我的电脑没找到。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de diàn nǎo méi zhǎo dào',
            'example_translation': 'Meu computador não foi encontrado.'},
 '20::水果店': {'word': '水果店',
             'answer': 'shui3guo3dian4',
             'pinyin_syllables': ['shui3', 'guo3', 'dian4'],
             'categories': ['Livro 20 e aulas 20.1 / 20.2'],
             'examples': ['这家水果店的水果都卖完了。'],
             'occurrences': 1,
             'example_pinyin': 'zhè jiā shuǐ guǒ diàn de shuǐ guǒ dōu mài wán le',
             'example_translation': 'As frutas desta frutaria se esgotaram.'},
 '20::水果': {'word': '水果',
            'answer': 'shui3guo3',
            'pinyin_syllables': ['shui3', 'guo3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['水果都卖完了。'],
            'occurrences': 1,
            'example_pinyin': 'shuǐ guǒ dōu mài wán le',
            'example_translation': 'Todas as frutas foram vendidas.'},
 '20::好看': {'word': '好看',
            'answer': 'hao3kan4',
            'pinyin_syllables': ['hao3', 'kan4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['这部电影不好看，我没看完。'],
            'occurrences': 1,
            'example_pinyin': 'zhè bù diàn yǐng bù hǎo kàn wǒ méi kàn wán',
            'example_translation': 'Este filme não é bom; não terminei de assistir.'},
 '20::看完': {'word': '看完',
            'answer': 'kan4wan2',
            'pinyin_syllables': ['kan4', 'wan2'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['这部电影不好看，我没看完。'],
            'occurrences': 1,
            'example_pinyin': 'zhè bù diàn yǐng bù hǎo kàn wǒ méi kàn wán',
            'example_translation': 'Este filme não é bom; não terminei de assistir.'},
 '20::部': {'word': '部',
           'answer': 'bu4',
           'pinyin_syllables': ['bu4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['这部电影不好看，我没看完。'],
           'occurrences': 1,
           'example_pinyin': 'zhè bù diàn yǐng bù hǎo kàn wǒ méi kàn wán',
           'example_translation': 'Este filme não é bom; não terminei de assistir.'},
 '20::山': {'word': '山',
           'answer': 'shan1',
           'pinyin_syllables': ['shan1'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我看见山上的房子了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ kàn jiàn shān shàng de fáng zi le',
           'example_translation': 'Vi a casa que fica na montanha.'},
 '20::介绍': {'word': '介绍',
            'answer': 'jie4shao4',
            'pinyin_syllables': ['jie4', 'shao4'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['请介绍一下自己。'],
            'occurrences': 1,
            'example_pinyin': 'qǐng jiè shào yí xià zì jǐ',
            'example_translation': 'Por favor, apresente-se brevemente.'},
 '20::老': {'word': '老',
           'answer': 'lao3',
           'pinyin_syllables': ['lao3'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我想当英语老师。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ xiǎng dāng yīng yǔ lǎo shī',
           'example_translation': 'Quero ser professor de inglês.'},
 '20::师': {'word': '师',
           'answer': 'shi1',
           'pinyin_syllables': ['shi1'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我想当英语老师。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ xiǎng dāng yīng yǔ lǎo shī',
           'example_translation': 'Quero ser professor de inglês.'},
 '20::考': {'word': '考',
           'answer': 'kao3',
           'pinyin_syllables': ['kao3'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['考官问我以前做过什么工作。'],
           'occurrences': 1,
           'example_pinyin': 'kǎo guān wèn wǒ yǐ qián zuò guò shén me gōng zuò',
           'example_translation': 'O entrevistador perguntou que trabalhos eu já fiz.'},
 '20::交': {'word': '交',
           'answer': 'jiao1',
           'pinyin_syllables': ['jiao1'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我经常跟中国朋友交流。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jīng cháng gēn zhōng guó péng you jiāo liú',
           'example_translation': 'Costumo conversar com amigos chineses.'},
 '20::流': {'word': '流',
           'answer': 'liu2',
           'pinyin_syllables': ['liu2'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我经常跟中国朋友交流。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jīng cháng gēn zhōng guó péng you jiāo liú',
           'example_translation': 'Costumo conversar com amigos chineses.'},
 '20::清': {'word': '清',
           'answer': 'qing1',
           'pinyin_syllables': ['qing1'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我的发音很清楚，说得很慢。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ de fā yīn hěn qīng chu shuō de hěn màn',
           'example_translation': 'Minha pronúncia é clara e falo devagar.'},
 '20::楚': {'word': '楚',
           'answer': 'chu3',
           'pinyin_syllables': ['chu3'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['我的发音很清楚，说得很慢。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ de fā yīn hěn qīng chu shuō de hěn màn',
           'example_translation': 'Minha pronúncia é clara e falo devagar.'},
 '20::介': {'word': '介',
           'answer': 'jie4',
           'pinyin_syllables': ['jie4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['请介绍一下自己。'],
           'occurrences': 1,
           'example_pinyin': 'qǐng jiè shào yí xià zì jǐ',
           'example_translation': 'Por favor, apresente-se brevemente.'},
 '20::绍': {'word': '绍',
           'answer': 'shao4',
           'pinyin_syllables': ['shao4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['请介绍一下自己。'],
           'occurrences': 1,
           'example_pinyin': 'qǐng jiè shào yí xià zì jǐ',
           'example_translation': 'Por favor, apresente-se brevemente.'},
 '20::字': {'word': '字',
           'answer': 'zi4',
           'pinyin_syllables': ['zi4'],
           'categories': ['Livro 20 e aulas 20.1 / 20.2'],
           'examples': ['这个字写对了。'],
           'occurrences': 1,
           'example_pinyin': 'zhè ge zì xiě duì le',
           'example_translation': 'Este caractere foi escrito corretamente.'},
 '20::还有': {'word': '还有',
            'answer': 'hai2you3',
            'pinyin_syllables': ['hai2', 'you3'],
            'categories': ['Livro 20 e aulas 20.1 / 20.2'],
            'examples': ['你还有别的优点吗？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ hái yǒu bié de yōu diǎn ma',
            'example_translation': 'Você tem outras qualidades?'},
 '20::英语': {'word': '英语',
            'answer': 'ying1yu3',
            'categories': ['Revisão · Aula 20'],
            'examples': ['你以前教过英语吗？'],
            'occurrences': 1,
            'display_pinyin': 'yīngyǔ',
            'example_pinyin': 'nǐ yǐ qián jiāo guò yīng yǔ ma',
            'example_translation': 'Você já ensinou inglês antes?'},
 '20::听': {'word': '听',
           'answer': 'ting1',
           'pinyin_syllables': ['ting1'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['小朋友都能听懂。'],
           'occurrences': 1,
           'example_pinyin': 'xiǎo péng you dōu néng tīng dǒng',
           'example_translation': 'Todas as crianças conseguem entender o que ouvem.',
           'display_pinyin': 'tīng'},
 '20::会': {'word': '会',
           'answer': 'hui4',
           'pinyin_syllables': ['hui4'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['如果你没听懂，我会再讲一遍。'],
           'occurrences': 1,
           'example_pinyin': 'rú guǒ nǐ méi tīng dǒng wǒ huì zài jiǎng yí biàn',
           'example_translation': 'Se você não entendeu, vou explicar mais uma vez.',
           'display_pinyin': 'huì'},
 '20::给': {'word': '给',
           'answer': 'gei3',
           'pinyin_syllables': ['gei3'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我会给学生讲英文故事。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ huì gěi xué sheng jiǎng yīng wén gù shi',
           'example_translation': 'Vou contar histórias em inglês aos alunos.',
           'display_pinyin': 'gěi'},
 '20::认真': {'word': '认真',
            'answer': 'ren4zhen1',
            'pinyin_syllables': ['ren4', 'zhen1'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['我的同事认真、勤奋、有责任心。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ de tóng shìrèn zhēn qín fèn yǒu zérèn xīn',
            'example_translation': 'Meu colega é dedicado, esforçado e responsável.',
            'display_pinyin': 'rèn zhēn'},
 '20::老师': {'word': '老师',
            'answer': 'lao3shi1',
            'categories': ['Revisão · Aula 20'],
            'examples': ['我很适合做老师。'],
            'occurrences': 1,
            'display_pinyin': 'lǎoshī',
            'example_pinyin': 'wǒ hěn shì hé zuò lǎo shī',
            'example_translation': 'Tenho perfil para ser professor.'},
 '20::警察': {'word': '警察',
            'answer': 'jing3cha2',
            'pinyin_syllables': ['jing3', 'cha2'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['他报警以后，警察来了。'],
            'occurrences': 1,
            'example_pinyin': 'tā bào jǐng yǐ hòu jǐng chá lái le',
            'example_translation': 'Depois que ele chamou a polícia, os policiais chegaram.',
            'display_pinyin': 'jǐng chá'},
 '20::医生': {'word': '医生',
            'answer': 'yi1sheng1',
            'pinyin_syllables': ['yi1', 'sheng1'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['医生在医院工作。'],
            'occurrences': 1,
            'example_pinyin': 'yī shēng zài yī yuàn gōng zuò',
            'example_translation': 'O médico trabalha no hospital.',
            'display_pinyin': 'yī shēng'},
 '20::中文': {'word': '中文',
            'answer': 'zhong1wen2',
            'pinyin_syllables': ['zhong1', 'wen2'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['我说中文说得很流利。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ shuō Zhōngwén shuō de hěn liúlì.',
            'example_translation': 'Eu falo chinês com muita fluência.',
            'display_pinyin': 'zhōng wén'},
 '20::说': {'word': '说',
           'answer': 'shuo1',
           'pinyin_syllables': ['shuo1'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我的发音很清楚，说得很慢。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ de fā yīn hěn qīng chu shuō de hěn màn',
           'example_translation': 'Minha pronúncia é clara e falo devagar.',
           'display_pinyin': 'shuō'},
 '20::得': {'word': '得',
           'answer': 'de',
           'pinyin_syllables': ['de5'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我的发音很清楚，说得很慢。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ de fā yīn hěn qīng chu shuō de hěn màn',
           'example_translation': 'Minha pronúncia é clara e falo devagar.',
           'display_pinyin': 'de'},
 '20::很': {'word': '很',
           'answer': 'hen3',
           'pinyin_syllables': ['hen3'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我的发音很清楚，说得很慢。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ de fā yīn hěn qīng chu shuō de hěn màn',
           'example_translation': 'Minha pronúncia é clara e falo devagar.',
           'display_pinyin': 'hěn'},
 '20::我': {'word': '我',
           'answer': 'wo3',
           'pinyin_syllables': ['wo3'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我明天去面试。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ míng tiān qù miàn shì',
           'example_translation': 'Amanhã vou a uma entrevista.',
           'display_pinyin': 'wǒ'},
 '20::你': {'word': '你',
           'answer': 'ni3',
           'pinyin_syllables': ['ni3'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['你以前教过英语吗？'],
           'occurrences': 1,
           'example_pinyin': 'nǐ yǐ qián jiāo guò yīng yǔ ma',
           'example_translation': 'Você já ensinou inglês antes?',
           'display_pinyin': 'nǐ'},
 '20::他': {'word': '他',
           'answer': 'ta1',
           'pinyin_syllables': ['ta1'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['他很有孝心。'],
           'occurrences': 1,
           'example_pinyin': 'tā hěn yǒu xiào xīn',
           'example_translation': 'Ele é muito dedicado aos pais.',
           'display_pinyin': 'tā'},
 '20::她': {'word': '她',
           'answer': 'ta1',
           'pinyin_syllables': ['ta1'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['她吃饱了。'],
           'occurrences': 1,
           'example_pinyin': 'tā chī bǎo le',
           'example_translation': 'Ela comeu até ficar satisfeita.',
           'display_pinyin': 'tā'},
 '20::我们': {'word': '我们',
            'answer': 'wo3men',
            'pinyin_syllables': ['wo3', 'men5'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['我们骑到华山路的路口。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ men qí dào huà shān lù de lù kǒu',
            'example_translation': 'Fomos de bicicleta até o cruzamento da Rua Huashan.',
            'display_pinyin': 'wǒ men'},
 '20::什么': {'word': '什么',
            'answer': 'shen2me',
            'pinyin_syllables': ['shen2', 'me5'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['考官问我以前做过什么工作。'],
            'occurrences': 1,
            'example_pinyin': 'kǎo guān wèn wǒ yǐ qián zuò guò shén me gōng zuò',
            'example_translation': 'O entrevistador perguntou que trabalhos eu já fiz.',
            'display_pinyin': 'shén me'},
 '20::做': {'word': '做',
           'answer': 'zuo4',
           'pinyin_syllables': ['zuo4'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我很适合做老师。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ hěn shì hé zuò lǎo shī',
           'example_translation': 'Tenho perfil para ser professor.',
           'display_pinyin': 'zuò'},
 '20::书法': {'word': '书法',
            'answer': 'shu1fa3',
            'pinyin_syllables': ['shu1', 'fa3'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['我学过书法。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xué guò shū fǎ',
            'example_translation': 'Já estudei caligrafia.',
            'display_pinyin': 'shū fǎ'},
 '20::打': {'word': '打',
           'answer': 'da3',
           'pinyin_syllables': ['da3'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['今天刮风，还打雷。'],
           'occurrences': 1,
           'example_pinyin': 'jīn tiān guā fēng hái dǎ léi',
           'example_translation': 'Hoje está ventando e também está trovejando.',
           'display_pinyin': 'dǎ'},
 '20::麻将': {'word': '麻将',
            'answer': 'ma2jiang4',
            'pinyin_syllables': ['ma2', 'jiang4'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['你打麻将打得怎么样？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ dǎ májiàng dǎ de zěnme yàng?',
            'example_translation': 'Como você joga mahjong?',
            'display_pinyin': 'má jiàng'},
 '20::汉语': {'word': '汉语',
            'answer': 'han4yu3',
            'pinyin_syllables': ['han4', 'yu3'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['你是什么时候开始学习汉语的？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ shì shén me shí hou kāi shǐ xué xí hàn yǔ de',
            'example_translation': 'Quando você começou a estudar chinês?',
            'display_pinyin': 'hàn yǔ'},
 '20::现在': {'word': '现在',
            'answer': 'xian4zai4',
            'pinyin_syllables': ['xian4', 'zai4'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['我现在应该怎么办？'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xiàn zài yīng gāi zěn me bàn',
            'example_translation': 'O que devo fazer agora?',
            'display_pinyin': 'xiàn zài'},
 '20::中国': {'word': '中国',
            'answer': 'zhong1guo2',
            'pinyin_syllables': ['zhong1', 'guo2'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['我经常跟中国朋友交流。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jīng cháng gēn zhōng guó péng you jiāo liú',
            'example_translation': 'Costumo conversar com amigos chineses.',
            'display_pinyin': 'zhōng guó'},
 '20::去': {'word': '去',
           'answer': 'qu4',
           'categories': ['Revisão · Aula 20'],
           'examples': ['我明天去面试。'],
           'occurrences': 1,
           'display_pinyin': 'qù',
           'example_pinyin': 'wǒ míng tiān qù miàn shì',
           'example_translation': 'Amanhã vou a uma entrevista.'},
 '20::能': {'word': '能',
           'answer': 'neng2',
           'pinyin_syllables': ['neng2'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['小朋友都能听懂。'],
           'occurrences': 1,
           'example_pinyin': 'xiǎo péng you dōu néng tīng dǒng',
           'example_translation': 'Todas as crianças conseguem entender o que ouvem.',
           'display_pinyin': 'néng'},
 '20::怎么办': {'word': '怎么办',
             'answer': 'zen3meban4',
             'pinyin_syllables': ['zen3', 'me5', 'ban4'],
             'categories': ['Revisão · Aula 20'],
             'examples': ['我现在应该怎么办？'],
             'occurrences': 1,
             'example_pinyin': 'wǒ xiàn zài yīng gāi zěn me bàn',
             'example_translation': 'O que devo fazer agora?',
             'display_pinyin': 'zěn me bàn'},
 '20::再': {'word': '再',
           'answer': 'zai4',
           'pinyin_syllables': ['zai4'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['如果你没听懂，我会再讲一遍。'],
           'occurrences': 1,
           'example_pinyin': 'rú guǒ nǐ méi tīng dǒng wǒ huì zài jiǎng yí biàn',
           'example_translation': 'Se você não entendeu, vou explicar mais uma vez.',
           'display_pinyin': 'zài'},
 '20::一': {'word': '一',
           'answer': 'yi1',
           'pinyin_syllables': ['yi1'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['如果你没听懂，我会再讲一遍。'],
           'occurrences': 1,
           'example_pinyin': 'rú guǒ nǐ méi tīng dǒng wǒ huì zài jiǎng yí biàn',
           'example_translation': 'Se você não entendeu, vou explicar mais uma vez.',
           'display_pinyin': 'yī'},
 '20::明天': {'word': '明天',
            'answer': 'ming2tian1',
            'pinyin_syllables': ['ming2', 'tian1'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['我明天去面试。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ míng tiān qù miàn shì',
            'example_translation': 'Amanhã vou a uma entrevista.',
            'display_pinyin': 'míng tiān'},
 '20::外卖': {'word': '外卖',
            'answer': 'wai4mai4',
            'pinyin_syllables': ['wai4', 'mai4'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['外卖会很快送到的。'],
            'occurrences': 1,
            'example_pinyin': 'wài mài huì hěn kuài sòng dào de',
            'example_translation': 'A comida vai chegar logo.',
            'display_pinyin': 'wài mài'},
 '20::快': {'word': '快',
           'answer': 'kuai4',
           'pinyin_syllables': ['kuai4'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['外卖会很快送到的。'],
           'occurrences': 1,
           'example_pinyin': 'wài mài huì hěn kuài sòng dào de',
           'example_translation': 'A comida vai chegar logo.',
           'display_pinyin': 'kuài'},
 '20::时间': {'word': '时间',
            'answer': 'shi2jian1',
            'pinyin_syllables': ['shi2', 'jian1'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['虽然时间很紧，不过我一个晚上就能准备好。'],
            'occurrences': 1,
            'example_pinyin': 'suīrán shí jiān hěn jǐn bú guò wǒ yí ge wǎn shang jiù néng zhǔn bèi hǎo',
            'example_translation': 'Embora o tempo seja curto, consigo me preparar em uma noite.',
            'display_pinyin': 'shí jiān'},
 '20::不过': {'word': '不过',
            'answer': 'bu2guo4',
            'pinyin_syllables': ['bu2', 'guo4'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['虽然时间很紧，不过我一个晚上就能准备好。'],
            'occurrences': 1,
            'example_pinyin': 'suīrán shí jiān hěn jǐn bú guò wǒ yí ge wǎn shang jiù néng zhǔn bèi hǎo',
            'example_translation': 'Embora o tempo seja curto, consigo me preparar em uma noite.',
            'display_pinyin': 'bú guò'},
 '20::一个': {'word': '一个',
            'answer': 'yi2ge',
            'categories': ['Revisão · Aula 20'],
            'examples': ['我会再讲一遍，或者换一个方法。'],
            'occurrences': 1,
            'display_pinyin': 'yíge',
            'example_pinyin': 'wǒ huì zài jiǎng yí biàn huò zhě huàn yí ge fāng fǎ',
            'example_translation': 'Vou explicar outra vez ou mudar de método.'},
 '20::就': {'word': '就',
           'answer': 'jiu4',
           'pinyin_syllables': ['jiu4'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['虽然时间很紧，不过我一个晚上就能准备好。'],
           'occurrences': 1,
           'example_pinyin': 'suīrán shí jiān hěn jǐn bú guò wǒ yí ge wǎn shang jiù néng zhǔn bèi hǎo',
           'example_translation': 'Embora o tempo seja curto, consigo me preparar em uma noite.',
           'display_pinyin': 'jiù'},
 '20::好': {'word': '好',
           'answer': 'hao3',
           'pinyin_syllables': ['hao3'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['当然，我能准备好明天的面试。'],
           'occurrences': 1,
           'example_pinyin': 'dāngrán wǒ néng zhǔn bèi hǎo míng tiān de miàn shì',
           'example_translation': 'Claro, consigo me preparar bem para a entrevista de amanhã.',
           'display_pinyin': 'hǎo'},
 '20::写': {'word': '写',
           'answer': 'xie3',
           'pinyin_syllables': ['xie3'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我今天写得完作业。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jīn tiān xiě de wán zuò yè',
           'example_translation': 'Consigo terminar de escrever a lição hoje.',
           'display_pinyin': 'xiě'},
 '20::汉字': {'word': '汉字',
            'answer': 'han4zi4',
            'pinyin_syllables': ['han4', 'zi4'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['这个汉字我学会了。'],
            'occurrences': 1,
            'example_pinyin': 'zhè ge hàn zì wǒ xué huì le',
            'example_translation': 'Aprendi este caractere chinês.',
            'display_pinyin': 'hàn zì'},
 '20::不': {'word': '不',
           'answer': 'bu4',
           'pinyin_syllables': ['bu4'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['对我来说，这份工作不太容易。'],
           'occurrences': 1,
           'example_pinyin': 'duì wǒ lái shuō zhè fèn gōng zuò bú tàiróng yì',
           'example_translation': 'Para mim, esse trabalho não é muito fácil.',
           'display_pinyin': 'bù'},
 '20::没': {'word': '没',
           'answer': 'mei2',
           'categories': ['Revisão · Aula 20'],
           'examples': ['如果你没听懂，我会再讲一遍。'],
           'occurrences': 1,
           'display_pinyin': 'méi',
           'example_pinyin': 'rú guǒ nǐ méi tīng dǒng wǒ huì zài jiǎng yí biàn',
           'example_translation': 'Se você não entendeu, vou explicar mais uma vez.'},
 '20::了': {'word': '了',
           'answer': 'le',
           'categories': ['Revisão · Aula 20'],
           'examples': ['我来中国已经很久了。'],
           'occurrences': 1,
           'display_pinyin': 'le',
           'example_pinyin': 'wǒ lái zhōng guó yǐ jīng hěn jiǔ le',
           'example_translation': 'Já faz muito tempo que cheguei à China.'},
 '20::吃': {'word': '吃',
           'answer': 'chi1',
           'pinyin_syllables': ['chi1'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我吃完了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ chī wán le',
           'example_translation': 'Terminei de comer.',
           'display_pinyin': 'chī'},
 '20::卖': {'word': '卖',
           'answer': 'mai4',
           'pinyin_syllables': ['mai4'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['外卖会很快送到的。'],
           'occurrences': 1,
           'example_pinyin': 'wài mài huì hěn kuài sòng dào de',
           'example_translation': 'A comida vai chegar logo.',
           'display_pinyin': 'mài'},
 '20::吗': {'word': '吗',
           'answer': 'ma',
           'pinyin_syllables': ['ma5'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['你以前教过英语吗？'],
           'occurrences': 1,
           'example_pinyin': 'nǐ yǐ qián jiāo guò yīng yǔ ma',
           'example_translation': 'Você já ensinou inglês antes?',
           'display_pinyin': 'ma'},
 '20::钱': {'word': '钱',
           'answer': 'qian2',
           'pinyin_syllables': ['qian2'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我借到钱了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ jiè dào qián le',
           'example_translation': 'Consegui dinheiro emprestado.',
           'display_pinyin': 'qián'},
 '20::这': {'word': '这',
           'answer': 'zhe4',
           'pinyin_syllables': ['zhe4'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['对我来说，这份工作不太容易。'],
           'occurrences': 1,
           'example_pinyin': 'duì wǒ lái shuō zhè fèn gōng zuò bú tàiróng yì',
           'example_translation': 'Para mim, esse trabalho não é muito fácil.',
           'display_pinyin': 'zhè'},
 '20::个': {'word': '个',
           'answer': 'ge',
           'pinyin_syllables': ['ge5'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我会再讲一遍，或者换一个方法。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ huì zài jiǎng yí biàn huò zhě huàn yí ge fāng fǎ',
           'example_translation': 'Vou explicar outra vez ou mudar de método.',
           'display_pinyin': 'ge'},
 '20::来': {'word': '来',
           'answer': 'lai2',
           'pinyin_syllables': ['lai2'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我来中国已经很久了。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ lái zhōng guó yǐ jīng hěn jiǔ le',
           'example_translation': 'Já faz muito tempo que cheguei à China.',
           'display_pinyin': 'lái'},
 '20::学校': {'word': '学校',
            'answer': 'xue2xiao4',
            'pinyin_syllables': ['xue2', 'xiao4'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['你今天早上是怎么来学校的？'],
            'occurrences': 1,
            'example_pinyin': 'nǐ jīn tiān zǎo shang shì zěn me lái xué xiào de',
            'example_translation': 'Como você veio para a escola hoje de manhã?',
            'display_pinyin': 'xué xiào'},
 '20::学': {'word': '学',
           'answer': 'xue2',
           'pinyin_syllables': ['xue2'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我很幽默，学生们都很喜欢我。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ hěn yōu mò xué sheng men dōu hěn xǐ huan wǒ',
           'example_translation': 'Sou bem-humorado e todos os alunos gostam de mim.',
           'display_pinyin': 'xué'},
 '20::都': {'word': '都',
           'answer': 'dou1',
           'categories': ['Revisão · Aula 20'],
           'examples': ['小朋友都能听懂。'],
           'occurrences': 1,
           'display_pinyin': 'dōu',
           'example_pinyin': 'xiǎo péng you dōu néng tīng dǒng',
           'example_translation': 'Todas as crianças conseguem entender o que ouvem.'},
 '20::的': {'word': '的',
           'answer': 'de',
           'pinyin_syllables': ['de5'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我的发音很清楚，说得很慢。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ de fā yīn hěn qīng chu shuō de hěn màn',
           'example_translation': 'Minha pronúncia é clara e falo devagar.',
           'display_pinyin': 'de'},
 '20::有': {'word': '有',
           'answer': 'you3',
           'categories': ['Revisão · Aula 20'],
           'examples': ['你还有别的优点吗？'],
           'occurrences': 1,
           'display_pinyin': 'yǒu',
           'example_pinyin': 'nǐ hái yǒu bié de yōu diǎn ma',
           'example_translation': 'Você tem outras qualidades?'},
 '20::是': {'word': '是',
           'answer': 'shi4',
           'pinyin_syllables': ['shi4'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['这是我找到的第二份兼职工作。'],
           'occurrences': 1,
           'example_pinyin': 'zhè shì wǒ zhǎo dào de dì èr fèn jiān zhí gōng zuò',
           'example_translation': 'Este é o segundo emprego de meio período que consegui.',
           'display_pinyin': 'shì'},
 '20::自己': {'word': '自己',
            'answer': 'zi4ji3',
            'pinyin_syllables': ['zi4', 'ji3'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['请介绍一下自己。'],
            'occurrences': 1,
            'example_pinyin': 'qǐng jiè shào yí xià zì jǐ',
            'example_translation': 'Por favor, apresente-se brevemente.',
            'display_pinyin': 'zì jǐ'},
 '20::喜欢': {'word': '喜欢',
            'answer': 'xi3huan',
            'pinyin_syllables': ['xi3', 'huan5'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['我很幽默，学生们都很喜欢我。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ hěn yōu mò xué sheng men dōu hěn xǐ huan wǒ',
            'example_translation': 'Sou bem-humorado e todos os alunos gostam de mim.',
            'display_pinyin': 'xǐ huan'},
 '20::为什么': {'word': '为什么',
             'answer': 'wei4shen2me',
             'categories': ['Revisão · Aula 20'],
             'examples': ['你为什么喜欢跑步？', '他为什么不喜欢游泳？', '你为什么最喜欢打网球？', '她为什么每周去健身房？'],
             'occurrences': 1,
             'display_pinyin': 'wèishénme'},
 '20::觉得': {'word': '觉得',
            'answer': 'jue2de',
            'categories': ['Revisão · Aula 20'],
            'examples': ['我觉得肉夹馍是中式汉堡包。'],
            'occurrences': 1,
            'display_pinyin': 'juéde',
            'example_pinyin': 'wǒ jué deròu jiā mó shì zhōng shì hàn bǎo bāo',
            'example_translation': 'Acho que o roujiamo é um hambúrguer ao estilo chinês.'},
 '20::经常': {'word': '经常',
            'answer': 'jing1chang2',
            'pinyin_syllables': ['jing1', 'chang2'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['我经常跟中国朋友交流。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jīng cháng gēn zhōng guó péng you jiāo liú',
            'example_translation': 'Costumo conversar com amigos chineses.',
            'display_pinyin': 'jīng cháng'},
 '20::跟': {'word': '跟',
           'answer': 'gen1',
           'categories': ['Revisão · Aula 20'],
           'examples': ['我经常跟中国朋友交流。'],
           'occurrences': 1,
           'display_pinyin': 'gēn',
           'example_pinyin': 'wǒ jīng cháng gēn zhōng guó péng you jiāo liú',
           'example_translation': 'Costumo conversar com amigos chineses.'},
 '20::他们': {'word': '他们',
            'answer': 'ta1men',
            'pinyin_syllables': ['ta1', 'men5'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['他们在客厅聊天儿。'],
            'occurrences': 1,
            'example_pinyin': 'tāmen zài kètīng liáotiānr.',
            'example_translation': 'Eles estão conversando na sala.',
            'display_pinyin': 'tā men'},
 '20::朋友': {'word': '朋友',
            'answer': 'peng2you',
            'pinyin_syllables': ['peng2', 'you5'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['我经常跟中国朋友交流。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ jīng cháng gēn zhōng guó péng you jiāo liú',
            'example_translation': 'Costumo conversar com amigos chineses.',
            'display_pinyin': 'péng you'},
 '20::真': {'word': '真',
           'answer': 'zhen1',
           'pinyin_syllables': ['zhen1'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我的朋友真诚、善良、热情。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ de péng you zhēn chéng shàn liángrè qíng',
           'example_translation': 'Meu amigo é sincero, bondoso e caloroso.',
           'display_pinyin': 'zhēn'},
 '20::不错': {'word': '不错',
            'answer': 'bu2cuo4',
            'pinyin_syllables': ['bu2', 'cuo4'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['我在学做西餐，做得也不错。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ zài xué zuò xīcān, zuò de yě búcuò.',
            'example_translation': 'Estou aprendendo a preparar comida ocidental e estou me saindo bem.',
            'display_pinyin': 'bú cuò'},
 '20::别的': {'word': '别的',
            'answer': 'bie2de',
            'categories': ['Revisão · Aula 20'],
            'examples': ['你还有别的优点吗？'],
            'occurrences': 1,
            'display_pinyin': 'biéde',
            'example_pinyin': 'nǐ hái yǒu bié de yōu diǎn ma',
            'example_translation': 'Você tem outras qualidades?'},
 '20::想': {'word': '想',
           'answer': 'xiang3',
           'categories': ['Revisão · Aula 20'],
           'examples': ['我很渴，想喝水。'],
           'occurrences': 1,
           'display_pinyin': 'xiǎng',
           'example_pinyin': 'wǒ hěn kě xiǎng hē shuǐ',
           'example_translation': 'Estou com muita sede e quero beber água.'},
 '20::打算': {'word': '打算',
            'answer': 'da3suan4',
            'pinyin_syllables': ['da3', 'suan4'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['我打算再买一个手机。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ dǎ suàn zài mǎi yí ge shǒu jī',
            'example_translation': 'Pretendo comprar outro celular.',
            'display_pinyin': 'dǎ suàn'},
 '20::上课': {'word': '上课',
            'answer': 'shang4ke4',
            'pinyin_syllables': ['shang4', 'ke4'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['即使明天下雨，我也要去上课。'],
            'occurrences': 1,
            'example_pinyin': 'jí shǐ míng tiān xià yǔ wǒ yě yào qù shàng kè',
            'example_translation': 'Mesmo que chova amanhã, vou à aula.',
            'display_pinyin': 'shàng kè'},
 '20::可以': {'word': '可以',
            'answer': 'ke3yi3',
            'pinyin_syllables': ['ke3', 'yi3'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['我希望可以做好这份工作。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ xī wàng kě yǐ zuò hǎo zhè fèn gōng zuò',
            'example_translation': 'Espero conseguir fazer bem este trabalho.',
            'display_pinyin': 'kě yǐ'},
 '20::但是': {'word': '但是',
            'answer': 'dan4shi4',
            'pinyin_syllables': ['dan4', 'shi4'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['书法很难，但是我学得还可以。'],
            'occurrences': 1,
            'example_pinyin': 'shūfǎ hěn nán, dànshì wǒ xué de hái kěyǐ.',
            'example_translation': 'Caligrafia é difícil, mas estou aprendendo razoavelmente bem.',
            'display_pinyin': 'dàn shì'},
 '20::不太': {'word': '不太',
            'answer': 'bu2tai4',
            'pinyin_syllables': ['bu2', 'tai4'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['对我来说，这份工作不太容易。'],
            'occurrences': 1,
            'example_pinyin': 'duì wǒ lái shuō zhè fèn gōng zuò bú tàiróng yì',
            'example_translation': 'Para mim, esse trabalho não é muito fácil.',
            'display_pinyin': 'bú tài'},
 '20::和': {'word': '和',
           'answer': 'he2',
           'pinyin_syllables': ['he2'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我愿意跟她和解。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ yuàn yì gēn tā hé jiě',
           'example_translation': 'Estou disposto a me reconciliar com ela.',
           'display_pinyin': 'hé'},
 '20::也': {'word': '也',
           'answer': 'ye3',
           'pinyin_syllables': ['ye3'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我的家人很包容，也很体贴。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ de jiārén hěn bāoróng yě hěn tǐ tiē',
           'example_translation': 'Minha família é tolerante e atenciosa.',
           'display_pinyin': 'yě'},
 '20::把': {'word': '把',
           'answer': 'ba3',
           'pinyin_syllables': ['ba3'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['警察把女司机带走了。'],
           'occurrences': 1,
           'example_pinyin': 'jǐng chá bǎ nǚ sī jī dài zǒu le',
           'example_translation': 'A polícia levou a motorista.',
           'display_pinyin': 'bǎ'},
 '20::马克': {'word': '马克',
            'answer': 'ma3ke4',
            'pinyin_syllables': ['ma3', 'ke4'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['我没有马克那么高。'],
            'occurrences': 1,
            'example_pinyin': 'wǒ méi yǒu mǎ kè nà me gāo',
            'example_translation': 'Eu não sou tão alto quanto Mark.',
            'display_pinyin': 'mǎ kè'},
 '20::李佳': {'word': '李佳',
            'answer': 'li3jia1',
            'pinyin_syllables': ['li3', 'jia1'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['李佳请马克吃饭。'],
            'occurrences': 1,
            'example_pinyin': 'lǐ jiā qǐng mǎ kè chī fàn',
            'example_translation': 'Li Jia convida Mark para comer.',
            'display_pinyin': 'lǐ jiā'},
 '20::日记': {'word': '日记',
            'answer': 'ri4ji4',
            'pinyin_syllables': ['ri4', 'ji4'],
            'categories': ['Revisão · Aula 20'],
            'examples': ['马克每天写日记。'],
            'occurrences': 1,
            'example_pinyin': 'mǎ kè měi tiān xiěrì jì',
            'example_translation': 'Mark escreve no diário todos os dias.',
            'display_pinyin': 'rì jì'},
 '20::到': {'word': '到',
           'answer': 'dao4',
           'pinyin_syllables': ['dao4'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我找到了一份兼职工作。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ zhǎo dào le yí fèn jiān zhí gōng zuò',
           'example_translation': 'Consegui um emprego de meio período.',
           'display_pinyin': 'dào'},
 '20::书': {'word': '书',
           'answer': 'shu1',
           'pinyin_syllables': ['shu1'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['我学过书法。'],
           'occurrences': 1,
           'example_pinyin': 'wǒ xué guò shū fǎ',
           'example_translation': 'Já estudei caligrafia.',
           'display_pinyin': 'shū'},
 '20::本': {'word': '本',
           'answer': 'ben3',
           'pinyin_syllables': ['ben3'],
           'categories': ['Revisão · Aula 20'],
           'examples': ['他看懂这本书了。'],
           'occurrences': 1,
           'example_pinyin': 'tā kàn dǒng zhè běn shū le',
           'example_translation': 'Ele entendeu este livro.',
           'display_pinyin': 'běn'}}
LESSON20_TRANSLATIONS = {'20::面试': 'entrevista; fazer uma entrevista',
 '20::交流': 'conversar; comunicar-se; trocar ideias',
 '20::以前': 'antes; antigamente',
 '20::教': 'ensinar',
 '20::发音': 'pronúncia; pronunciar',
 '20::清楚': 'claro; com clareza',
 '20::慢': 'devagar; lento',
 '20::懂': 'entender; compreender',
 '20::如果': 'se (condição)',
 '20::讲': 'falar; explicar; contar',
 '20::或者': 'ou (em afirmações)',
 '20::方法': 'método; maneira',
 '20::优点': 'qualidade; ponto forte; vantagem',
 '20::幽默': 'bem-humorado; humor',
 '20::故事': 'história; conto',
 '20::当然': 'claro; naturalmente',
 '20::准备': 'preparar; preparar-se',
 '20::已经': 'já',
 '20::久': 'muito tempo; duradouro',
 '20::份': 'classificador de empregos, porções e documentos',
 '20::兼职': 'emprego de meio período; trabalho parcial',
 '20::曾经': 'já; em algum momento no passado',
 '20::对…来说': 'para alguém; do ponto de vista de alguém',
 '20::容易': 'fácil',
 '20::信心': 'confiança',
 '20::虽然': 'embora; apesar de',
 '20::紧': 'apertado; escasso (tempo)',
 '20::有意思': 'interessante; divertido',
 '20::家人': 'familiares; família',
 '20::包容': 'tolerante; acolher as diferenças',
 '20::体贴': 'atencioso; cuidadoso com os outros',
 '20::孝心': 'dedicação e respeito pelos pais',
 '20::真诚': 'sincero',
 '20::善良': 'bondoso',
 '20::热情': 'caloroso; entusiasmado',
 '20::勤奋': 'esforçado; diligente',
 '20::责任心': 'senso de responsabilidade',
 '20::渴': 'com sede',
 '20::累': 'cansado',
 '20::手表': 'relógio de pulso',
 '20::重': 'pesado',
 '20::简单': 'simples; fácil',
 '20::房子': 'casa; imóvel',
 '20::找工作': 'procurar emprego',
 '20::工作': 'trabalho; trabalhar',
 '20::找': 'procurar',
 '20::当': 'ser; trabalhar como',
 '20::工程师': 'engenheiro',
 '20::过': 'partícula de experiência passada; passar',
 '20::学过': 'já ter estudado; ter aprendido antes',
 '20::教过': 'já ter ensinado',
 '20::去过': 'já ter ido',
 '20::做过': 'já ter feito; já ter trabalhado como',
 '20::适合': 'ser adequado; ter perfil para',
 '20::小朋友': 'criança; amiguinho',
 '20::听懂': 'entender o que se ouve',
 '20::没听懂': 'não ter entendido o que se ouviu',
 '20::准备好': 'estar pronto; preparar bem',
 '20::有信心': 'ter confiança',
 '20::有孝心': 'ser dedicado aos pais',
 '20::有责任心': 'ser responsável',
 '20::同事': 'colega de trabalho',
 '20::考官': 'examinador; entrevistador',
 '20::谢谢': 'obrigado',
 '20::而且': 'além disso; e também',
 '20::学生': 'aluno; estudante',
 '20::学生们': 'os alunos',
 '20::遍': 'vez (uma ação completa)',
 '20::换': 'trocar; mudar',
 '20::英文': 'língua inglesa; inglês escrito',
 '20::希望': 'esperar; ter esperança',
 '20::老板': 'chefe; proprietário',
 '20::让': 'deixar; permitir; pedir que alguém faça',
 '20::上班': 'ir trabalhar; estar no trabalho',
 '20::晚上': 'noite; à noite',
 '20::第二': 'segundo (ordinal)',
 '20::找到': 'encontrar; conseguir localizar',
 '20::还是': 'ainda; ou (em perguntas alternativas)',
 '20::做好': 'fazer bem; deixar pronto',
 '20::学好': 'aprender bem; dominar',
 '20::教好': 'ensinar bem',
 '20::送到': 'entregar; fazer chegar',
 '20::送': 'enviar; entregar; levar',
 '20::写得完': 'conseguir terminar de escrever',
 '20::写不完': 'não conseguir terminar de escrever',
 '20::写完': 'terminar de escrever',
 '20::写对': 'escrever corretamente',
 '20::写错': 'escrever errado',
 '20::听得懂': 'conseguir entender ao ouvir',
 '20::听不懂': 'não conseguir entender ao ouvir',
 '20::听清楚': 'ouvir com clareza',
 '20::听见': 'ouvir; escutar um som',
 '20::卖完': 'vender tudo; esgotar',
 '20::吃完': 'terminar de comer',
 '20::说完': 'terminar de falar',
 '20::完': 'terminar; acabar (complemento de resultado)',
 '20::对': 'correto; para; em relação a',
 '20::错': 'errado; erro',
 '20::作业': 'lição de casa; tarefa',
 '20::学会': 'aprender a fazer; dominar uma habilidade',
 '20::电话号码': 'número de telefone',
 '20::记住': 'memorizar; guardar na memória',
 '20::滑': 'escorregar; deslizar',
 '20::滑倒': 'escorregar e cair',
 '20::饱': 'satisfeito; cheio (após comer)',
 '20::吃饱': 'comer até ficar satisfeito',
 '20::买到': 'conseguir comprar',
 '20::票': 'passagem; ingresso; bilhete',
 '20::看懂': 'entender ao ler ou ver',
 '20::看见': 'ver; avistar',
 '20::借': 'pedir emprestado; emprestar',
 '20::借到': 'conseguir emprestado',
 '20::舒服': 'confortável; sentir-se bem',
 '20::不舒服': 'não se sentir bem; desconfortável',
 '20::电脑': 'computador',
 '20::水果店': 'frutaria',
 '20::水果': 'fruta',
 '20::好看': 'bonito; interessante de assistir',
 '20::看完': 'terminar de ler ou assistir',
 '20::部': 'classificador de filmes e aparelhos',
 '20::山': 'montanha',
 '20::介绍': 'apresentar; introduzir',
 '20::老': 'velho; elemento de 老师 e 老板',
 '20::师': 'mestre; professor; elemento de 老师',
 '20::考': 'examinar; fazer prova; elemento de 考官',
 '20::交': 'trocar; relacionar-se; elemento de 交流',
 '20::流': 'fluir; elemento de 交流',
 '20::清': 'claro; limpo; elemento de 清楚',
 '20::楚': 'claro; elemento de 清楚',
 '20::介': 'intermediar; elemento de 介绍',
 '20::绍': 'elemento de 介绍 (apresentar)',
 '20::字': 'caractere; letra',
 '20::还有': 'ainda ter; além disso',
 '20::英语': 'língua inglesa; inglês',
 '20::听': 'ouvir; escutar',
 '20::会': 'saber fazer; conseguir',
 '20::给': 'dar; para; em benefício de',
 '20::认真': 'atento; sério; dedicado',
 '20::老师': 'professor(a)',
 '20::警察': 'policial; polícia',
 '20::医生': 'médico',
 '20::中文': 'língua chinesa; chinês',
 '20::说': 'falar; dizer',
 '20::得': 'partícula que liga o verbo à avaliação da ação',
 '20::很': 'muito',
 '20::我': 'eu',
 '20::你': 'você',
 '20::他': 'ele',
 '20::她': 'ela',
 '20::我们': 'nós',
 '20::什么': 'o que; que',
 '20::做': 'fazer; preparar (comida)',
 '20::书法': 'caligrafia chinesa',
 '20::打': 'jogar; praticar (esporte ou jogo)',
 '20::麻将': 'mahjong',
 '20::汉语': 'língua chinesa; mandarim',
 '20::现在': 'agora',
 '20::中国': 'China',
 '20::去': 'ir',
 '20::能': 'poder; conseguir; ser capaz de',
 '20::怎么办': 'o que fazer',
 '20::再': 'de novo; outra vez',
 '20::一': 'um; uma',
 '20::明天': 'amanhã',
 '20::外卖': 'comida para viagem ou entrega',
 '20::快': 'rápido; depressa',
 '20::时间': 'tempo; horário',
 '20::不过': 'mas; porém',
 '20::一个': 'um; uma (com classificador)',
 '20::就': 'então; logo; já',
 '20::好': 'bom; bem',
 '20::写': 'escrever',
 '20::汉字': 'caracteres chineses',
 '20::不': 'não',
 '20::没': 'não (passado ou ausência)',
 '20::了': 'partícula de ação concluída ou mudança',
 '20::吃': 'comer',
 '20::卖': 'vender',
 '20::吗': 'partícula de pergunta (sim/não)',
 '20::钱': 'dinheiro',
 '20::这': 'isto; este; esta',
 '20::个': 'classificador geral',
 '20::来': 'vir',
 '20::学校': 'escola',
 '20::学': 'aprender; estudar',
 '20::都': 'todos; ambos',
 '20::的': 'partícula de posse ou atribuição',
 '20::有': 'ter; haver; existir',
 '20::是': 'ser; estar',
 '20::自己': 'si mesmo; próprio',
 '20::喜欢': 'gostar de',
 '20::为什么': 'por quê',
 '20::觉得': 'achar; considerar',
 '20::经常': 'frequentemente; com frequência',
 '20::跟': 'com; junto com',
 '20::他们': 'eles; elas',
 '20::朋友': 'amigo(a)',
 '20::真': 'realmente; de fato',
 '20::不错': 'bom; nada mal',
 '20::别的': 'outro(s); outra(s)',
 '20::想': 'querer; ter vontade de',
 '20::打算': 'planejar; pretender',
 '20::上课': 'ter aula; assistir à aula',
 '20::可以': 'poder; ser possível',
 '20::但是': 'mas; porém',
 '20::不太': 'não muito',
 '20::和': 'e; com',
 '20::也': 'também',
 '20::把': 'partícula que antepõe o objeto à ação',
 '20::马克': 'Mark (nome próprio)',
 '20::李佳': 'Li Jia (nome próprio)',
 '20::日记': 'diário pessoal',
 '20::到': 'chegar; até; para',
 '20::书': 'livro',
 '20::本': 'classificador de livros'}
BLOCK20_WORDS = list(LESSON20_CARDS)
CARDS.update(LESSON20_CARDS)
WORD_TRANSLATIONS.update(LESSON20_TRANSLATIONS)
for _cid, _card in LESSON20_CARDS.items():
    WORD_PINYIN[_cid] = _card['answer']
    if 'example_translation' in _card:
        EXAMPLE_TRANSLATIONS.setdefault(_card['examples'][0], _card['example_translation'])

BLOCK_WORDS = {"16": BLOCK16_WORDS, "17": BLOCK17_WORDS, "18": BLOCK18_WORDS, "19": BLOCK19_WORDS, "20": BLOCK20_WORDS}
BLOCK_LABELS = {"16": "Bloco 16", "17": "Bloco 17", "18": "Bloco 18", "19": "Bloco 19", "20": "Bloco 20"}
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
STATE_VERSION = 5
NEW_PRESSURE_CAP = 20
TRAINED_INDEX = 10
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
                next_is_vowel = bool(next_c) and (next_c in "aeiouvü" or next_c in ACCENT_TO_BASE)
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
    if CARDS.get(word, {}).get("display_pinyin"):
        return CARDS[word]["display_pinyin"]
    syllables = CARDS.get(word, {}).get("pinyin_syllables")
    if syllables:
        # Limites explícitos evitam atribuir tons a sílabas neutras intermediárias.
        return " ".join(accented_pinyin(s) for s in syllables).replace(" r", "r")
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
    variants = {main, *CARDS[word].get("answer_variants", [])}
    if CARDS[word]["word"] == "谁":
        variants.add("shui2")   # 谁: shéi ou shuí
    if CARDS[word]["word"] == "聊天儿":
        # O diacrítico de tiānr abrange a sílaba inteira com erhua.
        variants.add("liao2tianr1")
    return {normalize_pinyin(v) for v in variants}


def fresh_record() -> dict:
    return {"hits": 0, "misses": 0, "total_misses": 0, "correct_streak": 0,
            "stage": 0, "stage_repetitions": 0,
            "due": 0, "last_interval": None}


def initial_state() -> dict:
    default = next(iter(SESSIONS))
    return {"version": STATE_VERSION, "completed": 0,
            "session_counts": {sid: 0 for sid in SESSIONS},
            "rounds_without_new": {sid: 0 for sid in SESSIONS},
            "cards": {w: fresh_record() for w in CARDS},
            "current": None, "graded": False, "feedback": "",
            "was_correct": False, "early": False,
            "block": SESSION_BLOCK[default], "session": default}


def training_index(record: dict) -> int:
    return record["correct_streak"] - record["misses"]


def is_trained(record: dict) -> bool:
    return training_index(record) >= TRAINED_INDEX


def training_label(record: dict) -> str:
    index = training_index(record)
    if index >= TRAINED_INDEX:
        return "Treinado"
    if index >= 5:
        return "Bom"
    if index >= 1:
        return "OK"
    return "Em treino" if record["hits"] or record["total_misses"] else "Novo"


def is_new(record: dict) -> bool:
    return not (record["hits"] or record["total_misses"])


def new_card_pressure(state: dict, session_id: str) -> int:
    """Chance percentual de um novo cartão passar à frente de uma revisão."""
    return min(NEW_PRESSURE_CAP, state["rounds_without_new"][session_id])


def session_training(state: dict, session_id: str) -> tuple[int, int]:
    words = SESSIONS[session_id]
    return sum(is_trained(state["cards"][word]) for word in words), len(words)


def session_is_trained(state: dict, session_id: str) -> bool:
    trained, total = session_training(state, session_id)
    return total > 0 and trained == total


def session_display(state: dict, session_id: str) -> str:
    suffix = " · ✓ Treinada" if session_is_trained(state, session_id) else ""
    return SESSION_LABELS[session_id] + suffix


def repetitions_required(record: dict) -> int:
    return BASE_REPETITIONS[record["stage"]] + record["total_misses"]


def advance_stage(record: dict):
    record["stage_repetitions"] += 1
    if record["stage_repetitions"] >= repetitions_required(record):
        record["stage_repetitions"] = 0
        record["stage"] = min(record["stage"] + 1, len(CORRECT_INTERVALS) - 1)


def migrate_state(data: dict) -> dict:
    """Preserva os dados das versões 2–5, incluindo os relógios de revisão.

    Antes da v5, não havia registro explícito de acertos consecutivos. Sem
    erros históricos, todos os acertos são consecutivos. Com erros, usamos
    apenas a sequência mínima comprovada pela etapa e suas repetições;
    ciclos antigos completos na última faixa não podem ser reconstruídos.
    A pressão inicia em zero quando não havia esse registro.
    """
    state = initial_state()
    version = data.get("version")
    if version not in (2, 3, 4, STATE_VERSION):
        return state
    state["completed"] = max(0, int(data.get("completed", 0)))
    old_counts = data.get("session_counts", {})
    old_cards = data.get("cards", {})
    legacy_ids = {name: f"16:{i:02d}" for i, name in enumerate(LEGACY_SESSIONS, 1)}
    for old_sid, count in old_counts.items():
        sid = old_sid if version >= 4 else legacy_ids.get(old_sid)
        if sid in SESSIONS:
            state["session_counts"][sid] = max(0, int(count))
    if version == STATE_VERSION:
        for sid in SESSIONS:
            state["rounds_without_new"][sid] = min(NEW_PRESSURE_CAP, max(0, int(
                data.get("rounds_without_new", {}).get(sid, 0))))
    for word, rec in state["cards"].items():
        old = old_cards.get(word)
        if not isinstance(old, dict):
            continue
        rec["hits"] = max(0, int(old.get("hits", 0)))
        rec["misses"] = max(0, int(old.get("misses", 0)))
        rec["total_misses"] = max(rec["misses"], int(old.get("total_misses", rec["misses"])))
        if version >= 4:
            rec["stage"] = max(0, min(len(CORRECT_INTERVALS)-1, int(old.get("stage", 0))))
            rec["stage_repetitions"] = max(0, min(repetitions_required(rec)-1,
                                                   int(old.get("stage_repetitions", 0))))
            old_clock = int(old_counts.get(WORD_SESSION[word], 0))
        else:
            for _ in range(min(6, rec["hits"], max(0, int(old.get("stage", 0))))):
                advance_stage(rec)
            old_clock = (int(old_counts.get(LEGACY_WORD_SESSION.get(word), 0))
                         if version == 3 else state["completed"])
        if version == STATE_VERSION:
            streak = max(0, int(old.get("correct_streak", 0)))
        elif rec["total_misses"] == 0:
            streak = rec["hits"]
        elif version == 4:
            streak = (sum(BASE_REPETITIONS[i] + rec["total_misses"]
                          for i in range(rec["stage"])) + rec["stage_repetitions"])
        else:
            streak = min(6, max(0, int(old.get("stage", 0))))
        rec["correct_streak"] = min(rec["hits"], streak)
        remaining = min(CORRECT_INTERVALS[-1][1], int(old.get("due", 0)) - old_clock)
        rec["due"] = max(0, state["session_counts"][WORD_SESSION[word]] + remaining)
        last = old.get("last_interval")
        rec["last_interval"] = min(100, max(0, int(last))) if last is not None else None
    old_sid = data.get("session")
    sid = old_sid if version >= 4 else legacy_ids.get(old_sid)
    if sid in SESSIONS:
        state["session"] = sid
    current = data.get("current")
    if current in CARDS:
        state["session"] = WORD_SESSION[current]
        if data.get("graded") or not is_trained(state["cards"][current]):
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
    """Revisões vencidas cedem a novos cartões com chance de 0–20%.

    O sorteio só ocorre quando novos e vencidos disputam a próxima rodada.
    Não altera prazos nem intervalos: uma revisão adiada continua vencida.
    Sem vencidos, os novos mantêm a prioridade que já tinham.
    """
    recs = state["cards"]
    candidates = [w for w in candidates if not is_trained(recs[w])]
    if not candidates:
        return None, False
    session_id = state["session"]
    now = state["session_counts"][session_id]
    new = [w for w in candidates if is_new(recs[w])]
    due = [w for w in candidates if not is_new(recs[w]) and recs[w]["due"] <= now]
    pressure = new_card_pressure(state, session_id)
    if new and due and pressure and random.random() < pressure / 100:
        return random.choice(new), False
    if due:
        best_due = min(recs[w]["due"] for w in due)
        group = [w for w in due if recs[w]["due"] <= best_due + 2]
        if previous in group and len(group) > 1:
            group.remove(previous)
        weights = [1 + min(recs[w]["misses"], 10)*0.2 for w in group]
        return random.choices(group, weights=weights)[0], False
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
    was_new = is_new(rec)
    state["completed"] += 1
    session_name = WORD_SESSION[word]
    state["session_counts"][session_name] += 1
    state["rounds_without_new"][session_name] = (
        0 if was_new else min(NEW_PRESSURE_CAP,
                             state["rounds_without_new"][session_name] + 1))
    if correct:
        low, high = CORRECT_INTERVALS[rec["stage"]]
        rec["hits"] += 1
        rec["correct_streak"] += 1
        rec["misses"] = max(0, rec["misses"] - 1)
        advance_stage(rec)
    else:
        low, high = ERROR_INTERVAL
        rec["misses"] += 1
        rec["total_misses"] += 1
        rec["correct_streak"] = 0
        rec["stage"] = 0
        rec["stage_repetitions"] = 0
    delay = random.randint(low, high)
    rec["due"] = state["session_counts"][session_name] + delay
    rec["last_interval"] = delay
    return delay


def reset_session(state: dict, session_id: str):
    """Zera somente a sessão solicitada, preservando todas as outras."""
    state["completed"] = max(0, state["completed"] - state["session_counts"][session_id])
    state["session_counts"][session_id] = 0
    state["rounds_without_new"][session_id] = 0
    for word in SESSIONS[session_id]:
        state["cards"][word] = fresh_record()
    if state["session"] == session_id:
        state.update(current=None, graded=False, feedback="", was_correct=False, early=False)



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
        self.training_var = tk.StringVar()
        self.training_window = None
        self.current = self.data["current"]
        self._build_ui()
        if (self.current is None or self.current not in self._filtered()
                or (is_trained(self.data["cards"][self.current]) and not self.data["graded"])):
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
        style.configure("Training.Treeview", font=("Microsoft YaHei", 10), rowheight=30)
        style.configure("Training.Treeview.Heading", font=("Arial", 10, "bold"))
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
                                          values=[session_display(self.data, s) for s in self.sessions],
                                          state="readonly", width=42)
        self.session_combo.pack(side="left")
        self.session_combo.bind("<<ComboboxSelected>>", self._filter_changed)
        tk.Button(filter_box, text="◀", command=lambda: self._change_session(-1),
                  relief="flat", bg="#dfe8f5", padx=7).pack(side="left", padx=(6, 3))
        tk.Button(filter_box, text="▶", command=lambda: self._change_session(1),
                  relief="flat", bg="#dfe8f5", padx=7).pack(side="left")
        tk.Button(block_row, text="Zerar tudo", command=self._reset,
                  relief="flat", bg="#eff3f9", fg="#8b5360", padx=9, pady=6).pack(side="right")
        training_row = tk.Frame(root, bg="#eff3f9")
        training_row.pack(fill="x", pady=(0, 10))
        tk.Button(training_row, text="Progresso da sessão", command=self._show_training,
                  relief="flat", bg="#dfe8f5", fg="#164c85", padx=10, pady=7).pack(side="left")
        tk.Button(training_row, text="Zerar esta sessão", command=self._reset_session,
                  relief="flat", bg="#fee6e7", fg="#a52731", padx=10, pady=7).pack(side="right")
        self.training_banner = tk.Label(root, textvariable=self.training_var,
                                        font=("Arial", 11, "bold"), bg="#eff3f9",
                                        fg="#194f8b", anchor="w", justify="left")
        self.training_banner.pack(fill="x", pady=(0, 10))
        self._responsive_labels.append(self.training_banner)

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
        tk.Label(root, text=(f"{len(CARDS)} cartões · {len(BLOCKS)} bloco(s) · {len(SESSIONS)} sessões"),
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
        values = {"total": len(words), "seen": seen, "hits": hits,
                  "misses": misses,
                  "rate": f"{100*hits/(hits+misses):.1f}%" if hits+misses else "—"}
        for k, val in values.items():
            self.stats[k].config(text=str(val))
        session_id = self.data["session"]
        trained, total = session_training(self.data, session_id)
        complete = session_is_trained(self.data, session_id)
        self.progress["value"] = 100*trained/total if total else 0
        self.training_var.set(
            f"✓ Sessão treinada · {trained}/{total} cartões com índice 10"
            if complete else f"Treinamento: {trained}/{total} cartões treinados")
        self.training_banner.configure(fg="#137c48" if complete else "#194f8b")
        self.session_combo.configure(values=[session_display(self.data, s) for s in self.sessions])
        self.session_var.set(session_display(self.data, session_id))
        self._refresh_training()
        local_count = self.data["session_counts"][self.data["session"]]
        due = sum(1 for x in records if x["hits"]+x["misses"] > 0
                  and not is_trained(x) and x["due"] <= local_count)
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
            + (f" · Chance de novo: {new_card_pressure(self.data, session_id)}%"
               if len(words) > seen else "")
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
            complete = session_is_trained(self.data, self.data["session"])
            self.word_label.config(text="Sessão treinada ✓" if complete else "Sem palavras nesta sessão",
                                   font=("Arial", 26))
            self.info_var.set("Todos os cartões chegaram ao índice 10. Escolha outra sessão ou zere esta sessão."
                              if complete else "Escolha outra sessão")
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
        self.word_label.config(text=card["word"], font=("Microsoft YaHei", 46))
        early = " · Revisão antecipada (sem itens disponíveis)" if self.data["early"] else ""
        self.info_var.set(
            f"{record['hits']} acerto(s) no total · {record['correct_streak']} consecutivo(s) · "
            f"{record['misses']} erro(s) pendente(s)\n"
            f"Índice de treinamento: {training_index(record)}/10 · {training_label(record)}" + early)
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
            example_pin = card.get("example_pinyin") or pinyin_sentence(example)
            example_pt = card.get("example_translation") or EXAMPLE_TRANSLATIONS[example]
            self.example_pinyin_var.set(f"Pinyin: {example_pin}")
            self.example_translation_var.set(f"Tradução: {example_pt}")
            self.details.pack(fill="x", pady=(0, 10), before=self.check_btn.master)
            self.next_btn.configure(text="Concluir sessão  ✓"
                                    if session_is_trained(self.data, self.data["session"])
                                    else "Próxima palavra  →")
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
        if (self.current is None or self.data["graded"]
                or is_trained(self.data["cards"][self.current])):
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
            self.session_combo.current(new_idx)
            self._filter_changed()

    def _block_changed(self, _event=None):
        block = next(b for b, label in BLOCK_LABELS.items() if label == self.block_var.get())
        self.data["block"] = block
        self.sessions = list(BLOCKS[block])
        self.session_combo.configure(values=[session_display(self.data, s) for s in self.sessions])
        self.session_combo.current(0)
        self._filter_changed()

    def _filter_changed(self, _event=None):
        index = self.session_combo.current()
        if index < 0:
            return
        self.data["session"] = self.sessions[index]
        self.data["block"] = SESSION_BLOCK[self.data["session"]]
        if (self.current is None or self.current not in self._filtered()
                or (is_trained(self.data["cards"][self.current]) and not self.data["graded"])):
            self.data["graded"] = True
            self._next_card()
        else:
            self._render()
            save_state(self.data)

    def _show_training(self):
        if self.training_window is not None and self.training_window.winfo_exists():
            self.training_window.lift()
            self._refresh_training()
            return
        window = tk.Toplevel(self)
        self.training_window = window
        window.title("Progresso da sessão")
        window.geometry("810x560")
        window.minsize(720, 420)
        window.transient(self)
        window.configure(bg="#eff3f9")
        body = tk.Frame(window, bg="#eff3f9", padx=18, pady=16)
        body.pack(fill="both", expand=True)
        self.training_summary = tk.StringVar()
        tk.Label(body, textvariable=self.training_summary, font=("Arial", 12, "bold"),
                 bg="#eff3f9", fg="#194f8b", justify="left").pack(anchor="w", pady=(0, 10))
        tk.Label(body, text="Índice = acertos consecutivos − erros pendentes. Um erro reinicia a sequência.",
                 font=("Arial", 10), bg="#eff3f9", fg="#4d617c").pack(anchor="w", pady=(0, 4))
        tk.Label(body, text="1–4: OK     5–9: Bom     10: Treinado (sai da fila)",
                 font=("Arial", 10), bg="#eff3f9", fg="#4d617c").pack(anchor="w", pady=(0, 12))
        table_box = tk.Frame(body)
        table_box.pack(fill="both", expand=True)
        columns = ("word", "hits", "streak", "misses", "index", "status")
        self.training_table = ttk.Treeview(table_box, columns=columns, show="headings",
                                           style="Training.Treeview", selectmode="browse")
        for key, label, width in (("word", "Cartão", 160), ("hits", "Acertos totais", 115),
                                  ("streak", "Consecutivos", 115), ("misses", "Erros pendentes", 130),
                                  ("index", "Índice", 80), ("status", "Estado", 110)):
            self.training_table.heading(key, text=label)
            self.training_table.column(key, width=width, minwidth=60,
                                        anchor="w" if key in ("word", "status") else "center")
        scrollbar = ttk.Scrollbar(table_box, orient="vertical", command=self.training_table.yview)
        self.training_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.training_table.pack(side="left", fill="both", expand=True)
        self.training_table.tag_configure("Treinado", foreground="#137c48", background="#edf8f2")
        self.training_table.tag_configure("Bom", foreground="#194f8b")
        self.training_table.tag_configure("Novo", foreground="#788494")
        buttons = tk.Frame(body, bg="#eff3f9")
        buttons.pack(fill="x", pady=(12, 0))
        tk.Button(buttons, text="Zerar esta sessão", command=self._reset_session,
                  bg="#fee6e7", fg="#a52731", relief="flat", padx=12, pady=8).pack(side="left")
        tk.Button(buttons, text="Fechar", command=window.destroy,
                  bg="#dfe8f5", fg="#164c85", relief="flat", padx=12, pady=8).pack(side="right")
        self._refresh_training()

    def _refresh_training(self):
        if self.training_window is None or not self.training_window.winfo_exists():
            return
        sid = self.data["session"]
        trained, total = session_training(self.data, sid)
        self.training_summary.set(
            f"{BLOCK_LABELS[SESSION_BLOCK[sid]]} · {SESSION_LABELS[sid]}\n"
            f"{trained}/{total} cartões treinados"
            + (" · ✓ Sessão treinada" if session_is_trained(self.data, sid) else ""))
        existing = set(self.training_table.get_children())
        wanted = set(SESSIONS[sid])
        for word in existing - wanted:
            self.training_table.delete(word)
        for pos, word in enumerate(SESSIONS[sid]):
            record = self.data["cards"][word]
            label = training_label(record)
            values = (CARDS[word]["word"], record["hits"], record["correct_streak"], record["misses"],
                      training_index(record), label)
            if word in existing:
                self.training_table.item(word, values=values, tags=(label,))
                self.training_table.move(word, "", pos)
            else:
                self.training_table.insert("", "end", iid=word, values=values, tags=(label,))

    def _reset_session(self):
        sid = self.data["session"]
        if not messagebox.askyesno("Zerar esta sessão",
                                  f"Apagar o progresso de {SESSION_LABELS[sid]}?\n"
                                  "As outras sessões serão preservadas.", parent=self):
            return
        reset_session(self.data, sid)
        self.current = None
        self._next_card()

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
    assert all(WORD_BLOCK[w] == "16" for w in BLOCK16_WORDS)
    assert all(WORD_BLOCK[w] == "17" for w in BLOCK17_WORDS)
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
    for session_ids in BLOCKS.values():
        assert all(sum(hanzi_count(w) for w in SESSIONS[sid]) == 100
                   for sid in session_ids[:-1])
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
          f"{len(CARDS)} cartões | {len(SESSIONS)} sessões | "
          f"Blocos: {', '.join(BLOCKS)}")
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

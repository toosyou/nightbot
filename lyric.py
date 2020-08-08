import numpy as np
from nightbot import nightbot

lyrics = {
    '我難過的是':[
        '''放棄你 放棄愛\
        放棄的夢被打碎 忍住悲哀\
        我以為 是成全\
        你卻說你更不愉快''',

        '''忘了你 忘了愛\
        盡全力忘記我們 真心相愛\
        也忘了告訴你 失去的不能重來'''
    ],
    'I\'m still the same':[
        '''🤙🤙都好像沒有變🙄🙄Nothing changed👏👏還是討厭下雨天🌧🌧還是不愛認錯😨😨脾氣是硬了點😱😱 這我都清楚🧐🧐但我沒有辦法改變 我後悔高中花錢裝很吵的排氣管🔊🔊 想努力賺錢卻養成了壞習慣😡😡 我還想帶妳到處晃晃到處帶妳玩🥰😘 Cuz me without you it feels like😎😎'''
    ],
    'Without you':[
        '''I\'m still the same🤙🤙都好像沒有變🙄🙄Nothing changed👏👏還是討厭下雨天🌧🌧還是不愛認錯😨😨脾氣是硬了點😱😱 這我都清楚🧐🧐但我沒有辦法改變 我後悔高中花錢裝很吵的排氣管🔊🔊 想努力賺錢卻養成了壞習慣😡😡 我還想帶妳到處晃晃到處帶妳玩🥰😘 Cuz me without you it feels like😎😎'''
    ],
    '轟隆隆隆':[
        '🤣🤣隆隆隆隆衝衝衝衝😏😏😏拉風😎😎😎引擎發動🔑🔑🔑引擎發動+🚗+👉+🚗'
    ],
    '超跑情人夢':[
        '轟隆隆隆🤣🤣隆隆隆隆衝衝衝衝😏😏😏拉風😎😎😎引擎發動🔑🔑🔑引擎發動+🚗+👉+🚗'
    ],
    'BI BI':[
        '''紅燈停 綠燈行🚥🚥 看到行人要當心🚶♀🚶♀ 快車道 慢車道😈😈 平安回家才是王道 💪💪 開車🚗🚗不是騎車🏍🏍不怕沒戴安全帽👲👲只怕警察👮♂👮♂BI BI BI 叫我路邊靠 😩😩 BI BI BI BI BI 大燈忘了開😏😏 BI BI BI BI BI 駕照沒有帶 🤫🤫 BI BI BI BI BI 偷偷講電話😎😎 BI BI BI BI BI 沒繫安全帶 😬😬 我的夢幻車子🚗🚗就是最辣🌶🌶的美女👸👸 有她陪伴😏😏哪怕車上只有收音機 📻📻 我就像隻野狼🐺🐺身上披著羊🐑🐑的皮'''
    ],
    '子瑜':[
        '我老婆',
    ],
    '周子瑜':[
        '我老婆',
    ],
    '走起來':[
        '啊瓷'
    ],
    '哭啊':[
        '哭啊'
    ],
}

def random_lyrics(song):
    nightbot.send_channel_message(np.random.choice(lyrics[song]))
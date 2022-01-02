from transitions.extensions import GraphMachine

from utils import send_text_message, send_button_message
from linebot.models import MessageTemplateAction
from random import randrange
from translate import Translator

#global var
name=''
posibilities=100
lang=''
need_translate=''


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_start(self, event):
        text = event.message.text
        return bool(text.strip())

    def is_going_to_software(self, event):
        text = event.message.text
        return text.lower() == "初音"

    def is_going_to_chinese(self, event):
        text = event.message.text
        return text.lower() == "中文"

    def is_going_to_language(self, event):
        global name
        text = event.message.text
        name = text
        return text.lower() != "初音" and bool(text.strip())

    def is_going_to_german(self, event):
        text = event.message.text
        return text.lower() == "德文"

    def is_going_to_french(self, event):
        text = event.message.text
        return text.lower() == "法文"

    def is_going_to_prison(self, event):
        text=event.message.text
        return text.lower() == "steal"

    def is_going_to_nobody(self, event):
        text=event.message.text
        return text.lower() == "return"

    def is_going_to_friend(self, event):
        text=event.message.text
        return text.lower() == "gold_or_silver"

    def is_going_to_chat(self, event):
        text=event.message.text
        return text.lower() == "chat"

    def is_going_to_home(self, event):
        text=event.message.text
        return text.lower() == "home"

    def is_going_to_date(self, event):
        text=event.message.text
        return text.lower() == "date"

    def is_going_to_bff(self, event):
        text=event.message.text
        return text.lower() == "bff"


    def is_going_to_go(self, event):
        text=event.message.text
        return text.lower() == "go"

    def is_going_to_think(self, event):
        text=event.message.text
        return text.lower() == "think"

    def is_going_to_harass(self, event):
        text=event.message.text
        return text.lower() == "showgun"

    def is_going_to_poem(self, event):
        global need_translate
        text=event.message.text
        need_translate=text
        return text.lower() != "showgun" and bool(text.strip())

    def on_enter_software(self, event):
        title = '醒醒吧。'
        text = '初音只是個軟體( ｀д′)'
        btn = [
            MessageTemplateAction(
                label = '從頭開始',
                text = 'back'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_start(self, event):
        title = '邂逅開始'
        text = '請輸入(或選擇)一個名字成為你的邂逅對象'
        btn = [
            MessageTemplateAction(
                label = '莊坤達',
                text ='莊坤達'
            ),
            MessageTemplateAction(
                label = '初音',
                text = '初音'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)


    def on_enter_language(self, event):
        global name
        title = '關於' + name
        text = '請問他說什麼語言？'
        btn = [
            MessageTemplateAction(
                label = '德文',
                text ='德文'
            ),
            MessageTemplateAction(
                label = '法文',
                text = '法文'
            ),
            MessageTemplateAction(
                label = '中文',
                text = '中文'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_chinese(self, event):
        global name
        title = '有天走在路上你看到'+name+'在面前把錢包掉在地上'
        text = '你會...'
        btn = [
            MessageTemplateAction(
                label = '喊住他，歸還',
                text ='return'
            ),
            MessageTemplateAction(
                label = '問他是掉金錢包還是銀錢包',
                text = 'gold_or_silver'
            ),
            MessageTemplateAction(
                label = '自己偷偷暗崁起來',
                text = 'steal'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_prison(self, event):
        title = '利慾薰心。'
        text = '是什麼蒙蔽了我的雙眼？'
        btn = [
            MessageTemplateAction(
                label = '從頭開始',
                text = 'back'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
        self.go_back()

    def on_enter_nobody(self, event):
        title = '邂逅結束。'
        text = '你是個好人，但沒有緣份。'
        btn = [
            MessageTemplateAction(
                label = '從頭開始',
                text = 'back'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
        self.go_back()

    def on_enter_friend(self, event):
        global name
        title = '認識'
        text = name + '被你的話逗樂了，你決定...'
        btn = [
            MessageTemplateAction(
                label = '多聊幾句',
                text = 'chat'
            ),
            MessageTemplateAction(
                label = '回家吧，好累喔。',
                text = 'home'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_home(self, event):
        global name
        title = '休息是為了下一次的邂逅。'
        text = name + '與你就像兩條水平線，從此沒有交集。'
        btn = [
            MessageTemplateAction(
                label = '從頭來過',
                text = 'back'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
        self.go_back()
    
    def on_enter_chat(self, event):
        global name
        title = '邀約'
        text = name + '跟你的興趣、個性都很合，所以你決定..'
        btn = [
            MessageTemplateAction(
                label = '約會',
                text = 'date'
            ),
            MessageTemplateAction(
                label = '繼續當朋友',
                text = 'bff'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)


    def on_enter_bff(self, event):
        global name
        title = '相見恨晚'
        text = name + '與你成為一生的摯友。'
        btn = [
            MessageTemplateAction(
                label = '從頭來過',
                text = 'back'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
        self.go_back()

    def on_enter_date(self, event):
        global name
        title = '朋友以上？'
        text = '幾個月過去了，你跟' + name + '的關係越來越好，已經約會過了幾次，你確信你們互有好感，你決定...'
        btn = [
            MessageTemplateAction(
                label = '衝一波',
                text = 'go'
            ),
            MessageTemplateAction(
                label = '再想想好了',
                text = 'think'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def on_enter_think(self, event):
        global name
        title = '躊躇不定。'
        text = name + '覺得你對他沒興趣，跟別人在一起了。請祝福他。'
        btn = [
            MessageTemplateAction(
                label = '從頭開始',
                text = 'back'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
        self.go_back()

    def on_enter_go(self, event):
        global name
        global posibilities
        success=randrange(posibilities)
        if success==0:
            #reset posibilities
            title = '命中注定。'
            text = '你們開始交往了，當初他落掉的錢包難道就是命中注定？'
            btn = [
                MessageTemplateAction(
                    label = '從頭開始',
                    text = 'back'
                ),
                MessageTemplateAction(
                    label = str(posibilities),
                    text = 'back'
                ),
            ]
            url = 'https://imgur.com/7cTQOVP.jpg'
            send_button_message(event.reply_token, title, text, btn, url)
        else: 
            title = '再接再厲。'
            text = '你是個好人，' + name + '說。'
            btn = [
                MessageTemplateAction(
                    label = '從頭開始',
                    text = 'back'
                ),
                MessageTemplateAction(
                    label = str(posibilities),
                    text = 'back'
                ),
            ]
            url = 'https://imgur.com/7cTQOVP.jpg'
            send_button_message(event.reply_token, title, text, btn, url)
        
        self.go_back()
        
    def on_enter_german(self, event):
        global lang, need_translate
        lang='de'
        title = '我講中文他講德文，聽得懂嗎？'
        text = '請輸入(或選擇)中文語句'
        btn = [
            MessageTemplateAction(
                label = '要修(釣魚)竿嗎',
                text = 'showgun'
            ),
            MessageTemplateAction(
                label = '白日依山盡',
                text = '白日依山盡'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    
    def on_enter_poem(self, event):
        global lang, need_translate
        translator=Translator(provider='mymemory', to_lang=lang, from_lang="zh-TW")
        translation=translator.translate(need_translate)
        title = '要回答嗎？'
        
        #in case the message is to long
        if len(translation)>60:
            translation=translation[0:60]
        
        text = translation
        btn = [
            MessageTemplateAction(
                label = '要',
                text = 'bff'
            ),
            MessageTemplateAction(
                label = '不要',
                text = 'return'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    
    def on_enter_harass(self, event):
        title = '原來他聽得懂中文。'
        text = '你因性騷擾到警局備案。'
        btn = [
            MessageTemplateAction(
                label = '從頭來過',
                text = 'back'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
        self.go_back()

    def on_enter_french(self, event):
        title = '作者覺得法文難得要死0.0。'
        text = '乖，不要選這個選項。'
        btn = [
            MessageTemplateAction(
                label = '從頭來過',
                text = 'back'
            ),
        ]
        url = 'https://imgur.com/7cTQOVP.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
        self.go_back()


    def on_enter_user(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "輸入'start'重新開始")

    
    def on_exit_state2(self):
        print("Leaving state2")

    #def is_going_to_state3(self, event):



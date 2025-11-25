#!/usr/bin/env python3
"""
Скрипт инициализации конфигов на Render из переменных окружения
"""

import os
import sys

def create_main_config():
    """Создает configs/_main.cfg из переменных окружения"""
    
    golden_key = os.getenv('GOLDEN_KEY', '')
    tg_token = os.getenv('TG_TOKEN', '')
    
    if not golden_key or not tg_token:
        print("[ERROR] Необходимо установить GOLDEN_KEY и TG_TOKEN в Environment Variables на Render!")
        return False
    
    config_content = f"""[FunPay]
golden_key : {golden_key}
user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36
autoRaise : 1
autoResponse : 0
autoDelivery : 1
multiDelivery : 0
autoRestore : 1
autoDisable : 0
oldMsgGetMode : 0
locale : ru
keepSentMessagesUnread : 0

[Telegram]
enabled : 1
token : {tg_token}
secretKeyHash : $2b$12$omj93ERSTcF4Jcc3vuWspObyV.P86oOvXCyLwaNKcPSi6GOi1zi.q
blockLogin : 1

[BlockList]
blockDelivery : 0
blockResponse : 0
blockNewMessageNotification : 0
blockNewOrderNotification : 0
blockCommandNotification : 0

[NewMessageView]
includeMyMessages : 1
includeFPMessages : 1
includeBotMessages : 0
notifyOnlyMyMessages : 0
notifyOnlyFPMessages : 0
notifyOnlyBotMessages : 0
showImageName : 1

[Greetings]
ignoreSystemMessages : 0
onlyNewChats : 0
sendGreetings : 0
greetingsText : Привет, $chat_name!
greetingsCooldown : 2

[OrderConfirm]
watermark : 1
sendReply : 1
replyText : $username, спасибо за подтверждение заказа $order_id! Если не сложно, оставь, пожалуйста, отзыв!

[ReviewReply]
star1Reply : 0
star2Reply : 0
star3Reply : 0
star4Reply : 0
star5Reply : 1
star1ReplyText : 
star2ReplyText : 
star3ReplyText : 
star4ReplyText : 
star5ReplyText : 

[Proxy]
enable : 0
ip : 
port : 
login : 
password : 
check : 0

[Other]
watermark : 🐦
requestsDelay : 4
language : ru

"""
    
    os.makedirs("configs", exist_ok=True)
    
    with open("configs/_main.cfg", "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print("[OK] Конфиг configs/_main.cfg создан успешно!")
    return True

if __name__ == "__main__":
    if not os.path.exists("configs/_main.cfg"):
        if not create_main_config():
            sys.exit(1)
    else:
        print("[INFO] configs/_main.cfg уже существует")

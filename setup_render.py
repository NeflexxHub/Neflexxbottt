#!/usr/bin/env python3
"""
Инициализация конфигов на Render из Environment Variables
"""

import os
import sys
import traceback

def create_main_config():
    """Создает configs/_main.cfg из переменных окружения"""
    
    try:
        golden_key = os.getenv('GOLDEN_KEY', '').strip()
        tg_token = os.getenv('TG_TOKEN', '').strip()
        tg_admin_id = os.getenv('TG_ADMIN_ID', '1605524094').strip()
        
        print(f"[DEBUG] GOLDEN_KEY exists: {bool(golden_key)}")
        print(f"[DEBUG] TG_TOKEN exists: {bool(tg_token)}")
        print(f"[DEBUG] TG_ADMIN_ID: {tg_admin_id}")
        
        if not golden_key or not tg_token:
            print("[ERROR] ❌ GOLDEN_KEY или TG_TOKEN не установлены в Environment!")
            print("[ERROR] ❌ Установите их на Render в Settings → Environment")
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
        os.makedirs("storage/cache", exist_ok=True)
        
        with open("configs/_main.cfg", "w", encoding="utf-8") as f:
            f.write(config_content)
        
        # Добавляем админ ID в авторизованных пользователей
        import json
        auth_users_file = "storage/cache/tg_authorized_users.json"
        authorized_users = {tg_admin_id: {}}
        
        with open(auth_users_file, "w", encoding="utf-8") as f:
            json.dump(authorized_users, f, indent=2)
        
        print("[OK] ✅ Конфиг создан: configs/_main.cfg")
        print(f"[OK] ✅ Авторизированный пользователь добавлен: {tg_admin_id}")
        return True
        
    except Exception as e:
        print(f"[ERROR] ❌ Ошибка при создании конфига: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("[INFO] Инициализация Render deployment...")
    
    try:
        if not os.path.exists("configs/_main.cfg"):
            print("[INFO] Конфиг не найден, создаём...")
            if not create_main_config():
                print("[ERROR] Не удалось создать конфиг!")
                sys.exit(1)
        else:
            print("[INFO] Конфиг уже существует")
        
        print("[INFO] ✅ Инициализация завершена, запускаю main.py...")
        sys.exit(0)  # Успешное завершение
        
    except Exception as e:
        print(f"[ERROR] Критическая ошибка: {e}")
        traceback.print_exc()
        sys.exit(1)

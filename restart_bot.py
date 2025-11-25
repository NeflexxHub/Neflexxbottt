#!/usr/bin/env python3
"""
Скрипт автоматического перезапуска бота при падении.
Запускает main.py в бесконечном цикле, перезапуская при ошибках.
"""

import subprocess
import time
import sys

RESTART_DELAY = 5  # Задержка перед перезапуском (сек)
RESTART_ATTEMPTS = 0

def run_bot():
    """Запускает бота и ловит ошибки"""
    global RESTART_ATTEMPTS
    
    while True:
        try:
            RESTART_ATTEMPTS += 1
            print(f"\n{'='*60}")
            print(f"[RESTART] Попытка запуска #{RESTART_ATTEMPTS}")
            print(f"{'='*60}\n")
            
            # Запускаем main.py
            result = subprocess.run([sys.executable, 'main.py'], 
                                  capture_output=False, 
                                  text=True)
            
            print(f"\n[RESTART] ⚠️  Бот упал! Код выхода: {result.returncode}")
            
        except KeyboardInterrupt:
            print("\n[RESTART] 🛑 Остановка скрипта...")
            sys.exit(0)
        except Exception as e:
            print(f"\n[RESTART] ❌ Ошибка: {e}")
        
        # Ждём перед перезапуском
        print(f"[RESTART] ⏳ Перезапуск через {RESTART_DELAY} сек...")
        time.sleep(RESTART_DELAY)

if __name__ == "__main__":
    run_bot()

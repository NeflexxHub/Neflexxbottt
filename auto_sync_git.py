#!/usr/bin/env python3
"""
Автоматическая синхронизация плагинов и настроек с GitHub
Скрипт проверяет изменения и автоматически коммитит/пушит
"""

import os
import subprocess
import json
import time
from datetime import datetime

def run_git_command(cmd):
    """Запускает Git команду"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def has_changes():
    """Проверяет есть ли изменения в Git"""
    success, output, _ = run_git_command("git status --porcelain")
    if success:
        return bool(output.strip())
    return False

def auto_sync():
    """Автоматическая синхронизация"""
    
    print("[AUTO-SYNC] 🔄 Проверяю изменения...")
    
    # Проверяем стоим ли мы в Git репо
    success, _, _ = run_git_command("git rev-parse --git-dir")
    if not success:
        print("[AUTO-SYNC] ⚠️ Не в Git репо, пропускаю синхронизацию")
        return False
    
    # Проверяем есть ли изменения
    if not has_changes():
        print("[AUTO-SYNC] ✅ Нет изменений")
        return True
    
    print("[AUTO-SYNC] 📝 Есть изменения, коммитю...")
    
    # Добавляем ТОЛЬКО настройки плагинов (storage/plugins/)
    # Плагины (plugins/) загружаются один раз из Git и больше НЕ обновляются
    print("[AUTO-SYNC] 📂 Добавляю storage/plugins/ (только настройки)...")
    run_git_command("git add -A storage/plugins/ 2>/dev/null || true")
    run_git_command("git add -u 2>/dev/null || true")  # Добавляем удаленные файлы
    
    # Коммитим
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success, _, err = run_git_command(f'git commit -m "Auto-sync: {timestamp}"')
    
    if not success:
        if "nothing to commit" in err.lower():
            print("[AUTO-SYNC] ✅ Нечего коммитить")
            return True
        print(f"[AUTO-SYNC] ⚠️ Ошибка коммита: {err}")
        return False
    
    print("[AUTO-SYNC] ✅ Коммит создан")
    
    # Пушим
    print("[AUTO-SYNC] 🚀 Пушу на GitHub...")
    success, output, err = run_git_command("git push origin")
    
    if success:
        print("[AUTO-SYNC] ✅ Push успешен!")
        print(f"[AUTO-SYNC] Output: {output}")
        return True
    else:
        print(f"[AUTO-SYNC] ⚠️ Ошибка push: {err}")
        return False

if __name__ == "__main__":
    print("[AUTO-SYNC] 🤖 Запуск автоматической синхронизации...")
    auto_sync()
    print("[AUTO-SYNC] ✅ Синхронизация завершена")

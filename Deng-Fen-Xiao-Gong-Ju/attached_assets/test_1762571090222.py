numbers_dict = {
    1: None,
    2: None,
    5: None,
    8: None,
    10: None,
    11: None,
    12: None,
    13: None,
    14: None,
    15: None,
    17: None,
    18: None,
    19: None,
    20: None,
    23: None,
    24: None,
    25: None,
    26: None,
    27: None,
    28: None,
    30: None,
    31: None,
    32: None,
    33: None,
    34: None,
    35: None,
    36: None,
    37: None,
    38: None,
    40: None,
    41: None,
    42: None,
    43: None,
    44: None,
    45: None,
    46: None,
    47: None,
    49: None,
    50: None,
    51: None,
    52: None,
    53: None,
    55: None,
    56: None,
    57: None,
    58: None,
    59: None,
    60: None,
    61: None,
    62: None,
    63: None,
    64: None,
}

# 新增：匯入與持久化儲存
import os
import json
import sys
import subprocess
import shutil
SAVE_PATH = os.path.join(os.path.dirname(__file__), "numbers_dict.json")

# 新增：確保輸出立即 flush 並提供同樣行為的輸入提示
def safe_print(*args, **kwargs):
    kwargs.setdefault("flush", True)
    print(*args, **kwargs)

def safe_input(prompt=""):
    # 顯示提示並立即 flush，之後再呼叫內建 input
    if prompt:
        # 不在 input 裡印出提示，以避免在某些環境中提示被緩衝
        safe_print(prompt, end="")
    return input()

def load_dict():
    if os.path.exists(SAVE_PATH):
        try:
            with open(SAVE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {int(k): (int(v) if v is not None else None) for k, v in data.items()}
        except Exception as e:
            safe_print(f"載入儲存檔案失敗: {e}")
    return None

def save_dict():
    try:
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump({str(k): v for k, v in numbers_dict.items()}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        safe_print(f"儲存字典失敗: {e}")

_loaded = load_dict()
if _loaded:
    numbers_dict.update(_loaded)

# 每次啟動時自動清空所有 key 的值（設為 None），並儲存到檔案
for k in list(numbers_dict.keys()):
    numbers_dict[k] = None
save_dict()

def copy_to_clipboard(text: str) -> bool:
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except Exception:
        pass
    try:
        if sys.platform == "win32":
            subprocess.run("clip", input=text.encode("utf-8"), check=True, shell=True)
            return True
        if sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
            return True
        # linux: try xclip
        if shutil.which("xclip"):
            subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode("utf-8"), check=True)
            return True
    except Exception:
        pass
    return False

def process_input(s: str):
    s = s.strip()
    if s.lower() in ("exit", "quit"):
        return "exit"
    if s.lower() == "show":
        for k in sorted(numbers_dict):
            v = numbers_dict[k]
            safe_print(f"{k:02d} -> {v}" if v is not None else f"{k:02d} -> -")
        return None
    if s.lower() == "copy":
        values = ["" if numbers_dict[k] is None else str(numbers_dict[k]) for k in sorted(numbers_dict)]
        if all(v == "" for v in values):
            safe_print("沒有可複製的值。")
            return None
        text = "\n".join(values)
        if copy_to_clipboard(text):
            safe_print("值已複製到剪貼簿。")
        else:
            safe_print("無法複製到剪貼簿，以下為值：")
            safe_print(text)
        return None
    if not s.isdigit() or (len(s) not in [4, 5]):
        safe_print("輸入錯誤：請輸入4-5位數字(前兩位為key,後2-3位為value)。")
        return None

    key = int(s[:2])
    value = int(s[2:])
    if key not in numbers_dict:
        safe_print(f"錯誤：{key:02d} 號不在字典中，請重新輸入。")
        return None

    numbers_dict[key] = value
    save_dict()
    return None

def main():
    safe_print("輸入數字(show顯示字典,exit離開)。")
    try:
        while True:
            s = safe_input("> ")
            res = process_input(s)
            if res == "exit":
                break
    except (KeyboardInterrupt, EOFError):
        save_dict()

if __name__ == "__main__":
    main()


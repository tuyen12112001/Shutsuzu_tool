
import pyautogui
import pygetwindow as gw
import os
import time

def refresh_explorer(folder_path):
    """
    Refresh Explorer cho thư mục cụ thể:
    - Nếu cửa sổ Explorer đang mở thư mục đó, active và gửi F5.
    - Nếu không, mở lại thư mục.
    """
    try:
        folder_name = os.path.basename(folder_path)
        windows = [w for w in gw.getWindowsWithTitle(folder_name)]
        
        if windows:
            win = windows[0]
            win.activate()      # Đưa Explorer lên foreground
            time.sleep(0.5)     # Chờ active
            pyautogui.hotkey("f5")
            print(f"✅ Explorer refreshed cho thư mục: {folder_name}")
        else:
            os.startfile(folder_path)
            print(f"🔄 Không tìm thấy cửa sổ Explorer cho {folder_name}, đã mở lại thư mục.")
    except Exception as e:
        print(f"⚠ Lỗi khi refresh Explorer: {e}")

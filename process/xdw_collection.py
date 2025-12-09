import os
import time
import pyautogui
import pygetwindow as gw
import pyperclip
import difflib
from utils.check_ICAD_and_Docuworks import ensure_docuworks_running
from utils.rename import remove_suffix_3d_in_names
from utils.file_compare import compare_icd_xdw
from utils.refresh_explore import refresh_explorer

def delete_folder_in_docuworks(docuworks_folder):
    folder_name = os.path.basename(docuworks_folder)
    print(f"✅ Đang tìm và xóa folder: {folder_name}")

    if not ensure_docuworks_running():
        print("❌ Không tìm thấy cửa sổ DocuWorks.")
        return False

    # Về chế độ thư mục
    pyautogui.hotkey("alt", "left")
    time.sleep(1)

    # Bắt đầu duyệt
    direction = "down"
    steps = 0

    for i in range(1, 50):  # Giới hạn 50 lần để tránh vòng lặp vô hạn
        # Lấy tên folder hiện tại
        pyautogui.press("f2")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.5)
        pyautogui.press("esc")
        time.sleep(0.5)

        current_name = pyperclip.paste().strip()
        print(f"🔍 [{i}] Kiểm tra: {current_name}")

        
        # Tính độ giống nhau
        similarity = difflib.SequenceMatcher(None, current_name.lower(), folder_name.lower()).ratio()
        print(f"➡️ Độ giống nhau: {similarity:.2%}")

        # Nếu độ giống nhau >= 70%
        if similarity >= 0.7:
            print(f"✅ Tìm thấy folder giống '{folder_name}' ({similarity:.2%}), đang xóa...")
            pyautogui.press("delete")
            time.sleep(1)
            pyautogui.press("enter")
            print(f"✅ Đã xóa folder '{current_name}' trong DocuWorks.")
            return True


        # Điều hướng
        if direction == "down":
            pyautogui.hotkey("alt", "down")
            steps += 1
            if steps >= 5:  # Sau 10 lần thì đổi hướng
                direction = "up"
                steps = 0
        else:
            pyautogui.hotkey("alt", "up")
            steps += 1
            if steps >= 5:
                direction = "down"
                steps = 0

        time.sleep(0.8)

    print(f"⚠️ Không tìm thấy folder '{folder_name}' sau khi duyệt.")
    return False


def step3_collect_xdw(output_dir, docuworks_folder,icd_list):
    """
    ステップ3:
    - Kích hoạt DocuWorks.
    - Chọn tất cả file và cắt (Ctrl+X).
    - Mở Explorer đến output_dir và dán (Ctrl+V).
    - Xóa folder trong DocuWorks.
    """
    try:
        if not os.path.exists(output_dir):
            print(f"❌ Thư mục đích không tồn tại: {output_dir}")
            return 0

        print(f"✅ Sẽ dán file vào: {output_dir}")

        # Kiểm tra DocuWorks
        if not ensure_docuworks_running():
            print("❌ DocuWorks chưa mở hoặc không thể kích hoạt.")
            return 0

        # Chọn tất cả và cắt
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "c")
        time.sleep(1)

        # Mở thư mục đích trong Explorer
        os.startfile(output_dir)
        time.sleep(1)

        # Dán file vào thư mục đích
        pyautogui.hotkey("ctrl", "v")
        time.sleep(2)
        print("✅ Đã dán tất cả file vào thư mục đích.")

        # Đếm số file .xdw trong output_dir
        xdw_files = [f for f in os.listdir(output_dir) if f.lower().endswith(".xdw")]
        copied_count = len(xdw_files)
        print(f"✅ Tổng số file .xdw đã copy: {copied_count}")
        
        # ✅ So sánh trước khi rename
        missing, extra = compare_icd_xdw(output_dir, icd_list)

        try:
            rename_logs = remove_suffix_3d_in_names(
                target_dir=output_dir,
                target_exts=(".xdw",),
                conflict_strategy="skip"
            )

            changed = sum(1 for k, v in rename_logs.items() if v)
            print(f"🪄 '-3D' 除去によりリネームした .xdw 数: {changed}")
            refresh_explorer(output_dir)
        except Exception as e:
            print(f"❌ '-3D' 除去リネーム中にエラー: {e}")
            refresh_explorer(output_dir)
            pass

        return copied_count, missing, extra
    except Exception as e:
        print(f"❌ Lỗi khi thực hiện Step 3: {e}")
        return 0
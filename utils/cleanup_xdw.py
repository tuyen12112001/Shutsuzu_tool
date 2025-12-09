# process/cleanup_xdw.py
import os
import time
import pyautogui
from process.clear import force_delete
from utils.refresh_explore import refresh_explorer


def delete_all_xdw_files(output_folder):
    """
    削除 output_folder 内のすべての .xdw ファイル (強制削除)
    
    Args:
        output_folder: XDWファイルが格納されているフォルダパス
    
    Returns:
        (success: bool, deleted_count: int, error_msg: str)
    """
    try:
        if not os.path.exists(output_folder):
            return False, 0, f"フォルダが存在しません: {output_folder}"
        
        xdw_files = [f for f in os.listdir(output_folder) if f.lower().endswith(".xdw")]
        deleted_count = 0
        errors = []
        
        for xdw_file in xdw_files:
            file_path = os.path.join(output_folder, xdw_file)
            print(f"[削除開始] {xdw_file}")
            if force_delete(file_path):
                deleted_count += 1
                print(f"[削除完了] {xdw_file}")
            else:
                errors.append(f"{xdw_file} (強制削除失敗)")
        
        # ✅ Refresh Explorer sau khi xóa
        try:
            refresh_explorer(output_folder)
            print("🔄 Explorer refreshed sau khi xóa XDW.")
        except Exception:
            print(f"⚠ Lỗi khi refresh Explorer: {e}")
            pass

        if errors:
            error_msg = f"{deleted_count} 件削除しましたが、{len(errors)} 件削除できません:\n" + "\n".join(errors)
            print(f"[警告] {error_msg}")
            return False, deleted_count, error_msg
        
        success_msg = f"{deleted_count} 個のXDWファイルを強制削除しました。"
        print(f"[成功] {success_msg}")
        return True, deleted_count, success_msg
        
    except Exception as e:
        error_msg = f"XDWファイルの強制削除に失敗しました: {str(e)}"
        print(f"[エラー] {error_msg}")
        return False, 0, error_msg


def cleanup_xdw_on_user_request(app, output_folder):
    """
    ユーザーがXDWファイル削除を要求したときの処理
    削除 + メッセージ表示を一括処理
    
    Args:
        app: ShutsuzuuApp instance
        output_folder: XDWファイルが格納されているフォルダパス
    """
    from utils.UI_helpers import log_success, log_warning, log_error
    
    try:
        success, deleted_count, message = delete_all_xdw_files(output_folder)
        
        if success:
            # 成功メッセージ
            result_msg = (
                f" {deleted_count} 個のXDWファイルを削除しました。\n"
                "DocuWorksのファイルを確認してからお試しください。"
            )
            log_success(app, result_msg)
        else:
            # 失敗メッセージ
            result_msg = (
                f" XDWファイル削除に失敗しました:\n{message}\n"
                "ファイルを手動で削除してください。"
            )
            log_warning(app, result_msg)
                
        
# ✅ Refresh Explorer sau khi xóa XDW
        try:
            refresh_explorer(output_folder)
            print("🔄 Explorer refreshed sau khi xóa XDW.")
        except Exception as e:
            print(f"⚠ Lỗi khi refresh Explorer: {e}")
            pass
    
    except Exception as e:
        log_error(app, f"XDWファイル削除処理に失敗: {str(e)}")


def show_no_delete_xdw_message(app):
    """
    ユーザーが「削除しない」を選択した場合のメッセージ
    
    Args:
        app: ShutsuzuuApp instance
    """
    from utils.UI_helpers import log_warning
    
    no_delete_msg = (
        "⚠️ XDWファイルを削除しません。\n"
        "DocuWorksのファイルを確認して、手動で削除するか再度お試しください。"
    )
    log_warning(app, no_delete_msg)


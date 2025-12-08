
import os
import re

def remove_suffix_3d_in_names(
    target_dir: str,
    target_exts=(".xdw",),              # 例: (".xdw",) で XDW のみ対象。Noneなら全拡張子対象
    conflict_strategy: str = "skip"  # "append_counter" | "skip" | "overwrite"
):

    if not os.path.isdir(target_dir):
        raise FileNotFoundError(f"ディレクトリが見つかりません: {target_dir}")

    # 拡張子直前の '-3D' を検出・除去する正規表現（大小文字無視）
    # 例: 'name-3D.ext' -> 'name.ext'
    pattern = re.compile(r"^(?P<base>.+?)-3D(?P<ext>\.[^.]+)$", re.IGNORECASE)

    logs = {}

    for fname in os.listdir(target_dir):
        src_path = os.path.join(target_dir, fname)

        # ファイルのみ対象（フォルダは無視）
        if not os.path.isfile(src_path):
            logs[fname] = None
            continue

        # 対象拡張子フィルタ
        _, ext = os.path.splitext(fname)
        if target_exts is not None:
            # target_exts はタプル/リスト想定, 小文字比較
            if ext.lower() not in tuple(e.lower() for e in target_exts):
                logs[fname] = None
                continue

        m = pattern.match(fname)
        if not m:
            # '-3D' が拡張子直前ではない、または存在しない
            logs[fname] = None
            continue

        base = m.group("base")
        ext = m.group("ext")
        candidate_name = base + ext
        dst_path = os.path.join(target_dir, candidate_name)

        if os.path.exists(dst_path):
            if conflict_strategy == "skip":
                print(f"⚠️ 競合のためスキップ: {fname} -> {candidate_name}")
                logs[fname] = None
                continue
            elif conflict_strategy == "overwrite":
                # 既存ファイルを削除して上書き（注意！）
                try:
                    os.remove(dst_path)
                except Exception as e:
                    print(f"❌ 上書き失敗（既存削除できず）: {dst_path} / {e}")
                    logs[fname] = None
                    continue
                # 以降通常リネーム
            elif conflict_strategy == "append_counter":
                # 'name.ext', 'name (2).ext', 'name (3).ext' ... と連番付与で回避
                idx = 2
                while os.path.exists(dst_path):
                    candidate_name = f"{base} ({idx}){ext}"
                    dst_path = os.path.join(target_dir, candidate_name)
                    idx += 1

        try:
            os.rename(src_path, dst_path)
            print(f"✅ リネーム: {fname} -> {candidate_name}")
            logs[fname] = candidate_name
        except Exception as e:
            print(f"❌ リネーム失敗: {fname} -> {candidate_name} / {e}")
            logs[fname] = None

    return logs
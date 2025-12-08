import os
def compare_icd_xdw(output_folder, icd_list):
    """
    So sánh danh sách ICD (từ dữ liệu đã lưu) với danh sách XDW trong output_folder.
    Trả về:
        missing: ICD có nhưng không có XDW
        extra: XDW có nhưng không có ICD
    """
    # Danh sách ICD lấy từ icd_list (đã copy ở Step 1)
    icd_files = [os.path.splitext(os.path.basename(f))[0] for f in icd_list]

    # Danh sách XDW đọc từ thư mục
    xdw_files = [os.path.splitext(f)[0] for f in os.listdir(output_folder) if f.lower().endswith(".xdw")]

    # So sánh
    missing = [icd for icd in icd_files if icd not in xdw_files]
    extra = [xdw for xdw in xdw_files if xdw not in icd_files]

    return missing, extra

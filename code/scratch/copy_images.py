import os
import shutil
import pandas as pd

# 1. 定義路徑
base_dir = r"D:\NTU_PSY\Documents\Patric_Asen_BrainHackProject"
csv_path = os.path.join(base_dir, "subject_fMRI_nii", "images_used_in_fMRI.csv")
dest_dir = os.path.join(base_dir, "scratch", "fmri_used_images")

# 2. 建立新資料夾
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)
    print(f"已建立新資料夾: {dest_dir}")
else:
    print(f"資料夾已存在: {dest_dir}")

# 3. 讀取對照表 CSV
df = pd.read_csv(csv_path)

# 4. 篩選出 used_in_fMRI 為 True 的列
df_used = df[df["used_in_fMRI"] == True]
print(f"準備複製 {len(df_used)} 張圖片...")

# 5. 複製檔案
copied_count = 0
missing_count = 0

for idx, row in df_used.iterrows():
    # 原始檔案的相對路徑 (例如: THINGS_plus/images_THINGSplus-CC0/object_images_CC0/cashew.jpg)
    rel_path = row["relative_path"]
    src_file_path = os.path.join(base_dir, rel_path.replace("/", os.sep))
    
    # 目標檔案路徑
    dest_file_path = os.path.join(dest_dir, row["physical_filename"])
    
    # 檢查原始檔案是否存在
    if os.path.exists(src_file_path):
        shutil.copy2(src_file_path, dest_file_path)
        copied_count += 1
    else:
        print(f"警告: 找不到原始檔案 {src_file_path}")
        missing_count += 1

print(f"複製完成！成功複製 {copied_count} 張圖片。")
if missing_count > 0:
    print(f"共有 {missing_count} 張圖片找不到原始檔案。")

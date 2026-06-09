import pandas as pd
import glob
import os

base_dir = r"D:\NTU_PSY\Documents\Patric_Asen_BrainHackProject"
img_dir = os.path.join(base_dir, "THINGS_plus", "images_THINGSplus-CC0")

# 1. 載入受試者使用的圖片列表 (從 ALL_subjects_condition_clean.csv)
csv_path = os.path.join(base_dir, "subject_fMRI_nii", "ALL_subjects_condition_clean.csv")
df = pd.read_csv(csv_path)

# 獲取所有受試者使用過的獨特圖片路徑
used_images = set(df["image_filename"].dropna().unique())
print("fMRI 條件表中使用的獨特圖片數量:", len(used_images))

# 2. 掃描實體資料夾中的所有圖片
# 影像路徑可能是相對的，如 "dog/dog_12s.jpg"
# 我們遞迴搜尋資料夾下的所有 .jpg 檔案
all_files = glob.glob(os.path.join(img_dir, "**", "*.jpg"), recursive=True)
print("實體資料夾中總共有幾張圖片:", len(all_files))

# 將實體檔案路徑轉換為相對於 img_dir 的相對路徑（使用正斜線 /），以便與 csv 中的格式對比
all_relative_files = []
for f in all_files:
    rel_path = os.path.relpath(f, img_dir).replace("\\", "/")
    all_relative_files.append(rel_path)

print("實體資料夾相對路徑範例:", all_relative_files[:5])

# 3. 比對哪些實體檔案被使用在 fMRI 中
matched = [f for f in all_relative_files if f in used_images]
print("匹配上的實體圖片數量:", len(matched))

# 檢查是否有在條件表中有，但在實體資料夾找不到的
missing_physically = used_images - set(all_relative_files)
print("在條件表中有但實體資料夾找不到的數量:", len(missing_physically))
if missing_physically:
    print("缺少的實體檔案範例:", list(missing_physically)[:5])

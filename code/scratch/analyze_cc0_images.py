import pandas as pd
import glob
import os

base_dir = r"D:\NTU_PSY\Documents\Patric_Asen_BrainHackProject"
img_dir = os.path.join(base_dir, "THINGS_plus", "images_THINGSplus-CC0")

# 1. 載入受試者使用的概念 (從 ALL_subjects_condition_clean.csv)
csv_path = os.path.join(base_dir, "subject_fMRI_nii", "ALL_subjects_condition_clean.csv")
df = pd.read_csv(csv_path)

# 獲取所有受試者使用過的概念
used_concepts = set(df["concept"].dropna().unique())
print("fMRI 條件表中的獨特概念數量:", len(used_concepts))
print("前 10 個獨特概念範例:", sorted(list(used_concepts))[:10])

# 2. 獲取實體資料夾中所有的圖片檔案名稱
# 實體路徑可能是：D:\NTU_PSY\Documents\Patric_Asen_BrainHackProject\THINGS_plus\images_THINGSplus-CC0\object_images_CC0\aardvark.jpg
all_files = glob.glob(os.path.join(img_dir, "**", "*.jpg"), recursive=True)
print("\n實體資料夾中總共有幾張圖片:", len(all_files))

# 建立實體圖片檔名與概念名稱的映射
# 例如: 'aardvark.jpg' -> concept 'aardvark'
file_to_concept = {}
for f in all_files:
    filename = os.path.basename(f)
    concept_name, ext = os.path.splitext(filename)
    # 有些檔名可能需要清理，讓我們看看有沒有特殊符號
    file_to_concept[filename] = concept_name

print("實體圖片檔名與概念對應範例:")
for k in list(file_to_concept.keys())[:10]:
    print(f"  {k} -> {file_to_concept[k]}")

# 3. 比對實體圖片哪些對應的概念有出現在 fMRI 條件表中
concept_to_files = {v: k for k, v in file_to_concept.items()}

used_physical_images = []
for concept in sorted(list(used_concepts)):
    # 檢查該概念在實體資料夾中是否有對應的圖片
    # 常見命名可能是 `concept.jpg`
    matching_file = None
    if concept in concept_to_files:
        matching_file = concept_to_files[concept]
    
    if matching_file:
        used_physical_images.append({
            "concept": concept,
            "physical_filename": matching_file,
            "used_in_fMRI": True
        })
    else:
        # 如果沒找到對應的圖片
        print(f"警告: 條件表中的概念 '{concept}' 在實體資料夾中找不到對應的 jpg 檔案")

print(f"\n匹配到 fMRI 使用的實體圖片數量: {len(used_physical_images)}")

# 我們也來看看哪些實體圖片是「沒有」被 fMRI 使用的
unused_physical_images = []
for filename, concept in file_to_concept.items():
    if concept not in used_concepts:
        unused_physical_images.append({
            "concept": concept,
            "physical_filename": filename,
            "used_in_fMRI": False
        })

print(f"在實體資料夾中但「沒有」被 fMRI 使用的圖片數量: {len(unused_physical_images)}")
print("沒被使用的實體圖片範例:", [x["physical_filename"] for x in unused_physical_images[:10]])

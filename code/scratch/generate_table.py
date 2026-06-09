import pandas as pd
import glob
import os

base_dir = r"D:\NTU_PSY\Documents\Patric_Asen_BrainHackProject"
img_dir = os.path.join(base_dir, "THINGS_plus", "images_THINGSplus-CC0")
ratings_path = os.path.join(base_dir, "subject_fMRI_nii", "sub-01_condition_with_ratings.csv")
output_csv = os.path.join(base_dir, "subject_fMRI_nii", "images_used_in_fMRI.csv")

# 1. 讀取包含 Ratings 的對照表，並提取每個概念的唯一 grasp 和 hold 評分
df_ratings = pd.read_csv(ratings_path)
concept_ratings = df_ratings.groupby('concept')[['grasp_rating', 'hold_rating']].first().reset_index()

# 2. 讀取實體資料夾中所有的 jpg 檔案
all_files = glob.glob(os.path.join(img_dir, "**", "*.jpg"), recursive=True)

# 建立實體圖片檔名與概念名稱的對應
records = []
for f in all_files:
    filename = os.path.basename(f)
    concept_name, ext = os.path.splitext(filename)
    records.append({
        "concept": concept_name,
        "physical_filename": filename,
        "relative_path": os.path.relpath(f, base_dir).replace("\\", "/")
    })

df_physical = pd.DataFrame(records)

# 3. 合併實體圖片列表與評分資訊
df_merged = pd.merge(df_physical, concept_ratings, on="concept", how="left")

# 4. 新增「是否用於 fMRI 實驗」欄位
df_merged["used_in_fMRI"] = df_merged["grasp_rating"].notna()

# 5. 排序：先顯示有被 fMRI 使用的，再按 grasp_rating 降序排序，未使用的概念按字母排序
df_merged = df_merged.sort_values(
    by=["used_in_fMRI", "grasp_rating", "concept"],
    ascending=[False, False, True]
).reset_index(drop=True)

# 6. 儲存為 CSV 檔案
df_merged.to_csv(output_csv, index=False)
print("CSV 檔案儲存成功，路徑為:", output_csv)
print(f"總共照片數量: {len(df_merged)}")
print(f"其中用於 fMRI 的數量: {df_merged['used_in_fMRI'].sum()}")

# 7. 生成 Markdown 表格用於顯示在 Artifact
used_only = df_merged[df_merged["used_in_fMRI"] == True]
markdown_table = used_only.head(50).to_markdown(index=False)

artifact_dir = r"C:\Users\NTU_PSY\.gemini\antigravity-ide\brain\78f56f77-5049-48c9-a22f-11144fbbd7d8"
artifact_path = os.path.join(artifact_dir, "used_images_analysis.md")

with open(artifact_path, "w", encoding="utf-8") as f:
    f.write(f"""# fMRI 實驗影像使用情況分析 (fMRI Stimulus Image Analysis)

分析了 `images_THINGSplus-CC0` 資料夾內共 {len(df_physical)} 張照片，並與 fMRI 實驗條件表進行了比對：

- **影像總數**：{len(df_physical)} 張
- **用於 fMRI 實驗（sub-01 ~ sub-03）的影像數**：{df_merged['used_in_fMRI'].sum()} 張
- **未被使用的影像數**：{(df_merged['used_in_fMRI'] == False).sum()} 張

完整的比對結果已儲存為 CSV 檔案：[images_used_in_fMRI.csv](file:///{output_csv.replace('\\', '/')})

---

## 前 50 張最常/最易抓取並用於 fMRI 實驗的圖片列表

以下為有使用在 fMRI 實驗中、且依 `grasp_rating`（抓取易度評分）從高到低排序的前 50 張圖片列表：

{markdown_table}
""")

print("Markdown Artifact 生成成功，路徑為:", artifact_path)

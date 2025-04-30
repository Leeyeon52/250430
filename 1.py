import os
import shutil
import random
from pathlib import Path

# 원본 폴더와 대상 폴더 설정
src_dir = r"D:\52.군 경계 작전 환경 합성데이터\3.개방데이터\1.데이터\Validation\01.원천데이터\VS_EO_SU_DT"
dst_dir = r"D:\52.군 경계 작전 환경 합성데이터\images\images\val"

# 대상 폴더가 없으면 생성
os.makedirs(dst_dir, exist_ok=True)

# .jpg 파일 리스트 생성
jpg_files = [f for f in os.listdir(src_dir) if f.lower().endswith(".jpg")]

# 30% 샘플링
sample_size = int(len(jpg_files) * 0.3)
sampled_files = random.sample(jpg_files, sample_size)

# 복사
for file_name in sampled_files:
    src_file = os.path.join(src_dir, file_name)
    dst_file = os.path.join(dst_dir, file_name)
    shutil.copy2(src_file, dst_file)

print(f"{len(sampled_files)}개의 JPG 파일이 샘플링되어 복사되었습니다.")

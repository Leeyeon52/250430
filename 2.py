import os
import json
from PIL import Image

# 기본 경로

# 경로 딕셔너리
sets = {
    'train': {
        'json_folder': r"D:\52.군 경계 작전 환경 합성데이터\3.개방데이터\1.데이터\Training\02.라벨링데이터\TL_EO_SU_DT",
        'image_folder': r"D:\52.군 경계 작전 환경 합성데이터\images\images\train",
        'output_folder': r"D:\52.군 경계 작전 환경 합성데이터\images\labels\train"
    },
    'val': {
        'json_folder': r"D:\52.군 경계 작전 환경 합성데이터\3.개방데이터\1.데이터\Validation\02.라벨링데이터\VL_EO_SU_DT",
        'image_folder': r"D:\52.군 경계 작전 환경 합성데이터\images\images\val",
        'output_folder': r"D:\52.군 경계 작전 환경 합성데이터\images\labels\val"
    }    
}

subclass_to_idx = {
    11: 0, 12: 1, 13: 2,
    21: 3, 22: 4, 23: 5,
    31: 6, 41: 7, 42: 8
}

def convert_to_yolo(json_folder, image_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(json_folder):
        if file.endswith('.json'):
            base_name = os.path.splitext(file)[0]

            with open(os.path.join(json_folder, file), 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 이미지 경로 찾기
            image_path = None
            for ext in ['.jpg', '.jpeg', '.png']:
                candidate = os.path.join(image_folder, base_name + ext)
                if os.path.exists(candidate):
                    image_path = candidate
                    break

            if not image_path:
                print(f"⚠️ 이미지 없음: {base_name}")
                continue

            # 이미지 열기
            try:
                with Image.open(image_path) as img:
                    img_width, img_height = img.size
            except Exception as e:
                print(f"⚠️ 이미지 열기 실패: {image_path} - {e}")
                continue

            # YOLO 라벨 변환
            yolo_lines = []
            for ann in data.get("annotations", []):
                bbox = ann.get("bounding_box")
                if bbox and len(bbox) == 4:
                    # assuming bbox format is [w, h, x, y]
                    w, h, x, y = bbox

                    # 중앙 좌표 및 크기 계산 (이미지 크기 그대로 사용)
                    cx = (x + w / 2) / img_width  # 중심 좌표 X
                    cy = (y + h / 2) / img_height  # 중심 좌표 Y
                    w = w / img_width  # 너비 비율
                    h = h / img_height  # 높이 비율

                    # sub_class 값으로 클래스 id 결정
                    sub_class = ann.get("sub_class", 0)
                    class_id = subclass_to_idx.get(sub_class, -1)
                    if class_id == -1:
                        print(f"⚠️ 잘못된 sub_class 값: {sub_class} - {base_name}")
                        continue

                    # YOLO 형식으로 라인 추가
                    yolo_lines.append(f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

            # 결과 저장
            out_path = os.path.join(output_folder, base_name + ".txt")
            with open(out_path, "w", encoding='utf-8') as f:
                f.write("\n".join(yolo_lines))

            print(f"✅ 변환 완료: {base_name}.txt")

# 실행
for phase, paths in sets.items():
    print(f"\n📂 처리 중: {phase}")
    convert_to_yolo(paths['json_folder'], paths['image_folder'], paths['output_folder'])
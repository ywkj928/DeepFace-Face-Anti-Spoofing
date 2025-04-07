import torch
import torch.nn as nn
import cv2
import numpy as np
import os
from torchvision import transforms
from PIL import Image
from deepface import DeepFace
import torchvision.models as models

# ResNet 모델 정의
model = models.resnet50(pretrained=False)  # pretrained=True로 설정하면 미리 훈련된 가중치 사용
model.fc = nn.Linear(model.fc.in_features, 2)  # 이진 분류를 위한 출력층 수정

# 모델 가중치 로드
model.load_state_dict(torch.load('face_spoof_model.pth'))  # ResNet에 맞는 가중치 파일 필요
model.eval()  # 평가 모드로 설정

# 이미지 전처리
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # 이미지 크기 조정
    transforms.ToTensor(),  # 텐서로 변환
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # 정규화
])

def highlight_facial_areas(img: np.ndarray, faces_coordinates: list[tuple[int, int, int, int]], anti_spoofing: bool = True) -> np.ndarray:
    """ 얼굴 영역에 박스를 그리는 함수 """
    for x, y, w, h in faces_coordinates:
        color = (0, 255, 0) if anti_spoofing else (0, 0, 255)  # 진짜/가짜에 따라 색상 변경
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)  # 사각형 그리기
    return img

def is_real_face(emotion_probas: dict) -> bool:
    """ 표정이 'happy' 또는 'neutral'일 경우 실제 얼굴로 판단 """
    dominant_emotion = max(emotion_probas, key=emotion_probas.get)  # 가장 높은 확률의 감정 찾기
    return dominant_emotion in ["happy", "neutral"]  # 해당 감정인지 확인

def predict_image(img: np.ndarray) -> str:
    """ 이미지에서 진짜/가짜 얼굴 예측 """
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # OpenCV 이미지를 PIL 이미지로 변환
    img_tensor = transform(img_pil).unsqueeze(0)  # 전처리 후 텐서 변환

    with torch.no_grad():  # 기울기 계산 비활성화
        output = model(img_tensor)  # 모델 예측

    _, predicted = torch.max(output, 1)  # 예측된 클래스 q찾기
    return "진짜" if predicted.item() == 0 else "가짜"  # 클래스에 따라 결과 반환

# 바탕화면 경로 설정
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
photo_count = 0  # 찍은 사진 수

# 카메라 실행
cap = cv2.VideoCapture(0)
reference_img_path = "tests/dataset/img14.jpg"  # 비교할 등록된 얼굴 이미지

while cap.isOpened():
    ret, frame = cap.read()  # 프레임 읽기
    if not ret:
        break

    try:
        # 얼굴 감지 및 분석
        demographies = DeepFace.analyze(frame, actions=("age", "gender", "emotion"), enforce_detection=False)

        if demographies:
            demography = demographies[0]  # 첫 번째 분석 결과 가져오기
            x, y, w, h = demography["region"]["x"], demography["region"]["y"], demography["region"]["w"], demography["region"]["h"]

            # 표정 기반 안티 스푸핑 및 본인 여부 판별
            is_real = is_real_face(demography["emotion"])  # 실제 얼굴인지 판별
            face_region = frame[y:y+h, x:x+w]  # 얼굴 영역 추출
            face_prediction = predict_image(face_region)  # 얼굴 예측
            is_matched = (face_prediction == "진짜") and is_real  # 진짜 얼굴 여부 확인

            if is_matched:
                frame = highlight_facial_areas(frame, [(x, y, w, h)], anti_spoofing=True)  # 진짜 얼굴 박스 그리기
                status_text = "Real Face"  # 상태 텍스트
            else:
                frame = highlight_facial_areas(frame, [(x, y, w, h)], anti_spoofing=False)  # 가짜 얼굴 박스 그리기
                status_text = "Fake Face"  # 상태 텍스트

            # 감정 상태 텍스트 추가
            cv2.putText(frame, status_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # 화면 출력
        cv2.imshow("Face Recognition", frame)

        # 'c' 키를 누르면 사진 찍기
        if cv2.waitKey(1) & 0xFF == ord('c'):
            photo_count += 1
            photo_path = os.path.join(desktop_path, f"photo_{photo_count}.jpg")  # 사진 저장 경로
            cv2.imwrite(photo_path, frame)  # 사진 저장
            print(f"사진 {photo_count}장이 찍혔습니다. 저장 경로: {photo_path}")
        
        # 5장을 찍으면 종료
        if photo_count >= 5:
            print("5장 사진이 찍혔습니다. 프로그램을 종료합니다.")
            breakccc

    except Exception as e:
        print(f"Error: {e}")  # 에러 출력

# 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # 카메라 해제
cv2.destroyAllWindows()  # 모든 윈도우 닫기
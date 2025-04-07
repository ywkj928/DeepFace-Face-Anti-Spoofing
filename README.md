# DeepFace Anti-Spoofing 프로젝트

## 개요
우리는 DeepFace의 anti-spoofing 기능을 수행하여 기존 모델을 fine-tuning하여 DeepFace 기술을 파악하는 것을 목표로 하였습니다. 인간의 얼굴은 가장 일반적이면서도 매우 복잡한 구조로 이루어져 있습니다.

기존 AI가 만든 이미지와 실제 사람의 이미지를 준비하여 데이터셋을 구성하였고, DeepFace 모델의 2D 이미지와 3D 이미지에서 실제 사람 얼굴과 가짜 얼굴을 인식하는 성능 개선을 시도하였습니다. 얼굴 인식 모델은 ArcFace 모델을 사용하였으며, YOLO 모델을 통해 얼굴 탐지 및 정렬을 진행하고, OpenCV를 사용하여 실시간 감지를 수행하였습니다. 최종적으로 웹캠을 통해 다양한 환경에서 일관된 결과를 확인했습니다.

## 서론
최근 얼굴 인식 기술은 보안 시스템의 핵심 요소로 자리 잡으며 다양한 분야에서 활발히 활용되고 있습니다. 얼굴 인식 시스템은 개인의 얼굴 특징을 분석하여 신원 확인을 수행하며, 이는 소매점의 고객 관리, 공항의 출입 통제, 금융 거래 인증 등 여러 보안 환경에서 중요한 역할을 하고 있습니다. 그러나 기술 발전과 함께 스푸핑 공격 등의 보안 위협도 증가하고 있습니다. 따라서 얼굴 인식 기술의 보안을 강화하기 위한 연구가 필요하며, 'anti-spoofing' 기술이 그 핵심입니다.

## 본론

### 1. 이론적 배경
1. **얼굴 인식 기술**: 생체 인식의 일종으로, 개인의 얼굴을 분석하여 신원을 확인하는 기술입니다.
2. **스푸핑 공격**: 얼굴 인식 시스템의 취약점을 이용하여 신원을 위조하는 행위로, 사진, 동영상 또는 3D 마스크를 통해 이루어집니다.
3. **Anti-Spoofing 기술**: 스푸핑 공격을 방지하기 위한 기술로, 얼굴 인식 시스템의 보안을 강화하는 데 필수적입니다.

### 2. 구현 방법
1. **DeepFace.py**
   - 얼굴 인식 및 진짜/가짜 얼굴 판별
   - ResNet50 모델 로드 및 이진 분류를 위한 수정
   - OpenCV를 통한 실시간 비디오 캡쳐 및 사진 저장 기능

2. **ArcFace.py**
   - ArcFace 모델을 이용한 얼굴 인식
   - 미리 훈련된 가중치 다운로드 및 로드

3. **FasNet.py**
   - MiniFASNet 모델을 사용한 얼굴 안티 스푸핑
   - 이미지 전처리 및 얼굴 분석

4. **Yolo.py**
   - Yolo 모델을 이용한 얼굴 탐지
   - 모델 가중치 다운로드 및 로드
     
<div align="center">
    <img src="images/Model.jpg" alt="Real Face">
</div>

## 구현 결과
3D 입체 영상을 활용하여 사람과 인형을 구분하는 실험을 진행한 결과, 진짜와 가짜를 효과적으로 구분할 수 있음을 확인하였습니다. 반면, 2D 이미지 비교에서는 오검출이 발생하였습니다. 2D 영상에서의 신뢰도 높은 구분에는 한계가 있음을 알게 되었습니다.

### 결과 이미지
- **실제 얼굴**:
<div align="center">
    <img src="images/Real%20Face.jpg" width="450" height="300">
</div>

- **가짜 얼굴**:
<div align="center">
    <img src="images/Fake%20Face.jpg" width="450" height="300">
</div>
<div align="center">
    <img src="images/FakeFace.jpg" width="450" height="300">
</div>

## 결론
검증에 사용한 이미지와 비디오는 웹캠과 AI 생성 이미지를 활용하였습니다. 구현 결과에서 실제 인물은 진짜로 인식되었고, AI 생성 이미지와 인형은 가짜로 인식되었습니다. 그러나 실시간 영상에서 품질과 환경변수에 따라 오검출이 발생하는 문제도 있었습니다. 이를 해결하기 위해 전처리 과정과 필터링을 통한 이미지 개선 및 AI 생성 이미지의 패턴 학습을 고려하고 있습니다.

## 참고문헌
1. Taigman, Y., Yang, M., Ranzato, M., & Wolf, L. (2014). Closing the gap to human-level performance in face verification. *Proceedings of the IEEE Computer Vision and Pattern Recognition (CVPR)*.
2. Wang, M., & Deng, W. (2021). Deep face recognition: A survey. *Neurocomputing, 429*, 215-244.
3. Serengil, deepface 2024. A Benchmark of Facial Recognition Pipelines and Co-Usability Performances of Modules.
4. 아비라미 비나 (2024, 06.21). AI 얼굴 인식 애플리케이션.

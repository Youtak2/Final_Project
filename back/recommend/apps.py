import os
from django.apps import AppConfig

class RecommendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recommend'

    _already_ran = False  # ✅ 클래스 변수로 한번만 실행되도록 설정

    # def ready(self):
    #     if os.environ.get('RUN_MAIN') != 'true':
    #         return

    #     if RecommendConfig._already_ran:
    #         return
    #     RecommendConfig._already_ran = True

    #     print("🔄 자동 학습 데이터 생성 및 모델 학습 시작...")

    #     try:
    #         from recommend.ml_model import generate_training_data, train_model
    #         generate_training_data.main()
    #         train_model.main()
    #     except Exception as e:
    #         print(f"⚠️ 자동 학습 실패: {e}")

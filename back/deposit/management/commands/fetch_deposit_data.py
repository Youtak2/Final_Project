import requests
from django.core.management.base import BaseCommand
from deposit.models import DepositProduct
from django.conf import settings

class Command(BaseCommand):
    help = '금융감독원 OpenAPI에서 예적금 상품 정보를 가져와 DB에 저장합니다.'

    def handle(self, *args, **kwargs):
        base_url = 'https://finlife.fss.or.kr/finlifeapi'
        api_key = settings.FINLIFE_API_KEY
        endpoints = [
            ('예금', 'depositProductsSearch'),
            ('적금', 'savingProductsSearch'),
        ]

        for product_type, endpoint in endpoints:
            url = f"{base_url}/{endpoint}.json?auth={api_key}&topFinGrpNo=020000&pageNo=1"
            res = requests.get(url)
            data = res.json()

            base_list = data.get('result', {}).get('baseList', [])
            option_list = data.get('result', {}).get('optionList', [])

            for base in base_list:
                fin_prdt_cd = base['fin_prdt_cd']
                bank_name = base['kor_co_nm']
                name = base['fin_prdt_nm']

                for option in filter(lambda x: x['fin_prdt_cd'] == fin_prdt_cd, option_list):
                    try:
                        save_term = int(option['save_trm'])
                        rate = float(option['intr_rate']) if option['intr_rate'] else 0.0

                        unique_id = f"{fin_prdt_cd}_{save_term}"  # 고유 식별자 생성

                        DepositProduct.objects.update_or_create(
                            fin_prdt_cd=unique_id,  # 금융상품 고유 코드로 구분
                            defaults={
                                'name': name,
                                'bank_name': bank_name,
                                'product_type': product_type,
                                'save_term': save_term,
                                'rate': rate
                            }
                        )

                    except ValueError:
                        continue

        self.stdout.write(self.style.SUCCESS('✅ 예적금 데이터 수집 완료'))

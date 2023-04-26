# Paythere

>## Table of Contents

- [Execution](#Execution)
- [APIdocs](#APIdocs)
- [DB](#DB)
- [Architecture](#Architecture)
- [CodeRule](#CodeRule)
- [Technic](#Technic)
- [Retrospective](#Retrospective)


>## Execution
*   Environment
    *   port:5001(server),3000(mysql)
    *   docker:v20.10.23
    *   dockerCompose:v2.15.1

*   Project
    ```cmd
    cd paythere
    docker-compose up --build -d
    ```

*   TestCode
    ```cmd
    docker exec -it paythere_back /bin/bash
    export APP_ENV="test"
    echo $APP_ENV
    cd test
    pytest -vv
    ```
    *mysql_password=test_mysql*
>## APIdocs
    1.프로젝트를 실행
    2.아래 주소에 접속
## &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[http://localhost:5001/docs](http://localhost:5001/docs)

>## DB
*   ### users(회원)
    *   `id` int(11) NOT NULL AUTO_INCREMENT     *회원의 id정수값 사용*
    *   `phone_number` char(11) NOT NULL    *핸드폰번호의 길이는 고정되어 있기에 검색에 유리한 고정 문자사용*
    *   `hashed_password` varchar(255)  NOT NULL    *해쉬화된 비밀번호 저장*
    *   `created_at` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)  *정확하게 시간별로 조회하기 위해 밀리초 활용*
    *   `updated_at` timestamp(6) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(6)
    *   `deleted` tinyint(1) NOT NULL DEFAULT '0'   *회의 복원기능이 필요할 수 있어 소프트 딜리트 사용*
    *   PRIMARY KEY (`id`)  *회원 조회를 위한 기본값*
    *   UNIQUE KEY `phone_number` (`phone_number`)  *핸드폰번호 조회를 위한 유니크*

*   ### products(상품)
    *   `id` int(11) NOT NULL AUTO_INCREMENT    *상품의 id정수값 사용*
    *   `user_id` int(11) NOT NULL  *상품을 소유한 유저의 아이디*
    *   `category` varchar(255) NOT NULL    *정해진 길이가 없기에 가변 문자 사용*
    *   `net_price` decimal(10,2) NOT NULL  *소수점을 고정시킬 수 있어 가격 관리에 용이*
    *   `cost_price` decimal(10,2) NOT NULL
    *   `name` varchar(255) NOT NULL    *정해진 길이가 없기에 가변 문자 사용*
    *   `description` varchar(255) NOT NULL *정해진 길이가 없기에 가변 문자 사용*
    *   `barcode` varchar(13)NOT NULL  *한국은 13자리지만 다른 자릿수도 존재하기에 가변 문자 사용*
    *   `expiration_date` date NOT NULL *유통기한에 시간이 존재하지 않기에 날짜 사용*
    *   `size` varchar(20) NOT NULL *정해진 길이가 없고 길이가 크지 않음*
    *   `created_at` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
    *   `updated_at` timestamp(6) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(6)
    *   `deleted` tinyint(1) NOT NULL DEFAULT '0'   *상품의 복원기능이 필요할 수 있어 소프트 딜리트 사용*
    *   PRIMARY KEY (`id`)  *상품의 아이디를 통해 조회를 해야하기에 기본값 설정

*   ### products_initial(상품의 초성)
    *   `product_id` int(11) NOT NULL   *초성을 통해 상품 정보를 보기 위한 상품의 아이디*
    *   `initial` varchar(255) NOT NULL *상품 초성을 저장*

*   ### tokens(회원의 접근 토큰 저장)
    *   `access_token` varchar(256) NOT NULL    *다중로그인과 로그인 기록을 위한 접근토큰 저장*
    *   PRIMARY KEY (`access_token`)    *토큰을 조회해야하기에 기본값 설정*

>## Architecture
*   ### folder
    ![제목 없는 다이어그램 drawio (2)](https://user-images.githubusercontent.com/77044696/234506361-e701fb57-5c52-49b2-9054-c86e0fe5fb55.png)

    *api파일은 모든 서비스에 접근할 수 있으며 각 서비스는 다루는 테이블 하나의 모델만 접근할 수 있습니다.*
*   ### class
    ![스크린샷 2023-04-26 오후 4 51 47](https://user-images.githubusercontent.com/77044696/234507683-76d26e4e-a177-46a1-aeee-9d90c542aa7b.png)
    *가장 최상단의 main.py에서 각 서비스에 모델을 담고 모든 서비스를 모아 api에 주입합니다.*


>## CodeRule
*   ### 이름선언은 명확하게
    *   클래스:첫음은 대문자,붙여쓰기 *ExampleClass*
    *   인스턴스,변수,함수:모두 소문자,붙여쓰기 대신 "_" 사용    *example_function*
*   ### 누가봐도 어떤일을 하는지 알게
    ```python
    def get_user_products_by_page():
        """
            페이지크기만큼 유저의 상품을 불러옵니다.
        """
        ...
        return product_info_list
    def is_product_deleted_by_id():
        """
            해당아이디와 일치하는 상품이 삭제되었는지 확인합니다.
        """
        ...
        return True
    ```
    *   함수의 이름을 명확하게 표현
    *   주석을 통한 어떤 자세한 설명
*   ### 함수는 단순한 일을 하게
![제목 없는 다이어그램 drawio (3)](https://user-images.githubusercontent.com/77044696/234515322-9c18de83-337a-49d4-a906-6e302b9914bd.png)
*   ### 타입은 명확하게
    ```python
    def get_user_products_by_page(page: int)->int:
        """
            페이지크기만큼 유저의 상품을 불러옵니다.
        """
        ...
        return product_info_list
    ```

>## Technic
*   ### 초성검색
    1.  파이썬의 함수로 단어의 자음을 분리
        ```python
        def korean_to_initial(korean_word):
            """
            한글 단어를 입력받아서 초성/중성/종성을 구분하여 리턴해줍니다. 
            """
            ####################################
            # 초성 리스트. 00 ~ 18
            CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
            # 중성 리스트. 00 ~ 20
            JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
            # 종성 리스트. 00 ~ 27 + 1(1개 없음)
            JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
            ####################################
            r_lst = []
            for w in list(korean_word.strip()):
                if '가'<=w<='힣':
                    ch1 = (ord(w) - ord('가'))//588
                    ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
                    ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
                    r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
                else:
                    r_lst.append([w])
            initial_list=[ch[0] for ch in r_lst]
            return "".join(initial_list)

        print(korean_to_initial("자음 분리기"))
        ```
        출력
        ```cmd
        ㅈㅇ ㅂㄹㄱ
        ```
    2. 상품의 id와 자음을 저장하는 products_initial 테이블 생성

        *initial컬럼은 앞 뒤의 like검색을 해야하므로 인덱스 필수 x*
    
    3.  검색이름이 초성인지 일반 문자열인지 검사하여 2가지의 검색모드 분리
        ```python
        def get_user_products_by_name(self,name: str,user_id: int)->List[ProductInfo]:
                """
                    상품의 이름을 통해 검색한 정보들을 불러옵니다.
                """
                try:
                    #한글문자열의 초성만을 추출합니다.
                    initial_name=korean_to_initial(name)
                    
                    #추출한 초성과 일치할 경우 초성검색모드로 돌입합니다.
                    if initial_name==name:
                        user_product_list=self.product_model.select_product_by_user_id_with_initial(initial_name,user_id)
                    #추출한 초성과 일치하지 않을 경우 일반 검색모드로 돌입합니다.
                    else:
                        user_product_list=self.product_model.select_product_by_user_id_with_name(name,user_id)
                    
                    user_product_info_list=[ProductInfo(**product.dict()) for product in user_product_list if product.deleted==False]
                    return user_product_info_list
                except DatabaseError as es:
                    raise es
        ```

*   ### db세션
    1.  db를 모두 사용하면 안전하게 닫기위해 yield,finally 사용
        ```python
        def get_db():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()
        ```

    2.  api요청때마다 세션을 사용 할 수 있게 디펜던시 적용
        ```python
        @product_api.put("/{product_id}",status_code=Created_201.status_code,response_model=PutProductResponse)
        async def post_product(response: Response,new_product:CreateProduct,credentials: dict = Depends(verify_token),db: Session = Depends(get_db)):
        ```
    
    3.  setter메서드를 사용하여 api 단계에서 한번만 세션을 전달 후 모델이 세션을 사용가능하게 구현
        ```python
        class ProductModel:
            def set_db(self,db):
                self.db=db
        ```

        ```python
        class ProductService:
            def __init__(self,product_model,conf):
                self.conf=conf
                self.product_model=product_model
            
            def set_db(self,db):
                #서비스에 들어온 db를 모델에 다시 전달
                self.product_model.set_db(db)
                return self
        ```
        ```python
        updated_product_info=product_service.set_db(db).update_product_info_by_id(update_product,product_id)
        ```
        *setter가 없었다면 api->service->model에 해당 db를 인자로 계속 내려보내야한다.위의 과정을 통해 api에서 model의 db를 미리 안착시키고 편리하게 사용*
*   ### 트랜잭션
    1.  상품테이블에 상품을 저장시 초성테이블에 초성도 저장해야하는데 둘중에 하나라도 실패시 롤백을 하여 원래상태로 복구
        ```python
            def insert_product(self,new_product: InsertProduct,initial_name:str)->int:
                """
                    새로운 상품의 정보를 삽입합니다.
                """
                try:
                    #상품테이블에 상품을 저장 및 기입될 정보를 받아옵니다.
                    new_product=sql.Product(
                        **new_product.dict()
                    )
                    self.db.add(new_product)
                    self.db.flush()
                    self.db.refresh(new_product)
                    
                    #초성테이블에 초성을 저장합니다.
                    new_product_initial=sql.ProductInitial(
                        product_id=new_product.id,
                        initial=initial_name
                    )
                    self.db.add(new_product_initial)
                except:
                    #두 과정중에 한개라도 실패한다면 롤백을 통해 원래상태로 되돌리고 에러를 발생시키빈다.
                    print(traceback.format_exc())
                    self.db.rollback()
                    raise DatabaseError()
                else:
                    #두 저장과정이 모두 성공한다면 커밋을 통해 완전한 삽입을 합니다.
                    self.db.commit()
                    self.db.refresh(new_product)
                    self.db.refresh(new_product_initial)
                    new_product=Product(**new_product.__dict__)
                    return new_product
        ```
*   ### 로그아웃
    1.  해당 사용자가 로그인 된 상태인지 아닌지를 알려면 서버가 데이터를 담아두어야한다.

    2.  사용자가 다른기기로 다중 로그인을 할 수 있게하려면 로그인마다의 고유한 데이터를 담아두어야한다.

    3.  사용자가 로그인시 발급한 토큰자체를 db에 저장하여 로그인시 삽입,로그아웃시 삭제를 한다.
    *토큰자체를 조회해야하므로 토큰컬럼을 기본키로 설정*

    4.  해당 토큰이 db에 존재유무에 따라 로그인,로그아웃 상태를 판변하여 서비스접근을 제한한다.
        ```python
        access_token_logouted=user_service.set_db(db).is_user_access_token_logouted(access_token)
        #사용자가 로그아웃 된 상태라면 에러 발생
        if access_token_logouted==True:
            raise exception.UserLogouted()
        ```
>## Retrospective
*   ### 테스트코드
    예전에 짜던 테스트 코드는 그저 해당 api가 출력이 맞는지만 검사했지만 복잡한 서비스의 경우 예상치 못한 곳에서 버그나 의도치 않은 응답을 할 수 있다.이런점에서 최대한 사용자 입장에서 접근할 만한 루트를 생각하며 흐름을 중심으로 코드를 짜갔다.그리고 실패해야하는 케이스들을 함께 짜두어 보안적으로 강화를 시킬 수 있었다.
    
    ```python
    #4xx응답을 받아야하는 케이스
    def test_fail_get_product(client):
        #클라이언트가 로그아웃 한 상태에서 등록이 안되는지 확인
        ...
        #클라이언트의 소유가 아닌 상품은 안받아와지는지 확인
        ...
        #클라이언트가 존재하지 않는 상품을 요청할 때 안받아와지는지 확인

    #2xx응답을 받아야하는 케이스
    def test_get_product(client):
        #사용자가 정상적으로 상품을 받는지 확인
        ...
        #사용자가 새로운 상품을 등록하고 새로운 상품의 정보를 받는지 확인
        ...
        #사용자가 새로운 상품의 정보를 변경하고 상품의 정보를 받는지 확인
        ...
    ```

*   ### 개발단계
    
    fastapi라는 프레임워크를 잘 다뤄보지 않아 러닝커브가 심하게 왔었다.그리고 docker와 mysql의 세팅,데이터베이스를 설계하는 데 일의 순서가 없이 구현하는데만 급급했다.A라는 작업을 하다가 B라는 작업을 할때 A에서 작업을 했던 기억과 노하우가 금방 사라졌고 다시 A작업으로 돌아왔을 땐 효율이 극한으로 떨어졌다.이런 점들에서 개발단계의 순서를 개발 초기에 명확하게 구분하고 실행하는 것의 중요성을 느꼈다.예를 들면 fastapi에 pydantic을 사용하여 스키마들을 정의하는데 함수와 변수에 스키마들을 적용하가며 동시에 스키마를 만드니까 스키마의 변형이 너무 자주 일어났다.
    미리 스키마를 모두 만들어 놓고 그 틀 안에서 적용해 갔으면 개발효율이 늘었지 않았을까 싶다.

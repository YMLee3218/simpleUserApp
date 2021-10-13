#실행 방법
프로젝트 root에서

```shell
python manage.pyrnserver localhost:8000
```
를 실행하면 서버가 실행됩니다. 포트 번호는 필요에 따라 바꿔 주셔도 무방합니다.

#사용 기술
* 언어: Python 3.8
* 프레임워크: Django
* 데이터베이스: SQLite3
* 형상 관리: Git

#구현 스펙
###SMS 인증 기능
####인증 번호 요청
>URL: http://localhost:8000/sms-auth/send/
> 
>HTTP methods: POST

>요청 형식
>```json
>{
>  "phone_number": "010-1234-5678"
>}
>```

>답변 형식
>```json
>{
>  "auth_number": "12345"
>}
>```
* 인증 번호 유효시간: 5분

####인증 번호 검증
>URL: http://localhost:8000/sms-auth/verify/
>
>HTTP methods: POST

>요청 형식
>```json
>{
>  "phone_number": "010-1234-5678",
>  "auth_number": 12345
>}
>```

>답변 형식
>>성공
>>```json
>>{
>>  "verification_code": "d9c4361e-18d4-4e14-830e-4831a0935e9e"
>>}
>>```
>>* 본래는 SMS로 인증 번호를 전송해야 하나 편의상 response를 통해 인증 번호 전달
>
>>실패
>>* 인증 요청을 한 적이 없는 번호이거나 인증 정보가 만료되었을 시 
>>```json
>>{
>>  "message": "유효하지 않은 인증 정보입니다."
>>}
>>```
>>* 인증 번호가 일치하지 않을 시
>>```json
>>{
>>  "message": "인증 번호가 일치하지 않습니다."
>>}
>>```
* 인증 완료 코드 유효시간: 10분

###회원 가입 기능
>URL: http://localhost:8000/user/
>
>HTTP methods: POST

>요청 형식
>```json
>{
>  "email": "test123@gmail.com",
>  "nickname": "test123",
>  "password": "1234",
>  "name": "tester",
>  "phone_number": "010-1234-5678",
>  "verification_code": "d9c4361e-18d4-4e14-830e-4831a0935e9e"
>}
>```

>답변 형식
>>성공
>>```json
>>{
>>  "token": "48ea70a86bd31ef746559d54a10f6a185ad5740f"
>>}
>>```
>>* 로그인 시 header에 다음의 형식으로 입력하여 활용할 수 있음
>>```
>>Authorization: Token 토큰값
>>```
>
>>실패
>>* 이메일 형식이 유효하지 않을 시
>>```json
>>{
>>  "message": "유효하지 않은 형식의 이메일입니다."
>>}
>>```
>>* 인증 완료 코드가 만료되었거나 올바르지 않을 시
>>```json
>>{
>>  "message": "유효하지 않은 인증 정보입니다."
>>}
>>```
>>* 이미 해당 email이나 전화번호로 가입한 회원이 있을 시
>>```json
>>{
>>  "message": "이미 존재하는 회원입니다."
>>}
>>```

###로그인 기능
>URL: http://localhost:8000/user/login/
>
>HTTP methods: POST

>요청 형식
>>email로 로그인 시
>>```json
>>{
>>  "email": "test123@gmail.com",
>>  "password": "1234"
>>}
>>```
>
>>전화번호로 로그인 시
>>```json
>>{
>>  "phone_number": "010-1234-5678",
>>  "password": "1234"
>>}
>>```

>답변 형식
>>성공
>>```json
>>{
>>  "token": "48ea70a86bd31ef746559d54a10f6a185ad5740f"
>>}
>>```
>>* 로그인 시 header에 다음의 형식으로 입력하여 활용할 수 있음
>>```
>>Authorization: Token 토큰값
>>```
>
>>실패
>>* 회원 정보를 찾을 수 없을 시
>>```json
>>{
>>  "message": "존재하지 않는 회원입니다."
>>}
>>```
>>* 비밀번호가 일치하지 않을 시
>>```json
>>{
>>  "message": "비밀번호가 일치하지 않습니다."
>>}
>>```

###내 정보 보기 기능
>URL: http://localhost:8000/user/
>
>HTTP methods: GET

>요청 형식
>* 헤더에 다음 형식으로 token 입력 필요
>```
>Authorization: Token 토큰값
>```

>답변 형식
>>성공
>>```json
>>{
>>  "email": "test123@gmail.com",
>>  "nickname": "test123",
>>  "name": "tester",
>>  "phone_number": "010-1234-5678"
>>}
>
>>실패
>>* 헤더에 token이 없을 시
>>```json
>>{
>>  "message": "로그인이 필요합니다."
>>}
>>```
>>* Token 값이 유효하지 않을 시
>>```json
>>{
>>  "detail": "Invalid token."
>>}

###비밀번호 재설정 기능
>URL: http://localhost:8000/user/
>
>HTTP methods: PATCH

>요청 형식
>```json
>{
>  "password": "1234",
>  "phone_number": "010-1234-5678",
>  "verification_code": "d9c4361e-18d4-4e14-830e-4831a0935e9e"
>}
>```

>답변 형식
>>성공
>>```json
>>{
>>  "message": "비밀번호 변경이 완료되었습니다."
>>}
>>```
>
>>실패
>>* 인증 완료 코드가 만료되었거나 올바르지 않을 시
>>```json
>>{
>>  "message": "유효하지 않은 인증 정보입니다."
>>}
>>```

#구현 방법
* sms_auth와 user는 user가 sms_auth를 사용할 뿐 역할이 다르므로 분리하였습니다.
###sms_auth
* 전체 Flow
  1. 인증 번호 요청
  2. 인증 번호를 response로 수신(SMS 대신)
     * 인증 번호는 5분 동안 유효
  3. 해당하는 전화 번호와 인증 번호를 이용해 verification 요청
  4. 10분간 유효한 인증 확인 코드 전달


* 인증 번호나 인증 확인 코드는
  1. 장기적으로 저장되지 않으며,
  2. 자주 생성되고 지워지고
  3. 사라지더라도 크리티컬하지 않기 때문에 
* DB에 입력하기 보다는 메모리에 저장하는 것이 낫다고 판단하였습니다.
  * 이를 위해 Expire dict라는 custom dict 구현하였습니다.
  * asyncio를 이용하여, 주기적으로 원소들을 체크하며 expire 됐을 시 제거합니다.
  * element 수가 0일 경우 중지합니다.


* 어차피 한 번의 request에만 사용하면 되므로, 인증 확인 코드를 쿠키로 사용하지 않았습니다.
* 인증 확인 코드의 경우 만에 하나 중복이 발생하더라도 큰 문제가 없기 때문에 생성 시 uuid4를 이용합니다.


* 보안 및 메모리 관리를 위해, 인증 완료 후에는 expire date와 관계 없이 인증 정보 바로 삭제합니다.

###user
* 회원 가입, 비밀번호 재설정 시 sms_auth를 사용하여 인증 확인 코드를 미리 받을 필요가 있습니다.


* 회원 가입, 조회, 비밀번호 재설정의 경우 user resource에 대한 Create, Read, Update 동작이므로 /user url에서 http method만 변경합니다.
  * 비밀번호 재설정의 경우 resource의 일부만 변경하는 것이므로 PUT 대신 PATCH를 사용합니다.
* login은 user에 대한 CRUD는 아니므로 별개의 /login url을 사용합니다.


* 회원 가입 시 user name으로 uuid1로 생성된 uuid를 사용합니다.
  * MAC주소와 time, sequence로 생성하므로 중복될 위험이 거의 없습니다.
  * uuid1의 단점으로 MAC주소가 노출될 수 있다는 점이 있으나, 회원을 identify하기 위한 값일 뿐 외부에 노출하지 않으므로 노출될 위험은 적습니다.
  * email, phone_number 값은 고유한 값이고, 로그인 시 둘 중 하나의 정보를 사용하지만 충분히 변경할 수도 있는 값이기 때문에 id 값은 정보와 관계 없는 유니크한 값이어야 합니다.
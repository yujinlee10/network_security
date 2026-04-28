🟧 Step 4: 전체 통합 및 시각화 테스트
목표: 정상/위조 웹 서버 구축 및 클라이언트 관점의 최종 결과 확인.

경로: scenario/real-web/, scenario/fake-web/

파일: 각각의 index.html (Green vs Red), docker-compose.yml

요구사항:

real-web: 포트 8081  매핑.

fake-web: 포트 8082  매핑.

전체 서비스를 묶는 최상위 docker-compose.yml 작성.

최종 검증:

공격 전: curl --resolve bank.test:80:127.0.0.1 http://bank.test 접속 시 Green 페이지 확인.

공격 실행.

공격 후: 동일 명령어로 접속 시 Red 페이지(피싱 사이트) 확인.
🟩 Step 2: Auth Server 구현 및 연결
목표: 특정 도메인(bank.test)에 대한 권한을 가진 가짜 권한 서버 구축 및 리졸버 연동.

경로: scenario/auth/

파일: Dockerfile, named.conf, bank.test.zone

요구사항:

bank.test 도메인의 A 레코드  를 172.20.0.50 (Real Web)으로 설정.

호스트 포트 20053  (UDP/TCP) 매핑.

Resolver  설정 업데이트: bank.test 에 대한 질의를 auth 서버(172.20.0.20)로 전달(Forwarding)하도록 수정.

검증:

dig @localhost -p 10053 bank.test 수행 시 172.20.0.50 이 반환되는지 확인.
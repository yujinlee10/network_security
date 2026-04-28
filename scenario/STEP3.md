🟥 Step 3: Attacker 구현 및 공격 테스트
목표: Scapy를 이용한 패킷 주입 및 리졸버 캐시 오염 확인.

경로: scenario/attacker/

파일: Dockerfile, attack.py

요구사항:

Python Scapy 기반 공격 코드 작성.

CVE-2025-40778  취약점을 이용해 bank.test 의 IP를 172.20.0.60 (Fake Web)으로 변조하는 패킷 생성.

공격 컨테이너는 privileged: true 로 실행.

검증:

공격 실행 후 docker exec resolver rndc dumpdb -cache 명령어로 캐시 내 IP가 172.20.0.60 으로 바뀌었는지 확인.
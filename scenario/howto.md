1. Architecture
Node	Role	IP Address	Port
Resolver	Victim (BIND 9.18.x)	172.20.0.10	53/udp
Auth	Mock Authoritative Server	172.20.0.20	53/udp
Attacker	Scapy Spoofing Tool	172.20.0.30	-
Real Web	Green Page (Normal)	172.20.0.50	80/tcp
Fake Web	Red Page (Phishing)	172.20.0.60	80/tcp

2. Quick Start
Step 1: 환경 구축
전체 컨테이너를 빌드하고 백그라운드에서 실행합니다.

    Bash
    docker-compose up -d --build

Step 2: 네트워크 지연 설정 (Latency )
로컬 환경에서는 응답 속도가 너무 빠르므로, 성공적인 Race Condition  유도를 위해 권한 서버에 지연을 추가합니다. (5초~10초 권장)

    Bash
    docker exec -it auth tc qdisc replace dev eth0 root netem delay 5000ms

Step 3: 공격 실행
공격자 컨테이너에 접속하여 위조 패킷 송출 스크립트를 실행합니다.

    Bash
    docker exec -it attacker python3 attack.py

Step 4: 공격 트리거 (Trigger )
호스트 또는 클라이언트 노드에서 리졸버에게 질의를 던져 권한 서버와의 통신을 유도합니다.

    Bash
    dig @localhost -p 10053 bank.test

3. Verification
캐시 오염 확인
리졸버의 캐시 덤프를 생성하여 bank.test 가 172.20.0.60 (Fake Web)으로 매핑되었는지 확인합니다.

    Bash
    docker exec -it resolver rndc dumpdb -cache
    docker exec -it resolver grep "bank.test" /var/cache/bind/named_dump.db

최종 피싱 확인
curl 을 사용하여 변조된 웹 페이지가 로드되는지 검증합니다.

    Bash
    curl --resolve bank.test:80:127.0.0.1 -p 8081 http://bank.test

4. Troubleshooting
Permission Denied: tcpdump 나 tc 사용 시 권한 에러가 발생하면 docker-compose.yml 에 privileged: true 옵션을 확인하십시오.

Cache Hit: 이전에 질의한 기록이 남아있으면 공격이 작동하지 않습니다. 질의 전 항상 캐시를 초기화하십시오.

    Bash
    docker exec -it resolver rndc flush \
    dig @localhost -p 10053 bank.test

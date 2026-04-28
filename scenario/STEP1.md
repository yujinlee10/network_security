🟦 Step 1: Resolver (Victim) 구현
목표: 취약한 설정이 적용된 BIND9 리졸버 서버 구축.

경로: scenario/resolver/

파일: Dockerfile, named.conf

요구사항:

BIND9 v9.18.39 (취약 버전) 사용. 및 docker에 명시

named.conf 에서 recursion yes;, allow-query { any; };, dnssec-validation no; 설정.

호스트 포트 10053  (UDP/TCP) 매핑.

검증:

dig @localhost -p 10053 google.com 수행 시 정상적인 재귀 응답이 오는지 확인
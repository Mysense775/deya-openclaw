#!/usr/bin/env python3
"""
Intrusion Detection - обнаружение вторжений
Мониторит auth.log на brute-force, подозрительные входы
"""

import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
import json
import time
import subprocess

class IntrusionDetection:
    """Система обнаружения вторжений"""
    
    def __init__(self, log_file: str = '/var/log/auth.log'):
        self.log_file = Path(log_file)
        self.suspicious_activity = []
        self.banned_ips = set()
        
    def parse_auth_log(self, since_minutes: int = 60) -> list:
        """Парсит auth.log на события авторизации"""
        events = []
        cutoff_time = datetime.now() - timedelta(minutes=since_minutes)
        
        if not self.log_file.exists():
            # Пробуем journalctl для systemd
            result = subprocess.run(
                ['journalctl', '-u', 'ssh', '--since', f'{since_minutes} minutes ago', '--no-pager'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                log_content = result.stdout
            else:
                return events
        else:
            with open(self.log_file, 'r', errors='ignore') as f:
                log_content = f.read()
        
        # Паттерны для поиска
        patterns = {
            'failed_password': r'Failed password for (?:invalid user )?(\S+) from (\S+)',
            'accepted_password': r'Accepted password for (\S+) from (\S+)',
            'invalid_user': r'Invalid user (\S+) from (\S+)',
            'connection_closed': r'Connection closed by (\S+)',
            'reverse_mapping': r'reverse mapping checking getaddrinfo for .* failed',
            'break_in': r'POSSIBLE BREAK-IN ATTEMPT',
        }
        
        for line in log_content.split('\n'):
            # Парсим timestamp
            time_match = re.match(r'(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})', line)
            if time_match:
                timestamp_str = time_match.group(1)
                try:
                    timestamp = datetime.strptime(f"{datetime.now().year} {timestamp_str}", "%Y %b %d %H:%M:%S")
                except:
                    continue
                
                if timestamp < cutoff_time:
                    continue
            
            # Ищем события
            for event_type, pattern in patterns.items():
                match = re.search(pattern, line)
                if match:
                    event = {
                        'timestamp': timestamp_str if time_match else None,
                        'type': event_type,
                        'raw': line,
                        'matches': match.groups()
                    }
                    
                    if event_type == 'failed_password':
                        event['user'] = match.group(1)
                        event['ip'] = match.group(2)
                    elif event_type == 'accepted_password':
                        event['user'] = match.group(1)
                        event['ip'] = match.group(2)
                    elif event_type == 'invalid_user':
                        event['user'] = match.group(1)
                        event['ip'] = match.group(2)
                    
                    events.append(event)
        
        return events
    
    def detect_brute_force(self, events: list, threshold: int = 5) -> list:
        """Обнаруживает brute-force атаки"""
        # Группируем по IP
        ip_attempts = defaultdict(list)
        
        for event in events:
            if event['type'] in ['failed_password', 'invalid_user']:
                ip = event.get('ip')
                if ip:
                    ip_attempts[ip].append(event)
        
        brute_force_ips = []
        for ip, attempts in ip_attempts.items():
            if len(attempts) >= threshold:
                users_tried = set(e.get('user', 'unknown') for e in attempts)
                brute_force_ips.append({
                    'ip': ip,
                    'attempt_count': len(attempts),
                    'users_tried': list(users_tried),
                    'first_attempt': attempts[0]['timestamp'],
                    'last_attempt': attempts[-1]['timestamp'],
                    'severity': 'HIGH' if len(attempts) > 10 else 'MEDIUM'
                })
        
        return sorted(brute_force_ips, key=lambda x: x['attempt_count'], reverse=True)
    
    def detect_suspicious_users(self, events: list) -> list:
        """Обнаруживает подозрительную активность пользователей"""
        # Пользователи, пытающиеся зайти с разных IP
        user_ips = defaultdict(set)
        
        for event in events:
            if event['type'] in ['failed_password', 'accepted_password']:
                user = event.get('user')
                ip = event.get('ip')
                if user and ip:
                    user_ips[user].add(ip)
        
        suspicious = []
        for user, ips in user_ips.items():
            if len(ips) > 3:  # Много разных IP
                suspicious.append({
                    'user': user,
                    'unique_ips': len(ips),
                    'ips': list(ips),
                    'severity': 'MEDIUM'
                })
        
        return suspicious
    
    def detect_success_after_brute(self, events: list) -> list:
        """Обнаруживает успешные входы после множественных попыток"""
        # Группируем по IP
        ip_events = defaultdict(list)
        
        for event in events:
            ip = event.get('ip')
            if ip:
                ip_events[ip].append(event)
        
        compromised = []
        for ip, ip_events_list in ip_events.items():
            failures = [e for e in ip_events_list if e['type'] in ['failed_password', 'invalid_user']]
            successes = [e for e in ip_events_list if e['type'] == 'accepted_password']
            
            if len(failures) > 3 and successes:
                # Проверяем, что успех был после неудач
                last_failure = max(e['timestamp'] for e in failures)
                first_success = min(e['timestamp'] for e in successes)
                
                if first_success >= last_failure:
                    compromised.append({
                        'ip': ip,
                        'failed_attempts': len(failures),
                        'successful_user': successes[0].get('user'),
                        'severity': 'CRITICAL'
                    })
        
        return compromised
    
    def check_banned_ips(self) -> list:
        """Проверяет забаненные IP (fail2ban)"""
        banned = []
        
        # Проверяем iptables на наличие fail2ban правил
        result = subprocess.run(['iptables', '-L', '-n'], capture_output=True, text=True)
        
        fail2ban_chains = re.findall(r'(fail2ban-[^\s]+)', result.stdout)
        
        for chain in set(fail2ban_chains):
            chain_result = subprocess.run(
                ['iptables', '-L', chain, '-n'],
                capture_output=True, text=True
            )
            
            ips = re.findall(r'DROP\s+.*\s+(\d+\.\d+\.\d+\.\d+)', chain_result.stdout)
            for ip in ips:
                banned.append({
                    'ip': ip,
                    'chain': chain,
                    'reason': 'fail2ban'
                })
        
        return banned
    
    def analyze(self, since_minutes: int = 60) -> dict:
        """Полный анализ на предмет вторжений"""
        print(f"🔍 Analyzing authentication logs (last {since_minutes} minutes)...")
        
        events = self.parse_auth_log(since_minutes)
        
        if not events:
            return {
                'timestamp': datetime.now().isoformat(),
                'events_count': 0,
                'threats': [],
                'status': 'clean'
            }
        
        threats = []
        
        # Brute force detection
        brute_force = self.detect_brute_force(events)
        for ip_data in brute_force:
            threats.append({
                'type': 'brute_force',
                'severity': ip_data['severity'],
                'source': ip_data['ip'],
                'details': ip_data,
                'recommendation': f'Consider blocking IP: iptables -A INPUT -s {ip_data["ip"]} -j DROP'
            })
        
        # Suspicious users
        suspicious_users = self.detect_suspicious_users(events)
        for user_data in suspicious_users:
            threats.append({
                'type': 'suspicious_user',
                'severity': user_data['severity'],
                'source': user_data['user'],
                'details': user_data,
                'recommendation': 'Verify user activity and consider password reset'
            })
        
        # Successful brute force
        compromised = self.detect_success_after_brute(events)
        for comp in compromised:
            threats.append({
                'type': 'compromised_account',
                'severity': comp['severity'],
                'source': comp['ip'],
                'details': comp,
                'recommendation': f'CRITICAL: Possible account compromise. Block IP {comp["ip"]} and reset passwords'
            })
        
        # Already banned
        banned = self.check_banned_ips()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'events_count': len(events),
            'failed_attempts': len([e for e in events if e['type'] in ['failed_password', 'invalid_user']]),
            'successful_logins': len([e for e in events if e['type'] == 'accepted_password']),
            'banned_ips_count': len(banned),
            'threats': threats,
            'status': 'critical' if any(t['severity'] == 'CRITICAL' for t in threats) else 
                     'warning' if threats else 'clean'
        }
    
    def print_report(self, report: dict):
        """Выводит отчёт"""
        print(f"\n{'='*70}")
        print(f"🔍 INTRUSION DETECTION REPORT")
        print(f"{'='*70}")
        print(f"Events analyzed: {report['events_count']}")
        print(f"Failed attempts: {report['failed_attempts']}")
        print(f"Successful logins: {report['successful_logins']}")
        print(f"Banned IPs: {report['banned_ips_count']}")
        
        if report['threats']:
            print(f"\n⚠️  THREATS DETECTED ({len(report['threats'])}):")
            print("-" * 70)
            
            for threat in report['threats']:
                emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(threat['severity'], '•')
                print(f"\n{emoji} [{threat['severity']}] {threat['type'].upper()}")
                print(f"   Source: {threat['source']}")
                print(f"   {threat['recommendation']}")
                
                if 'details' in threat:
                    details = threat['details']
                    if 'attempt_count' in details:
                        print(f"   Attempts: {details['attempt_count']}")
                    if 'users_tried' in details:
                        print(f"   Users tried: {', '.join(details['users_tried'][:5])}")
        else:
            print("\n✅ No threats detected")
        
        print(f"\n{'='*70}")
    
    def watch_mode(self, interval: int = 60):
        """Режим непрерывного мониторинга"""
        print(f"👁️  Intrusion detection watch mode started (interval: {interval}s)")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                report = self.analyze(since_minutes=interval//60 + 1)
                
                if report['status'] != 'clean':
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ALERT: {report['status'].upper()}")
                    self.print_report(report)
                    
                    # Здесь можно добавить отправку уведомлений
                    # send_telegram_alert(report)
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Status: clean")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n👋 Watch mode stopped")

def main():
    parser = argparse.ArgumentParser(description='Intrusion Detection System')
    parser.add_argument('--analyze', '-a', action='store_true', help='Run analysis')
    parser.add_argument('--watch', '-w', action='store_true', help='Watch mode')
    parser.add_argument('--since', type=int, default=60, help='Analyze last N minutes')
    parser.add_argument('--interval', type=int, default=60, help='Watch interval in seconds')
    parser.add_argument('--threshold', type=int, default=5, help='Brute force threshold')
    parser.add_argument('--json', '-j', help='Export to JSON')
    
    args = parser.parse_args()
    
    detector = IntrusionDetection()
    
    if args.watch:
        detector.watch_mode(args.interval)
    elif args.analyze or not args.watch:
        report = detector.analyze(args.since)
        detector.print_report(report)
        
        if args.json:
            with open(args.json, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n✅ Report exported to {args.json}")
        
        # Exit code
        if report['status'] == 'critical':
            exit(2)
        elif report['status'] == 'warning':
            exit(1)
        else:
            exit(0)

if __name__ == '__main__':
    main()

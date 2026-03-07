#!/usr/bin/env python3
"""
Certificate Monitor - мониторинг SSL/TLS сертификатов
Проверяет срок действия, конфигурацию, уведомляет об истечении
"""

import argparse
import ssl
import socket
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import json

class CertificateMonitor:
    """Монитор SSL сертификатов"""
    
    def __init__(self):
        self.checks = []
    
    def check_certificate(self, hostname: str, port: int = 443) -> dict:
        """Проверяет сертификат хоста"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
                    
                    # Парсим даты
                    not_after = cert.get('notAfter')
                    not_before = cert.get('notBefore')
                    
                    expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                    start_date = datetime.strptime(not_before, '%b %d %H:%M:%S %Y %Z')
                    
                    days_until_expiry = (expiry_date - datetime.now()).days
                    
                    # Определяем статус
                    if days_until_expiry < 0:
                        status = 'EXPIRED'
                        severity = 'CRITICAL'
                    elif days_until_expiry < 7:
                        status = 'EXPIRING_SOON'
                        severity = 'CRITICAL'
                    elif days_until_expiry < 30:
                        status = 'WARNING'
                        severity = 'HIGH'
                    else:
                        status = 'VALID'
                        severity = 'INFO'
                    
                    return {
                        'hostname': hostname,
                        'port': port,
                        'status': status,
                        'severity': severity,
                        'expiry_date': expiry_date.isoformat(),
                        'start_date': start_date.isoformat(),
                        'days_until_expiry': days_until_expiry,
                        'issuer': cert.get('issuer'),
                        'subject': cert.get('subject'),
                        'ssl_version': version,
                        'cipher': cipher[0] if cipher else None,
                        'san': cert.get('subjectAltName', [])
                    }
                    
        except ssl.SSLError as e:
            return {
                'hostname': hostname,
                'port': port,
                'status': 'SSL_ERROR',
                'severity': 'HIGH',
                'error': str(e)
            }
        except socket.error as e:
            return {
                'hostname': hostname,
                'port': port,
                'status': 'CONNECTION_ERROR',
                'severity': 'HIGH',
                'error': str(e)
            }
        except Exception as e:
            return {
                'hostname': hostname,
                'port': port,
                'status': 'ERROR',
                'severity': 'HIGH',
                'error': str(e)
            }
    
    def check_local_certificates(self, cert_dir: str = '/etc/letsencrypt/live') -> list:
        """Проверяет локальные сертификаты Let's Encrypt"""
        certs = []
        cert_path = Path(cert_dir)
        
        if not cert_path.exists():
            return certs
        
        for domain_dir in cert_path.iterdir():
            if domain_dir.is_dir():
                cert_file = domain_dir / 'cert.pem'
                if cert_file.exists():
                    result = self._check_local_cert_file(cert_file, domain_dir.name)
                    certs.append(result)
        
        return certs
    
    def _check_local_cert_file(self, cert_file: Path, name: str) -> dict:
        """Проверяет локальный файл сертификата"""
        try:
            # Используем openssl для получения информации
            result = subprocess.run(
                ['openssl', 'x509', '-in', str(cert_file), '-noout', '-dates', '-subject', '-issuer'],
                capture_output=True, text=True
            )
            
            if result.returncode != 0:
                return {
                    'hostname': name,
                    'status': 'READ_ERROR',
                    'severity': 'MEDIUM',
                    'error': result.stderr
                }
            
            # Парсим вывод
            not_after = re.search(r'notAfter=(.+)', result.stdout)
            not_before = re.search(r'notBefore=(.+)', result.stdout)
            
            if not_after:
                expiry_date = datetime.strptime(not_after.group(1).strip(), '%b %d %H:%M:%S %Y %Z')
                days_until_expiry = (expiry_date - datetime.now()).days
                
                if days_until_expiry < 0:
                    status = 'EXPIRED'
                    severity = 'CRITICAL'
                elif days_until_expiry < 7:
                    status = 'EXPIRING_SOON'
                    severity = 'CRITICAL'
                elif days_until_expiry < 30:
                    status = 'WARNING'
                    severity = 'HIGH'
                else:
                    status = 'VALID'
                    severity = 'INFO'
                
                return {
                    'hostname': name,
                    'status': status,
                    'severity': severity,
                    'expiry_date': expiry_date.isoformat(),
                    'days_until_expiry': days_until_expiry,
                    'file': str(cert_file)
                }
            
        except Exception as e:
            return {
                'hostname': name,
                'status': 'ERROR',
                'severity': 'MEDIUM',
                'error': str(e)
            }
    
    def check_ssl_configuration(self, hostname: str, port: int = 443) -> dict:
        """Проверяет конфигурацию SSL (ciphers, protocols)"""
        issues = []
        
        # Проверка слабых cipher suites
        weak_ciphers = ['RC4', 'DES', '3DES', 'MD5', 'NULL']
        
        try:
            for cipher in weak_ciphers:
                result = subprocess.run(
                    ['openssl', 's_client', '-connect', f'{hostname}:{port}', 
                     '-cipher', cipher, '-servername', hostname],
                    input='Q', capture_output=True, text=True, timeout=5
                )
                
                if 'Cipher is ' in result.stdout and 'Cipher is :' not in result.stdout:
                    issues.append(f'Weak cipher supported: {cipher}')
        except:
            pass
        
        # Проверка SSLv2, SSLv3
        for version in ['ssl2', 'ssl3']:
            try:
                result = subprocess.run(
                    ['openssl', 's_client', '-connect', f'{hostname}:{port}',
                     f'-{version}', '-servername', hostname],
                    input='Q', capture_output=True, text=True, timeout=5
                )
                
                if 'Protocol : ' in result.stdout:
                    issues.append(f'Insecure protocol supported: {version.upper()}')
            except:
                pass
        
        return {
            'hostname': hostname,
            'port': port,
            'ssl_issues': issues,
            'severity': 'HIGH' if issues else 'INFO'
        }
    
    def print_report(self, results: list):
        """Выводит отчёт"""
        print(f"\n{'='*70}")
        print(f"🔒 SSL CERTIFICATE REPORT")
        print(f"{'='*70}")
        
        expired = [r for r in results if r.get('status') == 'EXPIRED']
        expiring = [r for r in results if r.get('status') in ['EXPIRING_SOON', 'WARNING']]
        valid = [r for r in results if r.get('status') == 'VALID']
        errors = [r for r in results if r.get('status') in ['ERROR', 'CONNECTION_ERROR', 'SSL_ERROR']]
        
        if expired:
            print(f"\n🔴 EXPIRED ({len(expired)}):")
            for r in expired:
                print(f"   {r['hostname']} - Expired {abs(r.get('days_until_expiry', 0))} days ago")
        
        if expiring:
            print(f"\n🟠 EXPIRING SOON ({len(expiring)}):")
            for r in expiring:
                print(f"   {r['hostname']} - {r.get('days_until_expiry', 'N/A')} days left")
        
        if errors:
            print(f"\n❌ ERRORS ({len(errors)}):")
            for r in errors:
                print(f"   {r['hostname']} - {r.get('error', 'Unknown error')}")
        
        if valid:
            print(f"\n✅ VALID ({len(valid)}):")
            for r in valid[:5]:  # Показываем первые 5
                print(f"   {r['hostname']} - {r.get('days_until_expiry', 'N/A')} days left")
            if len(valid) > 5:
                print(f"   ... and {len(valid) - 5} more")
        
        print(f"\n{'='*70}")

def main():
    parser = argparse.ArgumentParser(description='SSL Certificate Monitor')
    parser.add_argument('--domain', '-d', help='Check specific domain')
    parser.add_argument('--port', '-p', type=int, default=443, help='Port (default: 443)')
    parser.add_argument('--check-all', action='store_true', help='Check all local certificates')
    parser.add_argument('--cert-dir', default='/etc/letsencrypt/live', help='Certificate directory')
    parser.add_argument('--json', '-j', help='Export to JSON')
    parser.add_argument('--config', action='store_true', help='Check SSL configuration')
    
    args = parser.parse_args()
    
    monitor = CertificateMonitor()
    results = []
    
    if args.domain:
        result = monitor.check_certificate(args.domain, args.port)
        results.append(result)
        
        if args.config:
            config = monitor.check_ssl_configuration(args.domain, args.port)
            print(f"\nSSL Configuration Issues: {config['ssl_issues']}")
    
    elif args.check_all:
        results = monitor.check_local_certificates(args.cert_dir)
    
    else:
        # По умолчанию проверяем локальные сертификаты
        results = monitor.check_local_certificates(args.cert_dir)
    
    monitor.print_report(results)
    
    if args.json:
        with open(args.json, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n✅ Report exported to {args.json}")
    
    # Exit code
    expired = [r for r in results if r.get('status') == 'EXPIRED']
    if expired:
        exit(2)
    
    warning = [r for r in results if r.get('status') in ['EXPIRING_SOON', 'WARNING']]
    if warning:
        exit(1)
    
    exit(0)

if __name__ == '__main__':
    main()

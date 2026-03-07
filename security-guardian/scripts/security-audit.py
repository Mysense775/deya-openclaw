#!/usr/bin/env python3
"""
Security Audit - полный аудит безопасности системы
Проверяет конфигурации, права доступа, сетевые настройки
"""

import argparse
import subprocess
import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

class SecurityAudit:
    """Аудитор безопасности"""
    
    def __init__(self):
        self.findings = []
        self.score = 100
        self.hostname = os.uname().nodename
        
    def add_finding(self, level: str, category: str, title: str, 
                    description: str, remediation: str = None):
        """Добавляет находку аудита"""
        finding = {
            'timestamp': datetime.now().isoformat(),
            'level': level,  # CRITICAL, HIGH, MEDIUM, LOW, INFO
            'category': category,
            'title': title,
            'description': description,
            'remediation': remediation
        }
        self.findings.append(finding)
        
        # Уменьшаем score за проблемы
        if level == 'CRITICAL':
            self.score -= 20
        elif level == 'HIGH':
            self.score -= 10
        elif level == 'MEDIUM':
            self.score -= 5
        elif level == 'LOW':
            self.score -= 2
    
    def check_ssh_config(self):
        """Проверка конфигурации SSH"""
        ssh_config_path = Path('/etc/ssh/sshd_config')
        
        if not ssh_config_path.exists():
            self.add_finding('HIGH', 'SSH', 'SSH config not found',
                           'Cannot find /etc/ssh/sshd_config')
            return
        
        with open(ssh_config_path) as f:
            config = f.read()
        
        # Проверка RootLogin
        if re.search(r'^PermitRootLogin\s+yes', config, re.MULTILINE):
            self.add_finding(
                'CRITICAL', 'SSH', 'Root login enabled',
                'SSH allows direct root login. This is a major security risk.',
                'Set "PermitRootLogin no" in /etc/ssh/sshd_config'
            )
        else:
            self.add_finding('INFO', 'SSH', 'Root login disabled', 'Good')
        
        # Проверка PasswordAuthentication
        if re.search(r'^PasswordAuthentication\s+yes', config, re.MULTILINE):
            self.add_finding(
                'HIGH', 'SSH', 'Password authentication enabled',
                'SSH allows password authentication. Keys are more secure.',
                'Set "PasswordAuthentication no" and use SSH keys'
            )
        
        # Проверка порта
        port_match = re.search(r'^Port\s+(\d+)', config, re.MULTILINE)
        if port_match:
            port = int(port_match.group(1))
            if port == 22:
                self.add_finding(
                    'MEDIUM', 'SSH', 'SSH on default port 22',
                    'Using default port makes automated attacks easier.',
                    'Consider changing to non-standard port (e.g., 2222)'
                )
            else:
                self.add_finding('INFO', 'SSH', f'SSH on non-default port {port}', 'Good')
        
        # Проверка протокола
        if re.search(r'^Protocol\s+1', config, re.MULTILINE):
            self.add_finding(
                'CRITICAL', 'SSH', 'SSH Protocol 1 enabled',
                'Protocol 1 has known security vulnerabilities.',
                'Set "Protocol 2" in sshd_config'
            )
    
    def check_firewall(self):
        """Проверка firewall"""
        # Проверка UFW
        ufw_status = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
        
        if ufw_status.returncode == 0:
            if 'Status: active' in ufw_status.stdout:
                self.add_finding('INFO', 'Firewall', 'UFW is active', 'Good')
                
                # Проверяем дефолтные политики
                if 'Default: deny (incoming)' in ufw_status.stdout:
                    self.add_finding('INFO', 'Firewall', 'Default deny incoming', 'Good')
                else:
                    self.add_finding(
                        'HIGH', 'Firewall', 'Default allow incoming',
                        'UFW default policy allows incoming connections.',
                        'Run: ufw default deny incoming'
                    )
            else:
                self.add_finding(
                    'CRITICAL', 'Firewall', 'UFW is inactive',
                    'Firewall is disabled. System is exposed to network attacks.',
                    'Run: ufw enable'
                )
        else:
            # Проверка iptables
            iptables = subprocess.run(['iptables', '-L', '-n'], 
                                    capture_output=True, text=True)
            if iptables.returncode != 0 or 'Chain INPUT' not in iptables.stdout:
                self.add_finding(
                    'CRITICAL', 'Firewall', 'No firewall detected',
                    'Neither UFW nor iptables rules found.',
                    'Install and configure UFW: apt install ufw && ufw enable'
                )
    
    def check_file_permissions(self):
        """Проверка опасных прав доступа к файлам"""
        # SUID/SGID файлы
        result = subprocess.run(
            ['find', '/', '-perm', '-4000', '-o', '-perm', '-2000'],
            capture_output=True, text=True
        )
        
        suid_files = [f for f in result.stdout.strip().split('\n') if f and not f.startswith('/proc')]
        
        if len(suid_files) > 50:  # Много SUID файлов - подозрительно
            self.add_finding(
                'MEDIUM', 'Permissions', f'Many SUID/SGID files ({len(suid_files)})',
                'Large number of SUID/SGID files increases attack surface.',
                'Review files: find / -perm -4000 -ls'
            )
        
        # World-writable файлы
        ww_result = subprocess.run(
            ['find', '/', '-type', 'f', '-perm', '-002', '!', '-type', 'l'],
            capture_output=True, text=True
        )
        
        ww_files = [f for f in ww_result.stdout.strip().split('\n') if f and not f.startswith('/proc')][:20]
        
        if ww_files:
            self.add_finding(
                'HIGH', 'Permissions', f'World-writable files found ({len(ww_files)}+)',
                f'Files writable by anyone: {", ".join(ww_files[:5])}',
                'Remove write permissions: chmod o-w <file>'
            )
        
        # SSH директории пользователей
        for user_dir in Path('/home').iterdir():
            if user_dir.is_dir():
                ssh_dir = user_dir / '.ssh'
                if ssh_dir.exists():
                    stat = ssh_dir.stat()
                    if oct(stat.st_mode)[-3:] != '700':
                        self.add_finding(
                            'MEDIUM', 'Permissions', f'Wrong permissions on {ssh_dir}',
                            f'SSH directory has permissions {oct(stat.st_mode)[-3:]}, should be 700',
                            f'Run: chmod 700 {ssh_dir}'
                        )
    
    def check_services(self):
        """Проверка запущенных сервисов"""
        # Список потенциально опасных сервисов
        dangerous_services = [
            'telnet', 'ftp', 'rsh', 'rlogin', 'rexec', 
            'nfs', 'smb', 'samba', 'snmp'
        ]
        
        for service in dangerous_services:
            result = subprocess.run(
                ['systemctl', 'is-active', service],
                capture_output=True, text=True
            )
            if result.returncode == 0 and 'active' in result.stdout:
                self.add_finding(
                    'HIGH', 'Services', f'Dangerous service active: {service}',
                    f'{service} is running and may have security vulnerabilities.',
                    f'Run: systemctl stop {service} && systemctl disable {service}'
                )
        
        # Проверка exposed портов
        ports_result = subprocess.run(
            ['ss', '-tlnp'],
            capture_output=True, text=True
        )
        
        # Ищем порты слушающие на 0.0.0.0
        exposed_ports = []
        for line in ports_result.stdout.split('\n'):
            if '0.0.0.0:' in line or ':::" in line:
                match = re.search(r':(\d+)', line)
                if match:
                    port = int(match.group(1))
                    if port not in [22, 80, 443]:  # Стандартные порты нормальны
                        exposed_ports.append(port)
        
        if exposed_ports:
            self.add_finding(
                'MEDIUM', 'Services', f'Non-standard ports exposed: {exposed_ports}',
                'Services listening on public interfaces.',
                'Verify these services need to be publicly accessible'
            )
    
    def check_updates(self):
        """Проверка доступных обновлений безопасности"""
        # Для Ubuntu/Debian
        result = subprocess.run(
            ['apt', 'list', '--upgradable'],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            updates = [line for line in result.stdout.split('\n') if 'security' in line.lower()]
            
            if updates:
                self.add_finding(
                    'HIGH', 'Updates', f'Security updates available ({len(updates)})',
                    f'{len(updates)} security updates need to be installed.',
                    'Run: apt update && apt upgrade'
                )
            else:
                self.add_finding('INFO', 'Updates', 'No security updates pending', 'Good')
    
    def check_users(self):
        """Проверка пользователей и паролей"""
        # Пользователи без паролей
        shadow_path = Path('/etc/shadow')
        if shadow_path.exists():
            with open(shadow_path) as f:
                for line in f:
                    parts = line.split(':')
                    if len(parts) > 1:
                        username, password = parts[0], parts[1]
                        # Пустой пароль или !! означает отключенный аккаунт
                        if password == '' or password == '!!':
                            if username not in ['root', 'nobody', 'systemd-network']:
                                self.add_finding(
                                    'HIGH', 'Users', f'User {username} has no password',
                                    f'Account {username} has empty or locked password.',
                                    f'Set password: passwd {username} or remove user: userdel {username}'
                                )
        
        # Проверка sudoers
        sudoers_path = Path('/etc/sudoers')
        if sudoers_path.exists():
            with open(sudoers_path) as f:
                sudoers = f.read()
                if 'NOPASSWD' in sudoers:
                    self.add_finding(
                        'MEDIUM', 'Users', 'NOPASSWD in sudoers',
                        'Some users can run sudo without password.',
                        'Review /etc/sudoers and remove NOPASSWD where possible'
                    )
    
    def check_kernel(self):
        """Проверка версии ядра"""
        result = subprocess.run(['uname', '-r'], capture_output=True, text=True)
        kernel_version = result.stdout.strip()
        
        # Проверка на нестандартное ядро (может быть устаревшим)
        if 'generic' not in kernel_version and 'cloud' not in kernel_version:
            self.add_finding(
                'LOW', 'Kernel', f'Non-standard kernel: {kernel_version}',
                'Custom kernel may not receive security updates.',
                'Consider using distribution kernel'
            )
    
    def run_full_audit(self):
        """Запускает полный аудит"""
        print("🔒 Starting security audit...\n")
        
        checks = [
            ('SSH Configuration', self.check_ssh_config),
            ('Firewall', self.check_firewall),
            ('File Permissions', self.check_file_permissions),
            ('Services', self.check_services),
            ('Updates', self.check_updates),
            ('Users', self.check_users),
            ('Kernel', self.check_kernel),
        ]
        
        for name, check_func in checks:
            print(f"  Checking {name}...")
            try:
                check_func()
            except Exception as e:
                self.add_finding('ERROR', name, f'Check failed: {e}', str(e))
        
        return self.get_report()
    
    def get_report(self) -> Dict:
        """Возвращает полный отчёт"""
        # Группируем находки по уровню
        by_level = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': [], 'INFO': []}
        for finding in self.findings:
            level = finding['level']
            if level in by_level:
                by_level[level].append(finding)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'hostname': self.hostname,
            'score': max(0, self.score),
            'findings_count': len(self.findings),
            'by_level': {k: len(v) for k, v in by_level.items()},
            'findings': self.findings,
            'summary': self._generate_summary(by_level)
        }
    
    def _generate_summary(self, by_level: Dict) -> str:
        """Генерирует текстовую сводку"""
        lines = [
            f"Security Score: {max(0, self.score)}/100",
            "",
            "Findings by severity:",
            f"  🔴 CRITICAL: {len(by_level['CRITICAL'])}",
            f"  🟠 HIGH: {len(by_level['HIGH'])}",
            f"  🟡 MEDIUM: {len(by_level['MEDIUM'])}",
            f"  🟢 LOW: {len(by_level['LOW'])}",
            f"  ℹ️  INFO: {len(by_level['INFO'])}",
        ]
        return '\n'.join(lines)
    
    def print_report(self, report: Dict):
        """Выводит отчёт в консоль"""
        print(f"\n{'='*70}")
        print(f"🔒 SECURITY AUDIT REPORT")
        print(f"{'='*70}")
        print(f"Host: {report['hostname']}")
        print(f"Score: {report['score']}/100")
        print(f"Findings: {report['findings_count']}")
        print(f"{'='*70}")
        
        for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
            findings = [f for f in report['findings'] if f['level'] == level]
            if findings:
                emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢', 'INFO': 'ℹ️'}.get(level, '•')
                print(f"\n{emoji} {level} ({len(findings)}):")
                print("-" * 70)
                for f in findings:
                    print(f"\n  [{f['category']}] {f['title']}")
                    print(f"  {f['description']}")
                    if f.get('remediation'):
                        print(f"  💡 Fix: {f['remediation']}")
        
        print(f"\n{'='*70}")

def main():
    parser = argparse.ArgumentParser(description='Security Audit Tool')
    parser.add_argument('--full', '-f', action='store_true', help='Full audit')
    parser.add_argument('--check', choices=['ssh', 'firewall', 'files', 'services', 'updates', 'users', 'kernel'],
                       help='Check specific area')
    parser.add_argument('--json', help='Export report to JSON file')
    parser.add_argument('--html', help='Export report to HTML file')
    parser.add_argument('--auto-fix', action='store_true', help='Automatically fix issues (use with caution)')
    
    args = parser.parse_args()
    
    audit = SecurityAudit()
    
    if args.full:
        report = audit.run_full_audit()
    elif args.check:
        check_map = {
            'ssh': audit.check_ssh_config,
            'firewall': audit.check_firewall,
            'files': audit.check_file_permissions,
            'services': audit.check_services,
            'updates': audit.check_updates,
            'users': audit.check_users,
            'kernel': audit.check_kernel
        }
        check_map[args.check]()
        report = audit.get_report()
    else:
        report = audit.run_full_audit()
    
    # Вывод
    audit.print_report(report)
    
    # Экспорт
    if args.json:
        with open(args.json, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n✅ Report exported to {args.json}")
    
    if args.html:
        generate_html_report(report, args.html)
        print(f"\n✅ HTML report exported to {args.html}")
    
    # Exit code based on severity
    critical_count = len([f for f in audit.findings if f['level'] == 'CRITICAL'])
    high_count = len([f for f in audit.findings if f['level'] == 'HIGH'])
    
    if critical_count > 0:
        exit(2)
    elif high_count > 0:
        exit(1)
    else:
        exit(0)

def generate_html_report(report: Dict, output_path: str):
    """Генерирует HTML отчёт"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Security Audit Report - {report['hostname']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .header {{ background: #333; color: white; padding: 20px; border-radius: 8px; }}
        .score {{ font-size: 48px; font-weight: bold; }}
        .score-good {{ color: #4CAF50; }}
        .score-medium {{ color: #FF9800; }}
        .score-bad {{ color: #F44336; }}
        .finding {{ background: white; margin: 10px 0; padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .CRITICAL {{ border-left: 5px solid #F44336; }}
        .HIGH {{ border-left: 5px solid #FF9800; }}
        .MEDIUM {{ border-left: 5px solid #FFEB3B; }}
        .LOW {{ border-left: 5px solid #4CAF50; }}
        .INFO {{ border-left: 5px solid #2196F3; }}
        .level {{ font-weight: bold; text-transform: uppercase; }}
        .remediation {{ background: #e3f2fd; padding: 10px; margin-top: 10px; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔒 Security Audit Report</h1>
        <p>Host: {report['hostname']} | Date: {report['timestamp']}</p>
        <div class="score {'score-good' if report['score'] >= 80 else 'score-medium' if report['score'] >= 60 else 'score-bad'}">
            {report['score']}/100
        </div>
    </div>
"""
    
    for finding in report['findings']:
        html += f"""
    <div class="finding {finding['level']}">
        <span class="level">{finding['level']}</span> | <strong>{finding['category']}</strong>
        <h3>{finding['title']}</h3>
        <p>{finding['description']}</p>
        {f'<div class="remediation">💡 {finding["remediation"]}</div>' if finding.get('remediation') else ''}
    </div>
"""
    
    html += """
</body>
</html>
"""
    
    with open(output_path, 'w') as f:
        f.write(html)

if __name__ == '__main__':
    main()

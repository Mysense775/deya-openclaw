#!/usr/bin/env python3
"""
Server Monitor - мониторинг сервера в реальном времени
Отслеживает CPU, RAM, диск, сеть и отправляет алерты
"""

import argparse
import psutil
import time
import json
from datetime import datetime
from typing import Dict, Optional
import os

class ServerMonitor:
    """Мониторинг системных ресурсов"""
    
    def __init__(self):
        self.alert_thresholds = {
            'cpu': 80,      # %
            'ram': 85,      # %
            'disk': 90,     # %
            'load': 4.0     # load average per CPU
        }
    
    def get_cpu_info(self) -> Dict:
        """Информация о CPU"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # Load average (Unix only)
        try:
            load_avg = os.getloadavg()
        except AttributeError:
            load_avg = (0, 0, 0)
        
        return {
            'usage_percent': cpu_percent,
            'cores': cpu_count,
            'frequency_mhz': cpu_freq.current if cpu_freq else 0,
            'load_avg_1m': load_avg[0],
            'load_avg_5m': load_avg[1],
            'load_avg_15m': load_avg[2],
            'alert': cpu_percent > self.alert_thresholds['cpu'] or load_avg[0] > self.alert_thresholds['load'] * cpu_count
        }
    
    def get_memory_info(self) -> Dict:
        """Информация о памяти"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total_gb': mem.total / (1024**3),
            'available_gb': mem.available / (1024**3),
            'used_gb': mem.used / (1024**3),
            'usage_percent': mem.percent,
            'swap_total_gb': swap.total / (1024**3),
            'swap_used_gb': swap.used / (1024**3),
            'swap_percent': swap.percent,
            'alert': mem.percent > self.alert_thresholds['ram']
        }
    
    def get_disk_info(self) -> Dict:
        """Информация о дисках"""
        partitions = []
        alerts = []
        
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                used_percent = (usage.used / usage.total) * 100
                
                partition_info = {
                    'device': part.device,
                    'mountpoint': part.mountpoint,
                    'fstype': part.fstype,
                    'total_gb': usage.total / (1024**3),
                    'used_gb': usage.used / (1024**3),
                    'free_gb': usage.free / (1024**3),
                    'usage_percent': used_percent
                }
                
                partitions.append(partition_info)
                
                if used_percent > self.alert_thresholds['disk']:
                    alerts.append(f"{part.mountpoint}: {used_percent:.1f}%")
                    
            except PermissionError:
                continue
        
        return {
            'partitions': partitions,
            'alerts': alerts,
            'alert': len(alerts) > 0
        }
    
    def get_network_info(self) -> Dict:
        """Информация о сети"""
        net_io = psutil.net_io_counters()
        net_stats = psutil.net_if_stats()
        
        interfaces = []
        for iface, stats in net_stats.items():
            interfaces.append({
                'name': iface,
                'is_up': stats.isup,
                'speed_mbps': stats.speed,
                'mtu': stats.mtu
            })
        
        return {
            'bytes_sent_mb': net_io.bytes_sent / (1024**2),
            'bytes_recv_mb': net_io.bytes_recv / (1024**2),
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'errors_in': net_io.errin,
            'errors_out': net_io.errout,
            'interfaces': interfaces
        }
    
    def get_system_info(self) -> Dict:
        """Общая информация о системе"""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        return {
            'hostname': os.uname().nodename,
            'platform': os.uname().sysname,
            'boot_time': boot_time.strftime('%Y-%m-%d %H:%M:%S'),
            'uptime_days': uptime.days,
            'uptime_hours': uptime.seconds // 3600,
            'uptime_minutes': (uptime.seconds % 3600) // 60
        }
    
    def get_full_report(self) -> Dict:
        """Полный отчёт о состоянии системы"""
        return {
            'timestamp': datetime.now().isoformat(),
            'system': self.get_system_info(),
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'disk': self.get_disk_info(),
            'network': self.get_network_info()
        }
    
    def print_report(self, report: Dict):
        """Выводит красивый отчёт"""
        sys_info = report['system']
        cpu = report['cpu']
        mem = report['memory']
        disk = report['disk']
        net = report['network']
        
        print(f"\n{'='*60}")
        print(f"🖥️  {sys_info['hostname']} | {sys_info['platform']}")
        print(f"⏱️  Uptime: {sys_info['uptime_days']}d {sys_info['uptime_hours']}h {sys_info['uptime_minutes']}m")
        print(f"{'='*60}")
        
        # CPU
        cpu_alert = "⚠️" if cpu['alert'] else "✅"
        print(f"\n{cpu_alert} CPU")
        print(f"   Usage: {cpu['usage_percent']:.1f}% ({cpu['cores']} cores)")
        print(f"   Load: {cpu['load_avg_1m']:.2f} (1m), {cpu['load_avg_5m']:.2f} (5m), {cpu['load_avg_15m']:.2f} (15m)")
        
        # Memory
        mem_alert = "⚠️" if mem['alert'] else "✅"
        print(f"\n{mem_alert} Memory")
        print(f"   Used: {mem['used_gb']:.1f} GB / {mem['total_gb']:.1f} GB ({mem['usage_percent']:.1f}%)")
        print(f"   Available: {mem['available_gb']:.1f} GB")
        if mem['swap_percent'] > 0:
            print(f"   Swap: {mem['swap_used_gb']:.1f} GB / {mem['swap_total_gb']:.1f} GB ({mem['swap_percent']:.1f}%)")
        
        # Disk
        disk_alert = "⚠️" if disk['alert'] else "✅"
        print(f"\n{disk_alert} Disk")
        for part in disk['partitions']:
            status = "⚠️" if part['usage_percent'] > 90 else "🟡" if part['usage_percent'] > 70 else "✅"
            print(f"   {status} {part['mountpoint']}: {part['used_gb']:.1f} / {part['total_gb']:.1f} GB ({part['usage_percent']:.1f}%)")
        
        # Network
        print(f"\n🌐 Network")
        print(f"   Sent: {net['bytes_sent_mb']:.1f} MB | Recv: {net['bytes_recv_mb']:.1f} MB")
        active_interfaces = [i for i in net['interfaces'] if i['is_up']]
        print(f"   Active interfaces: {len(active_interfaces)}")
        
        # Alerts summary
        alerts = []
        if cpu['alert']:
            alerts.append(f"CPU high ({cpu['usage_percent']:.1f}%)")
        if mem['alert']:
            alerts.append(f"Memory high ({mem['usage_percent']:.1f}%)")
        if disk['alert']:
            alerts.append(f"Disk full: {', '.join(disk['alerts'])}")
        
        if alerts:
            print(f"\n⚠️  ALERTS:")
            for alert in alerts:
                print(f"   - {alert}")
        else:
            print(f"\n✅ System healthy")
        
        print(f"\n{'='*60}")
    
    def watch(self, interval: int = 5, alerts_only: bool = False):
        """Режим наблюдения в реальном времени"""
        print(f"👁️  Monitoring started (interval: {interval}s, press Ctrl+C to stop)\n")
        
        try:
            while True:
                report = self.get_full_report()
                
                if alerts_only:
                    # Показываем только если есть алерты
                    has_alert = report['cpu']['alert'] or report['memory']['alert'] or report['disk']['alert']
                    if has_alert:
                        self.print_report(report)
                        print("\n" + "-"*60 + "\n")
                else:
                    self.print_report(report)
                    print("\n" + "-"*60 + "\n")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n👋 Monitoring stopped")
    
    def check_alerts(self) -> list:
        """Проверяет условия для алертов"""
        report = self.get_full_report()
        alerts = []
        
        if report['cpu']['alert']:
            alerts.append({
                'type': 'cpu',
                'message': f"CPU usage is {report['cpu']['usage_percent']:.1f}%",
                'severity': 'warning' if report['cpu']['usage_percent'] < 95 else 'critical'
            })
        
        if report['memory']['alert']:
            alerts.append({
                'type': 'memory',
                'message': f"Memory usage is {report['memory']['usage_percent']:.1f}%",
                'severity': 'warning' if report['memory']['usage_percent'] < 95 else 'critical'
            })
        
        if report['disk']['alert']:
            for alert in report['disk']['alerts']:
                alerts.append({
                    'type': 'disk',
                    'message': f"Disk space warning: {alert}",
                    'severity': 'critical'
                })
        
        return alerts
    
    def export_json(self, filename: Optional[str] = None):
        """Экспортирует отчёт в JSON"""
        report = self.get_full_report()
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"✅ Report exported to {filename}")
        else:
            print(json.dumps(report, indent=2))

def main():
    parser = argparse.ArgumentParser(description='Мониторинг сервера')
    parser.add_argument('--watch', '-w', action='store_true', help='Режим наблюдения')
    parser.add_argument('--interval', '-i', type=int, default=5, help='Интервал в секундах (default: 5)')
    parser.add_argument('--alerts-only', '-a', action='store_true', help='Показывать только алерты')
    parser.add_argument('--json', '-j', help='Экспортировать в JSON файл')
    parser.add_argument('--check', '-c', action='store_true', help='Одна проверка и выход')
    parser.add_argument('--threshold-cpu', type=int, default=80, help='Порог CPU (default: 80)')
    parser.add_argument('--threshold-ram', type=int, default=85, help='Порог RAM (default: 85)')
    parser.add_argument('--threshold-disk', type=int, default=90, help='Порог Disk (default: 90)')
    
    args = parser.parse_args()
    
    monitor = ServerMonitor()
    
    # Устанавливаем пороги
    monitor.alert_thresholds['cpu'] = args.threshold_cpu
    monitor.alert_thresholds['ram'] = args.threshold_ram
    monitor.alert_thresholds['disk'] = args.threshold_disk
    
    if args.watch:
        monitor.watch(interval=args.interval, alerts_only=args.alerts_only)
    elif args.json:
        monitor.export_json(args.json)
    elif args.check:
        report = monitor.get_full_report()
        monitor.print_report(report)
        
        # Exit code based on alerts
        alerts = monitor.check_alerts()
        if alerts:
            print(f"\n❌ {len(alerts)} alert(s) found")
            sys.exit(1)
        else:
            print("\n✅ No alerts")
            sys.exit(0)
    else:
        # По умолчанию - одна проверка
        report = monitor.get_full_report()
        monitor.print_report(report)

if __name__ == '__main__':
    import sys
    main()

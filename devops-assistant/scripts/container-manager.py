#!/usr/bin/env python3
"""
Container Manager - управление Docker контейнерами
Запуск, остановка, перезапуск, просмотр логов, мониторинг
"""

import argparse
import subprocess
import json
import sys
from datetime import datetime
from typing import List, Dict, Optional

class ContainerManager:
    """Менеджер Docker контейнеров"""
    
    def __init__(self):
        self.check_docker()
    
    def check_docker(self):
        """Проверяет, установлен ли Docker"""
        try:
            subprocess.run(['docker', '--version'], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Docker не установлен или недоступен")
            sys.exit(1)
    
    def run_command(self, cmd: List[str]) -> tuple:
        """Выполняет shell команду"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)
    
    def list_containers(self, all_containers: bool = False, format_table: bool = True) -> List[Dict]:
        """Показывает список контейнеров"""
        cmd = ['docker', 'ps']
        if all_containers:
            cmd.append('-a')
        
        # Формат JSON для парсинга
        cmd.extend(['--format', '{{json .}}'])
        
        returncode, stdout, stderr = self.run_command(cmd)
        
        if returncode != 0:
            print(f"❌ Ошибка: {stderr}")
            return []
        
        containers = []
        for line in stdout.strip().split('\n'):
            if line:
                try:
                    container = json.loads(line)
                    containers.append(container)
                except json.JSONDecodeError:
                    continue
        
        if format_table:
            self._print_containers_table(containers)
        
        return containers
    
    def _print_containers_table(self, containers: List[Dict]):
        """Выводит таблицу контейнеров"""
        if not containers:
            print("📭 Нет запущенных контейнеров")
            return
        
        print(f"\n{'🐳':<3} {'NAME':<25} {'STATUS':<15} {'PORTS':<30} {'IMAGE':<30}")
        print("-" * 110)
        
        for c in containers:
            name = c.get('Names', 'N/A')[:24]
            status = c.get('Status', 'N/A')[:14]
            ports = c.get('Ports', 'N/A')[:29]
            image = c.get('Image', 'N/A')[:29]
            
            # Эмодзи статуса
            status_emoji = '🟢' if 'Up' in status else '🔴' if 'Exited' in status else '⚪'
            
            print(f"{status_emoji:<3} {name:<25} {status:<15} {ports:<30} {image:<30}")
        
        print(f"\nВсего: {len(containers)} контейнеров")
    
    def get_container_info(self, container_name: str) -> Optional[Dict]:
        """Получает детальную информацию о контейнере"""
        cmd = ['docker', 'inspect', container_name]
        returncode, stdout, stderr = self.run_command(cmd)
        
        if returncode != 0:
            print(f"❌ Контейнер {container_name} не найден: {stderr}")
            return None
        
        try:
            info = json.loads(stdout)
            return info[0] if info else None
        except json.JSONDecodeError:
            return None
    
    def start_container(self, container_name: str) -> bool:
        """Запускает контейнер"""
        print(f"🚀 Запуск {container_name}...")
        cmd = ['docker', 'start', container_name]
        returncode, stdout, stderr = self.run_command(cmd)
        
        if returncode == 0:
            print(f"✅ Контейнер {container_name} запущен")
            return True
        else:
            print(f"❌ Ошибка запуска: {stderr}")
            return False
    
    def stop_container(self, container_name: str, timeout: int = 30) -> bool:
        """Останавливает контейнер"""
        print(f"🛑 Остановка {container_name}...")
        cmd = ['docker', 'stop', '-t', str(timeout), container_name]
        returncode, stdout, stderr = self.run_command(cmd)
        
        if returncode == 0:
            print(f"✅ Контейнер {container_name} остановлен")
            return True
        else:
            print(f"❌ Ошибка остановки: {stderr}")
            return False
    
    def restart_container(self, container_name: str) -> bool:
        """Перезапускает контейнер"""
        print(f"🔄 Перезапуск {container_name}...")
        cmd = ['docker', 'restart', container_name]
        returncode, stdout, stderr = self.run_command(cmd)
        
        if returncode == 0:
            print(f"✅ Контейнер {container_name} перезапущен")
            return True
        else:
            print(f"❌ Ошибка перезапуска: {stderr}")
            return False
    
    def get_logs(self, container_name: str, tail: int = 100, follow: bool = False, 
                 since: Optional[str] = None) -> str:
        """Получает логи контейнера"""
        cmd = ['docker', 'logs', '--tail', str(tail)]
        
        if follow:
            cmd.append('-f')
        
        if since:
            cmd.extend(['--since', since])
        
        cmd.append(container_name)
        
        if follow:
            # Для follow mode запускаем без capture_output
            print(f"📋 Логи {container_name} (Ctrl+C для выхода):\n")
            subprocess.run(cmd)
            return ""
        else:
            returncode, stdout, stderr = self.run_command(cmd)
            
            if returncode != 0:
                return f"❌ Ошибка: {stderr}"
            
            return stdout
    
    def get_stats(self, container_name: Optional[str] = None) -> List[Dict]:
        """Получает статистику использования ресурсов"""
        cmd = ['docker', 'stats', '--no-stream', '--format', '{{json .}}']
        
        if container_name:
            cmd.append(container_name)
        
        returncode, stdout, stderr = self.run_command(cmd)
        
        if returncode != 0:
            print(f"❌ Ошибка: {stderr}")
            return []
        
        stats = []
        for line in stdout.strip().split('\n'):
            if line:
                try:
                    stat = json.loads(line)
                    stats.append(stat)
                except json.JSONDecodeError:
                    continue
        
        return stats
    
    def print_stats(self, stats: List[Dict]):
        """Выводит статистику в табличном виде"""
        if not stats:
            return
        
        print(f"\n{'CONTAINER':<25} {'CPU %':<10} {'MEM USAGE':<20} {'MEM %':<10} {'NET I/O':<25}")
        print("-" * 95)
        
        for s in stats:
            name = s.get('Name', 'N/A')[:24]
            cpu = s.get('CPUPerc', 'N/A')[:9]
            mem = s.get('MemUsage', 'N/A')[:19]
            mem_perc = s.get('MemPerc', 'N/A')[:9]
            net = s.get('NetIO', 'N/A')[:24]
            
            print(f"{name:<25} {cpu:<10} {mem:<20} {mem_perc:<10} {net:<25}")
    
    def health_check(self, container_name: str) -> Dict:
        """Проверяет здоровье контейнера"""
        info = self.get_container_info(container_name)
        
        if not info:
            return {'healthy': False, 'error': 'Container not found'}
        
        state = info.get('State', {})
        
        health = {
            'name': container_name,
            'running': state.get('Running', False),
            'status': state.get('Status', 'unknown'),
            'healthy': state.get('Health', {}).get('Status') == 'healthy' if state.get('Health') else state.get('Running', False),
            'started_at': state.get('StartedAt', 'N/A'),
            'exit_code': state.get('ExitCode', 0),
            'error': state.get('Error', '')
        }
        
        return health
    
    def auto_restart_unhealthy(self) -> List[str]:
        """Автоматически перезапускает нездоровые контейнеры"""
        print("🔍 Проверка здоровья контейнеров...")
        
        containers = self.list_containers(all_containers=False, format_table=False)
        restarted = []
        
        for c in containers:
            name = c.get('Names', '')
            health = self.health_check(name)
            
            if not health['healthy'] and health['running']:
                print(f"⚠️  {name} нездоров, перезапуск...")
                if self.restart_container(name):
                    restarted.append(name)
        
        return restarted

def main():
    parser = argparse.ArgumentParser(description='Управление Docker контейнерами')
    parser.add_argument('--list', '-l', action='store_true', help='Список контейнеров')
    parser.add_argument('--list-all', '-la', action='store_true', help='Список всех контейнеров')
    parser.add_argument('--start', help='Запустить контейнер')
    parser.add_argument('--stop', help='Остановить контейнер')
    parser.add_argument('--restart', '-r', help='Перезапустить контейнер')
    parser.add_argument('--logs', help='Показать логи контейнера')
    parser.add_argument('--tail', type=int, default=100, help='Количество строк логов (default: 100)')
    parser.add_argument('--follow', '-f', action='store_true', help='Следить за логами в реальном времени')
    parser.add_argument('--stats', '-s', action='store_true', help='Показать статистику')
    parser.add_argument('--health', help='Проверить здоровье контейнера')
    parser.add_argument('--auto-heal', action='store_true', help='Автоматически перезапустить нездоровые')
    
    args = parser.parse_args()
    
    manager = ContainerManager()
    
    if args.list or args.list_all:
        manager.list_containers(all_containers=args.list_all)
    
    elif args.start:
        manager.start_container(args.start)
    
    elif args.stop:
        manager.stop_container(args.stop)
    
    elif args.restart:
        manager.restart_container(args.restart)
    
    elif args.logs:
        logs = manager.get_logs(args.logs, tail=args.tail, follow=args.follow)
        if not args.follow:
            print(logs)
    
    elif args.stats:
        stats = manager.get_stats()
        manager.print_stats(stats)
    
    elif args.health:
        health = manager.health_check(args.health)
        print(json.dumps(health, indent=2))
    
    elif args.auto_heal:
        restarted = manager.auto_restart_unhealthy()
        if restarted:
            print(f"\n🔄 Перезапущено контейнеров: {len(restarted)}")
            for name in restarted:
                print(f"  ✅ {name}")
        else:
            print("\n✅ Все контейнеры здоровы")
    
    else:
        # По умолчанию показываем список запущенных
        manager.list_containers()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Backup Automation - автоматизация бэкапов
Создаёт бэкапы баз данных и файлов с ротацией
"""

import argparse
import subprocess
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import json
import tarfile

class BackupAutomation:
    """Автоматизация бэкапов"""
    
    def __init__(self, backup_dir: str = '/backup'):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Подкатегории
        self.db_backup_dir = self.backup_dir / 'databases'
        self.files_backup_dir = self.backup_dir / 'files'
        self.db_backup_dir.mkdir(exist_ok=True)
        self.files_backup_dir.mkdir(exist_ok=True)
    
    def backup_postgres(self, db_name: str, user: str = 'postgres', 
                       host: str = 'localhost', port: int = 5432,
                       password: str = None) -> str:
        """Создаёт бэкап PostgreSQL базы"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{db_name}_{timestamp}.sql"
        filepath = self.db_backup_dir / filename
        
        # Формируем команду pg_dump
        env = os.environ.copy()
        if password:
            env['PGPASSWORD'] = password
        
        cmd = [
            'pg_dump',
            '-h', host,
            '-p', str(port),
            '-U', user,
            '-F', 'p',  # Plain text
            '-f', str(filepath),
            db_name
        ]
        
        print(f"🗄️  Creating backup of {db_name}...")
        
        try:
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Сжимаем
            compressed = f"{filepath}.gz"
            subprocess.run(['gzip', str(filepath)], check=True)
            
            size_mb = os.path.getsize(compressed) / (1024 * 1024)
            print(f"✅ Database backup created: {compressed} ({size_mb:.1f} MB)")
            
            return compressed
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Backup failed: {e.stderr}")
            return None
        except FileNotFoundError:
            print("❌ pg_dump not found. Install PostgreSQL client.")
            return None
    
    def backup_files(self, source_path: str, backup_name: str = None,
                    exclude_patterns: list = None) -> str:
        """Создаёт бэкап файловой директории"""
        source = Path(source_path)
        
        if not source.exists():
            print(f"❌ Source path does not exist: {source_path}")
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name = backup_name or source.name
        filename = f"{name}_{timestamp}.tar.gz"
        filepath = self.files_backup_dir / filename
        
        print(f"📦 Creating backup of {source_path}...")
        
        try:
            with tarfile.open(filepath, 'w:gz') as tar:
                tar.add(source, arcname=name)
            
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"✅ Files backup created: {filepath} ({size_mb:.1f} MB)")
            
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return None
    
    def backup_docker_volumes(self, volume_name: str = None) -> str:
        """Создаёт бэкап Docker volumes"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if volume_name:
            # Бэкап конкретного volume
            filename = f"docker_volume_{volume_name}_{timestamp}.tar.gz"
            volumes_to_backup = [volume_name]
        else:
            # Бэкап всех volumes
            filename = f"docker_volumes_{timestamp}.tar.gz"
            # Получаем список volumes
            result = subprocess.run(
                ['docker', 'volume', 'ls', '-q'],
                capture_output=True,
                text=True
            )
            volumes_to_backup = result.stdout.strip().split('\n')
        
        filepath = self.files_backup_dir / filename
        temp_dir = self.backup_dir / 'temp_volumes'
        temp_dir.mkdir(exist_ok=True)
        
        print(f"🐳 Creating backup of Docker volumes...")
        
        try:
            # Создаём временные tar для каждого volume
            for volume in volumes_to_backup:
                if not volume:
                    continue
                    
                volume_path = temp_dir / volume
                volume_path.mkdir(exist_ok=True)
                
                # Копируем данные через контейнер
                subprocess.run([
                    'docker', 'run', '--rm',
                    '-v', f'{volume}:/source:ro',
                    '-v', f'{volume_path}:/backup',
                    'alpine', 'cp', '-a', '/source/.', '/backup/'
                ], check=True, capture_output=True)
            
            # Архивируем всё
            with tarfile.open(filepath, 'w:gz') as tar:
                tar.add(temp_dir, arcname='volumes')
            
            # Очищаем временные файлы
            shutil.rmtree(temp_dir)
            
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"✅ Docker volumes backup created: {filepath} ({size_mb:.1f} MB)")
            
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            # Cleanup
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            return None
    
    def rotate_backups(self, pattern: str, keep_count: int = 7):
        """Удаляет старые бэкапы, оставляя только последние N"""
        print(f"🔄 Rotating backups (keeping last {keep_count})...")
        
        # Находим все бэкапы по паттерну
        backups = sorted(self.backup_dir.glob(pattern))
        
        if len(backups) <= keep_count:
            print(f"   Found {len(backups)} backups, nothing to delete")
            return
        
        to_delete = backups[:-keep_count]
        
        for backup in to_delete:
            try:
                if backup.is_file():
                    backup.unlink()
                    print(f"   🗑️  Deleted: {backup.name}")
                elif backup.is_dir():
                    shutil.rmtree(backup)
                    print(f"   🗑️  Deleted directory: {backup.name}")
            except Exception as e:
                print(f"   ❌ Failed to delete {backup}: {e}")
        
        print(f"✅ Rotation complete: deleted {len(to_delete)}, kept {keep_count}")
    
    def list_backups(self):
        """Показывает список всех бэкапов"""
        print(f"\n📋 Backup Inventory ({self.backup_dir})")
        print("=" * 70)
        
        # Database backups
        print("\n🗄️  Database Backups:")
        db_backups = sorted(self.db_backup_dir.glob('*.sql*'))
        if db_backups:
            for backup in db_backups[-10:]:  # Последние 10
                size_mb = os.path.getsize(backup) / (1024 * 1024)
                print(f"   {backup.name:<50} {size_mb:>8.1f} MB")
        else:
            print("   No database backups found")
        
        # File backups
        print("\n📦 File Backups:")
        file_backups = sorted(self.files_backup_dir.glob('*.tar.gz'))
        if file_backups:
            for backup in file_backups[-10:]:
                size_mb = os.path.getsize(backup) / (1024 * 1024)
                print(f"   {backup.name:<50} {size_mb:>8.1f} MB")
        else:
            print("   No file backups found")
        
        print("\n" + "=" * 70)
    
    def verify_backup(self, backup_path: str) -> bool:
        """Проверяет целостность бэкапа"""
        backup = Path(backup_path)
        
        if not backup.exists():
            print(f"❌ Backup not found: {backup_path}")
            return False
        
        print(f"🔍 Verifying backup: {backup.name}")
        
        try:
            if backup.suffix == '.gz' and '.sql' in backup.name:
                # Проверка SQL бэкапа
                result = subprocess.run(
                    ['gunzip', '-t', str(backup)],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print("✅ Database backup is valid")
                    return True
                    
            elif backup.suffix == '.gz' or '.tar' in backup.name:
                # Проверка tar архива
                with tarfile.open(backup, 'r:*') as tar:
                    tar.getmembers()
                print("✅ Archive backup is valid")
                return True
            
            print("✅ Backup file exists and is readable")
            return True
            
        except Exception as e:
            print(f"❌ Backup verification failed: {e}")
            return False
    
    def get_backup_info(self, backup_path: str) -> dict:
        """Получает информацию о бэкапе"""
        backup = Path(backup_path)
        
        if not backup.exists():
            return {'error': 'Backup not found'}
        
        stat = backup.stat()
        
        return {
            'path': str(backup),
            'name': backup.name,
            'size_mb': stat.st_size / (1024 * 1024),
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'type': 'database' if '.sql' in backup.name else 'files'
        }

def main():
    parser = argparse.ArgumentParser(description='Автоматизация бэкапов')
    parser.add_argument('--backup-dir', '-d', default='/backup', help='Директория для бэкапов')
    
    # Database backup
    parser.add_argument('--db', help='Имя PostgreSQL базы для бэкапа')
    parser.add_argument('--db-user', default='postgres', help='Пользователь БД')
    parser.add_argument('--db-host', default='localhost', help='Хост БД')
    parser.add_argument('--db-port', type=int, default=5432, help='Порт БД')
    
    # Files backup
    parser.add_argument('--files', help='Путь к директории для бэкапа')
    parser.add_argument('--backup-name', help='Имя бэкапа (если не указано - используется имя директории)')
    
    # Docker volumes
    parser.add_argument('--docker-volume', help='Имя Docker volume для бэкапа')
    parser.add_argument('--all-volumes', action='store_true', help='Бэкап всех Docker volumes')
    
    # Rotation
    parser.add_argument('--rotate', help='Паттерн для ротации (например: *.sql.gz)')
    parser.add_argument('--keep', type=int, default=7, help='Количество бэкапов для хранения')
    
    # Info
    parser.add_argument('--list', '-l', action='store_true', help='Показать список бэкапов')
    parser.add_argument('--verify', help='Проверить целостность бэкапа')
    parser.add_argument('--info', help='Информация о бэкапе')
    
    args = parser.parse_args()
    
    backup = BackupAutomation(args.backup_dir)
    
    if args.db:
        result = backup.backup_postgres(
            args.db,
            user=args.db_user,
            host=args.db_host,
            port=args.db_port
        )
        if result and args.rotate:
            backup.rotate_backups(f"{args.db}_*.sql.gz", args.keep)
    
    elif args.files:
        result = backup.backup_files(args.files, args.backup_name)
        if result and args.rotate:
            pattern = f"{args.backup_name or Path(args.files).name}_*.tar.gz"
            backup.rotate_backups(pattern, args.keep)
    
    elif args.docker_volume:
        result = backup.backup_docker_volumes(args.docker_volume)
    
    elif args.all_volumes:
        result = backup.backup_docker_volumes()
    
    elif args.rotate:
        backup.rotate_backups(args.rotate, args.keep)
    
    elif args.list:
        backup.list_backups()
    
    elif args.verify:
        backup.verify_backup(args.verify)
    
    elif args.info:
        info = backup.get_backup_info(args.info)
        print(json.dumps(info, indent=2))
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

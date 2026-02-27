from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess
import json
from datetime import datetime
from pathlib import Path

app = FastAPI(title="Deya Dashboard", version="1.0.0")

# Статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Шаблоны
templates = Jinja2Templates(directory="templates")

# Пути
WORKSPACE = Path("/root/.openclaw/workspace")
SKILLS_DIR = WORKSPACE / "skills"
MEMORY_DIR = WORKSPACE / "memory"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Главная страница - чат с Деей"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Deya Dashboard",
        "agent_name": "Deya",
        "status": "online"
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Дашборд со статистикой"""
    # Собираем статистику
    stats = {
        "skills_count": len([d for d in SKILLS_DIR.iterdir() if d.is_dir()]),
        "memory_files": len(list(MEMORY_DIR.glob("*.md"))),
        "today": datetime.now().strftime("%Y-%m-%d"),
        "status": "active"
    }
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "stats": stats
    })

@app.get("/skills", response_class=HTMLResponse)
async def skills_page(request: Request):
    """Страница управления скиллами"""
    skills = []
    
    for skill_dir in SKILLS_DIR.iterdir():
        if skill_dir.is_dir() and skill_dir.name != "__pycache__":
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                with open(skill_file) as f:
                    content = f.read()
                    # Извлекаем имя из первой строки
                    name = content.split('\n')[0].replace('# ', '').strip()
                    skills.append({
                        "name": name,
                        "folder": skill_dir.name,
                        "installed": True
                    })
    
    return templates.TemplateResponse("skills.html", {
        "request": request,
        "skills": skills
    })

@app.get("/api/skills")
async def api_skills():
    """API для списка скиллов (JSON)"""
    skills = []
    
    for skill_dir in SKILLS_DIR.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                skills.append({
                    "name": skill_dir.name,
                    "path": str(skill_dir)
                })
    
    return JSONResponse({"skills": skills})

@app.post("/api/skills/install")
async def install_skill(file: bytes = Form(...)):
    """Установка нового скилла"""
    # Сохраняем файл
    # Распаковываем
    # Проверяем SKILL.md
    return JSONResponse({"status": "installed"})

@app.get("/memory", response_class=HTMLResponse)
async def memory_page(request: Request):
    """Страница просмотра памяти"""
    memory_files = []
    
    for md_file in sorted(MEMORY_DIR.glob("*.md"), reverse=True):
        memory_files.append({
            "name": md_file.name,
            "date": md_file.stem,
            "size": md_file.stat().st_size
        })
    
    return templates.TemplateResponse("memory.html", {
        "request": request,
        "files": memory_files
    })

@app.get("/api/memory/{filename}")
async def get_memory(filename: str):
    """Получить содержимое файла памяти"""
    file_path = MEMORY_DIR / filename
    
    if file_path.exists() and file_path.suffix == ".md":
        with open(file_path) as f:
            content = f.read()
        return JSONResponse({"content": content})
    
    return JSONResponse({"error": "File not found"}, status_code=404)

@app.get("/channels", response_class=HTMLResponse)
async def channels_page(request: Request):
    """Управление каналами"""
    return templates.TemplateResponse("channels.html", {
        "request": request,
        "channels": [
            {"name": "@dayanrouter", "platform": "telegram", "status": "active"}
        ]
    })

@app.get("/tasks", response_class=HTMLResponse)
async def tasks_page(request: Request):
    """Задачи и cron"""
    # Получаем cron jobs
    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True
        )
        cron_jobs = result.stdout
    except:
        cron_jobs = "# No cron jobs"
    
    return templates.TemplateResponse("tasks.html", {
        "request": request,
        "cron_jobs": cron_jobs
    })

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """Настройки инстанса"""
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "config": {
            "model": "moonshot/kimi-k2.5",
            "timezone": "Europe/Berlin",
            "language": "ru"
        }
    })

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket для чата с Деей"""
    await websocket.accept()
    
    while True:
        try:
            # Получаем сообщение
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Тут будет интеграция с OpenClaw
            # Пока просто эхо
            response = {
                "role": "assistant",
                "content": f"Привет! Я Дея. Получила: {message.get('content', '')}",
                "timestamp": datetime.now().isoformat()
            }
            
            await websocket.send_json(response)
            
        except Exception as e:
            await websocket.send_json({"error": str(e)})
            break

@app.post("/api/execute")
async def execute_command(command: str = Form(...)):
    """Выполнить команду в системе"""
    try:
        # Ограничиваем команды для безопасности
        allowed_prefixes = ["openclaw", "python", "ls", "cat", "grep"]
        
        if not any(command.startswith(p) for p in allowed_prefixes):
            return JSONResponse({"error": "Command not allowed"}, status_code=403)
        
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(WORKSPACE)
        )
        
        return JSONResponse({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        })
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/memory", response_class=HTMLResponse)
async def memory_page(request: Request):
    """Страница памяти"""
    memory_files = []
    
    if MEMORY_DIR.exists():
        for md_file in sorted(MEMORY_DIR.glob("*.md"), reverse=True):
            stat = md_file.stat()
            memory_files.append({
                "name": md_file.name,
                "date": md_file.stem,
                "size": stat.st_size
            })
    
    return templates.TemplateResponse("memory.html", {
        "request": request,
        "files": memory_files
    })

@app.get("/channels", response_class=HTMLResponse)
async def channels_page(request: Request):
    """Страница каналов"""
    return templates.TemplateResponse("channels.html", {
        "request": request,
        "channels": [
            {"name": "@dayanrouter", "platform": "telegram", "status": "active"}
        ]
    })

@app.get("/tasks", response_class=HTMLResponse)
async def tasks_page(request: Request):
    """Страница задач"""
    # Получаем cron jobs
    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True
        )
        cron_jobs = result.stdout
    except:
        cron_jobs = "# No cron jobs configured"
    
    return templates.TemplateResponse("tasks.html", {
        "request": request,
        "cron_jobs": cron_jobs
    })

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """Страница настроек"""
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "config": {
            "model": "moonshot/kimi-k2.5",
            "timezone": "Europe/Berlin",
            "language": "ru"
        }
    })

@app.post("/api/settings")
async def save_settings(request: Request):
    """Сохранить настройки"""
    data = await request.json()
    # Сохранить в файл
    settings_file = WORKSPACE / "dashboard_settings.json"
    with open(settings_file, "w") as f:
        json.dump(data, f, indent=2)
    return JSONResponse({"status": "saved"})

@app.get("/api/settings")
async def get_settings():
    """Получить настройки"""
    settings_file = WORKSPACE / "dashboard_settings.json"
    if settings_file.exists():
        with open(settings_file) as f:
            return JSONResponse(json.load(f))
    return JSONResponse({
        "model": "moonshot/kimi-k2.5",
        "timezone": "Europe/Berlin",
        "language": "ru"
    })

@app.post("/api/channels/post")
async def create_post(request: Request):
    """Создать пост в Telegram"""
    data = await request.json()
    # Здесь будет интеграция с Telegram API
    return JSONResponse({"status": "posted", "text_preview": data.get("text", "")[:50]})

@app.delete("/api/skills/{skill_name}")
async def delete_skill(skill_name: str):
    """Удалить скилл"""
    skill_path = SKILLS_DIR / skill_name
    if skill_path.exists():
        import shutil
        shutil.rmtree(skill_path)
        return JSONResponse({"status": "deleted"})
    return JSONResponse({"error": "Skill not found"}, status_code=404)

@app.post("/api/memory/create")
async def create_memory(request: Request):
    """Создать файл памяти"""
    data = await request.json()
    filename = data.get("filename")
    content = data.get("content", "")
    
    if not filename:
        return JSONResponse({"error": "No filename"}, status_code=400)
    
    file_path = MEMORY_DIR / filename
    with open(file_path, "w") as f:
        f.write(content)
    
    return JSONResponse({"status": "created", "filename": filename})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

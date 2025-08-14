import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# 创建 FastAPI 应用实例
app = FastAPI()

# --- CORS 中间件 ---
# 这是非常重要的一步！
# 因为前端(localhost:5173)和后端(localhost:8000)在不同端口上运行，
# 浏览器默认会阻止跨域请求。这里我们允许来自前端的请求。
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 常量定义 ---
BASE_PATH = Path("./dataset")
TASKS = [f"task{i:03d}" for i in range(1, 401)]

# --- API 端点 (Endpoints) ---

@app.get("/api/tasks")
async def get_tasks_list():
    """
    提供所有可用任务的列表。
    前端可以通过访问 http://127.0.0.1:8000/api/tasks 来获取这个列表。
    """
    return {"tasks": TASKS}


@app.get("/api/tasks/{task_name}/{idx}")
async def get_task_data(task_name: str, idx: int):
    """
    提供特定任务中特定索引的样本数据。
    例如: http://127.0.0.1:8000/api/tasks/task001/0
    """
    if task_name not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found")

    file_path = BASE_PATH / f"{task_name}.json"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Data file for {task_name} not found.")

    with open(file_path, "r") as f:
        data = json.load(f)
    
    train_set = data.get("train", [])
    if not (0 <= idx < len(train_set)):
        raise HTTPException(status_code=404, detail=f"Index {idx} out of bounds for {task_name}.")

    return train_set[idx]
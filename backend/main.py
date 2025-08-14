import json
import random  # <--- 1. Import the 'random' module
# We no longer need Path or HTTPException for this endpoint
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- FastAPI App and CORS setup (no changes here) ---
app = FastAPI()

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

# --- Constants (no changes here) ---
TASKS = [f"task{i:03d}" for i in range(1, 401)]

# --- Helper Function for Data Generation ---

def generate_random_grid():
    """
    Generates a 2D grid with random dimensions and random cell values (0-9).
    """
    # 2. Define random height and width for the grid
    height = random.randint(3, 12)
    width = random.randint(3, 12)
    
    # 3. Create the grid using nested list comprehensions
    grid = [[random.randint(0, 9) for _ in range(width)] for _ in range(height)]
    return grid

# --- API Endpoints ---

@app.get("/api/tasks")
async def get_tasks_list():
    """
    Provides all available tasks. This endpoint remains unchanged.
    The frontend dropdown will still work as before.
    """
    return {"tasks": TASKS}


@app.get("/api/tasks/{task_name}/{idx}")
async def get_task_data(task_name: str, idx: int):
    """
    Generates and returns a random sample with 'input' and 'output' grids.
    
    NOTE: This function no longer depends on the 'dataset' folder.
    It ignores the task_name and idx parameters and returns new random data
    on every call. This is perfect for UI testing.
    """
    # 4. Generate a random grid for 'input'
    input_grid = generate_random_grid()
    
    # 5. Generate another random grid for 'output'
    output_grid = generate_random_grid()
    
    # 6. Return them in the expected JSON format
    return {"input": input_grid, "output": output_grid}
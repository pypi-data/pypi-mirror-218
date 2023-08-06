import os
import sys

sys.path.append(os.getcwd())
import shutil
import json
import time
import typer
import dotenv
from typing import Optional
from rich import print as rprint
from rich.progress import track


app = typer.Typer()

# Add the project directory to the Python path


def nice_progress(desc: str = "Doing stuff"):
    total = 0
    for _ in track(range(100), description=desc):
        time.sleep(0.001)
        total += 1


@app.command(name="create-project")
def create_project(project_name: str):
    """
    Create a new project directory with the given name.
    """
    # Create the project directory
    nice_progress(desc="Creating project directory :crystal_ball: ")
    os.makedirs(project_name)
    rprint(
        f"[bold green]Created project directory:[/bold green] :rocket: {project_name}"
    )

    # Create subdirectories
    subdirectories = ["routes", "handlers", "structure"]
    for directory in subdirectories:
        path = os.path.join(project_name, directory)
        os.makedirs(path)
        rprint(f"[bold green]Created directory:[/bold green] :fire: {path}")
        open(os.path.join(path, "__init__.py"), "w", encoding="utf-8").close()
        # Add __init__.py file

    # Create requirements.txt file
    requirements_file = os.path.join(project_name, "requirements.txt")
    with open(requirements_file, "w", encoding="utf-8") as f:
        f.write("fastapi[all]\n")
        f.write("python-dotenv\n")
    rprint(
        f"[bold green]Created requirements.txt file:[/bold green] :fire: {requirements_file}"
    )

    # Create main.py file
    main_file = os.path.join(project_name, "main.py")
    open(main_file, "w", encoding="utf-8").close()
    rprint(f"[bold green]Created main.py file:[/bold green] :fire: {main_file}")

    # Create .env file
    env_file = os.path.join(project_name, f"{project_name}.env")
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(f"""project_name={project_name}""")
    rprint(f"[bold green]Created .env file:[/bold green] :fire: {env_file}")

    # Add the subdirectories to the Python path
    for directory in subdirectories:
        sys.path.append(os.path.join(project_name, directory))
    rprint(
        f"[bold green]Added subdirectories to Python path:[/bold green] :fire: {subdirectories}"
    )


@app.command(name="create-route")
def create_route(project_name: str, route_name: str):
    nice_progress(desc="Creating route :crystal_ball: ")
    with open(
        os.path.join(project_name, "routes", f"{route_name}.py"), "w", encoding="utf-8"
    ) as f:
        f.write(f"""# Path: {project_name}\\routes\\{route_name}.py""")

    rprint(f"[bold green]Created route:[/bold green] :fire: {route_name}")


@app.command(name="create-handler")
def create_handler(project_name: str, handler_name: str):
    nice_progress(desc="Creating handler :crystal_ball: ")
    with open(
        os.path.join(project_name, "handlers", f"{handler_name}.py"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"""# Path: {project_name}\\handlers\\{handler_name}.py""")

    rprint(f"[bold green]Created handler:[/bold green] :fire: {handler_name}")


@app.command(name="create-structure")
def create_structure(project_name: str, structure_name: str):
    nice_progress(desc="Creating structure :crystal_ball: ")
    with open(
        os.path.join(project_name, "structure", f"{structure_name}.py"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"""# Path: {project_name}\\structure\\{structure_name}.py""")

    rprint(f"[bold green]Created structure:[/bold green] :fire: {structure_name}")


@app.command(name="delete-route")
def delete_route(project_name: str, route_name: str):
    nice_progress(desc="Deleting route :crystal_ball: ")
    os.remove(os.path.join(project_name, "routes", f"{route_name}.py"))
    rprint(f"[bold green]Deleted route:[/bold green] :fire: {route_name}")


@app.command(name="delete-handler")
def delete_handler(project_name: str, handler_name: str):
    nice_progress(desc="Deleting handler :crystal_ball: ")
    os.remove(os.path.join(project_name, "handlers", f"{handler_name}.py"))
    rprint(f"[bold green]Deleted handler:[/bold green] :fire: {handler_name}")


@app.command(name="delete-structure")
def delete_structure(project_name: str, structure_name: str):
    nice_progress(desc="Deleting structure :crystal_ball: ")
    os.remove(os.path.join(project_name, "structure", f"{structure_name}.py"))
    rprint(f"[bold green]Deleted structure:[/bold green] :fire: {structure_name}")


@app.command(name="add-dependency")
def add_dependency(project_name: str, dependency: str):
    """
    Add a dependency to the requirements.txt file.
    """
    # Add the dependency to the requirements.txt file
    nice_progress(desc="Adding dependency :crystal_ball: ")
    with open(
        os.path.join(project_name, "requirements.txt"), "a", encoding="utf-8"
    ) as f:
        f.write(f"{dependency}\n")
    rprint(
        f"[bold green]Added dependency to requirements.txt:[/bold green] :rocket: {dependency}"
    )


@app.command(name="remove-dependency")
def remove_dependency(project_name: str, dependency: str):
    """
    Remove a dependency from the requirements.txt file.
    """
    # Remove the dependency from the requirements.txt file
    nice_progress(desc="Removing dependency :crystal_ball: ")
    with open(
        os.path.join(project_name, "requirements.txt"), "r+", encoding="utf-8"
    ) as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            if line.strip("\n") != dependency:
                f.write(line)
        f.truncate()
    rprint(
        f"[bold green]Removed dependency from requirements.txt:[/bold green] :rocket: {dependency}"
    )


@app.command(name="add-subdirectory")
def add_subdirectory(project_name: str, subdirectory: str):
    """
    Add a subdirectory to the Python path.
    """
    # Add the subdirectory to the Python path
    nice_progress(desc="Adding subdirectory to Python path :crystal_ball: ")
    sys.path.append(os.path.join(project_name, subdirectory))
    rprint(
        f"[bold green]Added subdirectory to Python path:[/bold green] :rocket: {subdirectory}"
    )


@app.command(name="remove-subdirectory")
def remove_subdirectory(project_name: str, subdirectory: str):
    """
    Remove a subdirectory from the Python path.
    """
    # Remove the subdirectory from the Python path
    nice_progress(desc="Removing subdirectory from Python path :crystal_ball: ")
    sys.path.remove(os.path.join(project_name, subdirectory))
    rprint(
        f"[bold green]Removed subdirectory from Python path:[/bold green] :rocket: {subdirectory}"
    )


@app.command(name="add-environment-variable")
def add_environment_variable(project_name: str, variable: str):
    """
    Add an environment variable to the .env file.
    """
    # Add the environment variable to the .env file
    nice_progress(desc="Adding environment variable :crystal_ball: ")
    with open(os.path.join(project_name, ".env"), "a", encoding="utf-8") as f:
        f.write(f"{variable}\n")
    rprint(
        f"[bold green]Added environment variable to .env:[/bold green] :rocket: {variable}"
    )


@app.command(name="remove-environment-variable")
def remove_environment_variable(project_name: str, variable: str):
    """
    Remove an environment variable from the .env file.
    """
    # Remove the environment variable from the .env file
    nice_progress(desc="Removing environment variable :crystal_ball: ")
    with open(os.path.join(project_name, ".env"), "r+", encoding="utf-8") as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            if line.strip("\n") != variable:
                f.write(line)
        f.truncate()
    rprint(
        f"[bold green]Removed environment variable from .env:[/bold green] :rocket: {variable}"
    )


@app.command(name="sync")
def sync(project_name: str):
    """
    Impport the project's dependencies, subdirectories, and environment variables into main.py.
    """
    # Import the project's dependencies, subdirectories, and environment variables into main.py
    nice_progress(desc="Syncing project :crystal_ball: ")
    routes = os.listdir(os.path.join(project_name, "routes"))
    handlers = os.listdir(os.path.join(project_name, "handlers"))
    structure = os.listdir(os.path.join(project_name, "structure"))
    env_file = os.path.join(project_name, ".env")
    dotenv.load_dotenv(env_file)

    routes.remove("__init__.py")
    handlers.remove("__init__.py")
    structure.remove("__init__.py")

    with open(os.path.join(project_name, "main.py"), "w", encoding="utf-8") as f:
        if len(routes) > 0:
            f.write(
                f"from {project_name}.routes import {', '.join([route.split('.')[0] for route in routes])}\n"
            )
        elif len(handlers) > 0:
            f.write(
                f"from {project_name}.handlers import {', '.join([handler.split('.')[0] for handler in handlers])}\n"
            )
        elif len(structure) > 0:
            f.write(
                f"from {project_name}.structure import {', '.join([structure.split('.')[0] for structure in structure])}\n"
            )
        else:
            pass

        f.write("\n")
        f.write(
            f"""from fastapi import FastAPI
from dotenv import load_dotenv
import os

app = FastAPI()\n""")
        f.write("\n")
        f.write("load_dotenv('{project_name}.env')\n")
        f.write("env_test = os.getenv('{project_name}')\n\n")
        f.write("""
@app.get("/")
def read_root():
    return {"Hello": "World"}
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
        """
        )
    rprint("[bold green]Synced project:[/bold green] :rocket: ")

@app.command(name="delete-project")
def delete_project(project_name: str):
    """
    Delete the project directory with the given name.
    """
    # Delete the project directory
    nice_progress(desc="Deleting project directory :crystal_ball: ")
    shutil.rmtree(project_name)
    rprint(
        f"[bold green]Deleted project directory:[/bold green] :rocket: {project_name}"
    )


if __name__ == "__main__":
    app()

import os
from datetime import datetime

def create_folder(dir: str) -> None:
    print(os.path.exists(dir))
    if not os.path.exists(dir):
        try:
            os.mkdir(dir)
        except:
            raise Exception("ERROR - cannot create the folder")

def create_user(name: str, email: str, dir: str) -> None:
    print(os.path.exists(f"{dir}/{name}.md"))
    if not os.path.exists(f"{dir}/{name}.md"):
        try:
            create_folder(dir)
            with open(f"{dir}/{name}.md", "w") as f:
                f.write(f"| Name | Email |\n")
                f.write(f"| ---- | ----- |\n")
                f.write(f"| {name} | {email} |\n\n\n")
                f.write(f"| in | out | content |\n")
                f.write(f"| -- | --- | ------- |\n")
        except:
            raise Exception("ERROR - cannot create the user file")


def get_time() -> str:
    now = datetime.now()
    time, day = now.strftime("%H:%M:%S"), now.strftime("%Y-%m-%d")
    return f"{day}_{time}"

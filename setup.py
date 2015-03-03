import cx_Freeze

executables = [cx_Freeze.Executable("FlappyBird.py")]
cx_Freeze.setup(
    name="Flappy Bird",
    options={"build_exe": {"packages": ["pygame", "pymysql"], "include_files": ["bg.jpg"]}},
    description="Flappy Bird",
    version="1.9",
    executables=executables)

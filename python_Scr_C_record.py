import subprocess


def record():
    # Compile the C file
    compile_process = subprocess.run(["gcc", "-o", "record", "record.c", "-lasound"])
    if compile_process.returncode != 0:
        print("Compilation failed.")
        exit(1)

    # Run the compiled executable
    run_process = subprocess.run(["./record > output.raw"])
    if run_process.returncode != 0:
        print("Execution failed.")
        exit(1)

import subprocess

def run_git_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=r"c:\Users\Amari\immigration-aigent")
        return f"Command: {command}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}\nCode: {result.returncode}\n"
    except Exception as e:
        return f"Error running {command}: {str(e)}\n"

output = run_git_command("git status")
with open(r"c:\Users\Amari\immigration-aigent\git_status_check.txt", "w") as f:
    f.write(output)

print("Status captured.")

import subprocess


res = subprocess.run(['cargo', 'test'], cwd='../linked_list/src', capture_output=True, text=True)
print(res.stdout)
print("------   stderr   ------")
print(res.stderr)
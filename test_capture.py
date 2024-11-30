import subprocess
import json

# Run the cargo test command
result = subprocess.run(
    ['cargo', 'test', '--no-run', '--message-format=json'], 
    capture_output=True, 
    text=True
)

# Parse each JSON object from the output
for line in result.stdout.splitlines():
    try:
        # Parse the JSON line
        data = json.loads(line)
        
        # Check if it has an error code
        if data.get('reason') == 'compiler-message':
            message = data.get('message', {})
            code = message.get('code', {})
            if code:
                error_code = code.get('code', None)
                print(f"Error code: {error_code}")
    except json.JSONDecodeError:
        # Skip lines that are not valid JSON
        continue






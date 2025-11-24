from flask import Flask, jsonify, send_from_directory, request
import subprocess
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route("/generate", methods=["GET"])
def generate_text():
    try:    
        num_samples = request.args.get("num_samples", "1")
        dataset = request.args.get("out_dir", "out-movies")

        print(num_samples + "|" + dataset)

        result=subprocess.run(
            [
                sys.executable, "sample.py",
                f"--num_samples={num_samples}",
                f"--out_dir={dataset}"                
            ],
            capture_output=True,
            text=True
        )
        # print("STDOUT:", repr(result.stdout))
        # print("STDERR:", repr(result.stderr))
        # print("RETURN CODE:", result.returncode)

        return jsonify({
            "output": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        })
    except Exception as e:
        return jsonify({
            "output": str(e)
        })
    

if __name__ == "__main__":
    app.run(debug=True)


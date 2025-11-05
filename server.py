from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

namespace = {}

@app.route("/run", methods=["POST"])
def run_code():
    code_str = request.json.get("code", "")
    stdout = ""
    stderr = ""

    try:
        result = eval(code_str, namespace)
        if result is not None:
            stdout = str(result)
    except SyntaxError:
        try:
            exec(code_str, namespace)
        except Exception as e:
            stderr = str(e)
    except Exception as e:
        stderr = str(e)

    return jsonify({"stdout": stdout, "stderr": stderr})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

from NL2OPT import run_code, parse_execution_log

problem = "IndustryOR_21"
code_path = f"output2/{problem}_gencode.py"
data_path = f"output2/{problem}_instances.json"

def execute_code(code_path, data_path):
    execution_result = run_code(code_path, data_path)
    parsed_result = parse_execution_log(execution_result["log"])
    return parsed_result

if __name__ == "__main__":
    parsed_result = execute_code(code_path, data_path)
    print(f"결과: {parsed_result}")
    
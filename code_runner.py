from NL2OPT import run_code, parse_execution_log

problem = "IndustryOR_21"
code_path = f"output2/{problem}_gencode.py"
data_path = f"output2/{problem}_instances.json"

if __name__ == "__main__":
    execution_result = run_code(code_path, data_path)
    parsed_result = parse_execution_log(execution_result["log"])
    print(f"결과: {parsed_result}")
    
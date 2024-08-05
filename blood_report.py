from langchain_community.document_loaders import PyMuPDFLoader
import pymupdf4llm
from llm import llm
from utils import parse_float
from prompts import (
    extract_blood_test_prompt,
    convert_unit_prompt,
    blood_test_answer_prompt,
    base_structure,
    base_structure_male,
    base_structure_female,
)
import json

def analyze_blood_report(file_path, gender):
    llm_input_token_count = 0
    llm_output_token_count = 0

    # Read blood report content
    read_blood_report_result = read_blood_report(file_path)
    llm_input_token_count += read_blood_report_result["usage"].get("input_tokens", 0)
    llm_output_token_count += read_blood_report_result["usage"].get("output_tokens", 0)
    if read_blood_report_result["invalid_response"]:
        return read_blood_report_result["content"]
    report = read_blood_report_result["content"]

    # Standardize blood report to have same unit as the base structure
    standardize_report_response = standardize_blood_report(report)
    standardized_report = standardize_report_response["standardized_blood_test_json"]
    llm_input_token_count += standardize_report_response["usage"].get("input_tokens", 0)
    llm_output_token_count += standardize_report_response["usage"].get(
        "output_tokens", 0
    )

    # Collect reasons for each test
    derived_reasons = collect_reasons(standardized_report, gender)

    # Generate answer
    llm_answer_response = generate_llm_answer(derived_reasons)
    llm_input_token_count += llm_answer_response["usage"].get("input_tokens", 0)
    llm_output_token_count += llm_answer_response["usage"].get("output_tokens", 0)

    return llm_answer_response["content"]


def read_blood_report(file_path):
    blood_report_text = pymupdf4llm.to_markdown(file_path)
    _extract_blood_test_prompt = extract_blood_test_prompt + "\n" + blood_report_text
    blood_test_read_response = llm.invoke(_extract_blood_test_prompt)
    invalid_response = False
    try:
        json.loads(
            blood_test_read_response.content.replace("```json", "").replace("```", "")
        )
    except json.JSONDecodeError:
        invalid_response = True

    return {
        "content": blood_test_read_response.content,
        "usage": blood_test_read_response.usage_metadata,
        "invalid_response": invalid_response,
    }


def standardize_blood_report(report):
    _convert_unit_prompt = convert_unit_prompt + "\n" + report
    conversion_response = llm.invoke(_convert_unit_prompt)
    standardized_blood_test_json = json.loads(
        conversion_response.content.replace("```json", "").replace("```", "")
    )

    return {
        "standardized_blood_test_json": standardized_blood_test_json,
        "usage": conversion_response.usage_metadata,
    }


def collect_reasons(standardized_blood_test_json, gender):
    reasons = {}
    _base_structure = base_structure
    if gender == "Male":
        _base_structure.update(base_structure_male)
    else:
        _base_structure.update(base_structure_female)
        
    print('base:', _base_structure)
    print('json:', standardized_blood_test_json)

    for test_name, test_value in standardized_blood_test_json.items():
        if test_name in _base_structure:
            if test_value["value"] is not None and _base_structure[test_name]["upper_limit"] is not None and _base_structure[test_name]["lower_limit"] is not None:
                test_value_number = parse_float(test_value["value"])
                upper_limit_value = parse_float(
                    _base_structure[test_name]["upper_limit"]
                )
                lower_limit_value = parse_float(
                    _base_structure[test_name]["lower_limit"]
                )                
                if test_value_number is None or (
                    upper_limit_value is None or lower_limit_value is None
                ):
                    continue

                if (
                    _base_structure[test_name]["reasons_low"] is not None
                    and test_value_number < lower_limit_value
                ):
                    reasons[test_name] = {
                        "reason": _base_structure[test_name]["reasons_low"],
                        "value": test_value_number,
                        "analysis": "low",
                    }
                elif (
                    _base_structure[test_name]["reasons_high"] is not None
                    and test_value_number > upper_limit_value
                ):
                    reasons[test_name] = {
                        "reason": _base_structure[test_name]["reasons_high"],
                        "value": test_value_number,
                        "analysis": "high",
                    }
    return reasons


def generate_llm_answer(reasons):
    _blood_test_answer_prompt = blood_test_answer_prompt + json.dumps(reasons)
    blood_test_answer_response = llm.invoke(_blood_test_answer_prompt)
    return {
        "content": blood_test_answer_response.content,
        "usage": blood_test_answer_response.usage_metadata,
    }

from langchain_community.document_loaders import PyMuPDFLoader
import pymupdf4llm
from llm import llm
from utils import parse_float
import json

convert_unit_prompt = """
You are an excellent doctor and you understand all the unit conversion formula in blood test report. Help me to convert the blood test report in JSON to the same unit and according value as the base structure below:
"Haemoglobin (HGB)","g/L"
"Red Blood Cells","x10(12)/L"
"Haematocrit (HCT)","L/L"
"Mean Cell Volume (MCV)","fl"
"Red Cell Distribution Width (RDW)","%"
"Mean Cell Haemoglobin (MCH)","pg"
"MCHC","g/L"
"Platelets","x10(9)/L"
"Platelet Volume (MPV)","fl"
"Fibrinogen",""
"White Blood Cells","x10(9)/L"
"Neutrophils","x10(9)/L"
"Monocytes","x10(9)/L"
"Basophils","x10(9)/L"
"Eosinophils","x10(9)/L"
"Lymphocytes","x10(9)/L"
"Ferritin","ug/L"
"Calcium","mmol/L"
"Glucose",""
"Glycomark",""
"Globulin","g/L"
"Albumin","g/L"
"Creatine Kinase (CK)","IU/L"
"C-Reactive Protein (CRP)","mg/L"
"Homocysteine",""
"ESR",""
"Total Protein","g/L"
"HbA1c","mmol/mol"
"Iron","umol/L"
"T.I.B.C","umol/L"
"Transferin Saturation","%"
"Transferin",""
"Cystatin C",""
"Sodium","mmol/mol"
"Potassium","mmol/mol"
"Fructosamine",""
"Stress response",""
"Chloride",""
"Urea","mmol/mol"
"Phosphate/Phosphorus",""
"Creatinine","umol/L"
"eGFR(MDRD)(Caucasian only)","ml/min/1.73m2"
"Anion cap",""
"AST","UL/L"
"Alk Phosphatase (ALP)","IU/L"
"Alanine Transaminase (ALT)","IU/L"
"Gamma-Glutamyl Transferase (GGT)","IU/L"
"Blood Urea Nitrogen (BUN)",""
"Total Bilirubin","umol/L"
"Lactase dehydrogenase (LDH)",""
"Uric Acid","umol/L"
"Cholesterol","mmol/L"
"HDL","mmol/L"
"LDL","mmol/L"
"Triglycerides","mmol/L"
"Non HDL Cholesterol","mmol/L"
"Chol:HDL ratio","ratio"
"Cortisol (Random)","nmol/L"
"Testosterone","nmol/L"
"Free-Testosterone (Calculated)","nmol/L"
"Prolactin","mU/L"
"Oestradiol","IU/L"
"Progesterone","nmol/L"
"LH","IU/L"
"FSH","IU/L"
"DHEA-Sulphate","nmol/L"
"Sex Hormone Binding Globulin (SHBG)","nmol/L"
"Fasting Insulin",""
"TSH","mIU/L"
"Free T4 (Thyroxine)","pmol/L"
"Free T3 (Triiodothyronine)","pmol/L"
"RT3",""
"Total PSA","ng/mL"
"Anti-Thyroidperoxidase abs","kIU/L"
"Anti-Thyroglobulin abs","kIU/L"
"Vitamin D (25 OH)","nmol/L"
"Magnesium",""
"B12-Active","pmol/L"
"Folate","ng/mL"

Keep the answer in JSON format same as the input blood test report, just only change the unit if it is different from the base structure and according value after conversion.
Any unit conversion that you are not sure, please leave it as is, never make up the formula.
Answer structure: {<test_name>: {unit: <unit>, value: <value>}}
Example answer: {"Haemoglobin (HGB)": {unit: "g/L", value: "140"},...}

Don't need to explain the answer, just return the answer in JSON format.
"""

extract_blood_test_prompt = """
You are an excellent blood test report reader. I will provide you a blood test report and you will find all the test cases in the report. Extract the test name, its result, and its unit.
The test name can be different across each report, so use your perfect knowledge to map to the listed name as I provided below. You will only extract the tests that exist in the blood test report and are also listed below:
"Haemoglobin (HGB)", "Red Blood Cells", "Haematocrit (HCT)", "Mean Cell Volume (MCV)", "Red Cell Distribution Width (RDW)", "Mean Cell Haemoglobin (MCH)", "MCHC", "Platelets", "Platelet Volume (MPV)", "Fibrinogen", "White Blood Cells", "Neutrophils", "Monocytes", "Basophils", "Eosinophils", "Lymphocytes", "Ferritin", "Calcium", "Glucose", "Glycomark", "Globulin", "Albumin", "Creatine Kinase (CK)", "C-Reactive Protein (CRP)", "Homocysteine", "ESR", "Total Protein", "HbA1c", "Iron", "T.I.B.C", "Transferin Saturation", "Transferin", "Cystatin C", "Sodium", "Potassium", "Fructosamine", "Stress response", "Chloride", "Urea", "Phosphate/Phosphorus", "Creatinine", "eGFR(MDRD)(Caucasian only)", "Anion cap", "AST", "Alk Phosphatase (ALP)", "Alanine Transaminase (ALT)", "Gamma-Glutamyl Transferase (GGT)", "Blood Urea Nitrogen (BUN)", "Total Bilirubin", "Lactase dehydrogenase (LDH)", "Uric Acid", "Cholesterol", "HDL", "LDL", "Triglycerides", "Non HDL Cholesterol", "Chol:HDL ratio", "Cortisol (Random)", "Testosterone", "Free-Testosterone (Calculated)", "Prolactin", "Oestradiol", "Progesterone", "LH", "FSH", "DHEA-Sulphate", "Sex Hormone Binding Globulin (SHBG)", "Fasting Insulin", "TSH", "Free T4 (Thyroxine)", "Free T3 (Triiodothyronine)", "RT3", "Total PSA", "Anti-Thyroidperoxidase abs", "Anti-Thyroglobulin abs", "Vitamin D (25 OH)", "Magnesium", "B12-Active", "Folate"
Here is the blood test report:
"""

base_structure = {
    "Haemoglobin (HGB)": {
        "upper_limit": "150",
        "lower_limit": "140",
        "reasons_high": "Dehydration, respiratory disease, polycythaemia, smoking, high altitude, blood clot, lung disease",
        "reasons_low": "Anaemia, Iron deficiency, Vitamin B9 or B12 deficiency, inherited haemoglobin defects, Cirrhosis of liver, bleeding or haemorrhage, kidney disease, heavy period",
    },
    "Red Blood Cells": {
        "upper_limit": "5.5",
        "lower_limit": "4.8",
        "reasons_high": "Dehydration, Severe Diarrhoea, Kidney disease, pulmonary fibrosis, polycythaemia, medications: gentamicin, methyldopa, low oxygen levels, heart or lung disease",
        "reasons_low": "Anaemia, Blood loss, repeated infections, congestive heart failure, anorexia, haemorrhage, autoimmune disease, chronic kidney disease",
    },
    "Haematocrit (HCT)": {
        "upper_limit": "0.47",
        "lower_limit": "0.35",
        "reasons_high": "Dehydration, smoking, respiratory disease, high altitude, overproduction of red blood cells, spleen hypofunction, exogenous testosterone, sleep apnoea",
        "reasons_low": "Digestive inflammation, blood loss, destruction of red blood cells, decreased red blood cell production, low immunity (thymus hypofunction), inadequate protein intake or absorption, nutrient deficiency: iron, vitamin B6, B9, B12, C, Copper, Manganese, or iodine",
    },
    "Mean Cell Volume (MCV)": {
        "upper_limit": "89",
        "lower_limit": "85",
        "reasons_high": "Macrocytic anaemia, pernicious anaemia, vitamin B9 or B12 deficiency, alcoholism, low stomach acid, gluten intolerance, dysbiosis, bacterial overgrowth",
        "reasons_low": "Microcytic anaemia, iron deficiency, thalassemia, internal bleeding, coeliac disease, gluten intolerance, dysbiosis, bacterial overgrowth, B6 deficiency",
    },
    "Red Cell Distribution Width (RDW)": {
        "upper_limit": "13",
        "lower_limit": "12",
        "reasons_high": "Elevated homocystiene, low stomach acid, gluten sensitivity, poor glutathione status, mercury toxicity, nutrient deficiency: Iron, B9, B12, pernicious anaemia",
        "reasons_low": "Acute or chronic bacterial infection, inflammation, heavy periods, childhood disease (measles, mumps, etc.)",
    },
    "Mean Cell Haemoglobin (MCH)": {
        "upper_limit": "31.9",
        "lower_limit": "28",
        "reasons_high": "Macrocytic anaemia, vitamin B9 or B12 deficiency, low stomach acid, gluten intolerance, leaky gut, IBS, coeliac disease",
        "reasons_low": "Microcytic anaemia, iron deficiency, blood loss (internal bleeding), Vitamin B6, C, or K deficiency, coeliac disease, leaky gut, imbalanced gut flora, heavy metals",
    },
    "MCHC": {
        "upper_limit": "350",
        "lower_limit": "330",
        "reasons_high": "Hyperchromia, low stomach acid, early stage autoimmunity, chronic obstructive pulmonary disease, nutrient deficiencies: B9, B12, high lipids = false elevations. Medications: antibiotics, ibuprofen, paracetamol, or interferon",
        "reasons_low": "Hypochromia, Thalassaemia, heavy metals, heavy periods, nutrient deficiencies: Iron, B6, or C",
    },
    "Platelets": {
        "upper_limit": "275",
        "lower_limit": "225",
        "reasons_high": "Thrombocytosis, atherosclerosis, poor spleen function, chronic inflammation, nutrient deficiencies: magnesium, omega 3, or vitamin E, stroke, cardiovascular disease… (jabbed)",
        "reasons_low": "Leukaemia, liver disease, systemic virus or bacterial infections, immune system dysfunction, idiopathic thrombocytopenia, heavy metals, Alzheimer's disease, medication: heparin, quinine, valproic acid",
    },
    "Platelet Volume (MPV)": {
        "upper_limit": "9.5",
        "lower_limit": "8.5",
        "reasons_high": "Vitamin D deficiency, obesity, thyroid disorders",
        "reasons_low": "Inflammatory disease, impaired bone marrow function",
    },
    "White Blood Cells": {
        "upper_limit": "7.5",
        "lower_limit": "5.5",
        "reasons_high": "Active infection, inflammatory response, stress, allergies, recent exercise, high refined carbohydrate diet, intestinal parasites, asthma",
        "reasons_low": "Chronic infection, immunosuppression, compromised immunity, autoimmune disease, bone marrow failure or cancer, liver or spleen disease, poor protein intake, poor protein absorption",
    },
    "Neutrophils": {
        "upper_limit": "60",
        "lower_limit": "40",
        "reasons_high": "Chronic bacterial infection, asthma, emphysema, late stages of pregnancy, recent exercise, stress, extreme cold or heat, intestinal parasites",
        "reasons_low": "Hepatitis, rheumatoid arthritis, parathyroid hyperfunction, exposure to certain carcinogens, poor infection resistance, protein deficiency, nutrient deficiencies: Zinc, or Vitamin C. Mononucleosis",
    },
    "Monocytes": {
        "upper_limit": "7",
        "lower_limit": "0",
        "reasons_high": "Bacteria or viral infection, recovery phase of infection, chronic inflammation, muscle wasting, liver dysfunction, intestinal parasites, congestion in the urinary tract",
        "reasons_low": "Bone marrow disease, HIV/AIDS, Autoimmune disease, corticosteroid therapy, Nutrient deficiencies: B12 OR B9",
    },
    "Basophils": {
        "upper_limit": "1",
        "lower_limit": "0",
        "reasons_high": "Severe food allergy, inflammation, Leukaemia, splenectomy, chronic sinus infection, asthma, eczema, hypothyroidism",
        "reasons_low": None,
    },
    "Eosinophils": {
        "upper_limit": "3",
        "lower_limit": "0",
        "reasons_high": "Parasitic infection, attempt to detoxify through the skin, inflammatory bowel disease, adrenal dysfunction, food allergies and sensitivities, hyperthyroidism, Asthma, dermatitis",
        "reasons_low": None,
    },
    "Lymphocytes": {
        "upper_limit": "1.1",
        "lower_limit": "3.1",
        "reasons_high": "Infections, autoimmune disorders, cancer of lymphatic system or blood, late stages of pregnancy, poor detoxification capacity, adrenal fatigue, viral infection, systemic toxicity",
        "reasons_low": "Immunosuppressant drugs, hepatitis, rheumatoid arthritis, chronic viral infection, poor defense against viruses and cancer, chronic inflammation, heavy metal toxicity, connective tissue breakdown",
    },
    "Ferritin": {
        "upper_limit": "100",
        "lower_limit": "50",
        "reasons_high": "Liver disease, inflammation, hemochromatosis, chronic infection, autoimmune disease, recent blood transfusions, cancer",
        "reasons_low": "Iron deficiency, poor protein intake, low stomach acid, poorly controlled celiac disease, gluten intolerance, leaky gut, food allergies, sugar cravings",
    },
    "Calcium": {
        "upper_limit": "2.6",
        "lower_limit": "2.4",
        "reasons_high": None,
        "reasons_low": None,
    },
    "Glucose": {
        "upper_limit": "4.9",
        "lower_limit": "4.3",
        "reasons_high": None,
        "reasons_low": None,
    },
    "Globulin": {
        "upper_limit": "28",
        "lower_limit": "24",
        "reasons_high": "Hypochlorhydria, liver cell damage, oxidative stress, heavy metal toxicity, chronic inflammation or infection, autoimmune disease",
        "reasons_low": "Digestive dysfunction, digestive inflammation (such as IBD), immune insufficiency",
    },
    "Albumin": {
        "upper_limit": "45",
        "lower_limit": "40",
        "reasons_high": "Dehydration, anabolic steroid use, growth hormone, insulin",
        "reasons_low": "Hypochlorhydria, liver dysfunction, oxidative stress, vitamin C deficiency, acute infection, kidney dysfunction, pregnancy, impaired protein synthesis, malabsorption, Crohn's disease, coeliac",
    },
    "Creatine Kinase (CK)": {
        "upper_limit": "135",
        "lower_limit": "65",
        "reasons_high": "Exercise/overtraining, obesity, medications, drugs/toxins",
        "reasons_low": "Catabolic/low muscle mass, autoimmune, pregnant",
    },
    "C-Reactive Protein (CRP)": {
        "upper_limit": "0.55",
        "lower_limit": "0",
        "reasons_high": "Chronic fatigue syndrome, autoimmune disease, obesity, cardiovascular risk, stress, poor diet, physical inactivity",
        "reasons_low": None,
    },
    "TSH": {
        "upper_limit": "5.6",
        "lower_limit": "0.5",
        "reasons_high": "Hypothyroidism, Hashimoto’s disease, iodine deficiency, stress, poor diet, heavy metal toxicity, medication side effects",
        "reasons_low": "Hyperthyroidism, thyroiditis, excessive iodine intake, Graves’ disease, thyroid nodules, thyroid cancer",
    },
    "Free T4": {
        "upper_limit": "22",
        "lower_limit": "11",
        "reasons_high": "Hyperthyroidism, excessive iodine intake, medication side effects, stress",
        "reasons_low": "Hypothyroidism, iodine deficiency, thyroiditis, medication side effects, pituitary dysfunction",
    },
    "Free T3": {
        "upper_limit": "6.2",
        "lower_limit": "3.5",
        "reasons_high": "Hyperthyroidism, excessive iodine intake, medication side effects, stress",
        "reasons_low": "Hypothyroidism, iodine deficiency, thyroiditis, medication side effects, pituitary dysfunction",
    },
    "Testosterone": {
        "upper_limit": "27",
        "lower_limit": "10",
        "reasons_high": "Testosterone therapy, anabolic steroid use, conditions causing excess testosterone production",
        "reasons_low": "Hypogonadism, pituitary dysfunction, chronic illness, stress, medication side effects, excessive physical exercise",
    },
    "Vitamin D": {
        "upper_limit": "90",
        "lower_limit": "50",
        "reasons_high": "Supplementation overdose, excessive sun exposure",
        "reasons_low": "Deficiency, inadequate sunlight exposure, poor dietary intake, malabsorption",
    },
    "Vitamin B12": {
        "upper_limit": "700",
        "lower_limit": "250",
        "reasons_high": "Supplementation, liver disease",
        "reasons_low": "Deficiency, pernicious anaemia, malabsorption, certain medications",
    },
    "Folate": {
        "upper_limit": "45",
        "lower_limit": "20",
        "reasons_high": "Supplementation, liver disease",
        "reasons_low": "Deficiency, malabsorption, certain medications",
    },
}

blood_test_answer_prompt = """
After I submitted the blood test report to analyze, I asked doctor to provide the reasons and analysis of the test results. And he gave me the reasons and analysis in JSON format.
You help me to understand and summarize for me in layman language.
Here is the reasons and analysis:
"""


def analyze_blood_report(file_path):
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
    derived_reasons = collect_reasons(standardized_report)

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


def collect_reasons(standardized_blood_test_json):
    reasons = {}
    for test_name, test_value in standardized_blood_test_json.items():
        if test_name in base_structure:
            if test_value["value"] is not None:
                test_value_number = parse_float(test_value["value"])
                upper_limit_value = parse_float(
                    base_structure[test_name]["upper_limit"]
                )
                lower_limit_value = parse_float(
                    base_structure[test_name]["lower_limit"]
                )
                if test_value_number is None or (
                    upper_limit_value is None or lower_limit_value is None
                ):
                    continue

                if (
                    base_structure[test_name]["reasons_low"] is not None
                    and test_value_number < lower_limit_value
                ):
                    reasons[test_name] = {
                        "reason": base_structure[test_name]["reasons_low"],
                        "value": test_value_number,
                        "analysis": "low",
                    }
                elif (
                    base_structure[test_name]["reasons_high"] is not None
                    and test_value_number > upper_limit_value
                ):
                    reasons[test_name] = {
                        "reason": base_structure[test_name]["reasons_high"],
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

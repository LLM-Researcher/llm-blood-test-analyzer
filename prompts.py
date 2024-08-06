convert_unit_prompt = """
You are an excellent doctor and you understand all the unit conversion formula in blood test report. Help me to convert the blood test report in JSON to the same unit and according value as the base structure below:
Haemoglobin (HGB) - g/L
Homocysteine - umol/L
Red Blood Cells - x10(12)/L
Haematocrit (HCT) - L/L
Mean Cell Volume (MCV) - fl
Red Cell Distribution Width (RDW) - %
Mean Cell Haemoglobin (MCH) - pg
MCHC - g/L
Platelets - x10(9)/L
Platelet Volume (MPV) - fl
White Blood Cells - x10(9)/L
Neutrophils - x10(9)/L
Lymphocytes - x10(9)/L
Monocytes - x10(9)/L
Basophils - x10(9)/L
Eosinophils - x10(9)/L
Ferritin - ug/L
Calcium - mmol/L
Insulin (fasting) - mU/L
Glucose - mmol/L
HOMA - IR Score - ratio
ESR - mg/L
Globulin - g/L
Albumin - g/L
Creatine Kinase (CK) - IU/L
C-Reactive Protein (CRP) - mg/L
Total Protein - g/L
HbA1c-(IFCC) - mmol/mol
Iron - umol/L
Transferrin - g/L
Transferrin Saturation - %
T.I.B.C - umol/L
Cystatin C - mg/L
Sodium - mmol/mol
Potassium - mmol/mol
Chloride - mmol/L
Phosphorus - mmol/L
Urea / BUN - mmol/mol
Creatinine - umol/L
eGFR(MDRD)(Caucasian only) - ml/min/1.73m2
AST - UL/L
Alanine Transaminase (ALT) - IU/L
Gamma-Glutamyl Transferase (GGT) - IU/L
LDH - IU/L
Total Bilirubin - umol/L
Alk Phosphatase (ALP) - IU/L
Uric Acid - umol/L
Cholesterol - mmol/L
HDL - mmol/L
LDL - mmol/L
Triglycerides - mmol/L
Chol:HDL ratio - ratio
Non HDL Cholesterol - mmol/L
Cortisol (Random) - nmol/L
Testosterone - nmol/L
Free-Testosterone (Calculated) - nmol/L
Prolactin - mU/L
Oestradiol - IU/L
Progesterone - nmol/L
LH - IU/L
FSH - IU/L
DHEA-Sulphate - umol/L
Sex Hormone Binding Globulin (SHBG) - nmol/L
TSH - mU/L
Free T4 (Thyroxine) - pmol/L
Free T3 (Triiodothyronine) - pmol/L
Total PSA - ng/mL
Anti-Thyroglobulin abs - kIU/L
Anti-Thyroidperoxidase abs - kIU/L
Vitamin D (25 OH) - nmol/L
B12-Active - pmol/L
Serum Folate - ng/mL
Folate - ng/mL
Magnesium - mmol/L

Keep the answer in JSON format same as the input blood test report, just only change the unit if it is different from the base structure and according value after conversion.
Any unit conversion that you are not sure, please leave it as is, never make up the formula.
Answer structure: {<test_name>: {unit: <unit>, value: <value>}}
Example answer: {"Haemoglobin (HGB)": {unit: "g/L", value: "140"},"Homocysteine": {unit: "umol/L", value: "30"}}

Never change the answer structure or format. Don't need to explain the answer, just return the answer in JSON format.
"""

extract_blood_test_prompt = """
You are an excellent blood test report reader. I will provide you a blood test report and you will find all the test cases in the report. Extract the test name, its result, and its unit.
The test name can be different across each report, so use your perfect knowledge to map to the listed name as I provided below. You will only extract the tests that exist in the blood test report and are also listed below:
Haemoglobin (HGB), Homocysteine, Red Blood Cells, Haematocrit (HCT), Mean Cell Volume (MCV), Red Cell Distribution Width (RDW), Mean Cell Haemoglobin (MCH), MCHC, Platelets, Platelet Volume (MPV), White Blood Cells, Neutrophils, Lymphocytes, Monocytes, Basophils, Eosinophils, Ferritin, Calcium, Insulin (fasting), Glucose, HOMA - IR Score, ESR, Globulin, Albumin, Creatine Kinase (CK), C-Reactive Protein (CRP), Total Protein, HbA1c-(IFCC), Iron, Transferrin, Transferrin Saturation, T.I.B.C, Cystatin C, Sodium, Potassium, Chloride, Phosphorus, Urea / BUN, Creatinine, eGFR(MDRD)(Caucasian only), AST, Alanine Transaminase (ALT), Gamma-Glutamyl Transferase (GGT), LDH, Total Bilirubin, Alk Phosphatase (ALP), Uric Acid, Cholesterol, HDL, LDL, Triglycerides, Chol:HDL ratio, Non HDL Cholesterol, Cortisol (Random), Testosterone, Free-Testosterone (Calculated), Prolactin, Oestradiol, Progesterone, LH, FSH, DHEA-Sulphate, Sex Hormone Binding Globulin (SHBG), TSH, Free T4 (Thyroxine), Free T3 (Triiodothyronine), Total PSA, Anti-Thyroglobulin abs, Anti-Thyroidperoxidase abs, Vitamin D (25 OH), B12-Active, Serum Folate, Folate, Magnesium.

Answer structure: {<test_name>: {unit: <unit>, value: <value>}}
Example answer: {"Haemoglobin (HGB)": {unit: "g/L", value: "140"},"Homocysteine": {unit: "umol/L", value: "30"}}

Here is the blood test report:
"""

base_structure = {
  "Homocysteine": {
    "upper_limit": "10",
    "lower_limit": "6",
    "reasons_high": "B12/B6/B9 deficiency, vitamin C deficiency, MTHFR gene mutation, smoking, hypothyroidism, high muscle mass, cardiovascular disease / stroke risk",
    "reasons_low": "Glutathione need, low protein intake, pregnancy, insulin resistance, oxidative stress, hyperthyroidism, excessive folate supplementation"
  },
  "Haematocrit (HCT)": {
    "upper_limit": "0.48",
    "lower_limit": "0.38",
    "reasons_high": "Dehydration, smoking, respiratory disease, high altitude, overproduction of red blood cells, spleen hypofunction, exogenous testosterone, sleep apnoea",
    "reasons_low": "Digestive inflammation, IBD, blood loss, destruction of red bloods cells, decreased red blood cell production, anemia, low immunity (thymus hypofunction), inadequate protein intake or absorption, nutrient deficiency: iron, vitamin B6, B9, B12, C, copper, manganese, or iodine"
  },
  "Mean Cell Volume (MCV)": {
    "upper_limit": "89",
    "lower_limit": "82",
    "reasons_high": "Macrocytic anaemia, pernicious anaemia, vitamin B9 or B12 deficiency, alcoholism, low stomach acid, gluten intolerance, dysbiosis, bacterial overgrowth",
    "reasons_low": "Microcytic anaemia (low iron, B6), thalassemia, internal bleeding, heavy metals, blood loss, parasites, bacterial - coeliac disease, gluten intolerance"
  },
  "Red Cell Distribution Width (RDW)": {
    "upper_limit": "13",
    "lower_limit": "0",
    "reasons_high": "Elevated homocystiene, low MCV + RBC, low hemo, low irom, low ferritin, low stomach acid, gluten sensitivity, poor glutathione status, mercury toxicity, nutrient deficency: Iron. B9, B12, pernicious anaemia",
    "reasons_low": "Jake's not convinced that low RDW is a concern. - Acute or chronic bacterial infection, inflammation, heavy periods, childhood disease (measles, mumps, e.t.c)"
  },
  "Mean Cell Haemoglobin (MCH)": {
    "upper_limit": "32",
    "lower_limit": "28",
    "reasons_high": "Microcytic anaemia (iron, B6, blood loss), iron deficiency, blood loss (internal bleeding, heavy periods), Vitamin B6, C, or K deficiency, coeliac disease, leaky gut, imbalanced gut flora, heavy metals",
    "reasons_low": "Macrocytic anaemia, vitamin B9 or B12 deficiency, low stomach acid, excessive alcohol - gluten intolerance, leaky gut, IBS, coeliac disease"
  },
  "MCHC": {
    "upper_limit": "350",
    "lower_limit": "320",
    "reasons_high": "Hyperchromia, Celiac, leaky gut, alcohol, low stomach acid, early stage autoimmiunity, chronic obstructive pulmonary disease, nutrient deficiences: B9, B12, high lipids = false elevations. Medications: antibiotics, ibuprofen, paracetamol, or interferon)",
    "reasons_low": "Anemia (low iron, B6, blood loss), Hypovhromia, thalassaemia, heavy metals. heavy periods, nutrient deficiences: Iron, B6, or C"
  },
  "Platelets": {
    "upper_limit": "300",
    "lower_limit": "200",
    "reasons_high": "Iron deficiency, Hemolytic anemia, Stress, Infection, Inflammation, Cancer, Thrombocytosis, atherosclerosis, - poor spleen function, chronic inflammation, nutrient deficiencies: magnesium, omega 3, or vitamin E, stroke, cardiovascular disease",
    "reasons_low": "Alcoholism, Bleeding, Leukaemia, liver disease, systemic virus or bacterial infections, immune system dysfunction, idiopathic thrombocytopenia, heavy metals, Alzheimer's disease, medication: heparin, quinine, valproic acid"
  },
  "Platelet Volume (MPV)": {
    "upper_limit": "9.5",
    "lower_limit": "8.5",
    "reasons_high": "Vitamin D deficiency, obesity, thyroid disorders",
    "reasons_low": "Inflammatory disease, impaired bone marrow function"
  },
  "White Blood Cells": {
    "upper_limit": "7.5",
    "lower_limit": "5.5",
    "reasons_high": "Active infection, inflammatory response, viral, stress, allergies, recent exercise, high refined carbohydrate diet, intestinal parasites, asthma",
    "reasons_low": "Chronic infection, immunosupression, compromised immunity, parasite, viral, autoimmune disease, bone marrow failure or cancer, liver or spleen disease, poor protein intake, poor protein absorption"
  },
  "Neutrophils": {
    "upper_limit": "4.5",
    "lower_limit": "3.0",
    "reasons_high": "bacterial infection, asthma, emphysema, late stages of pregnancy, recent exercise, stress, extreme cold or heat, intestinal parasites",
    "reasons_low": "Chronic infection/inflammation (bacterial, viral, parasitic), decreased bone marrow production, parasites, intestinal inflammation (IBD, leaky gut etc), autoimmunity, copper, Hepatitis, rheumatoid arthritis, parathyroid hyper function, exposure to certain carcinogens, poor infection resistance, protein deficiency, nutrient deficiencies: Zinc, or Vitamin C. Mononucleosis"
  },
  "Lymphocytes": {
    "upper_limit": "3.1",
    "lower_limit": "1.1",
    "reasons_high": "Infections, autoimmune disorders, cancer of lymphatic system or blood, late stages of pregnancy, poor detoxification capacity, adrenal fatigue, viral infection, systemic toxicity, IBD, exercise",
    "reasons_low": "Immunosuppressant drugs, hepatitis, rheumatoid arthritis, chronic viral infection, poor defence against viruses and cancer, zinc, chronic inflammation, heavy metal toxicity, connective tissue breakdown"
  },
  "Monocytes": {
    "upper_limit": "0.5",
    "lower_limit": "0.3",
    "reasons_high": "Bacteria or viral infection, recovery phase of infection, chronic inflammation, muscle wasting, inflammation, liver dysfunction, intestinal parasites, congestion in the urinary tract, non alchohol fatty liver",
    "reasons_low": "My not always be a cause for concern, Immunosuppresive meds, chronic immune dysregulation / intestinal permeability, Bone marrow disease, HIV/AIDs, autoimmune disease, corticosteroid therapy, nutrient deficicences: B12 OR B9"
  },
  "Basophils": {
    "upper_limit": "0.1",
    "lower_limit": "0.0",
    "reasons_high": "Influenza, chronic hemolytic anemia, parasite, hypo thyroid, intestinal permeability, severe food allergy, inflammation, Leukaemia, splenectomy, chronic sinus infection, asthma, eczema, hypothyroidism",
    "reasons_low": "Acute or severe infections, bone marrow suppression, stress or chronic inflammation, allergic reactions, hyperthyroidism, autoimmune disorders, Cushing's, prolonged emotional stress"
  },
  "Eosinophils": {
    "upper_limit": "0.3",
    "lower_limit": "0.0",
    "reasons_high": "Parasitic infection (worms), attempt to detoxify through the skin, inflammatory bowel disease, adrenal dysfunction, food allergies and sensitivities, hyperthyroidism, Asthma, dermatitis",
    "reasons_low": "Stress or chronic inflammation, autoimmune disorders, Cushing's, medications such as corticosteroids, physical/emotional stress, bone marrow suppression"
  },
  "Ferritin": {
    "upper_limit": "150",
    "lower_limit": "50",
    "reasons_high": "B6, Anemia, Liver disease, inflammation, hemochromatosis, chronic infection, autoimmune disease, recent blood transfusions, cancer",
    "reasons_low": "Iron deficiency, infection, poor protein intake, low stomach acid, poorly controlled celiac disease, gluten intolerance, leaky gut, food allergies, sugar cravings"
  },
  "Calcium": {
    "upper_limit": "2.45",
    "lower_limit": "2.3",
    "reasons_high": "Hyperthyroidism, hyperparathyroidism, cancer, excessive vitamin D, dehydration, prolonged immobilisation, granulomatous diseases, medications, milk-alkali syndrome, familial hypocalciuric hypercalcemia",
    "reasons_low": "Hypoparathyroidism, vitamin D deficiency, chronic kidney disease, malabsorption disorders, hypoabuminemia, acute pancreatitis, magnesium deficiency, medications, removal or parathyroid glands"
  },
  "Insulin (fasting)": {
    "upper_limit": "6",
    "lower_limit": "2",
    "reasons_high": "Insulin resistance, Fatty liver, Pancreatic growths, Obesity, Medications, Pregnancy, Dysbiosis/LPS",
    "reasons_low": "Type 1 diabetes, Pituitary insufficiency, GABA deficiency, Low GLP 1"
  },
  "Glucose": {
    "upper_limit": "5",
    "lower_limit": "4.4",
    "reasons_high": "Insulin resistance, Fatty Liver, Hyperthyroidism, Pregnancy, Diabetes, stress, illness, medications, pancreatitis, Cushing's, excessive carbohydrate intake, hormonal disorders, infection",
    "reasons_low": "Hypoadrenal function, Hypothyroidism, Hypoglycemia, Nurtient deficiencies - Diabetes mellitus, excessive insulin, inadequate food intake, prolonged fasting, medications, alcohol, liver disease, endocrine disorders, infection, insulinomas, genetic conditions"
  },
  "ESR": {
    "upper_limit": "15",
    "lower_limit": "1",
    "reasons_high": "Chronic Inflammation (Autoimmune disorders like rheumatoid arthritis, lupus, or inflammatory bowel disease can cause persistently high ESR), Chronic low-grade inflammation related to lifestyle factors or metabolic issues may also elevate ESR, Infections (bacterial, viral. fungal, parasitic), Nutrient deficiency anaemia. Metabolic syndrome, Toxin exposure (environmental or heavy metals), gut dysbiosis (intestinal permeability) Hormone imbalances or thyroid disorders, Stress, cancers, lifestyle factors (smoking, alcohol, lack of physical activity.",
    "reasons_low": None
  },
  "Globulin": {
    "upper_limit": "28",
    "lower_limit": "22",
    "reasons_high": "Hypochlorhydria, liver cell damage, Gallbladder dysfunction, Parasites, Low serotonin (tryp is depleted by elevated globulin), Elevated estrogen, oxidative stress, heavy metal toxicity, chronic inflammation or infection, autoimmune disease",
    "reasons_low": "Anemia, Digestive dysfunction, digestive inflammation (such as IBD), immune insufficiency"
  },
  "Albumin": {
    "upper_limit": "50",
    "lower_limit": "40",
    "reasons_high": "Dehydration - anabolic steroid use, growth hormone, insulin",
    "reasons_low": "hypochlorhydria, liver dysfunction, oxidative stress, vitamin c deficiency, acute infection, kidney dysfunction, pregnancy, impaired protein synthesis, malabsorption, chrons disease, coeliac"
  },
  "Creatine Kinase (CK)": {
    "upper_limit": "192",
    "lower_limit": "26",
    "reasons_high": "Exercise/overtraining, obesity, medications, drugs/toxins",
    "reasons_low": "Catabolic/low muscle mass, autoimmune, pregnant"
  },
  "C-Reactive Protein (CRP)": {
    "upper_limit": "1",
    "lower_limit": "0",
    "reasons_high": "Chronic fatigue syndrome, autoimmune disease, obesity, cardiovascular risk, stress, poor diet",
    "reasons_low": "Medications, normal health, localised infection, liver disease, malnutrition, autoimmune disorders, genetic variations, aging"
  },
  "Total Protein": {
    "upper_limit": "78",
    "lower_limit": "62",
    "reasons_high": "Refer to Alb/Glob - Dehydration, adrenal fatigue, diabetes, rheumatoid arthritis, liver or gallbladder dysfunction, chronic inflammation, chronic infection",
    "reasons_low": "Refer to Alb/Glob - Extensive burns, liver disease, malabsorption, malnutrition, connective tissue breakdown, connective tissue breakdown, excess of free calcium, low protein intake, zinc deficiency"
  },
  "HbA1c-(IFCC)": {
    "upper_limit": "34",
    "lower_limit": "31",
    "reasons_high": "Metabolic syndrome, pre-diabetes, diabetes, damage to kidney, eyes, blood vessels, heart, and nerve, increased congestive heart failure, risk, fatty liver, lead toxicity",
    "reasons_low": "Hypoglycaemia, autoimmune heamolytic anemia, blood loss, anemia, sickle cell anemia, lead toxicity, pregnancy, chronic renal disease, iron chelation, high dose vitamin C"
  },
  "Iron": {
    "upper_limit": "23.2",
    "lower_limit": "14.3",
    "reasons_high": "Iron overload, liver dysfunction, heamochromattosis, iron conversion problem, vittamin B6,B9,or B12 deficiency, copper deficiency, molybdenum deficiency, viral infection",
    "reasons_low": "Aneamia, Inflammation, menorrhagia, blood loss, internal bleeding, coeliac disease, low protein intake, low stomach acid, lack of vitamin C"
  },
  "Transferrin Saturation": {
    "upper_limit": "35",
    "lower_limit": "20",
    "reasons_high": "Iron overload, Hemochromatosis, Thalassemia, Iron supplementation/infusion or Acute Inflammation",
    "reasons_low": "Anemia or Iron def, Anemia of chronic disease infection"
  },
  "T.I.B.C": {
    "upper_limit": "62",
    "lower_limit": "44",
    "reasons_high": "High estrogen/con pill, Iron deficiency anemia, chronic blood loss, pregnancy, iron chelation therapy, liver disease, hemolytic anemia, inflammatory disorders",
    "reasons_low": "Iron overload, hemochromatosis, liver disease, inflammation, pregnancy, malnutrition, medications, anemia"
  },
  "Cystatin C": {
    "upper_limit": "0.9",
    "lower_limit": "0.53",
    "reasons_high": "Kidney disease, inflammation or infection, reduced eGFR, medications, high protein intake, cardiovascular disease, kidney injury, autoimmune disorders, obstructed urinary tract, diabetes mellitus",
    "reasons_low": "Normal kidney function, liver disease, malnutrition, severe inflammation, pregnancy, genetic factors"
  },
  "Sodium": {
    "upper_limit": "143",
    "lower_limit": "137",
    "reasons_high": "Dehydration, diarrhoea, High aldosterone, High intake, - vomiting, polyuria, Cushing's disease, diabetes, steroids, Aspirin, NSAIDs, excessive intake of liquorice & calcium",
    "reasons_low": "Overhydration, Diuretics, Fluid loss (vom, loose, sweating etc), Low intake, Hypothyroid, Addisons, Adrenal insufficiency (low Aldoisterone) - low stomach acid, emotional stress, acid stress, adrenal fatigue, vasopressin, tricyclic antidepressants, NSAIDs, ACE inhibitors, sulphonylreas"
  },
  "Potassium": {
    "upper_limit": "4.5",
    "lower_limit": "4",
    "reasons_high": "Dehydration / Impaired kidney function, Acute increase in potassium intake, Low Aldosterone, Cell damage (eg excess exercise)",
    "reasons_low": "Adrenal stress / high aldosterone, Fluid loss (eg vom, loose, sweating etc), High insulin, Low magnesium"
  },
  "Chloride": {
    "upper_limit": "105",
    "lower_limit": "100",
    "reasons_high": "Acidosis, Hyperventilation, Kidney dysfunction, Diarrhea, Dehydration",
    "reasons_low": "Vomitting, Metabolic alkalosis, Low stomach acid, Adrenal insufficiency"
  },
  "Phosphorus": {
    "upper_limit": "1.29",
    "lower_limit": "0.97",
    "reasons_high": "Excess Vit D, Kidney Insufficiency, Parathyroid hypofunction, Bone Growth (eg in children), Excess processed foods",
    "reasons_low": "Poor absorbtion (LSA), Low vitamin D, High insulin / refined carb intake"
  },
  "Urea / BUN": {
    "upper_limit": "6.9",
    "lower_limit": "4",
    "reasons_high": "High protein diet, Dehydration, Poor kidney function, Catabolsim (adrenal stress), Dysbiosis (LPS) - overall electrolyte balance in the body, low calcium or magnesium, gut dysbiosis, mitochondrial dysfunction, diet high in sugar or processed foods, obstructed urine flow, decreased blood flow to urine",
    "reasons_low": "Low protein intake, Excess hydration, B6 need, Livery dys - Low sodium, adrenal fatigue, hypochlorydia, emotional stress, liver dysfuntion, occurs during pregnancy"
  },
  "Creatinine": {
    "upper_limit": "100",
    "lower_limit": "60",
    "reasons_high": "Kidney insufficiency, Dehydration, Hyperthyoridism, Increased muscle, Parasitic infections, creatine supps (mild increase) - Benign prostatic hyperplasia, urinary tract congestion, renal insufficiency, uterine hypertrophy, creatine supplementation, overconsumption of protein, dehydration, over exercising",
    "reasons_low": "Low protein intake, Muscle atrophy, lack of physical activity, inadequate dietary protein, impaired digestion, low vitamin D, hypo-caloric diets, plant based diets, under exercising, catabolism."
  },
  "eGFR(MDRD)(Caucasian only)": {
    "upper_limit": "120",
    "lower_limit": "90",
    "reasons_high": "No reason for concern Jake D - Pregnancy, increase muscle mass, hyperthyroidism, obesity, hypervolemia, high protein intake, medications",
    "reasons_low": "Higher than avg muscle mass, Creatine supps, Acute exercise (elevates for 1-3 days post), Kidney disease, dehydration, vitamin D deficiency, adrenal hypofunction"
  },
  "Gamma-Glutamyl Transferase (GGT)": {
    "upper_limit": "24",
    "lower_limit": "12",
    "reasons_high": "Excess glutathione breakdown, Toxin exposure (xenobiotics), Bilary dysfunction, Oxidative stress, Excess alchohol consumption, Fatty liver, Magnesium deficiency - Liver cell damage, mercury toxicity, attempt to clear out any unwanted toxins, excess iron, viral infection",
    "reasons_low": "Low amino acid/glutathione precursors, Hypothyroid, Negative gram bacteria overgrowth (Jake has seen this pattern a lot) - Zinc, magnesium, vitamin B6, A, deficiency, impaired protein utilisation, impaired liver detoxification"
  },
  "LDH": {
    "upper_limit": "200",
    "lower_limit": "140",
    "reasons_high": "Tissue / bone damage, Inflammation / Infection, Hypothyroid, Liver damage, Anemia",
    "reasons_low": "Hypoglycemia (LBS), Ketogenic diet, Insulin resistance"
  },
  "Total Bilirubin": {
    "upper_limit": "13.6",
    "lower_limit": "5",
    "reasons_high": "Increased RBC breakdown, Gilbert's syndrome, Bile duct obstruction, SIBO, Livery dysfunction - thymus dysfunction, impaired phase 2 liver detoxification due to impaired glucocordidation or an overload of sulphating or glycination",
    "reasons_low": "Zinc deficiency, Oxidative stress - Spleen insufficiency, associations to cardiac pathology (such as angina, coronary artery disease, or arthersclorosis"
  },
  "Alk Phosphatase (ALP)": {
    "upper_limit": "100",
    "lower_limit": "65",
    "reasons_high": "gallstones, obesity, elevated oesteoblast activity, tumours",
    "reasons_low": "Bilary dysfunction, Liver damage, Bone damage / Bone growth (children), IBD, Pregnancy - Low zinc, Vitamin C and Magnesium have also been associated - Wilsons disease, oral contraceptive pill use, hypochlorydia"
  },
  "Uric Acid": {
    "upper_limit": "360",
    "lower_limit": "140",
    "reasons_high": "Gout & arthralgia (joint pain), Atherosclerosis, oxidative stress, renal insufficiency, circulatory disorders, leaky gut syndrome, mycotoxin exposure, candida, high purine consumption, alcohol, excessive exercise",
    "reasons_low": "Molybdenum deficiency, vitamin B12 deficiency, vitamin B9 deficiency, copper deficiency, poor detoxification"
  },
  "Cholesterol": {
    "upper_limit": "6.2",
    "lower_limit": "4.2",
    "reasons_high": "Negative gram bacteria (high LPS), Intestinal permeability, Livery dyfunction, Excess alcohol intake, Inflammation/autoimmunity - gallbladder dysfunction, Hypothyroid, High insulin, Gene variations, Pregnancy - Metabolic syndrome, chronic bacterial and viral infections, H pylori, cardiovascular disease, atherosclerosis",
    "reasons_low": "Liver dysfunction, Hyperthyroid, Low fat intake / fat malabsorbtion, Chronic inflammation, Low steriodal hormones - Oxidative stress, heavy metal toxicity, malnutrition, maganese deficiency, adrenal hyperfunction, autoimmune disorders"
  },
  "HDL": {
    "upper_limit": "2.2",
    "lower_limit": "1.29",
    "reasons_high": "Cholestasis (low bile flow), Insulin resistance, Hyperthyroid, Anabolic steroid - Atherosclerosis, cardiovascular disease risks, raw food diets, poor response to inflammation, obesity, high trans fatty acid consumption, fatty liver, metabolic syndrome",
    "reasons_low": "Autoimmune disorders, low carbohydrate or high protein diet, and high intense levels of physical activity"
  },
  "LDL": {
    "upper_limit": "4.4",
    "lower_limit": "2.07",
    "reasons_high": "Biliary insufficiency / gallbladder dysfunction, Hypothyroid, High insulin, Gene variations, Pregnancy, Anabolic steriods - cardiovascular disease, atherosclerosis, hyperlipidaemia, oxidative stress, hyperthyroidism, H pylori",
    "reasons_low": "Inflammation / LPS, Hyperthyroid, Low fat intake/absorbtion - associated risk of: depression, cancer, anxiety, and memory impairment. Low LDL throughout pregnancy is associated with premature birth and low birth rate."
  },
  "Triglycerides": {
    "upper_limit": "1",
    "lower_limit": "0.6",
    "reasons_high": "Obesity, early stages hyperglycaemia, metabolic syndrome, hyper-caloric diet, diabetes, fatty liver, poor metabolism of fats, H pylori, smoking, alcohol, hypothyroidism, cardiovascular disease, atherosclerosis, stroke, medications: corticosteroids, HIV medications, beta blockers, oestrogen, and bile acid sequestrants",
    "reasons_low": "Liver / biliary dysfunction, adrenal hyperfunction, hyperthyroidism, malnutrition, low fat diet, digestive malabsorption, autoimmune disorders, medication: statins, metformin, high dose niacin"
  },
  "Chol:HDL ratio": {
    "upper_limit": "3",
    "lower_limit": "0",
    "reasons_high": "Poor diet, chronic inflammation, insulin resistance, stress",
    "reasons_low": "High HDL cholesterol levels, normal or low total cholesterol levels"
  },
  "Non HDL Cholesterol": {
    "upper_limit": "4.4",
    "lower_limit": "0",
    "reasons_high": "Poor diet, insulin resistance, thyroid dysfunction, chronic inflammation",
    "reasons_low": "Liver disease, malnutrition, genetic disorders, medications, chronic inflammation, hyperthyroidism, advanced age"
  },
  "TSH": {
    "upper_limit": "2.5",
    "lower_limit": "1",
    "reasons_high": "Hypothyrodism (hashimotos/thyorid gland dysfunction), Lithium or fluoride exposure, Excess iodine, Older age (may have higher TSH without hypo) - pituitary dysfunction, low progrestorone, adrenal fatigue",
    "reasons_low": "Primary Hyperthyroidism (graves/thyroid gland disruption), Secondary hypothyroidism (pituitary gland dysfunction), Tertiary hypothyroidism (hypothalamus dysfunction), Dopamine agonists, Exogenous thyroid hormone use, Pregnancy, HPA axis dysfunction - Grave's disease, thyroiditis, pituitary dysfunction, liver toxicity"
  },
  "Free T4 (Thyroxine)": {
    "upper_limit": "20",
    "lower_limit": "13",
    "reasons_high": "Hyperthyroidism, thyroid meds, pregnancy - Grave's disease, liver toxicity, nutrient deficiences: Vitamin A, B, magnesium, selenium, or zinc",
    "reasons_low": "Hypothyriodism (primary, secondary, tertiary), malnurishment - Hashimoto's, protein malabsorption, dysbiosis, low progestorone, adrenal fatgiue, nutrient deficiency: tyrosine or iodine"
  },
  "Free T3 (Triiodothyronine)": {
    "upper_limit": "6.9",
    "lower_limit": "4.6",
    "reasons_high": "Hyperthyroidisnm,  Thyroid meds, Pregnancy, Excess Iodine - Grave's diseas, historty of childhood sexual abuse",
    "reasons_low": "Hypothyroidism (primary, secondary, tertiary), malnurishment/nutrient deficiencies, inflammation/infection, High cholesterol - Hashimoto's, thyroiditis, liver disease, kidney disease, low calorie diet, low progestorone, nutrient deficiences: selenium, or Zinc"
  },
  "Total PSA": {
    "upper_limit": "2.5",
    "lower_limit": "0",
    "reasons_high": "Hormonal imbalance/disorders, endocrine disorders, rare effect from some medications or treatments, cross-reactivity in the body possibly due to tumours.",
    "reasons_low": "Low levels are expected in females"
  },
  "Anti-Thyroglobulin abs": {
    "upper_limit": None,
    "lower_limit": None,
    "reasons_high": "Grave's disease, Hashimotos, Excess iodine - Sjogren's disease, lupus, or rheumatoid arthiritis, dysbiosis, heavy metal toxicity, PCOS, Stress, environmental factors",
    "reasons_low": "No clinical significance as a low result is desired"
  },
  "Anti-Thyroidperoxidase abs": {
    "upper_limit": None,
    "lower_limit": None,
    "reasons_high": "Grave's disease, Hashimoto's, Other autoimmune such as Celiac and autoimmune gastritis, spontaneous miscarriage and recurrent miscarriage - Sjogren's disease, lupus, or rheumatoid arthiritis, dysbiosis, heavy metal toxicity, PCOS, stress, environmental factors",
    "reasons_low": "No clinical significance as a low result is desired"
  },
  "Vitamin D (25 OH)": {
    "upper_limit": "225",
    "lower_limit": "125",
    "reasons_high": "Over-supplementation, Mag deficiency, Excess calcium and kidney stone formation - hypercalcemia",
    "reasons_low": "D deficiency, cardiovascular disease, metabolic diseases, and cancer, Osteoporosis, Inflammation or infection, Autoimmunity, Genetic (affecting conversion or receptors), Medication use (e.g. cholestyramine) - Lack of sunlight exposure, calcium over-supplementation, magnesium deficiency, multiple sclerosis, cardiovascular disease, rickets, oesteoporosis, hypertension"
  },
  "B12-Active": {
    "upper_limit": "590.24",
    "lower_limit": "332.01",
    "reasons_high": "Methylation defect, liver disease, kidney disease, increased cancer risk",
    "reasons_low": "Coeliac disease, Chrohn's disease, elevated homocysteine, dysbiosis, plant based diets, burning sensation in mouth and mouth ulcers, medication: proton pump inhibitors, antacids, metformin"
  },
  "Serum Folate": {
    "upper_limit": "25",
    "lower_limit": "15",
    "reasons_high": None,
    "reasons_low": None
  },
  "Folate": {
    "upper_limit": "25",
    "lower_limit": "15",
    "reasons_high": "Supplementation, MTHFR gene mutation, B12 deficiency, kidney disease, cancer",
    "reasons_low": "Poor diet, malabsorption, alcohol abuse, certain medications, increased requirement, MTHFR gene mutation"
  },
  "Magnesium": {
    "upper_limit": "1",
    "lower_limit": "0.9",
    "reasons_high": "Hypothyroid, dehydration / poor kidney clearance, Adrenal insufficiency, Excess breakdown of RBC",
    "reasons_low": "Adrenal hyperfunction, Excessive alcohol, Fluid loss (loose stools etc), Metabolic dysfunction"
  }
}

base_structure_male = {
  "Haemoglobin (HGB)": {
    "upper_limit": "155",
    "lower_limit": "145",
    "reasons_high": "Dehydration (low water intake, excess exercise, parasites), respiratory disease, asthma (red cells increase to try and increase oxidation) - polycythaemia, smoking, high altitude, blood clot, lung disease",
    "reasons_low": "Anaemia, Iron deficiency, Vitamin B9 or B12 deficiency, copper, magnesium, donating blood, low stomach acid causing malabsorbtion - inherited haemoglobin defects, Cirrhosis of liver, bleeding or haemorrhage, kidney disease, heavy period"
  },
  "Red Blood Cells": {
    "upper_limit": "4.9",
    "lower_limit": "4.2",
    "reasons_high": "Dehydration, respiraroy distress (asthma, emphysema), steroid use, severe diarrhoea, kidney disease, pulmonary fibrosis, polycythaemia, medications: gentamicin, methydopa, low oxygen levels, heart or lung disease",
    "reasons_low": "Anaemia (copper, low iron, blood loss, B12, 9, 6), repeated infections, congestive heart failure,  anorexia, haemorrhage, autoimmune disease, chronic kidney disease"
  },
  "AST": {
    "upper_limit": "25",
    "lower_limit": "15",
    "reasons_high": "Liver damage, inflammation, medication, muscle damage, potential yeast if raised with ALT, Recent exercise, Hypothyroid, infection",
    "reasons_low": "Low B6 - severe liver dysfunction, genetic disorders, malabsorption issues"
  },
  "Alanine Transaminase (ALT)": {
    "upper_limit": "23",
    "lower_limit": "13",
    "reasons_high": "Liver damage, Infection (viral), Fatty liver, Excessive muscle breakdown, Bilary issues, Pancreatitis - Dysfunction located within the liver, fatty liver / cirrhosis of the liver, alcohol, biliary tract obstruction, excessive muscle breakdown, heavy metals (particularly lead), viral infection: herpes, mononucleosis, celiac disease, chrons disease, ulcerative colitis",
    "reasons_low": "Low B6 - Vitamin B12 deficiency, urinary tract infection, fatty liver (early development, poor functioning of Krebs cycle (leading to low energy)"
  },
  "Testosterone": {
    "upper_limit": "31.2",
    "lower_limit": "24.27",
    "reasons_high": "Acne, hair loss, adrenal fatigue, PCOS, Painful intercourse, hirsutism, infertility, Amenorrhoea",
    "reasons_low": "Low DHEA, low pregnenolone, Infertility, Low libido, osteoporosis, painful intercourse, low confidence, chronic depression, low stress resilience, oligomenorrhea"
  },
  "Cortisol (Random)": {
    "upper_limit": "275",
    "lower_limit": "18",
    "reasons_high": "Cushing syndrome, asthma, lupus, rheumatoid arthritis, pituitary gland dysfunction",
    "reasons_low": "Autoimmune, HIV/AIDS, problems with pituitary gland, traumatic brain injury"
  },
  "Oestradiol": {
    "upper_limit": "111.13",
    "lower_limit": "73.42",
    "reasons_high": "Impaired detoxification, adfrenal dysfunction",
    "reasons_low": "Stress, adrenal fatigue, excessive exercise"
  },
  "Progesterone": {
    "upper_limit": "3.92",
    "lower_limit": "3.18",
    "reasons_high": "Urinary incontinence, migranes, diabetes, chronic fatigue syndrome",
    "reasons_low": "Acute infections, cancer risk, oestrogen excess, hypothyroidism, adrenal fatigue"
  },
  "Prolactin": {
    "upper_limit": "200",
    "lower_limit": "0",
    "reasons_high": "Pituitary tumour, low dopamine, stress",
    "reasons_low": "Low immune response, low oestrogen, low melatonin"
  },
  "LH": {
    "upper_limit": "9.3",
    "lower_limit": "1.5",
    "reasons_high": "Adrenal fatigue, hypothyroidism, low DHEA",
    "reasons_low": "Anorexia, amenorrhoea, pituitary disorders, stress, malnutrition, hypothylamus dysfunction"
  },
  "FSH": {
    "upper_limit": "8",
    "lower_limit": "1.6",
    "reasons_high": "Adrenal fatigue, hypothyroidism, low DHEA, Chemotherapy, or radiation therapy",
    "reasons_low": "Anorexia, pituitary disorders, stress"
  },
  "DHEA-Sulphate": {
    "upper_limit": "18.73",
    "lower_limit": "9.5",
    "reasons_high": "High stress levels, acne (due to increased androgens) and mood swings.",
    "reasons_low": "Fatigue, depression, muscle weakness/decreased muscle mass, low sex drive, inflammation, memory/cognitive issues and previous/current head injuries. adrenal fatigue"
  },
  "Sex Hormone Binding Globulin (SHBG)": {
    "upper_limit": "40",
    "lower_limit": "30",
    "reasons_high": "Excess oestrogen, hyperthyroidism",
    "reasons_low": "Insulin resistance, hypothyroidism, adrenal fatigue"
  },
  "Free-Testosterone (Calculated)": {
    "upper_limit": "0.62",
    "lower_limit": "0.2",
    "reasons_high": "Acne, hair loss, adrenal fatigue, hirsutism, infertility",
    "reasons_low": "Infertility, Low libido, osteoporosis, painful intercourse, low confidence, chronic depression, low stress resilience, oligomenorrhea"
  },
}

base_structure_female = {
  "Haemoglobin (HGB)": {
    "upper_limit": "145",
    "lower_limit": "135",
    "reasons_high": "Dehydration (low water intake, excess exercise, parasites), respiratory disease, asthma (red cells increase to try and increase oxidation) - polycythaemia, smoking, high altitude, blood clot, lung disease",
    "reasons_low": "Anaemia, Iron deficiency, Vitamin B9 or B12 deficiency, copper, magnesium, donating blood, low stomach acid causing malabsorbtion - inherited haemoglobin defects, Cirrhosis of liver, bleeding or haemorrhage, kidney disease, heavy period"
  },
  "Red Blood Cells": {
    "upper_limit": "4.5",
    "lower_limit": "3.9",
    "reasons_high": "Dehydration, respiraroy distress (asthma, emphysema), steroid use, severe diarrhoea, kidney disease, pulmonary fibrosis, polycythaemia, medications: gentamicin, methydopa, low oxygen levels, heart or lung disease",
    "reasons_low": "Anaemia (copper, low iron, blood loss, B12, 9, 6), repeated infections, congestive heart failure,  anorexia, haemorrhage, autoimmune disease, chronic kidney disease"
  },
  "AST": {
    "upper_limit": "22",
    "lower_limit": "12",
    "reasons_high": "Liver damage, inflammation, medication, muscle damage, potential yeast if raised with ALT, Recent exercise, Hypothyroid, infection",
    "reasons_low": "Low B6 - severe liver dysfunction, genetic disorders, malabsorption issues"
  },
  "Alanine Transaminase (ALT)": {
    "upper_limit": "19",
    "lower_limit": "9",
    "reasons_high": "Liver damage, Infection (viral), Fatty liver, Excessive muscle breakdown, Bilary issues, Pancreatitis - Dysfunction located within the liver, fatty liver / cirrhosis of the liver, alcohol, biliary tract obstruction, excessive muscle breakdown, heavy metals (particularly lead), viral infection: herpes, mononucleosis, celiac disease, chrons disease, ulcerative colitis",
    "reasons_low": "Low B6 - Vitamin B12 deficiency, urinary tract infection, fatty liver (early development, poor functioning of Krebs cycle (leading to low energy)"
  },
  "Cortisol (Random)": {
    "upper_limit": "456",
    "lower_limit": "113",
    "reasons_high": "Cushing syndrome, asthma, lupus, rheumatoid arthritis, pituitary gland dysfunction",
    "reasons_low": "Autoimmune, HIV/AIDS, problems with pituitary gland, traumatic brain injury"
  },
  "Testosterone": {
    "upper_limit": "1.67",
    "lower_limit": "0.29",
    "reasons_high": "Acne, hair loss, adrenal fatigue, PCOS, painful intercourse, hirsutism, infertility, amenorrhoea",
    "reasons_low": "Low DHEA, low pregnenolone, infertility, low libido, osteoporosis, painful intercourse, low confidence, chronic depression, low stress resilience, oligomenorrhea"
  },
  "Free-Testosterone (Calculated)": {
    "upper_limit": "0.03",
    "lower_limit": "0.003",
    "reasons_high": "Acne, hair loss, adrenal fatigue, PCOS, Painful intercourse, hirsutism, infertility, amenorrhoea",
    "reasons_low": "Infertility, low libido, osteoporosis, painful intercourse, low confidence, chronic depression, low stress resilience, oligomenorrhea"
  },
  "Prolactin": {
    "upper_limit": "300",
    "lower_limit": "0",
    "reasons_high": "PCOS, Breastfeeding, pituitary tumour, low dopamine",
    "reasons_low": "Low immune response, low oestrogen, low melatonin"
  },
  "Oestradiol": {
    "upper_limit": "854",
    "lower_limit": "45.4",
    "reasons_high": "Functional cyst, diminished ovarian reserve, ovarian dysfunction, adrenal dysfunction, impaired detoxification",
    "reasons_low": "Menopause, stress, adrenal fatigue, excessive exercise"
  },
  "Progesterone": {
    "upper_limit": "2.84",
    "lower_limit": "0.181",
    "reasons_high": "Pregnancy, ovarian tumour, urinary incontinence, migranes, diabetes, chronic fatigue syndrome",
    "reasons_low": "Anovulation, acute infections, cancer risk, oestrogen excess, premenstrual syndrome, hypothyroidism, adrenal fatigue"
  },
  "LH": {
    "upper_limit": "12.6",
    "lower_limit": "2.4",
    "reasons_high": "Menopause, adrenal fatigue, hypothyroidism, low DHEA",
    "reasons_low": "Anorexia, amenorrhoea, pituitary disorders, stress, malnutrition, hypothylamus dysfunction"
  },
  "FSH": {
    "upper_limit": "12.5",
    "lower_limit": "3.5",
    "reasons_high": "Menopause, adrenal fatigue, hypothyroidism, low DHEA, chemotherapy, or radiation therapy",
    "reasons_low": "Anorexia, amenorrhoea, pituitary disorders, stress"
  },
  "DHEA-Sulphate": {
    "upper_limit": "9.23",
    "lower_limit": "2.68",
    "reasons_high": "High stress levels, acne (due to increased androgens), hair growth (women), PCOS, irregular periods and mood swings.",
    "reasons_low": "Fatigue, depression, muscle weakness/decreased muscle mass, low sex drive, inflammation, memory/cognitive issues and previous/current head injuries. adrenal fatigue"
  },
  "Sex Hormone Binding Globulin (SHBG)": {
    "upper_limit": "128",
    "lower_limit": "27.1",
    "reasons_high": "Excess oestrogen, hyperthyroidism, PCOS, Metabolic Dysfunction, high bioavailable testosterone",
    "reasons_low": "Insulin resistance, hypothyroidism, adrenal fatigue, low bioavailable testosterone, ageing, high estrogen or synthetic estrogen (contraceptives), disordered eating, hyperthyroidism"
  },
}

blood_test_answer_prompt = """
You are Doctor Mark Dini. You are expert in analyzing blood test results.
I submitted the blood test report to your system analyze and I got the reasons and analysis of the test results.
Now you help me to understand and summarize for me in layman language.
Here is the reasons and analysis:
"""

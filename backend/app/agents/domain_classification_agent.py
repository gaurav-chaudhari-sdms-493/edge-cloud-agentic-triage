from app.agents.base import AgentState

HEALTHCARE_KEYWORDS = {
    # Original Keywords
    "doctor", "hospital", "fever", "pain", "symptom", "medicine", "prescription",
    "appointment", "insurance", "patient", "emergency", "clinic", "cough",
    "headache", "diabetes", "blood pressure",

    # Symptoms & Conditions
    "ache", "acne", "aids", "allergy", "alzheimer's", "anemia", "angina", "anxiety",
    "appendicitis", "arthritis", "asthma", "autism", "back pain", "bacteria",
    "bleeding", "blister", "bloating", "blood clot", "bone fracture", "bronchitis",
    "bruise", "burn", "cancer", "cardiac arrest", "chest pain", "chickenpox",
    "cholesterol", "cold", "concussion", "constipation", "cramp", "cyst",
    "dementia", "depression", "diarrhea", "dizziness", "dysentery", "ebola",
    "eczema", "edema", "epilepsy", "fatigue", "flu", "food poisoning", "fungus",
    "gallstone", "gastritis", "glaucoma", "gout", "h1n1", "hay fever", "heart attack",
    "heart disease", "heartburn", "hemorrhoid", "hepatitis", "hernia", "herpes",
    "hiv", "hives", "hypertension", "hypothermia", "indigestion", "infection",
    "inflammation", "influenza", "insomnia", "jaundice", "joint pain", "kidney stone",
    "leukemia", "lice", "lupus", "lyme disease", "malaria", "measles", "meningitis",
    "migraine", "miscarriage", "mono", "mononucleosis", "mrsa", "multiple sclerosis",
    "mumps", "muscle strain", "nausea", "obesity", "osteoporosis", "ovarian cyst",
    "pancreatitis", "parkinson's", "pneumonia", "polio", "preeclampsia", "psoriasis",
    "rabies", "rash", "rheumatoid arthritis", "ringworm", "rosacea", "rubella",
    "salmonella", "scabies", "scarlet fever", "schizophrenia", "seizure", "sepsis",
    "shingles", "sinusitis", "smallpox", "sore throat", "sprain", "stomach ache",
    "strep throat", "stroke", "sunburn", "swelling", "tendinitis", "tetanus",
    "thrush", "thyroid", "tonsillitis", "tuberculosis", "tumor", "ulcer", "uti",
    "urinary tract infection", "vertigo", "virus", "wart", "whooping cough", "yeast infection",
    "zika",

    # Medical Specialties & Professionals
    "allergist", "anesthesiologist", "audiologist", "cardiologist", "chiropractor",
    "dermatologist", "dietitian", "endocrinologist", "epidemiologist", "gastroenterologist",
    "geneticist", "geriatrician", "gynecologist", "hematologist", "immunologist",
    "internist", "medic", "midwife", "nephrologist", "neurologist", "nurse",
    "nutritionist", "obgyn", "obstetrician", "oncologist", "ophthalmologist",
    "optometrist", "orthodontist", "orthopedist", "otolaryngologist", "paramedic",
    "pathologist", "pediatrician", "pharmacist", "physician", "physiotherapist",
    "podiatrist", "psychiatrist", "psychologist", "pulmonologist", "radiologist",
    "rheumatologist", "surgeon", "therapist", "urologist", "veterinarian",

    # Treatments & Procedures
    "ablation", "acupuncture", "adenoidectomy", "amniocentesis", "amputation",
    "angioplasty", "antibiotic", "antidepressant", "antifungal", "antihistamine",
    "antiseptic", "antiviral", "appendectomy", "autopsy", "bariatric surgery",
    "biopsy", "blood test", "blood transfusion", "bone marrow transplant",
    "braces", "bypass surgery", "c-section", "cast", "catheter", "cauterization",
    "cesarean section", "chemotherapy", "cholecystectomy", "circumcision",
    "colonoscopy", "colposcopy", "coronary bypass", "cpr", "ct scan", "defibrillation",
    "detox", "dialysis", "echocardiogram", "eeg", "ekg", "electrocardiogram",
    "electroencephalogram", "endoscopy", "enema", "epidural", "euthanasia",
    "extraction", "eye exam", "gastric bypass", "gene therapy", "hearing aid",
    "hemodialysis", "hormone therapy", "hospice", "hysterectomy", "immunization",
    "immunotherapy", "implant", "in vitro fertilization", "incubation", "infusion",
    "injection", "inpatient", "insulin", "intubation", "ivf", "laparoscopy",
    "lasik", "liposuction", "lobotomy", "lumpectomy", "mammogram", "mastectomy",
    "medication", "mri", "nebulizer", "neurosurgery", "organ transplant", "outpatient",
    "pacemaker", "palliative care", "pap smear", "pet scan", "phlebotomy",
    "physical therapy", "placebo", "plasma", "platelet", "prognosis", "prophylaxis",
    "prosthesis", "psychotherapy", "radiation therapy", "rehabilitation", "root canal",
    "saline", "sedation", "sonogram", "spinal tap", "splint", "stem cell therapy",
    "stent", "sterilization", "stitch", "supplement", "suppository", "surgery",
    "suture", "thoracotomy", "tonsillectomy", "tracheostomy", "transfusion",
    "transplant", "ultrasound", "vaccination", "vaccine", "vasectomy", "venipuncture",
    "ventilator", "x-ray",

    # Anatomy & Biology
    "abdomen", "adrenal gland", "alveoli", "amino acid", "amniotic fluid", "anatomy",
    "antibody", "antigen", "aorta", "appendix", "artery", "atrium", "axon",
    "bile", "bladder", "blood cell", "blood vessel", "bone", "brain", "bronchus",
    "capillary", "carbohydrate", "cartilage", "cell", "cerebellum", "cerebrum",
    "cervix", "circulatory system", "clavicle", "coccyx", "collagen", "colon",
    "cornea", "cortex", "cranium", "diaphragm", "digestive system", "dna",
    "duodenum", "eardrum", "endocrine system", "endorphin", "enzyme", "epidermis",
    "epiglottis", "esophagus", "estrogen", "eustachian tube", "fallopian tube",
    "femur", "fetus", "fibula", "follicle", "gallbladder", "gamete", "ganglion",
    "gene", "gland", "glucose", "glycogen", "gut", "hdl", "heart", "hemoglobin",
    "hormone", "humerus", "hypothalamus", "ileum", "immune system", "intestine",
    "iris", "jaw", "jejunum", "joint", "keratin", "kidney", "larynx", "ldl",
    "ligament", "liver", "lung", "lymph", "lymph node", "mandible", "marrow",
    "maxilla", "melanin", "membrane", "meniscus", "metabolism", "molecule",
    "mucus", "muscle", "myelin", "nasal", "nerve", "nervous system", "neuron",
    "neurotransmitter", "norepinephrine", "nostril", "nucleus", "nutrient",
    "olfactory", "optic nerve", "organ", "ovary", "ovum", "pancreas", "patella",
    "pelvis", "penis", "pharynx", "pituitary gland", "placenta", "plasma",
    "platelet", "pons", "progesterone", "prostate", "protein", "pupil", "radius",
    "rectum", "red blood cell", "reflex", "reproductive system", "respiratory system",
    "retina", "rib", "rna", "saliva", "scapula", "sclera", "scrotum", "serotonin",
    "serum", "skeleton", "skull", "small intestine", "spinal cord", "spleen",
    "sternum", "stomach", "synapse", "synovial fluid", "tarsal", "tendon",
    "testicle", "testosterone", "thalamus", "thorax", "thymus", "thyroid gland",
    "tibia", "tissue", "tonsil", "trachea", "ulna", "umbilical cord", "ureter",
    "urethra", "urine", "uterus", "uvula", "vagina", "vein", "ventricle",
    "vertebra", "villus", "vitamin", "vocal cord", "white blood cell", "womb", "zygote",

    # Healthcare System & General
    "acute", "admission", "adverse effect", "ambulatory", "benefit", "board-certified",
    "case manager", "chart", "chronic", "claim", "clinical trial", "co-payment",
    "consent", "consultation", "contagious", "copay", "coverage", "critical",
    "deductible", "diagnosis", "discharge", "disease", "disorder", "dosage",
    "dose", "durable medical equipment", "electronic health record", "ehr",
    "eligibility", "epidemic", "exposure", "family history", "first aid", "generic",
    "genetic", "health", "healthcare", "hereditary", "hipaa", "hmo", "home care",
    "hospice care", "illness", "immunity", "in-network", "informed consent",
    "injury", "intensive care", "icu", "liability", "living will", "long-term care",
    "malpractice", "managed care", "medical history", "medical record", "medicaid",
    "medicare", "network", "nicu", "out-of-network", "outbreak", "over-the-counter",
    "palliative", "pandemic", "pharmacy", "phr", "physician-patient privilege",
    "policy", "ppo", "pre-existing condition", "premium", "preventive care",
    "primary care", "prognosis", "provider", "quarantine", "referral", "relapse",
    "remission", "screening", "secondary care", "side effect", "specialist",
    "stable", "sterile", "symptomatic", "syndrome", "terminal", "tertiary care",
    "triage", "urgent care", "vital signs", "vitals", "waiting list", "wellness",
    "workers compensation", "wound"
}


class DomainClassificationAgent:
    def run(self, state: AgentState) -> AgentState:
        input_text = state.content.lower()
        if any(keyword in input_text for keyword in HEALTHCARE_KEYWORDS):
            state.domain = "healthcare"
            state.supported_domain = True
            state.domain_confidence = 0.95
        else:
            state.domain = "other"
            state.supported_domain = False
            state.domain_confidence = 0.90
        return state

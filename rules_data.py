def evaluate_rules(symptoms):
    rules = [
        # Rule 1 – Cardiac or respiratory emergency
        (lambda s: "Chest Pain" in s or "Shortness of Breath" in s,
         "Urgent", "Possible cardiac or respiratory emergency."),

        # Rule 2 – Infection
        (lambda s: "Fever" in s and "Cough" in s,
         "Normal", "Likely mild respiratory infection."),

        # Rule 3 – Stomach upset
        (lambda s: "Abdominal Pain" in s or "Vomiting" in s or "Diarrhea" in s,
         "Moderate", "Possible gastrointestinal issue."),

        # Rule 4 – Pregnancy related
        (lambda s: "Pregnant" in s and "Nausea" in s,
         "Moderate", "Possible morning sickness or hormonal imbalance."),

        # Rule 5 – Severe fatigue
        (lambda s: "Fatigue" in s and "Headache" in s,
         "Normal", "Likely dehydration or stress."),

        # Rule 6 – Mental health
        (lambda s: "Anxiety" in s or "Depression" in s,
         "Normal", "Possible mental health concern, consult a specialist.")
    ]

    for condition, urgency, diagnosis in rules:
        if condition(symptoms):
            return diagnosis, urgency

    return "No clear diagnosis. Further evaluation needed.", "Normal"

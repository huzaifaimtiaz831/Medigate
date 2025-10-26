import customtkinter as ctk
from tkinter import messagebox
from medigate.rules_data import evaluate_rules
from medigate.utils import save_to_excel

def run_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("MediGate — AI Triage Assistant")
    app.geometry("850x700")

    # --- Title ---
    title = ctk.CTkLabel(app, text="🩺 MediGate — Triage Assistant", font=("Segoe UI", 28, "bold"))
    title.pack(pady=20)

    # --- Patient Info Frame ---
    info_frame = ctk.CTkFrame(app)
    info_frame.pack(pady=10, fill="x", padx=40)

    ctk.CTkLabel(info_frame, text="Name:", font=("Segoe UI", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    name_entry = ctk.CTkEntry(info_frame, placeholder_text="Enter patient name")
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    ctk.CTkLabel(info_frame, text="Age:", font=("Segoe UI", 14)).grid(row=0, column=2, padx=10, pady=5, sticky="w")
    age_entry = ctk.CTkEntry(info_frame, placeholder_text="Age")
    age_entry.grid(row=0, column=3, padx=10, pady=5)

    ctk.CTkLabel(info_frame, text="Gender:", font=("Segoe UI", 14)).grid(row=0, column=4, padx=10, pady=5, sticky="w")
    gender_var = ctk.StringVar(value="Select")
    gender_menu = ctk.CTkOptionMenu(info_frame, variable=gender_var, values=["Male", "Female"])
    gender_menu.grid(row=0, column=5, padx=10, pady=5)

    # --- Symptoms Selection Frame ---
    symptom_frame = ctk.CTkScrollableFrame(app, label_text="Select Symptoms", width=700, height=250)
    symptom_frame.pack(pady=10)

    # --- Symptom List ---
    symptoms = [
        "Fever", "Cough", "Chest Pain", "Shortness of Breath", "Headache", "Nausea",
        "Vomiting", "Dizziness", "Abdominal Pain", "Fatigue", "Sore Throat",
        "Back Pain", "Rash", "Diarrhea", "Bleeding", "Joint Pain", "Vision Problem",
        "Swelling", "Palpitations", "Weight Loss", "Pregnant"
    ]

    symptom_vars = {}
    checkboxes = {}

    def update_symptom_visibility(*args):
        gender = gender_var.get()
        if gender == "Male":
            checkboxes["Pregnant"].grid_remove()
        elif gender == "Female":
            checkboxes["Pregnant"].grid()
    gender_var.trace("w", update_symptom_visibility)

    # Place symptoms in 2 columns
    col_count = 2
    for i, symptom in enumerate(symptoms):
        var = ctk.BooleanVar()
        symptom_vars[symptom] = var
        cb = ctk.CTkCheckBox(symptom_frame, text=symptom, variable=var)
        checkboxes[symptom] = cb
        cb.grid(row=i // col_count, column=i % col_count, sticky="w", padx=10, pady=5)

    # --- Result Display ---
    result_frame = ctk.CTkFrame(app)
    result_frame.pack(pady=10, fill="x", padx=40)

    result_label = ctk.CTkLabel(result_frame, text="Diagnosis: ", font=("Segoe UI", 16, "bold"))
    result_label.pack(anchor="w", padx=10, pady=5)

    urgency_box = ctk.CTkLabel(result_frame, text="Urgency: ", font=("Segoe UI", 16, "bold"), fg_color="#222", corner_radius=10, padx=10, pady=10)
    urgency_box.pack(anchor="w", padx=10, pady=5, fill="x")

    # --- Diagnose Button ---
    def diagnose():
        name = name_entry.get().strip()
        age = age_entry.get().strip()
        gender = gender_var.get()
        selected = [s for s, v in symptom_vars.items() if v.get()]

        if not name or not age or gender == "Select":
            messagebox.showwarning("Input Error", "Please fill all patient details.")
            return

        if not selected:
            messagebox.showwarning("Input Error", "Please select at least one symptom.")
            return

        diagnosis, urgency = evaluate_rules(selected)

        # Update labels
        result_label.configure(text=f"Diagnosis: {diagnosis}")
        urgency_box.configure(text=f"Urgency: {urgency}")

        if urgency == "Critical":
            urgency_box.configure(fg_color="#8B0000")
        elif urgency == "Urgent":
            urgency_box.configure(fg_color="#FF8C00")
        else:
            urgency_box.configure(fg_color="#006400")

        # Save to Excel
        save_to_excel(name, age, gender, ", ".join(selected), diagnosis, urgency)

    diagnose_btn = ctk.CTkButton(app, text="Diagnose", font=("Segoe UI", 16, "bold"), command=diagnose)
    diagnose_btn.pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    run_gui()

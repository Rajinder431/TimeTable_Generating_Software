# backend/timetable_solver.py

from ortools.sat.python import cp_model

def generate_timetable():
    model = cp_model.CpModel()

    # Define classes and semesters
    classes = ["FY", "SY"]
    semesters = {
        "FY": [1, 2],
        "SY": [3, 4]
    }

    # Subjects mapped to (semester, class)
    subjects = {
        (1, "FY"): ["Maths", "Physics", "Chemistry", "Lab1", "Lab2"],
        (2, "FY"): ["Biology", "Computer", "Lab3", "Lab4"],
        (3, "SY"): ["Electronics", "Mechanics", "Lab5", "Lab6"],
    }

    # Teacher assignments per subject
    teachers = {
        "Maths": "Mr. A",
        "Physics": "Ms. B",
        "Chemistry": "Dr. C",
        "Biology": "Dr. D",
        "Computer": "Ms. E",
        "Electronics": "Mr. F",
        "Mechanics": "Ms. G",
        "Lab1": "Lab Incharge 1",
        "Lab2": "Lab Incharge 2",
        "Lab3": "Lab Incharge 3",
        "Lab4": "Lab Incharge 4",
        "Lab5": "Lab Incharge 5",
        "Lab6": "Lab Incharge 6"
    }

    # Timetable structure
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    slots_per_day = 6
    time_slots = [(day, slot) for day in days for slot in range(1, slots_per_day + 1)]

    # Create assignment variables
    assignments = {}
    for cls in classes:
        for semester in semesters[cls]:
            for sub in subjects.get((semester, cls), []):
                for (day, slot) in time_slots:
                    assignments[(sub, day, slot)] = model.NewBoolVar(f'{sub}_{day}_{slot}')

    # ✅ Debug Info
    total_subjects = sum(len(subjects.get((sem, cls), [])) for cls in classes for sem in semesters[cls])
    total_slots = len(time_slots)
    print(f"📚 Total subjects needing slots: {total_subjects}")
    print(f"🕒 Total available time slots (per subject): {total_slots}")
    print(f"🔢 Total assignment variables: {len(assignments)}")

    # Constraint: No overlapping subjects in the same time slot
    for (sub1, day, slot1), var1 in assignments.items():
        for (sub2, day2, slot2), var2 in assignments.items():
            if sub1 != sub2 and day == day2 and slot1 == slot2:
                model.AddBoolOr([var1.Not(), var2.Not()])

    # Constraint: A teacher cannot teach two subjects at the same time
    for (sub1, day, slot1), var1 in assignments.items():
        for (sub2, day2, slot2), var2 in assignments.items():
            if sub1 != sub2 and teachers.get(sub1) == teachers.get(sub2) and day == day2 and slot1 == slot2:
                model.AddBoolOr([var1.Not(), var2.Not()])

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Collect results
    output = []
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("✅ Solution found!")
        for (sub, day, slot), var in assignments.items():
            if solver.Value(var) == 1:
                output.append(f'{sub} assigned to {day} at Slot {slot}')
    else:
        print("❌ No solution found.")
        output.append("No solution found.")

    return output

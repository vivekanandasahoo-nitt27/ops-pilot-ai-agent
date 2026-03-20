def human_review(state: dict):

    print("\n🚨 HUMAN REVIEW REQUIRED")
    print("Message:", state["incident_text"])

    approval = input("Approve action? (yes/no): ").strip().lower()

    state["human_approval"] = approval

    print("Captured approval:", approval)  # debug

    return state
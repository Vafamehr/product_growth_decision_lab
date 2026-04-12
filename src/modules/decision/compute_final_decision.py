def compute_final_decision(conv_p, conv_lift, rev_p, rev_lift):
    print("\n===== FINAL DECISION ENGINE =====")

    alpha = 0.05

    # =========================
    # LOGIC
    # =========================
    if rev_p < alpha and rev_lift > 0:
        decision = "SHIP TREATMENT (Revenue Driven)"

    elif conv_p < alpha and conv_lift > 0:
        decision = "SHIP TREATMENT (Conversion Driven)"

    elif (rev_p < alpha and rev_lift < 0) or (conv_p < alpha and conv_lift < 0):
        decision = "ROLLBACK TREATMENT"

    else:
        decision = "INCONCLUSIVE — CONTINUE EXPERIMENT"

    print(f"Decision: {decision}")
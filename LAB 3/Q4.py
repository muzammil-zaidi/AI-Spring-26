def calculate_utility(time, cost, weight_time, weight_cost):
    """
    Higher utility is better.
    Since lower time and cost are preferred, we use negative values.
    """
    return -(weight_time * time + weight_cost * cost)


def recommend_delivery(option_a, option_b, weight_time=0.6, weight_cost=0.4):
    """
    option_a and option_b are dictionaries with 'time' and 'cost'
    """

    utility_a = calculate_utility(
        option_a["time"], option_a["cost"], weight_time, weight_cost
    )
    utility_b = calculate_utility(
        option_b["time"], option_b["cost"], weight_time, weight_cost
    )

    print(f"Utility of Option A: {utility_a:.2f}")
    print(f"Utility of Option B: {utility_b:.2f}")

    if utility_a > utility_b:
        return "Option A (Faster but more expensive)"
    else:
        return "Option B (Cheaper but slower)"

option_a = {
    "time": 2,
    "cost": 15
}

option_b = {
    "time": 5,
    "cost": 8
}

customer_1 = {"weight_time": 0.6, "weight_cost": 0.4}
customer_2 = {"weight_time": 0.4, "weight_cost": 0.6}

print("Customer 1 Recommendation:")
print(recommend_delivery(option_a, option_b, **customer_1))

print("\nCustomer 2 Recommendation:")
print(recommend_delivery(option_a, option_b, **customer_2))

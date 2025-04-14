import numpy as np
from datetime import datetime

np.random.seed(0)

NUM_TRIALS = 10000
LAYOVER = 30  # minutes

# Time helpers
def time_to_minutes(time_str):
    t = datetime.strptime(time_str, "%H:%M")
    return t.hour * 60 + t.minute

def minutes_to_time(mins):
    return f"{int(mins // 60):02}:{int(mins % 60):02}"

def sample_flight(mu, sigma):
    min_time = mu - 3 * sigma
    max_time = mu + 3 * sigma
    sample = np.random.normal(mu, sigma)
    return max(min(sample, max_time), min_time)

def simulate_airline(schedule, scheduled_arrival_str):
    stranded = 0
    arrivals = []
    scheduled_arrival = time_to_minutes(scheduled_arrival_str)

    for _ in range(NUM_TRIALS):
        current_time = time_to_minutes("8:00")

        # First flight (A -> B/E)
        leg1 = schedule[0]
        current_time += sample_flight(leg1["mu"], leg1["sigma"])

        # Second flight (B -> C or E -> F)
        took_flight2 = False
        for flight in schedule[1]:
            if current_time + LAYOVER <= time_to_minutes(flight["depart"]):
                current_time = time_to_minutes(flight["depart"])
                current_time += sample_flight(flight["mu"], flight["sigma"])
                took_flight2 = True
                break
        if not took_flight2:
            stranded += 1
            continue

        # Third flight (C -> D or F -> D)
        took_flight3 = False
        for flight in schedule[2]:
            if current_time + LAYOVER <= time_to_minutes(flight["depart"]):
                current_time = time_to_minutes(flight["depart"])
                current_time += sample_flight(flight["mu"], flight["sigma"])
                arrivals.append(current_time)
                took_flight3 = True
                break
        if not took_flight3:
            stranded += 1

    arrivals = np.array(arrivals)
    on_time_prob = np.mean(arrivals <= scheduled_arrival) if len(arrivals) > 0 else 0
    avg_arrival = np.mean(arrivals) if len(arrivals) > 0 else 0
    stranded_prob = stranded / NUM_TRIALS

    return minutes_to_time(avg_arrival), round(on_time_prob, 4), round(stranded_prob, 4)

# Airline One Schedule (times in minutes)
airline_one = [
    {"mu": 240, "sigma": 24},  # A->B
    [  # B->C
        {"depart": "12:30", "mu": 240, "sigma": 24},
        {"depart": "13:00", "mu": 240, "sigma": 24},
    ],
    [  # C->D
        {"depart": "17:00", "mu": 210, "sigma": 24},
        {"depart": "17:30", "mu": 210, "sigma": 24},
        {"depart": "18:00", "mu": 210, "sigma": 24},
    ]
]

# Airline Two Schedule
airline_two = [
    {"mu": 210, "sigma": 48},  # A->E
    [  # E->F
        {"depart": "12:00", "mu": 240, "sigma": 48},
        {"depart": "12:30", "mu": 240, "sigma": 48},
    ],
    [  # F->D
        {"depart": "16:30", "mu": 210, "sigma": 48},
        {"depart": "17:00", "mu": 210, "sigma": 48},
        {"depart": "17:30", "mu": 210, "sigma": 48},
    ]
]

# Run simulations
avg1, ontime1, stranded1 = simulate_airline(airline_one, "21:00")
avg2, ontime2, stranded2 = simulate_airline(airline_two, "20:30")

# Display results
print("Airline One Results:")
print("  Average Arrival Time:", avg1)
print("  On-Time Probability (≤21:00):", ontime1)
print("  Stranded Probability:", stranded1)

print("\nAirline Two Results:")
print("  Average Arrival Time:", avg2)
print("  On-Time Probability (≤20:30):", ontime2)
print("  Stranded Probability:", stranded2)

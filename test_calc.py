from knightpower_calc import state_power, talent_bonus, lover_ballroom, lover_greeting

print("Testing KnightPower formulas...\n")

print(f"State Power (5 stars, level 30, book bonus 9): {state_power(5, 30, 9):.2f}")
print(f"Talent Bonus (5 stars, level 30): {talent_bonus(5, 30):.2f}")
print(f"Lover Ballroom (charm 1200): {lover_ballroom(1200):.2f}")
print(f"Lover Greeting (charm 1200): {lover_greeting(1200):.2f}")

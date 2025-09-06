import json
import logging
from flask import request
from routes import app

def solve_mages_gambit(intel, reserve, fronts, stamina):

    # end in cooldown
    if not intel:
        return 10 
    
    current_mana = reserve
    current_stamina = stamina
    total_time = 0
    last_front = None
    
    for i, (front, mana_cost) in enumerate(intel):
        # insufficient mana -> cooldown
        if current_mana < mana_cost:
            total_time += 10 
            current_mana = reserve
            current_stamina = stamina
            last_front = None # reset after cooldown
        
        # insufficient stamina -> cooldown
        elif current_stamina == 0:
            total_time += 10
            current_mana = reserve
            current_stamina = stamina
            last_front = None
        
        # Cast
        if last_front != front:
            total_time += 10 # new target +10 min        
        current_mana -= mana_cost
        current_stamina -= 1
        last_front = front
    
    # end in cooldown
    total_time += 10
    
    return total_time

def solve_multiple_cases(test_cases):

    results = []
    
    for case in test_cases:
        intel = case["intel"]
        reserve = case["reserve"] 
        fronts = case["fronts"]
        stamina = case["stamina"]
        
        time_needed = solve_mages_gambit(intel, reserve, fronts, stamina)
        results.append({"time": time_needed})
    
    return results

@app.route('/the-mages-gambit', methods=['POST'])
def evaluate_mage():
    data = request.get_json()  
    output = solve_multiple_cases(data)
    return output
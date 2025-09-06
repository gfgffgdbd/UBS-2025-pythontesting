import json
import logging
import math
from flask import Flask, request, jsonify

from routes import app

logger = logging.getLogger(__name__)

def calculate_distance(customer_location, booking_center_location):
    """Calculate Euclidean distance between customer and booking center."""
    x1, y1 = customer_location
    x2, y2 = booking_center_location
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_latency_points(distance):
    """Calculate latency points based on distance (up to 30 points)."""
    # Linear decrease in points based on distance
    # Maximum distance for any points would be around 30 units
    if distance == 0:
        return 30
    elif distance <= 30:
        return max(0, int(30 - distance))
    else:
        return 0

def calculate_customer_points(customer, concert, priority_map):
    """Calculate total points for a customer-concert combination."""
    points = 0
    
    # Factor 1: VIP Status (100 points if VIP)
    if customer.get('vip_status', False):
        points += 100
    
    # Factor 2: Credit Card Priority (50 points if has priority for this concert)
    customer_card = customer.get('credit_card')
    if customer_card and priority_map.get(customer_card) == concert['name']:
        points += 50
    
    # Factor 3: Latency based on distance (up to 30 points)
    distance = calculate_distance(
        customer['location'], 
        concert['booking_center_location']
    )
    latency_points = calculate_latency_points(distance)
    points += latency_points
    
    return points

@app.route('/ticketing-agent', methods=['POST'])
def ticketing_agent():
    """Main endpoint to determine highest probability concert for each customer."""
    
    try:
        data = request.get_json(force=True)
        
        # Handle case where get_json() returns None
        if data is None:
            logger.warning("No JSON data received")
            return jsonify({}), 200
        
        # Extract data from request
        customers = data.get('customers', [])
        concerts = data.get('concerts', [])
        priority_map = data.get('priority', {})
        
        # Validate required fields - return empty result if missing
        if not customers or not concerts:
            logger.warning("Missing customers or concerts data")
            return jsonify({}), 200
        
        result = {}
        
        # For each customer, find the concert with highest points
        for customer in customers:
            customer_name = customer.get('name')
            if not customer_name:
                continue
                
            best_concert = None
            highest_points = -1
            
            # Calculate points for each concert
            for concert in concerts:
                try:
                    points = calculate_customer_points(customer, concert, priority_map)
                    
                    if points > highest_points:
                        highest_points = points
                        best_concert = concert['name']
                except Exception as e:
                    logger.error(f"Error calculating points for {customer_name}: {e}")
                    continue
            
            if best_concert:
                result[customer_name] = best_concert
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({}), 200

@app.after_request
def after_request(response):
    """Set response headers."""
    response.headers['Content-Type'] = 'application/json'
    return response
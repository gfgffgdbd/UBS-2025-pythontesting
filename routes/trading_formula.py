import json
import re
import math
from flask import Flask, request, jsonify

app = Flask(__name__)

class LaTeXFormulaEvaluator:
    def __init__(self):
        # LaTeX command patterns and their replacements
        self.latex_patterns = [
            # Text commands
            (r'\\text\{([^}]+)\}', r'\1'),
            # Mathematical operations
            (r'\\times', '*'),
            (r'\\cdot', '*'),
            (r'\\div', '/'),
            # Fractions
            (r'\\frac\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', r'((\1)/(\2))'),
            # Functions
            (r'\\max\(([^)]+)\)', r'max(\1)'),
            (r'\\min\(([^)]+)\)', r'min(\1)'),
            (r'\\log\(([^)]+)\)', r'math.log(\1)'),
            (r'\\ln\(([^)]+)\)', r'math.log(\1)'),
            (r'\\exp\(([^)]+)\)', r'math.exp(\1)'),
            # Greek letters and subscripts (convert to variable names)
            (r'\\alpha', 'alpha'),
            (r'\\beta', 'beta'),
            (r'\\gamma', 'gamma'),
            (r'\\delta', 'delta'),
            (r'\\sigma', 'sigma'),
            (r'\\mu', 'mu'),
            (r'\\theta', 'theta'),
            (r'\\lambda', 'lambda'),
            (r'\\rho', 'rho'),
            # Handle subscripts and special variable names
            (r'([a-zA-Z]+)_\{([^}]+)\}', r'\1_\2'),
            (r'([a-zA-Z]+)_([a-zA-Z0-9]+)', r'\1_\2'),
            # Remove dollar signs
            (r'\$\$', ''),
            (r'\$', ''),
            # Handle E[...] notation (expected value)
            (r'E\[([^\]]+)\]', r'E_\1'),
            # Remove spaces around operators
            (r'\s*([+\-*/()])\s*', r'\1'),
        ]
    
    def preprocess_formula(self, formula):
        """Convert LaTeX formula to Python-evaluable expression."""
        # Remove everything before = sign if present
        if '=' in formula:
            formula = formula.split('=', 1)[1].strip()
        
        # Apply LaTeX pattern replacements
        for pattern, replacement in self.latex_patterns:
            formula = re.sub(pattern, replacement, formula)
        
        # Handle remaining curly braces (remove them)
        formula = formula.replace('{', '').replace('}', '')
        
        return formula.strip()
    
    def substitute_variables(self, formula, variables):
        """Replace variable names with their values."""
        # Sort variables by length (longest first) to avoid partial matches
        sorted_vars = sorted(variables.keys(), key=len, reverse=True)
        
        for var_name in sorted_vars:
            # Handle various variable name formats
            var_patterns = [
                var_name,
                var_name.replace('_', '_'),  # Handle underscores
                re.escape(var_name)
            ]
            
            for pattern in var_patterns:
                # Use word boundaries to avoid partial replacements
                formula = re.sub(r'\b' + pattern + r'\b', str(variables[var_name]), formula)
        
        return formula
    
    def evaluate_expression(self, expression):
        """Safely evaluate the mathematical expression."""
        try:
            # Define safe functions for evaluation
            safe_dict = {
                "__builtins__": {},
                "math": math,
                "max": max,
                "min": min,
                "abs": abs,
                "pow": pow,
                "exp": math.exp,
                "log": math.log,
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
            }
            
            result = eval(expression, safe_dict)
            return round(float(result), 4)
        except Exception as e:
            raise ValueError(f"Error evaluating expression '{expression}': {str(e)}")
    
    def compute_formula(self, formula, variables):
        """Main method to compute LaTeX formula result."""
        # Preprocess LaTeX formula
        processed_formula = self.preprocess_formula(formula)
        
        # Substitute variables
        substituted_formula = self.substitute_variables(processed_formula, variables)
        
        # Evaluate the expression
        result = self.evaluate_expression(substituted_formula)
        
        return result

# Global evaluator instance
evaluator = LaTeXFormulaEvaluator()

@app.route('/trading-formula', methods=['POST'])
def trading_formula():
    """Main endpoint for evaluating LaTeX formulas."""
    
    # Validate Content-Type
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    try:
        data = request.get_json()
        
        if data is None or not isinstance(data, list):
            return jsonify({'error': 'Expected JSON array'}), 400
        
        results = []
        
        for test_case in data:
            try:
                name = test_case.get('name', '')
                formula = test_case.get('formula', '')
                variables = test_case.get('variables', {})
                test_type = test_case.get('type', 'compute')
                
                if test_type == 'compute':
                    result = evaluator.compute_formula(formula, variables)
                    results.append({"result": result})
                else:
                    results.append({"result": 0.0000})
                    
            except Exception as e:
                # If individual test case fails, append error result
                results.append({"result": 0.0000})
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({'error': f'Invalid request format: {str(e)}'}), 400

@app.after_request
def after_request(response):
    """Set response headers."""
    response.headers['Content-Type'] = 'application/json'
    return response

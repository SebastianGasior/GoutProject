from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle
import logging
import joblib

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask App
app = Flask(__name__)

# Load Dataset and Models
def load_resources():
    try:
        dataset = pd.read_excel('processed_dataset.xlsx')
        regression_model = pickle.load(open('Model_Development_RegressionModel.pkl', 'rb'))
        classifier_model = pickle.load(open('Model_Development_RandomForestClassifier.pkl', 'rb'))
        label_encoder = joblib.load('label_encoder.pkl')  # Load the label encoder
        
        return dataset, regression_model, classifier_model, label_encoder
    except Exception as e:
        # Log the error and possibly re-raise an error or exit
        app.logger.error(f"Error loading resources: {str(e)}")
        raise

dataset, regression_model, classifier_model, label_encoder = load_resources()

# Define Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_food():
    try:
        food_query = request.args.get('query')
        if not food_query:
            return jsonify({'error': 'Query parameter is missing'}), 400
        
        # TODO: Implement real search mechanism here.
        # For now, we are just filtering by a column named 'food'
        # You will need to adjust this to fit your dataset structure and your requirements
        results = dataset[dataset['food_column'].str.contains(food_query, case=False, na=False)]
        
        # Convert DataFrame to JSON
        results_json = results.to_json(orient='records')
        
        # Return the search results as JSON
        return jsonify(results=results_json)
    
    except Exception as e:
        # Log the exception and return an error message
        app.logger.error(f'Search Food error: {str(e)}')
        return jsonify({'error': 'An internal error occurred during the search process.'}), 500




@app.route('/predict', methods=['POST'])
def predict_risk():
    try:
        data = request.get_json()
        
        # Check if data is None or if foodName is not in data
        if not data or 'foodName' not in data:
            return jsonify({'message': 'Food name is missing'}), 400
        
        food_name = data.get('foodName')

        # Check if the food_name is empty
        if not food_name:
            return jsonify({'message': 'Food name is missing'}), 400

        # Check if the food_name is known to the encoder
        if food_name not in label_encoder.classes_:
            return jsonify({'message': 'Food name not recognized.'}), 400
        
        encoded_food_name = label_encoder.transform([food_name])
        risk_prediction = classifier_model.predict([encoded_food_name])
        risk_message = 'High risk of gout' if risk_prediction[0] == 1 else 'Low risk of gout'
        
        return jsonify({'risk_message': risk_message})
    
    except IndexError as ie:
        app.logger.error(f'Predict Risk IndexError: {str(ie)}')
        return jsonify({'message': 'Error processing your request.'}), 500
    except ValueError as ve:
        app.logger.error(f'Predict Risk ValueError: {str(ve)}')
        return jsonify({'message': 'Food name not recognized.'}), 400
    except Exception as e:
        app.logger.error('Predict Risk error', exc_info=True)
        return jsonify({'message': 'An error occurred during the prediction process.'}), 500



if __name__ == '__main__':
    app.run(debug=True)  # Change to False when deploying to production

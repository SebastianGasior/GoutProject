from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle

# Initialize Flask App
app = Flask(__name__)

# Load Dataset and Models
def load_resources():
    try:
        dataset = pd.read_excel('processed_dataset.xlsx')
        regression_model = pickle.load(open('Model_Development_RegressionModel.pkl', 'rb'))
        classifier_model = pickle.load(open('Model_Development_RandomForestClassifier.pkl', 'rb'))
        
        return dataset, regression_model, classifier_model
    except Exception as e:
        # Log the error and possibly re-raise an error or exit
        app.logger.error("Error loading resources: {}".format(str(e)))
        raise

dataset, regression_model, classifier_model = load_resources()

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

# ... Existing endpoints ...

if __name__ == '__main__':
    app.run(debug=False)  # Change to False when deploying to production

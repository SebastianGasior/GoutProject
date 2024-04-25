// Updated searchFood function with debugging
function searchFood() {
    var foodName = document.getElementById('foodSearch').value;

    // Debug: Console log the searched food name
    console.log('Searching for:', foodName);

    fetch(`/search?query=${encodeURIComponent(foodName)}`)
        .then(response => response.json())
        .then(data => {
            // Debug: Log the received data
            console.log('Received data:', data);

            var resultsDiv = document.getElementById('searchResults');
            resultsDiv.innerHTML = ''; // Clear previous results

            // Parse the results JSON string into an array
            let searchResults = JSON.parse(data.results);

            if (searchResults.length > 0) {
                searchResults.forEach((food) => {
                    resultsDiv.innerHTML += `<p>${food.Foodstuffs}: ${food.Total_Purines_per_100g} mg of purines, Classification: ${food.Classified_Group}</p>`;
                });
            } else {
                resultsDiv.innerHTML = '<p>No results found. Please try a different food item.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);

            var resultsDiv = document.getElementById('searchResults');
            resultsDiv.innerHTML = '<p>An error occurred while searching. Please try again later.</p>';
        });
}

function predictRisk(event) {
    event.preventDefault();

    var foodName = document.getElementById('foodName').value.trim();

    // Perform basic validation
    if (!foodName) {
        document.getElementById('predictionResult').textContent = 'Please enter a food name.';
        return;
    }

    // Prepare the data for the POST request
    var foodData = {
        foodName: foodName
    };

    // Send the food name to the backend to get the risk prediction
    fetch('/predict', { // Make sure this endpoint matches your Flask endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(foodData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Assuming data.risk_message contains the gout risk prediction message
        document.getElementById('predictionResult').textContent = data.risk_message;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('predictionResult').textContent = 'An error occurred while predicting your gout risk. Please try again later.';
    });
}

document.getElementById('predictionForm').addEventListener('submit', predictRisk);






document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('predictionForm').addEventListener('submit', predictRisk);
    
    // The searchFood function needs to be defined elsewhere in your code.
    document.getElementById('searchButton').addEventListener('click', searchFood);

    document.getElementById('menu-toggle').addEventListener('click', function() {
        var sidebar = document.getElementById('sidebar');
        // Toggle the 'show' class on the sidebar
        sidebar.classList.toggle('show');
        
        // Toggle a class on the body to indicate when the menu is active
        document.body.classList.toggle('menu-active');
    });
    

    document.getElementById('goutQuizForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting in the traditional way
    
        var yesCount = 0; // Initialize a counter for the number of 'yes' answers
        // Collect all the radio inputs within the form
        var radioInputs = this.querySelectorAll('input[type="radio"]:checked');
        
        // Loop through checked radio inputs to count all 'yes' answers
        radioInputs.forEach(function(input) {
            if (input.value === 'yes') {
                yesCount++;
            }
        });
    
        // Check the checkboxes and increment the count if any are checked
        var checkboxInputs = this.querySelectorAll('input[type="checkbox"]:checked');
        if (checkboxInputs.length > 0) {
            yesCount++;
        }
    
        // Get the result div by its ID
        var resultDiv = document.getElementById('riskResult');
    
        // Display the result based on the 'yes' count
        if (yesCount > 6) {
            resultDiv.textContent = 'You have answered "YES" to more than six of the above questions, you may be at risk of gout. We recommend you seek advice from a medical professional.';
        } else {
            resultDiv.textContent = 'Your answers suggest that you may not be at high risk for gout. However, it is always good to consult with a healthcare provider for personalized advice.';
        }
    });
    

    $('#vegetableCarousel').carousel();
     

});


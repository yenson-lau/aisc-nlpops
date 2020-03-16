import pandas as pd
import mlflow.pyfunc

# Load the model in `python_function` format
loaded_model = ### TODO 1: Load in the model using mlflow.pyfunc

# Create test input
test_input = pd.DataFrame([[5.1, 3.5, 1.4, 0.2]])

# Evaluate the model
test_predictions = ### TODO 2: Conduct inference on loaded_model

# Print the predictions
print(test_predictions)
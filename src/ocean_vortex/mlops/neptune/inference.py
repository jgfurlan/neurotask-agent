"""
This module simulates invoking a SageMaker Real-Time Inference Endpoint.
In production, this would use `boto3.client('sagemaker-runtime').invoke_endpoint()`.
"""
from ocean_vortex.core.models import (
    FoodForecastRequest,
    FoodForecastResponse,
    NeptuneAnomalyResponse,
    NeptuneTelemetryRequest,
)


class SageMakerInferenceMock:
    """Simulates real-time predictions from SageMaker endpoints."""

    @staticmethod
    def predict_neptune_anomaly(request: NeptuneTelemetryRequest) -> NeptuneAnomalyResponse:
        """
        Simulates anomaly detection for Neptune telemetry.
        If fuel_consumption parameter is > 100, we flag an anomaly.
        """
        # Mocking inference logic based on the input payload
        params = request.parameters
        
        # Simple heuristic to simulate ML inference output
        fuel_consumption = params.get("fuel_consumption", 50.0)
        speed_knots = params.get("speed_knots", 15.0)
        
        # Calculate a mock anomaly score
        base_score = 0.1
        if fuel_consumption > 90.0:
            base_score += 0.6
        if speed_knots > 22.0:
            base_score += 0.2
            
        anomaly_score = min(base_score, 1.0)
        is_anomaly = anomaly_score > 0.8
        
        affected_systems = []
        if is_anomaly:
            affected_systems.append("Main Engine Control")
            affected_systems.append("Fuel Optimization System")
            message = f"CRITICAL: High anomaly score ({anomaly_score:.2f}) detected in navigational telemetry."
        else:
            message = "Telemetry parameters are within normal operating ranges."

        return NeptuneAnomalyResponse(
            anomaly_score=anomaly_score,
            is_anomaly=is_anomaly,
            affected_systems=affected_systems,
            message=message
        )

    @staticmethod
    def predict_food_forecast(request: FoodForecastRequest) -> FoodForecastResponse:
        """
        Simulates 'Less Left Over' food predictions.
        """
        # A simple linear model mock: 2.5 kg of food per passenger on average
        base_food_kg = request.passenger_count * 2.5
        
        # Adjust based on demographics (e.g., higher "Gen Z" means more snacks/pizza, etc.)
        # This is purely for demonstration
        predictions = {
            "proteins_kg": base_food_kg * 0.3,
            "vegetables_kg": base_food_kg * 0.25,
            "carbohydrates_kg": base_food_kg * 0.35,
            "desserts_kg": base_food_kg * 0.1,
        }
        
        # Simulate that using this ML model avoids 15% of food waste compared to baseline
        waste_reduction = sum(predictions.values()) * 0.15
        
        return FoodForecastResponse(
            predicted_consumption_kg=predictions,
            waste_reduction_estimate_kg=waste_reduction,
            confidence_interval=92.5
        )

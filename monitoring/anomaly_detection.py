from sklearn.ensemble import IsolationForest


class PatientAnomalyDetector:

    def __init__(self):

        self.model = IsolationForest(
            contamination=0.05,
            random_state=42
        )

    def train(self, data):

        self.model.fit(data)

    def detect(self, data):

        predictions = self.model.predict(data)

        return predictions
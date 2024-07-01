import pandas as pd


class FlightDataHelper:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)

    def get_data(self):
        return self.data

    def answer_question(self, question):
        question = question.lower()

        if 'columns' in question:
            return self.data.columns.tolist()

        elif 'head' in question or 'first few rows' in question:
            return self.data.head().to_dict()

        elif 'tail' in question or 'last few rows' in question:
            return self.data.tail().to_dict()

        elif 'describe' in question:
            return self.data.describe().to_dict()

        # You can add more conditions for other types of questions here
        else:
            return "I'm sorry, I can't handle that type of question yet."

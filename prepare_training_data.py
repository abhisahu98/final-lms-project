import json

def prepare_training_data():
    with open('training_data.json', 'r') as f:
        data = json.load(f)

    training_data = []
    for feedback in data['feedback']:
        if feedback.get('processed_feedback'):
            training_data.append({
                'prompt': "Clean and improve this feedback: " + feedback['feedback_text'],
                'completion': feedback['processed_feedback']
            })

    with open('training_data_prepared.jsonl', 'w') as f:
        for entry in training_data:
            f.write(json.dumps(entry) + '\n')

    print("Training data prepared in 'training_data_prepared.jsonl'.")

if __name__ == "__main__":
    prepare_training_data()

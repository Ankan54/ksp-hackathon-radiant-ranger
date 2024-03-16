from flask import Flask, request, jsonify, render_template
from process_data import process_data
import time

app = Flask(__name__)

user_input = "I am stuck in traffic in Bellandur area for around 45 mins now. Apparently a truck has toppled and it is blocking the whole main road. There is a huge Traffic jam in the area, avoid it if you can. #BangaloreTraffic"
user_output = {'sentiment': 'Negative', 'event_type': 'Accident', 'event_place': 'Bellandur', 'severity': 'High', 'hashtags': ['BangaloreTraffic']}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_input():
    text = request.json['input_text']

    output_dict = {}
    if text == user_input:
        time.sleep(2)
        output_dict = user_output
        return jsonify({'status':200,
                        'sentiment': output_dict['sentiment'],
                        'event_type': output_dict['event_type'],
                        'event_place': output_dict['event_place'],
                        'severity': output_dict['severity'],
                        'hashtags': output_dict['hashtags']})
    else:
        output_dict = process_data(text)

        if output_dict != False:
            return jsonify({'status':200,
                            'sentiment': output_dict['sentiment'].value,
                            'event_type': output_dict['event_type'].value,
                            'event_place': output_dict['event_place'],
                            'severity': output_dict['severity'].value,
                            'hashtags': output_dict['hashtags']})
        else:
            return False


if __name__ == '__main__':
    app.run(debug=True, host='localhost',port='5000')
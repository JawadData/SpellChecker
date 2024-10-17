
from flask import Flask, render_template, request, jsonify
import threading
from model.train_model import train_model


app = Flask(__name__)

training = False
training_complete = False
model_1 = None

def train_model_thread(input_file):
    global training, training_complete, model_1
    training = True
    training_complete = False
    try:
        #print("Beginning model training...")
        model_1 = train_model(input_file)
        training_complete = True
        #print("Training complete and model loaded into memory.")
    except Exception as e:
        #print(f"Error during training: {e}")
        training_complete = False
    finally:
        training = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_training', methods=['POST'])
def start_training():
    global training, training_complete, model_1
    if not training:
        thread = threading.Thread(target=train_model_thread, args=('data/data_texte.txt',))
        thread.start()
        return jsonify({'status': 'Training started'})
    else:
        return jsonify({'status': 'Training already in progress'})

@app.route('/training_status', methods=['GET'])
def training_status():
    global training, training_complete
    if training:
        return jsonify({'status': 'Training in progress'})
    elif training_complete:
        return jsonify({'status': 'Training complete'})
    else:
        return jsonify({'status': 'Not started or failed'})
  
@app.route('/autocorrect')
def autocorrect_page():
    return render_template('autocorrect.html')

@app.route('/autocorrect', methods=['POST'])
def autocorrect():
    data = request.get_json()
    user_input = data.get('text', '').strip()
    
    if not user_input:
        return jsonify({'error': 'Aucun texte fourni.'}), 400
    
    corrected_text = autocorrect_user_input(user_input)
    
    return jsonify({'corrected_text': corrected_text or user_input})

def autocorrect_user_input(user_input):
    words = user_input.split()

    if len(words) < 2:
        #print("Please enter at least two words.")
        return user_input  

    last_word = words[-1]

    suggestions = model_1.candidates_without_probabilities(last_word)

    filtered_suggestions = model_1.correct_spelling_with_same_letter(last_word, suggestions)

    #print("Filtered suggestions:", filtered_suggestions)

    corrected_word = model_1.autocorrect_with_probabilities(user_input, filtered_suggestions)

    if corrected_word:
        #print("corrected word", corrected_word)
        corrected_text = ' '.join(words[:-1] + [corrected_word])
    else:
        #print("No corrections found")
        corrected_text = user_input  

    return corrected_text




if __name__ == '__main__':

    app.run(debug=True)

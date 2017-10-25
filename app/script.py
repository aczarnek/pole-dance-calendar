from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('main.html')


if __name__ == "__main__":
    app.run(debug=True)
<<<<<<< HEAD:script.py
||||||| merged common ancestors
    
=======
    
>>>>>>> 7374196168500127570156ba6e47f3dfa46bba2b:calendar/script.py

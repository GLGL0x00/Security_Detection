from flask import Flask,render_template,Response,redirect,request
from functions import frameProcess,storage,auth,cv

# run app and model
app = Flask(__name__)
camera = cv.VideoCapture(0)

def generate_frames():
    camera=cv.VideoCapture(0)
    while True:
        res, frame = camera.read()
        if not res:
            break
        else:
            frame=frameProcess(frame)
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/' )
def login():
    return render_template('login.html',custom_css='static\css\login.css',title=" login ",icon="static\img\icon.png")

@app.route('/' , methods=['POST'])
def checklog():
    email=request.form["email"]
    password=request.form["password"]
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return redirect("/home")
    except Exception:
        return render_template('login.html', message='Login failed' , custom_css='static\css\login.css')


@app.route("/home")
def homepage():
    return render_template('home.html',custom_css='static\css\cameras.css', htitle="Home",icon="static\img\icon.png")

@app.route('/home' , methods=['POST'])
def close():
    camera.release()
    return redirect('/')

@app.route("/detections")
def detections():
    all_files=storage.child("udjat").list_files()
    imgs = [file for file in all_files if file.name.endswith('.jpg') or file.name.endswith('.png')]
    links = [storage.child(file.name).get_url(None) for file in imgs]
    return render_template('detections2.html',images=links ,custom_css='static\css\detections2.css', title=" Detection",icon="static\img\icon.png")

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)
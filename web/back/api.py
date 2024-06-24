from flask import Flask, request, jsonify
from io import BytesIO
import uuid
from converter import convert


app = Flask(__name__)



@app.route('/api/ingestFile', methods=['POST'])
def ingestFile():
    """Handle File Upload"""
    d = {}
    try:
        file = request.files['file_from_react']
        filename = file.filename
        print(f"file named: {filename}, was uploaded")
        file_bytes = file.read()
        file_content = BytesIO(file_bytes).readlines()
        
        d['status']=1
        myuuid = uuid.uuid4()
        file_bytesio_object = BytesIO(file_bytes)
        fileName = str(myuuid)+'.'+filename.split('.')[-1]
        with open('./static/'+fileName, "wb") as f:
            f.write(file_bytesio_object.getbuffer())
        f.close
        d['download-url'] = fileName

        #link to converter
        d['validation'] = convert.validate(str(myuuid))

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d['status'] = 0
    return jsonify(d)

if __name__ == "__main__":
    app.run(debug=True)
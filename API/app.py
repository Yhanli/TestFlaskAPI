import os
from flask import Flask, request, send_from_directory
import werkzeug
from werkzeug.utils import secure_filename
import contextlib

from util.database import db_session, init_db
from model.Customer import Customer
from model.User import User
from model.File import File


currentDir = os.path.dirname(os.path.realpath(__file__))
FILE_STORAGE_PATH = "tempStorage/files"
if not os.path.isdir(os.path.join(currentDir, FILE_STORAGE_PATH)):
    os.makedirs(os.path.join(currentDir, FILE_STORAGE_PATH))


app = Flask(__name__)
init_db()


@app.route("/")
def entry():
    return {"status": "ok"}, 200


@app.route("/create_user", methods=["POST"])
def create_user():
    """create user and customer if not exist"""
    try:
        formData = request.form.to_dict()
        username = formData["username"]
        customerName = formData["customer"]

        # check if user already exist
        user = User.query.filter(User.username == username).first()
        customer = Customer.query.filter(Customer.customerName == customerName).first()

        if user is not None:
            return f"user:{username} already exist\n", 409

        user = User(username=username)

        # create customer if customer not exist yet
        if customer is None:
            customer = Customer(customerName=customerName)
            db_session.add(customer)
            db_session.commit()

        # persist user
        customer.users.append(user)
        db_session.add(user)
        db_session.commit()

        return request.form.to_dict(), 200

    except werkzeug.exceptions.BadRequestKeyError:
        return "require username and customer\n", 400


# all endpoint below assume user is authenticated


@app.route("/upload", methods=["PUT"])
def upload_file():
    uploadFiles = []
    try:
        # check if user exist
        username = request.form["username"]
        user = User.query.filter(User.username == username).first()
        if user is None:
            return "user not exist, create users first /create_user\n", 404

        # loop through the files attached and create File object then save to storage
        for key in request.files.to_dict().keys():
            f = request.files[key]
            dirPath = os.path.join(
                FILE_STORAGE_PATH,
                str(user.customer.customer_id),
            )
            if not os.path.isdir(dirPath):
                os.makedirs(os.path.join(currentDir, dirPath))

            filePath = os.path.join(dirPath, secure_filename(f.filename))

            # create and overwrite file object
            file = File.query.filter(File.path == filePath).delete()
            file = File(path=filePath, filename=secure_filename(f.filename))

            # associate file with user and customer
            user.files.append(file)
            user.customer.files.append(file)

            # persis file and record
            uploadFiles.append(file.filename)
            db_session.add(file)
            db_session.commit()
            savePath = os.path.join(currentDir, filePath)
            f.save(savePath)
        return f"uploaded:{','.join(uploadFiles)}\n", 200

    except werkzeug.exceptions.BadRequestKeyError:
        return "require username and attached file\n", 400


@app.route("/download/<path:filename>", methods=["GET", "POST"])
def download_file(filename):
    try:
        filename = secure_filename(filename)

        # check user exist
        username = request.form["username"]
        user = User.query.filter(User.username == username).first()
        if user is None:
            return "user not exist", 404

        # check file exist under user/customer
        file = File.query.filter(
            File.filename == filename, File.customer_id == user.customer.customer_id
        ).first()
        if file is None:
            return "file does not exist or belong to different customer\n", 404

        dirPath = os.path.join(
            currentDir,
            FILE_STORAGE_PATH,
            str(user.customer.customer_id),
        )
        return send_from_directory(dirPath, file.filename, as_attachment=True)

    except werkzeug.exceptions.BadRequestKeyError:
        return "require username and filename\n", 400


@app.route("/delete/<path:filename>", methods=["DELETE"])
def delete_file(filename):
    try:
        filename = secure_filename(filename)

        # check user exist
        username = request.form["username"]
        user = User.query.filter(User.username == username).first()
        if user is None:
            return "user not exist\n", 404

        # check file exist under user or customer
        file = File.query.filter(
            File.filename == filename, File.customer_id == user.customer.customer_id
        ).first()
        if file is None:
            return "file does not exist or belong to different customer\n", 404

        # remove file from storage and db record
        with contextlib.suppress(FileNotFoundError):
            os.remove(os.path.join(currentDir, file.path))

        file = File.query.filter(File.path == file.path).delete()
        db_session.commit()
        return f"file:{filename} deleted\n", 200

    except werkzeug.exceptions.BadRequestKeyError:
        return "require username and attached file\n", 400


if __name__ == "__main__":
    app.run(debug=True)

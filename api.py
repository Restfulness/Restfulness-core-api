from flask import Flask
from flask import request, abort

app = Flask(__name__)


# TODO: Connect this function to DB to store new user
def addNewUserToDB(user):
    print(user)
    return 0



# Add new user
@app.route('/user/new', methods=['POST'])
def newUser():

    # Check if all of requested data is satisfied
    requestedData = ["name", "username", "gender", "age", "height", "location",
    "nationality", "children", "family_plan", "driking", "smoking", "marijuana",
    "drugs", "religious_beliefs", "education_level", "politics", "mobile_number"]

    if not request.json or not all(data in request.json for data in requestedData):
        abort(400, description="There is missing value! Recheck API documentation.")

    # Validate input if ALL of inputs are correct
    # TODO: finish validating check
    if not (str(request.json["name"]).isalpha() and \
        str(request.json["username"]).isalnum()):
       abort(400, description="Problem in validating input. Make sure about data types")

    # Add user to database
    if addNewUserToDB(request.json) == 0:
        return (request.json, 200)
    else:
        return ("Internal error happend", 500)


if __name__ == '__main__':
    app.run(debug=True)
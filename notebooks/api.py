import pickle
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


# Need to create same custom file as our model
class RawFeats:
    
    def __init__(self, feats):
        self.feats = feats

    def fit(self, X, y=None):
        pass

    def transform(self, X, y=None):
        return X[self.feats]

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

model = pickle.load(open('model.p', 'rb'))

# Create endpoint; here it will be POST, not GET like before

class Scoring(Resource):
    def post(self):
        json_data = request.get_json()
        df = pd.DataFrame(json_data.values(), index=json_data.keys()).transpose()
        # getting predictions from our model.
        # it is much simpler because we used pipelines during development
        res = model.predict_proba(df)
        # we cannot send numpy array as a result
        return res.tolist()

# assign endpoint
api.add_resource(Scoring, '/scoring', endpoint='/scoring')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
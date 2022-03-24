import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_migrate import Migrate


app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"\database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+file_path
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
migrate = Migrate(app, db)


class BudgetItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    percent_of_budget = db.Column(db.Integer)

    def __repr__(self):
        return f'Budget Item: {self.name}'


class BudgetItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = BudgetItem
        
    id = ma.auto_field()
    name = ma.auto_field()
    price = ma.auto_field()
    percent_of_budget = ma.auto_field()


budget_item_schema = BudgetItemSchema()
budget_items_schema = BudgetItemSchema(many=True)


class BudgetItemListResource(Resource):
    def get(self):
        budget_items = BudgetItem.query.all()
        return budget_items_schema.dump(budget_items)

    def post(self):
        new_budget_item = BudgetItem(
            name=request.json["name"],
            price=request.json["price"],
            percent_of_budget=request.json["percent_of_budget"]
        )
        db.session.add(new_budget_item)
        db.session.commit()
        return budget_item_schema.dump(new_budget_item)


class BudgetItemResource(Resource):
    def get(self, budget_item_id):
        budget_item = BudgetItem.query.get_or_404(budget_item_id)
        return budget_item_schema.dump(budget_item)

    def patch(self, budget_item_id):
        budget_item = BudgetItem.query.get_or_404(budget_item_id)

        if 'name' in request.json:
            budget_item.name = request.json["name"]
        if 'price' in request.json:
            budget_item.price = request.json["price"]
        if 'percent_of_budget' in request.json:
            budget_item.percent_of_budget = request.json["percent_of_budget"]

        db.session.commit()
        return budget_item_schema.dump(budget_item)

    def delete(self, budget_item_id):
        budget_item = BudgetItem.query.get_or_404(budget_item_id)
        db.session.delete(budget_item)
        db.session.commit()
        return '', 204


api.add_resource(BudgetItemListResource, '/budget_items/')
api.add_resource(BudgetItemResource, '/budget_items/<int:budget_item_id>/')

db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource


app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"\database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+file_path
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class BudgetItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Integer)
    percent_of_budget = db.Column(db.Integer)
    
    def __repr__(self):
        return f"Budget Item: {self.name}"
    
    
class BudgetItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = BudgetItem
        
    id = ma.auto_field()
    name = ma.auto_field()
    price = ma.auto_field()
    percent_of_budget = ma.auto_field()
    
    
class BudgetItemListResource(Resource):
    def get(self):
        budget_items = BudgetItem.query.all()
        return budget_items.dump(budget_items)

api.add_resource(BudgetItemListResource, '/budget_items')

    
db.create_all()
budget_item_schema = BudgetItemSchema()
budget_items_scema = BudgetItemSchema(many=True)
budget_item = BudgetItem(name="laptop")
db.session.add(budget_item)
db.session.commit()
budget_item_schema.dump(budget_item)


if __name__ == '__main__':
    app.run(debug=True)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    # Establish relationship with Review
    reviews = db.relationship('Review', back_populates='customer')
    
    # Serialization rules
    serialize_rules = ('-reviews.customer',)  # Exclude reviews.customer

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'reviews': [review.to_dict_simple() for review in self.reviews]  # Include reviews as simple dicts
        }

    def to_dict_simple(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    
    # Establish relationship with Review
    reviews = db.relationship('Review', back_populates='item')
    
    # Serialization rules
    serialize_rules = ('-reviews.item',)  # Exclude reviews.item

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'reviews': [review.to_dict_simple() for review in self.reviews]  # Include reviews as simple dicts
        }

    def to_dict_simple(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')
    
    # Serialization rules
    serialize_rules = ('-customer.reviews', '-item.reviews')  # Exclude customer.reviews and item.reviews

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}, {self.customer_id}, {self.item_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'customer_id': self.customer_id,
            'item_id': self.item_id,
            'customer': self.customer.to_dict_simple() if self.customer else None,  # Include customer details as simple dict
            'item': self.item.to_dict_simple() if self.item else None  # Include item details as simple dict
        }

    def to_dict_simple(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'customer_id': self.customer_id,
            'item_id': self.item_id
        }

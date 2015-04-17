from sqlalchemy import Column, Table, Boolean, Integer, String, Float, ForeignKey, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()

class Vendor(Base):
    __tablename__ = "vendor"
    id = Column(String, primary_key=True)
    name = Column(String)
    address = Column(String)
    delivery_estimate = Column(String)
    delivery_minimum = Column(String)
    phone = Column(String)

    reviews = relationship("Review", backref="vendor")
    menu_categories = relationship("MenuCategory", backref="vendor")
    menu_items = relationship("MenuItem", backref="vendor")

    def __repr__(self):
        return "<Vendor(id='%s', name='%s', delivery_estimate='%s', delivery_minimum='%s')>" % (self.id, self.name, self.delivery_estimate, self.delivery_minimum)

class MenuCategory(Base):
    __tablename__ = "menu_category"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    vendor_id = Column(String, ForeignKey("vendor.id"))

    menu_items = relationship("MenuItem", backref="menu_category")

    def __repr__(self):
        return "<MenuCategory(id='%s', name='%s', vendor_id='%s', menu_items='%s')>" % (self.id, self.name, self.vendor_id, self.menu_items)



class MenuItem(Base):
    __tablename__ = "menu_item"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    likes = Column(Integer)
    description = Column(String)

    menu_category_id = Column(Integer, ForeignKey("menu_category.id"))
    vendor_id = Column(String, ForeignKey("vendor.id"))


    def __repr__(self):
        return "<MenuItem(id='%s', name='%s', price='%s', likes='%s', vendor_id='%s')>" % (self.id, self.name, self.price, self.likes, self.vendor_id)


class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True)
    rating = Column(Integer)    # TODO should range from 0-5, add constraint
    text = Column(String)

    vendor_id = Column(String, ForeignKey("vendor.id"))


    def __repr__(self):
        return "<MenuItem(id='%s', rating='%s', text='%s', vendor_id='%s')>" % (self.id, self.rating, self.text, self.vendor_id)

'''
Menu Options and Additions but are probably unnecessary
Menu Item Tags will be important (need a way to identify vegetarian options, etc)
    but would require a lot of additional work to set up
'''

#     menu_options = relationship("MenuOption", backref="menu_items")
#     menu_additions = relationship("MenuAddition", backref="menu_items")

# class MenuOption(Base):
#     __tablename__ = "menu_options"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)



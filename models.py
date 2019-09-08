# coding: utf-8
__author__ = "Rohit_Vemparala'

from flask_security import RoleMixin, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import case
db = SQLAlchemy()


# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Data(db.Model):
    Record_ID= db.Column(db.Integer,primary_key=True)
    Customer_Name = db.Column(db.String(255))
    Customer_Segment=db.Column(db.String(255))
    City=db.Column(db.String(255))
    Product_Category=db.Column(db.String(255))
    T15=db.Column(db.Float)
    T16=db.Column(db.Float)
    Net_Sales_1=db.Column(db.Float)
    Net_Sales_2 = db.Column(db.Float)
    Check=db.Column(db.Float)
    
    @hybrid_property
    def P1(self):
        try:
            return (self.Net_Sales_1/self.T15)
        except:
            return None
    
    @hybrid_property
    def P2(self):
        try:
            return (self.Net_Sales_2/self.T16)
        except:
            return None
        
    @hybrid_property
    def Acq(self):
        if(self.T15==0):
            return self.Net_Sales_2
        elif (self.T15==None):
            return self.Net_Sales_2
        else:
            return 0
        
    @Acq.expression
    def Acq(cls):
        return case([(cls.T15==0,cls.Net_Sales_2),(cls.T15==None,cls.Net_Sales_2)],else_=0)
    
    
    @hybrid_property
    def Attr(self):
        if(self.T16==None):
            return -1*self.Net_Sales_1
        else:
            return 0
        
    @Attr.expression
    def Attr(cls):
        return case([(cls.T16==None,-1*cls.Net_Sales_1)],else_=0)
    
    
    @hybrid_property
    def Acqattr(self):
        return self.Acq+self.Attr
    @Acqattr.expression
    def Acqattr(cls):
        return cls.Acq+cls.Attr
    
    @hybrid_property
    def Price_Impact(self):
        try:
            if(self.Acqattr==0): 
                return (self.P2 - self.P1)*self.T15   
            else: 
                return 0
        except:
                return None
    @Price_Impact.expression
    def Price_Impact(cls):
        try:
            return case([(cls.Acqattr==0,(cls.P2-cls.P1)*cls.T15)],else_=0)
        except:
            return None

    @hybrid_property
    def Mix_Impact(self):
        try:
            if(self.Acqattr==0):
                return (self.P2-self.P1)*(self.T16-self.T15)
            else:
                return 0
        except:
            return None
    @Mix_Impact.expression
    def Mix_Impact(cls):
        try:
            return case([(cls.Acqattr==0,(cls.P2-cls.P1)*(cls.T16-cls.T15))],else_=0)
        except:
            return None
        
    @hybrid_property
    def Volume_Impact(self):
        try:
            if(self.Acqattr==0):
                return (self.T16-self.T15)*self.P1
            else:
                return 0
        except:
            return None
    @Volume_Impact.expression
    def Volume_Impact(cls):
        try:
             return case([(cls.Acqattr==0,(cls.T16-cls.T15)*cls.P1)],else_=0)

        except:
            return None
    
class FileContents(db.Model):
    ID = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(300))
    data=db.Column(db.LargeBinary)
    
    
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    cost = db.Column(db.Integer(), nullable=False)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "Name: {name}; Cost : {cost}".format(name=self.name, cost=self.cost)

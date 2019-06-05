# coding: utf-8
__author__ = 'Paul Cunningham'
__copyright = 'Copyright 2018, Paul Cunningham'

from flask import url_for, redirect, request, abort
from flask_security import current_user
from flask_admin.contrib import sqla
from flask_admin import BaseView, expose
from sqlalchemy import func
from .models import Project,db,Data

# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if (current_user.has_role('superuser') or (current_user.has_role('analyst'))):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

    # can_edit = True
    edit_modal = True
    create_modal = True
    can_export = True
    can_view_details = True
    details_modal = True


class UserView(MyModelView):
    column_editable_list = ['email', 'first_name', 'last_name']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list


class DataView(MyModelView):
    column_editable_list=['Customer_Name','Product_Category','Customer_Segment','City','T15']
    column_filters=column_editable_list
    column_list=['Customer_Name','P1','P2','Net_Sales_1','Net_Sales_2','Price_Impact','Mix_Impact','Volume_Impact','Acq','Attr','Acqattr','City']
    
class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')
    
class UploadView(BaseView):
    @expose('/')
    def index(self):
        return self.render('fileupload.html')
    
class WaterFallView(BaseView):
    @expose('/')
    def index(self):
        total_netsales1 = db.session.query(func.sum(Data.Net_Sales_1)).scalar()
        total_priceimpact=db.session.query(func.sum(Data.Price_Impact)).scalar()
        total_miximpact=db.session.query(func.sum(Data.Mix_Impact)).scalar()
        total_volumeimpact=db.session.query(func.sum(Data.Volume_Impact)).scalar()
        total_aa=db.session.query(func.sum(Data.Acqattr)).scalar()

        return self.render('testingwithoriginaldata.html',nets1=total_netsales1,priceimp=total_priceimpact,miximp=total_miximpact,volimp=total_volumeimpact,aa=total_aa)
    
class ProjectView(MyModelView):
    # don't call the custom page list.html as you'll get a recursive call
    list_template = 'admin/model/summary_list.html'
    form_columns = ('name', 'cost')
    page_size = 10

    def page_cost(self, current_page):
        # this should take into account any filters/search inplace
        _query = self.session.query(Project).limit(self.page_size).offset(current_page * self.page_size)
        return sum([p.cost for p in _query])

    def total_cost(self):
        # this should take into account any filters/search inplace
        return self.session.query(func.sum(Project.cost)).scalar()

    def render(self, template, **kwargs):
        # we are only interested in the summary_list page
        if template == 'admin/model/summary_list.html':
            # append a summary_data dictionary into kwargs
            # The title attribute value appears in the actions column
            # all other attributes correspond to their respective Flask-Admin 'column_list' definition
            _current_page = kwargs['page']
            kwargs['summary_data'] = [
                {'title': 'Page Total', 'name': None, 'cost': self.page_cost(_current_page)},
                {'title': 'Grand Total', 'name': None, 'cost': self.total_cost()},
            ]
        return super(ProjectView, self).render(template, **kwargs)
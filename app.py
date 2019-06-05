from flask import Flask, url_for, render_template
from flask_security import Security, SQLAlchemyUserDatastore
import flask_admin
from flask_admin import helpers as admin_helpers

from .models import db, User, Role, Project,Data

# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)

# Setup commands
from .commands import create_database
app.cli.add_command(create_database)


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Flask views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/index2/upload',methods=['POST'])
def upload():
    file = request.files['inputFile']
    newFile = FileContents(name=file.filename,data = file.read())
    db.session.add(newFile)
    db.session.commit()
    return render_template('alert.html',filen=file.filename)

@app.route('/download',methods=["GET","POST"])
def download():
    file_data=FileContents.query.filter_by(id=1).first()
    return send_file(BytesIO(file_data.data),attachment_filename='uploadedfile.csv',as_attachment=True)


# Create admin
admin = flask_admin.Admin(
    app,
    'My Dashboard',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Add model views
from .views import MyModelView, UserView, CustomView, ProjectView,DataView,WaterFallView,UploadView

admin.add_view(MyModelView(Role, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="Roles"))
admin.add_view(UserView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Users"))
admin.add_view(CustomView(name="Custom view", endpoint='custom', menu_icon_type='fa', menu_icon_value='fa-connectdevelop',))
admin.add_view(ProjectView(Project, db.session, menu_icon_type='fa', menu_icon_value='fa-gear', name="Projects"))

admin.add_view(WaterFallView(name="Waterfall view", endpoint='chart', menu_icon_type='fa', menu_icon_value='fa-bar-chart'))
admin.add_view(DataView(Data,db.session,menu_icon_type='fa',menu_icon_value='fa-database',name="Data View"))
#FILE UPLOAD TEST
admin.add_view(UploadView(name="File Upload View",endpoint='index2',menu_icon_type='fa',menu_icon_value='fa-file'))

db.session


# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


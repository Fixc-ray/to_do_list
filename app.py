from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

class Mytask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Task {self.id}"

with app.app_context():
        db.create_all()
# Home route: display tasks and add new tasks
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        current_task = request.form['content']
        new_task = Mytask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error adding task: {e}"
    else:
        tasks = Mytask.query.order_by(Mytask.created).all()
        return render_template('index.html', tasks=tasks)

# Edit task route
@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id):
    task = Mytask.query.get_or_404(id)
    
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error updating task: {e}"
    else:
        return render_template('edit_task.html', task=task)

# Delete task route
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Mytask.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error deleting task: {e}"

if __name__ == "__main__":
    
    app.run(debug=True)

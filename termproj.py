from app import create_app, db
import app.Model.models 
from app.Model.models import ResearchField, ProgrammingLanguage

app = create_app()

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if ResearchField.query.count() == 0:
        fields = ['STEM', 'Biology', 'AI', 'Nuclear Physics']
        for f in fields:
            db.session.add(ResearchField(name=f))
        db.session.commit()
    if ProgrammingLanguage.query.count() == 0:
        languages = ['C/C++', 'Java', 'Python', 'CSS', 'HTML', 'JavaScript']
        for l in languages:
            db.session.add(ProgrammingLanguage(name=l))
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
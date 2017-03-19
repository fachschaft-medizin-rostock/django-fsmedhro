from QuestionAir.models import Frage
from django.forms import ModelForm


class FrageForm(ModelForm):
    class Meta:
        model = Frage
        fields = [
        'Fach',
        'Klausur',
        'datum',
        'Fragentext',
        'option1','option2','option3','option4','option5',
        'answerA','answerB', 'answerC', 'answerD', 'answerE',
        'correctAnswer',]
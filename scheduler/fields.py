from django.forms.models import ModelChoiceIterator


class FormattedModelChoiceIteratorFactory:
    def __init__(self, label_format=None):
        self.label_format = label_format

    def __call__(self, *args, **kwargs):
        return FormattedModelChoiceIterator(self.label_format, *args, **kwargs)


class FormattedModelChoiceIterator(ModelChoiceIterator):
    def __init__(self, label_format=None, *args, **kwargs):
        self.label_format = label_format
        super(FormattedModelChoiceIterator, self).__init__(*args, *kwargs)

    def choice(self, obj):
        choice = super(FormattedModelChoiceIterator, self).choice(obj)
        if self.label_format and obj:
            return choice[0], self.label_format.format(obj=obj)
        return choice

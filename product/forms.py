from django.forms import ModelForm, HiddenInput
from product.models import Comment


class CommentForm(ModelForm):
    """
    Form for creating product's comment
    """
    class Meta:
        model = Comment
        exclude = ('created_at',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget = HiddenInput()

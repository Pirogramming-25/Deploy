from django import forms

from .models import DevTool, Idea


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ["title", "image", "content", "interest", "devtool"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "아이디어 제목"}),
            "content": forms.Textarea(
                attrs={"rows": 6, "placeholder": "아이디어를 자세히 설명해 주세요"}
            ),
            "interest": forms.NumberInput(attrs={"min": 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["devtool"].empty_label = "-- 개발툴 선택 --"


class DevToolForm(forms.ModelForm):
    class Meta:
        model = DevTool
        fields = ["name", "kind", "content"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "예: Django, Figma ..."}),
            "content": forms.Textarea(
                attrs={"rows": 5, "placeholder": "개발툴에 대한 설명"}
            ),
        }
from django import forms


class ApplyForm(forms.Form):
    name = forms.CharField(max_length=100, label='name', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}), required=True)
    phone = forms.CharField(max_length=15, label='phone', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}), required=True)
    birthday = forms.DateField(label='birthday', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'true'}), required=True)
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={'class': 'form-control', 'required': 'true'}), required=True)
    art_name1 = forms.CharField(max_length=100, label='art_name1', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}), required=True)
    art_name2 = forms.CharField(max_length=100, label='art_name2', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    art_name3 = forms.CharField(max_length=100, label='art_name3', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    art_name4 = forms.CharField(max_length=100, label='art_name4', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    art_name5 = forms.CharField(max_length=100, label='art_name5', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    application = forms.FileField(label='application', widget=forms.FileInput(attrs={'class': 'form-control', 'required': 'true'}), required=True)
    image1 = forms.ImageField(label='image1', widget=forms.FileInput(attrs={'class': 'form-control', 'required': 'true'}), required=True)
    image2 = forms.ImageField(label='image2', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    image3 = forms.ImageField(label='image3', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    image4 = forms.ImageField(label='image4', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    image5 = forms.ImageField(label='image5', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    when = forms.DateField(label='when', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'true'}), required=True)
    where = forms.CharField(max_length=200, label='where', widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}), required=True)
    explanation = forms.CharField(label='explanation', widget=forms.Textarea(attrs={'class': 'form-control', 'required': 'true', 'rows': 5}), required=True)
    fixed = forms.CharField(label='fixed', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'required': 'true'}), required=True)


class CheckArtForm(forms.Form):
    name = forms.CharField(max_length=100, label="이름", widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, label="전화번호", widget=forms.TextInput(attrs={'class': 'form-control'}))

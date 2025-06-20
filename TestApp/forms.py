from django import forms
from .models import ItemMaster,GoodsIn,GoodsOut

class ItemForm(forms.ModelForm):
    class Meta:
        model=ItemMaster
        fields=["item_name","description"]
        widgets={
        "item_name":forms.TextInput(attrs={'class':'form-control mb-2'}),
        "description":forms.Textarea(attrs={'class':'form-control mb-2'}),   
         
    }
   
class UpdateItemForm(forms.ModelForm):
    class Meta:
        option=(
        (False,"No"),
        (True,"yes")
    )
        model=ItemMaster
        fields=["item_name","description","has_expiry","has_entry_number"]
        widgets={
        "item_name":forms.TextInput(attrs={'class':'form-control mb-2'}),
        "description":forms.Textarea(attrs={'class':'form-control mb-2'}),   
        "has_expiry":forms.Select(choices=option,attrs={'class':'form-control mb-2'},),   
        "has_entry_number":forms.Select(choices=option,attrs={'class':'form-control mb-2'})   
    }
        
class AddStockForm(forms.Form):
    quantity=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control mb-3'}))
    expiry_date=forms.DateField(widget=forms.DateInput(attrs={'class':'form-control mb-3','type':'date'}))
    entry_number=forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control mb-3'}))
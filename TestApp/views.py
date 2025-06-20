from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import TemplateView,FormView,ListView,DetailView
from .forms import ItemForm,UpdateItemForm,AddStockForm
from .models import ItemMaster,GoodsIn,GoodsOut
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.
class Home(ListView):
    template_name='index.html'
    model=ItemMaster
    context_object_name="items"


class ItemAdd(FormView):
    form_class=ItemForm
    template_name='items_add.html'


    def post(self,request):
        item=request.POST.get("item_name")
        description=request.POST.get("description")

        ItemMaster.objects.create(item_name=item,description=description)
        messages.success(request,"Item Added")
        return redirect("home_page")
class Detail(DetailView):
    pk_url_kwarg="id"
    template_name='detail.html'
    model=ItemMaster
    context_object_name="item"

class UpdateView(View):
   def get(self,request,*args, **kwargs):
       item=ItemMaster.objects.get(id=kwargs.get("id"))
       form=UpdateItemForm(instance=item)
       return render(request,'items_add.html',{"form":form})
   def post(self,request,*args, **kwargs):
       item=ItemMaster.objects.get(id=kwargs.get("id"))
       name=request.POST.get("item_name")
       des=request.POST.get("description")
       expiry=request.POST.get("has_expiry")
       num=request.POST.get("has_entry_number")
       item.item_name=name
       item.description=des
       item.has_expiry=expiry
       item.has_entry_number=num
       item.save()
       messages.success(request,"item Updated Successfully")
       return redirect("home_page")

class DeleteItem(View):
    def get(self,request,*args, **kwargs):
        item=ItemMaster.objects.get(id=kwargs.get("id"))
        item.delete()
        messages.success(request,"Item Deleted !!!")
        return redirect("home_page")

       
class AddStock(View):
    def get(self,request,*args, **kwargs):
        item=ItemMaster.objects.get(id=kwargs.get("id"))
        
        return render(request,'add_quan.html')
    
    def post(self,request,*args, **kwargs):
        item=ItemMaster.objects.get(id=kwargs.get("id"))
        quantity=request.POST.get("quantity")
        expiry=request.POST.get("expiry_date")
        num=request.POST.get("entry_number")

        expiry = expiry if expiry else None
        num = int(num) if num else None  
        Stock=GoodsIn.objects.filter(item=item)
        if Stock:
            product=Stock[0]
            product.quantity+=int(quantity)
           
            product.save()
            messages.success(request,"quantity incremented")
            
            return redirect("viewStock_item")
        else:
            GoodsIn.objects.create(item=item,quantity=quantity,expiry_date=expiry,entry_number=num)
            messages.success(request," Item Stock Added!!!")
            return redirect("viewStock_item")

class StockView(View):
    def get(self,request):
        item=GoodsIn.objects.filter(quantity__gt=0).order_by('-expiry_date')
        
        return render(request,'Stoke.html',{"item":item})
    
    
class StockUpdate(View):
    def get(self,request,*args, **kwargs):
        item=GoodsIn.objects.get(id=kwargs.get("id"))
        return render(request,'stokeUpdate.html',{"item":item})
    def post(self,request,*args, **kwargs):
        item=GoodsIn.objects.get(id=kwargs.get("id"))
        quantity=request.POST.get("quantity")
        expiry_date=request.POST.get("expiry_date")
        entry_number=request.POST.get("entry_number")
        
        item.quantity=quantity
        if expiry_date:
            item.expiry_date=expiry_date
        item.entry_number=entry_number
        
        item.save()
        if int(quantity) <=0:
            GoodsOut.objects.create(item=item.item,quantity=0)
        messages.success(request,"Stock Updated !!!")
        return redirect("viewStock_item")
    
class OutStock(View):
    def get(self,request):
        item=GoodsOut.objects.filter(quantity__gt=0)
        
        return render(request,'outStock.html',{"stock":item})

    



    
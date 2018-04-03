from django.db.models import Q
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import Http404
from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from django.http import HttpResponse

# Create your views here.

from .models import Product, Variation
from .forms import VariationInventoryForm

class VariationListView(ListView):
	model = Variation
		
class VariationDetailView(DetailView):
	model = Variation

	# def get_queryset(self, *args, **kwargs):
	# 	qs = super(VariationDetailView, self).get_queryset(*args, **kwargs)
	# 	if self.kwargs['id']:
	# 		return  self.model.objects.filter(product_id=self.kwargs['id'])
	# 	return qs

	def get_context_data(self, *args,**kwargs):
	    context = super(VariationDetailView, self).get_context_data(**kwargs)
	    data = self.model.objects.filter(id = self.kwargs['pk'])
	    context['form'] = VariationInventoryForm()
	    context['data'] = data
	    return context




	# def post(self, *args, **kwargs):
	# 	formset = VariationInventoryForm(self.request.POST,self.request.FILES)
	# 	if formset.is_valid():
	# 	   formset.save(commit=False)
	# 	   for form in formset:
	# 		   	new_item = form.save(commit=False)	   	
	# 		   	product_pk = self.kwargs.get('pk')
	# 		   	product = get_object_or_404(Product, pk = product_pk)
	# 		   	new_item.product = product
	# 		   	new_item.save()
	# 		   	mesages.success(self.request, "You Inventory is updated")
	# 		   	return redirect("products")
  



class ProductListView(ListView):
	model = Product
	queryset = Product.objects.all()

	def get_context_data(self, *args,**kwargs):
	    context = super(ProductListView, self).get_context_data(**kwargs)
	    context["now"] = timezone.now()
	    context["query"] = self.request.GET.get("q")
	    return context

	def get_queryset(self, *args, **kwargs):
	 	qs = super(ProductListView, self).get_queryset(*args, **kwargs)
	 	query = self.request.GET.get("q")
	 
	 	if query:
	 		qs = self.model.objects.filter(
	 			Q(title__icontains=query) |
	 			Q(description__icontains=query)
	 			)
	 		try:
	 			qs2 = self.model.objects.filter(
	 				Q(price=query)
	 				)
	 			qs = (qs | qs2 ).distinct()
	 		except:
	 			pass

	 	return qs


class ProductDetailView(DetailView):
	model = Product


def product_detail_view_func(request, id):
	# product_instance = Product.objects.get(id=id)
	product_instance = get_object_or_404(Product, id=id)
	try:
		product_instance = Product.objects.get(id=id)
	except Product.DoesNotExist:
		raise Http404
	except:
		raise Http404

	template = "products/product_detail.html"
	context = {
		"object" : product_instance
	}

	return render(request, template, context)

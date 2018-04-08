from django.db.models import Q
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import Http404
from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect


# Create your views here.
from .mixins import StaffRequiredMixin, LoginRequiredMixin
from .models import Product, Variation, Category
from .forms import VariationInventoryForm,VariationInventoryFormSet

class CategoryListView(ListView):
	model = Category
	queryset = Category.objects.all()
	template_name = 'products/product_list.html'

class CategoryDetailView(DetailView):
	model = Category
	
	def get_context_data(self, *args,**kwargs):
	    context = super(CategoryDetailView, self).get_context_data(*args,**kwargs)
	    obj = self.get_object()
	    product_set =  obj.product_set.all()
	    default_category = obj.default_category.all()
	    products = ( product_set | default_category).distinct()
	    context["products"] = products
	    return context

class VariationListView(StaffRequiredMixin,ListView):
	model = Variation
	queryset = Variation.objects.all()

	def get_context_data(self, *args,**kwargs):
	    context = super(VariationListView, self).get_context_data(*args,**kwargs)
	    # context['form'] = VariationInventoryForm(initial={'price': data.price , 'sale_price': data.sale_price, 'inventory': data.inventory})
	    context['formset'] = VariationInventoryFormSet(queryset=self.get_queryset())
	    return context

	def get_queryset(self, *args, **kwargs):
		product_pk = self.kwargs['pk']
		if product_pk is not None:
			product = get_object_or_404(Product, pk=product_pk)
			queryset = self.model.objects.filter(product=product)
		return queryset

	def post(self,request,*args,**kwargs):
		formset = VariationInventoryFormSet(self.request.POST, self.request.FILES)
		print(self.request.POST)
		if formset.is_valid():
			formset.save(commit=False)
			for form in formset:
				new_item = form.save(commit=False)
				product_pk = self.kwargs['pk']
				product = get_object_or_404(Product,pk=product_pk)
				new_item.product = product
				new_item.save()

			messages.success(self.request, "You Inventory is updated")
			return redirect('products')

		raise Http404		



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

import random
class ProductDetailView(DetailView):
	model = Product

	def get_context_data(self, *args,**kwargs):
	    context = super(ProductDetailView, self).get_context_data(*args,**kwargs)
	    instance = self.get_object()
	    context["related"] = sorted(self.model.objects.get_related(instance)[:6], key= lambda x: random.random())
	    return context


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

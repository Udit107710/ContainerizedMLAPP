from django.shortcuts import render, HttpResponse
from sklearn.externals import joblib
import numpy as np
import pandas as pd
from sklearn import datasets
from .models import Results
from .forms import PredictForm
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
file_name = dir_path + "/iris_svm_model.pkl"

def predict(requests):
	#return render(request, 'myapp/predict_form.html')
	if requests.method == 'POST' :
		my_form = PredictForm(requests.POST)
		if my_form.is_valid():
			petal_length = my_form.cleaned_data['petal_length']
			petal_width = my_form.cleaned_data['petal_width']
			sepal_length = my_form.cleaned_data['sepal_length']
			sepal_width = my_form.cleaned_data['sepal_width'] 
			
			iris = datasets.load_iris()
			target = iris.target_names

			val = np.array([petal_length, petal_width,sepal_length,sepal_width])
			model = joblib.load(file_name)
			y_pred = model.predict(val.reshape(1,-1))
			prediction = target[y_pred[0]]
			#result = Results(petal_length= petal_length, petal_width=petal_width, sepal_length=sepal_length, sepal_width-sepal_width, prediction=prediction)
			#results.save()
			result = my_form.save(commit= False)
			result.prediction = prediction 
			result.save()
			return render(requests, 'myapp/result.html',{'prediction': prediction} )
		else:
			return HttpResponse( my_form.errors)
	else:
		my_form = PredictForm()
		return render(requests, 'myapp/predict_form.html', {'form': my_form})


			

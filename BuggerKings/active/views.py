from django.shortcuts import render, redirect
from funcs.functions import main
import sys
sys.path.append('..')
from active import forms


def form_name_view(request):
    form = forms.FormName()
    if request.method == 'POST':
        form = forms.FormName(request.POST)
        if form.is_valid():
            print('Validation success!')
            print(form.cleaned_data['type_opt'])
            if form.cleaned_data['type_opt'] == "compra":
                type_opt = True
            else:
                type_opt = False
            print(type_opt)
            request.session['estimate_gain'], request.session['estimate_value'], = \
                main(form.cleaned_data['symbol'], form.cleaned_data['exercise_time'], form.cleaned_data['price'],
                     form.cleaned_data['riskfree'], type_opt)
            request.session['symbol'] = form.cleaned_data['symbol']
            return redirect(results)
    return render(request, 'form.html', {'form': form})


def results(request):
    try:
        estimate_gain = request.session['estimate_gain']
        estimate_value = request.session['estimate_value']
        symbol = request.session['symbol']
        del request.session['estimate_gain']
        del request.session['estimate_value']
        del request.session['symbol']
        return render(request, 'results.html', {'estimate_gain': estimate_gain, 'estimate_value': estimate_value,
                                                'symbol': symbol})
    except KeyError:
        return redirect('/')

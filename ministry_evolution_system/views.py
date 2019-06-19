import random
from django.shortcuts import render, redirect
from vote.forms import UserLoginForm
from nid.models import NidInfo, PhoneList, VerifyMobile


def generate_otp():
    return random.randint(1000, 9999)

def home(request):
    return render(request, 'index.html')


def user_login(request):
    forms = UserLoginForm()
    if request.method == 'POST':
        forms = UserLoginForm(request.POST)
        if forms.is_valid():
            nid = forms.cleaned_data['nid_number']
            mobile = forms.cleaned_data['mobile_number']
            print(nid, mobile)

            try:
                phone_obj = PhoneList.objects.get(nid__nid_number=nid, mobile_number=mobile)
                otp = generate_otp()
                request.session["otp"] = otp
                verify_obj = VerifyMobile.objects.create(mobile=phone_obj, otp=otp)

                request.session["verify_id"] = verify_obj.id 
                return redirect('verify_phone')


            except Exception as e:
                print("not found", str(e))
                context = {'forms': forms, 'err':'NID and Mobile number doesn\'t match'}
                return render(request, 'login.html', context)
            
    context = {'forms': forms}
    return render(request, 'login.html', context)


def verify_phone(request):
    verify_id = request.session["verify_id"]
    otp = request.session["otp"]
    verify_obj = VerifyMobile.objects.get(id=verify_id)
    if request.method == 'POST':
        otp = request.POST.get('otp', None)

        if str(verify_obj.otp) == otp:
            request.session["user"] = verify_obj.mobile.mobile_number
            del request.session["verify_id"]
            verify_obj.delete()
            return redirect('get-ministry')
        context = {'errMsg': 'OTP Doesn\'t match'}
        return render(request, 'verify.html', context)
    
    return render(request, 'verify.html', {'otp': otp})


def user_logout(request):
    del request.session['user']
    return redirect('home')
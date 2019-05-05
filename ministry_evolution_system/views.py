from django.shortcuts import render, redirect
from vote.forms import UserLoginForm
from nid.models import NidInfo, PhoneList, VerifyMobile

def home(request):
    return render(request, 'index.html')


def user_login(request):
    forms = UserLoginForm()
    if request.method == 'POST':
        forms = UserLoginForm(request.POST)
        if forms.is_valid():
            nid = forms.cleaned_data['nid_number']
            mobile = forms.cleaned_data['mobile_number']

            try:
                phone_obj = PhoneList.objects.get(nid__nid_number=nid, mobile_number=mobile)
                VerifyMobile.objects.create(mobile=phone_obj, otp=1234)

                request.session["phonelist_id"] = phone_obj.id 
                return redirect('verify_phone')


            except Exception as e:
                print("not found", str(e))
            
    context = {'forms': forms}
    return render(request, 'login.html', context)


def verify_phone(request):
    phone_id = request.session["phonelist_id"]
    phone_obj = VerifyMobile.objects.get(id=phone_id)
    if request.method == 'POST':
        otp = request.POST.get('otp', None)

        if str(phone_obj.otp) == otp:
            request.session["user"] = phone_obj.mobile.mobile_number
            return redirect('get-ministry')
    
    return render(request, 'verify.html')
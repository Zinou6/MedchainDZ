from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from .blockchain import Wallet, transaction, Block, display_transaction, mine
import json
from Crypto.PublicKey import RSA
import hashlib
from hashlib import sha256
from urllib.parse import urlparse
from uuid import uuid4
from collections import namedtuple
from json import JSONEncoder


def customJsonDecoder(jsonDict):
    return namedtuple('T',jsonDict.keys())(*jsonDict.values())


last_block_hash = None

class Blockchain:

    def __init__(self):
        global last_block_hash
        self.chain          = [] 
        
        fileBlocks = open('hospital/blocks.json')
        data = json.load(fileBlocks,object_hook=customJsonDecoder)

        if(len(data) == 0):
            #Create a Genesis Block
            self.block = Block()
            self.block.index = len(self.chain)
            self.block.previous_block_hash = last_block_hash
            self.block.Nonce = 0
            digest = hashlib.sha256((str(self.block)).encode('ascii')).hexdigest()

            #digest = hash(new_block)
            self.block.hash = digest
            last_block_hash = digest    

            self.chain.append(self.block)

            self.block.saveTOjson()
        else:
            self.chain      = data
            last_block_hash = self.chain[len(self.chain)-1].hash
        #self.nodes = set()

    '''
    def add_node(self, address): 
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/blockchain')
            if response.status_code == 200:
                length  = response.json()['length']
                chain   = response.json()['chain']
                if length > max_length:
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    '''


blockchain = Blockchain()


#node_address = str(uuid4()).replace('-', '')
#root_node = 'e36f0158f0aed45b3bc755dc52ed4560d'

'''
# Connecting new nodes
def connect_node(request): 
    if request.method == 'POST':
        received_json = json.loads(request.body)
        nodes = received_json.get('nodes')
        if nodes is None:
            return "No node", HttpResponse(status=400)
        for node in nodes:
            blockchain.add_node(node)
        response = {'message': 'All the nodes are now connected. The Sudocoin Blockchain now contains the following nodes:',
                    'total_nodes': list(blockchain.nodes)}
    return JsonResponse(response) 

# Replacing the chain by the longest chain if needed
def replace_chain(request): 
    if request.method == 'GET':
        is_chain_replaced = blockchain.replace_chain()
        if is_chain_replaced:
            response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                        'new_chain': blockchain.chain}
        else:
            response = {'message': 'All good. The chain is the largest one.',
                        'actual_chain': blockchain.chain}
    return JsonResponse(response)
'''

# Blockchain views
def blockchain_view(request):
    fileBlocks = open('hospital/blocks.json')
    blockchain.chain = json.load(fileBlocks,object_hook=customJsonDecoder)
    context = {
        'blocks' : blockchain.chain,
    }
    return render(request, 'hospital/blockchain.html', context = context)

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')


#for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')

#for showing signup/login button for receptionist
def receptionistclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/receptionistclick.html')

#for showing signup/login button for doctor
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')


#for showing signup/login button for patient
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/patientclick.html')




def admin_signup_view(request):
    out_dict = {}
    list1 = []
    dict1 = {}
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            #Create a wallet for admin user
            new_wallet = Wallet()
            user=form.save()
            user.set_password(user.password)
            user.identity = new_wallet.identity
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            
            #Save the wallet in json file
            out_dict["public_key"]=new_wallet._public_key.exportKey().decode()
            out_dict["private_key"]=new_wallet._private_key.exportKey().decode()
            list1.append(out_dict)
            dict1["walletinfo"]=list1
            with open("hospital/Admin_Wallet_details.json","w") as fil:
                fil.write(json.dumps(dict1))

            return HttpResponseRedirect('/adminlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})

def receptionist_signup_view(request):
    out_dict = {}
    list1 = []
    dict1 = {}
    userForm=forms.ReceptionistUserForm()
    receptionistForm=forms.ReceptionistForm()
    context={   'userForm':userForm,
                'receptionistForm':receptionistForm
            }
    if request.method=='POST':
        userForm=forms.ReceptionistUserForm(request.POST)
        receptionistForm=forms.ReceptionistForm(request.POST,request.FILES)
        if userForm.is_valid() and receptionistForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            receptionist=receptionistForm.save(commit=False)

            #Create a wallet for admin user
            new_wallet = Wallet()
            receptionist.user=user
            receptionist.identity = new_wallet.identity
            receptionist=receptionist.save()
            my_receptionist_group = Group.objects.get_or_create(name='RECEPTIONIST')
            my_receptionist_group[0].user_set.add(user)

            #Save the wallet in json file
            out_dict["public_key"]=new_wallet._public_key.exportKey().decode()
            out_dict["private_key"]=new_wallet._private_key.exportKey().decode()
            list1.append(out_dict)
            dict1["walletinfo"]=list1
            with open("hospital/Receptionist_Wallet_details.json","w") as fil:
                fil.write(json.dumps(dict1))
        
        return HttpResponseRedirect('/receptionistlogin')
    return render(request,'hospital/receptionistsignup.html',context=context)

def doctor_signup_view(request):
    out_dict = {}
    list1 = []
    dict1 = {}
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    context={   'userForm':userForm,
                'doctorForm':doctorForm
            }
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False) 
            #Create a wallet for admin user
            new_wallet = Wallet()
            doctor.user=user
            doctor.identity = new_wallet.identity
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            
            
            #Save the wallet in json file
            out_dict["public_key"]=new_wallet._public_key.exportKey().decode()
            out_dict["private_key"]=new_wallet._private_key.exportKey().decode()
            list1.append(out_dict)
            dict1["walletinfo"]=list1
            with open("hospital/Doctor_Wallet_details.json","w") as fil:
                fil.write(json.dumps(dict1))

        return HttpResponseRedirect('/doctorlogin')
    return render(request,'hospital/doctorsignup.html',context=context)


def patient_signup_view(request):
    out_dict = {}
    list1 = []
    dict1 = {}
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            #Create a wallet for admin user
            new_wallet       = Wallet()
            patient.user     = user
            patient.identity = new_wallet.identity
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            today = date.today()
            patient.age = today.year - patient.brth_day.year
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            
           
            #Save the wallet in json file
            out_dict["public_key"]=new_wallet._public_key.exportKey().decode()
            out_dict["private_key"]=new_wallet._private_key.exportKey().decode()
            list1.append(out_dict)
            dict1["walletinfo"]=list1
            with open("hospital/Patient_Wallet_details.json","w") as fil:
                fil.write(json.dumps(dict1))
        '''
        else:
            print(userForm.is_valid())
            print(patientForm.is_valid())
            print(patientForm['assignedDoctorId'])
            for field in patientForm:
                print("Field Error:", field.name,  field.errors)
        '''
        return HttpResponseRedirect('/patientlogin')   
    return render(request,'hospital/patientsignup.html',context=mydict)






#-----------for checking user is doctor , patient or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()
def is_receptionist(user):
    return user.groups.filter(name='RECEPTIONIST').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):    
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'hospital/doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'hospital/patient_wait_for_approval.html')
    elif is_receptionist(request.user):
        accountapproval=models.Receptionist.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('receptionist-dashboard')
        else:
            return render(request,'hospital/receptionist_wait_for_approval.html')




#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    receptionistcount=models.Receptionist.objects.all().filter(status=True).count()
    pendingreceptionistcount=models.Receptionist.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'receptionistcount':receptionistcount,
    'pendingreceptionistcount':pendingreceptionistcount,
    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    global blockchain 
    global last_block_hash
    global digest

    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    
    #Create a Transaction
    new_transaction = transaction(
        "ADMIN",
        doctor.identity,
        hash("DELETE DOCTOR")
        )

    user.delete()
    doctor.delete()

    #Create a block
    new_block = Block()
    new_block.index = len(blockchain.chain)
    new_block.previous_block_hash = last_block_hash

    #signature = new_transaction.sign_transaction()
    new_block.verified_transactions.append(new_transaction.to_dict())

    new_block.Nonce = mine (str(new_block))[0]

    digest = mine (str(new_block))[1]
    new_block.hash = digest
    last_block_hash = digest
    blockchain.chain.append(new_block)
    new_block.saveTOjson()

    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    out_dict = {}
    list1 = []
    dict1 = {}
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            #Create a wallet for admin user
            new_wallet = Wallet()
            doctor.identity = new_wallet.identity
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

            #Save the wallet in json file
            out_dict["public_key"]=new_wallet._public_key.exportKey().decode()
            out_dict["private_key"]=new_wallet._private_key.exportKey().decode()
            list1.append(out_dict)
            dict1["walletinfo"]=list1
            with open("hospital/AddDoctor_Wallet_details.json","w") as fil:
                fil.write(json.dumps(dict1))

            global blockchain 
            global last_block_hash
            global digest
    
            #Create a block
            new_block = Block()
            new_block.index = len(blockchain.chain)
            new_block.previous_block_hash = last_block_hash

            #Create a Transaction
            new_transaction = transaction(
                "ADMIN",
                doctor.identity,
                hash("ADD DOCTOR")
            )

            #signature = new_transaction.sign_transaction()
            new_block.verified_transactions.append(new_transaction.to_dict())

            new_block.Nonce = mine (str(new_block))[0]

            digest = mine (str(new_block))[1]
            new_block.hash = digest
            last_block_hash = digest
            blockchain.chain.append(new_block)
            new_block.saveTOjson()

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save() 
    global blockchain 
    global last_block_hash
    global digest
    
    #Create a block
    new_block = Block()
    new_block.index = len(blockchain.chain)
    new_block.previous_block_hash = last_block_hash

    #Create a Transaction
    new_transaction = transaction(
        "ADMIN",
        doctor.identity,
        hashlib.sha256(("APPROVE DOCTOR").encode('ascii')).hexdigest()
    )

    #signature = new_transaction.sign_transaction()
    new_block.verified_transactions.append(new_transaction.to_dict())

    new_block.Nonce = mine (str(new_block))[0]

    digest = mine (str(new_block))[1]
    new_block.hash = digest
    last_block_hash = digest
    blockchain.chain.append(new_block)
    new_block.saveTOjson()

    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    global blockchain 
    global last_block_hash
    global digest
    
    #Create a block
    new_block = Block()
    new_block.index = len(blockchain.chain)
    new_block.previous_block_hash = last_block_hash

    #Create a Transaction
    new_transaction = transaction(
        "ADMIN",
        doctor.identity,
        hashlib.sha256(("REJECT DOCTOR").encode('ascii')).hexdigest()
    )

    #signature = new_transaction.sign_transaction()
    new_block.verified_transactions.append(new_transaction.to_dict())

    new_block.Nonce = mine (str(new_block))[0]

    digest = mine (str(new_block))[1]
    new_block.hash = digest
    last_block_hash = digest
    blockchain.chain.append(new_block)
    new_block.saveTOjson()

    return redirect('admin-approve-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_Specialisation.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_receptionist_view(request):
    return render(request,'hospital/admin_receptionist.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_receptionist_view(request):
    receptionist=models.Receptionist.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_receptionist.html',{'receptionist':receptionist})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_receptionist_from_hospital_view(request,pk):
    receptionist=models.Receptionist.objects.get(id=pk)
    user=models.User.objects.get(id=receptionist.user_id)

    global blockchain 
    global last_block_hash
    global digest
    
    #Create a block
    new_block = Block()
    new_block.index = len(blockchain.chain)
    new_block.previous_block_hash = last_block_hash

    #Create a Transaction
    new_transaction = transaction(
        "ADMIN",
        receptionist.identity,
        hashlib.sha256(("DELETE RECEPTIONIST").encode('ascii')).hexdigest()
    )

    #signature = new_transaction.sign_transaction()
    new_block.verified_transactions.append(new_transaction.to_dict())

    new_block.Nonce = mine (str(new_block))[0]

    digest = mine (str(new_block))[1]
    new_block.hash = digest
    last_block_hash = digest
    blockchain.chain.append(new_block)
    new_block.saveTOjson()
    user.delete()
    receptionist.delete()

    return redirect('admin-view-receptionist')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_receptionist_view(request,pk):
    receptionist=models.Receptionist.objects.get(id=pk)
    user=models.User.objects.get(id=receptionist.user_id)

    userForm=forms.ReceptionistUserForm(instance=user)
    receptionistForm=forms.ReceptionistForm(request.FILES,instance=receptionist)
    mydict={'userForm':userForm,'receptionistForm':receptionistForm}
    if request.method=='POST':
        userForm=forms.ReceptionistUserForm(request.POST,instance=user)
        receptionistForm=forms.ReceptionistForm(request.POST,request.FILES,instance=receptionist)
        if userForm.is_valid() and receptionistForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            receptionist=receptionistForm.save(commit=False)
            receptionist.status=True
            receptionist.save()
            return redirect('admin-view-receptionist')
    return render(request,'hospital/admin_update_receptionist.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_receptionist_view(request):
    #those whose approval are needed
    receptionist=models.Receptionist.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_receptionist.html',{'receptionist':receptionist})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_receptionist_view(request,pk):
    receptionist=models.Receptionist.objects.get(id=pk)
    user=models.User.objects.get(id=receptionist.user_id)
    user.delete()
    receptionist.delete()
    global blockchain 
    global last_block_hash
    global digest
    
    #Create a block
    new_block = Block()
    new_block.index = len(blockchain.chain)
    new_block.previous_block_hash = last_block_hash

    #Create a Transaction
    new_transaction = transaction(
        "ADMIN",
        receptionist.identity,
        hashlib.sha256(("REJECT RECEPCIONIST").encode('ascii')).hexdigest()
    )

    #signature = new_transaction.sign_transaction()
    new_block.verified_transactions.append(new_transaction.to_dict())

    new_block.Nonce = mine (str(new_block))[0]

    digest = mine (str(new_block))[1]
    new_block.hash = digest
    last_block_hash = digest
    blockchain.chain.append(new_block)
    new_block.saveTOjson()

    return redirect('admin-approve-receptionist') 


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_receptionist_view(request,pk):
    receptionist=models.Receptionist.objects.get(id=pk)
    receptionist.status=True
    receptionist.save() 
    global blockchain 
    global last_block_hash
    global digest
    
    #Create a block
    new_block = Block()
    new_block.index = len(blockchain.chain)
    new_block.previous_block_hash = last_block_hash

    #Create a Transaction
    new_transaction = transaction(
        "ADMIN",
        receptionist.identity,
        hashlib.sha256(("APPROVE RECEPTIONIST").encode('ascii')).hexdigest()
    )

    #signature = new_transaction.sign_transaction()
    new_block.verified_transactions.append(new_transaction.to_dict())

    new_block.Nonce = mine (str(new_block))[0]

    digest = mine (str(new_block))[1]
    new_block.hash = digest
    last_block_hash = digest
    blockchain.chain.append(new_block)
    new_block.saveTOjson()

    return redirect(reverse('admin-approve-receptionist'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_receptionist_view(request):
    global blockchain 
    global last_block_hash
    global digest
    out_dict = {}
    list1 = []
    dict1 = {}
    userForm=forms.ReceptionistUserForm()
    receptionistForm=forms.ReceptionistForm()
    mydict={'userForm':userForm,'receptionistForm':receptionistForm}
    if request.method=='POST':
        userForm=forms.ReceptionistUserForm(request.POST)
        receptionistForm=forms.ReceptionistForm(request.POST,request.FILES)
        if userForm.is_valid() and receptionistForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            receptionist=receptionistForm.save(commit=False)
            receptionist.user=user
            receptionist.status=True

            #Create a wallet for admin user
            new_wallet = Wallet()
            receptionist.identity = new_wallet.identity
            receptionist.save()

            my_receptionist_group = Group.objects.get_or_create(name='RECEPTIONIST')
            my_receptionist_group[0].user_set.add(user)
           
            #Save the wallet in json file
            out_dict["public_key"]=new_wallet._public_key.exportKey().decode()
            out_dict["private_key"]=new_wallet._private_key.exportKey().decode()
            list1.append(out_dict)
            dict1["walletinfo"]=list1
            with open("hospital/AddReceptionist_Wallet_details.json","w") as fil:
                fil.write(json.dumps(dict1))
    
            #Create a block
            new_block = Block()
            new_block.index = len(blockchain.chain)
            new_block.previous_block_hash = last_block_hash

            #Create a Transaction
            new_transaction = transaction(
                "ADMIN",
                receptionist.identity,
                hashlib.sha256(("ADD RECEPTIONIST").encode('ascii')).hexdigest()
            )

            #signature = new_transaction.sign_transaction()
            new_block.verified_transactions.append(new_transaction.to_dict())

            new_block.Nonce = mine (str(new_block))[0]

            digest = mine (str(new_block))[1]
            new_block.hash = digest
            last_block_hash = digest
            blockchain.chain.append(new_block)
            new_block.saveTOjson()

        return HttpResponseRedirect('admin-view-receptionist')
    return render(request,'hospital/admin_add_receptionist.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})


#-----------------APPOINTMENT START--------------------------------------------------------------------

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)
var = 0
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_document(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    patientIdForm=forms.PatientIdForm()
    mydict ={
        'doctor':doctor,
        'patients':patients,
        'patientIdForm':patientIdForm,
    }
    if request.method == 'POST':
        patientIdForm=forms.PatientIdForm(request.POST)
        if patientIdForm.is_valid():
            print(patientIdForm.fields['patientId'])
            PID = request.POST.get('patientId')
            if 'prescription' in request.POST:
                print(PID)
                return redirect('doctor-add-prescription', patieniID= PID)
            elif 'radiology' in request.POST:
                print(PID)
                return redirect('doctor-add-radio', patieniID= PID)
            elif 'analyse' in request.POST:
                print(PID)
                return redirect('doctor-add-analyse', patieniID= PID)
            elif 'comment' in request.POST:
                print(PID)
                return redirect('doctor-add-comment', patieniID= PID)
    return render(request,'hospital/doctor-view-document.html',context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_prescription(request, patieniID):
    global blockchain 
    global last_block_hash
    global digest
    
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    patient=models.Patient.objects.get(user_id=patieniID)
    PrescriptionForm=forms.PrescriptionForm()
    
    mydict={'PrescriptionForm':PrescriptionForm,
            'doctor':doctor,
            'doctorName':doctor.get_name,
            'doctorDepartment':doctor.department,
            'todayDate':date.today(),
            'patientName':patient.get_name,
            'patientAge':patient.age,
    }
    if request.method=='POST':
        PrescriptionForm=forms.PrescriptionForm(request.POST)
        if PrescriptionForm.is_valid():
            prescription=PrescriptionForm.save()
            prescription.doctorId=request.user.id
            prescription.patientId=patieniID
            prescription.date=date.today()
            prescription.save()
            dict1={
                'prescription':prescription,
                'prescription_date':prescription.date,
            }
            #Create a block
            new_block = Block()
            new_block.index = len(blockchain.chain)
            new_block.previous_block_hash = last_block_hash

            #Create a Transaction
            new_transaction = transaction(
            doctor.identity,
            patient.identity,
            hashlib.sha256((str(dict1)).encode('ascii')).hexdigest()
            )

            #signature = new_transaction.sign_transaction()
            new_block.verified_transactions.append(new_transaction.to_dict())

            new_block.Nonce = mine (str(new_block))[0]

            digest = mine (str(new_block))[1]
            new_block.hash = digest
            last_block_hash = digest
            blockchain.chain.append(new_block)
            new_block.saveTOjson()

        else:
            for field in PrescriptionForm:
                print("Field Error:", field.name,  field.errors)
        return HttpResponseRedirect('/doctor-view-document')

    return render(request,'hospital/doctor_add_prescription.html',context=mydict)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_radio(request, patieniID):
    global blockchain 
    global last_block_hash
    global digest
    
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    patient=models.Patient.objects.get(user_id=patieniID)
    RadiologyForm = forms.RadiologyForm()
    mydict ={   'RadiologyForm':RadiologyForm,
                'doctor':doctor,
                'doctorName':doctor.get_name,
                'doctorDepartment':doctor.department,
                'todayDate':date.today(),
                'patientName':patient.get_name,
                'patientAge':patient.age,
            }
    if request.method=='POST':
        RadiologyForm = forms.RadiologyForm(request.POST)
        if RadiologyForm.is_valid():
            radiology=RadiologyForm.save()
            radiology.doctorId=request.user.id
            radiology.patientId=patieniID
            radiology.date=date.today()
            radiology.save()
            dict1={
                'radiology':radiology,
                'radiology_date':radiology.date,
            }

            #Create a block
            new_block = Block()
            new_block.index = len(blockchain.chain)
            new_block.previous_block_hash = last_block_hash

            #Create a Transaction
            new_transaction = transaction(
            doctor.identity,
            patient.identity,
            hashlib.sha256((str(dict1)).encode('ascii')).hexdigest()
            )

            #signature = new_transaction.sign_transaction()
            new_block.verified_transactions.append(new_transaction.to_dict())

            new_block.Nonce = mine (str(new_block))[0]

            digest = mine (str(new_block))[1]
            new_block.hash = digest
            last_block_hash = digest
            blockchain.chain.append(new_block)
            new_block.saveTOjson()

        return HttpResponseRedirect('/doctor-view-document')

    return render(request,'hospital/doctor_add_radiology.html',context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_analyse(request, patieniID):
    global blockchain 
    global last_block_hash
    global digest
    
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    patient=models.Patient.objects.get(user_id=patieniID)
    AnalyseForm = forms.AnalyseForm()
    mydict ={   'AnalyseForm':AnalyseForm,
                'doctor':doctor,
                'doctorName':doctor.get_name,
                'doctorDepartment':doctor.department,
                'todayDate':date.today(),
                'patientName':patient.get_name,
                'patientAge':patient.age,
            }
    if request.method=='POST':
        AnalyseForm = forms.AnalyseForm(request.POST)
        if AnalyseForm.is_valid():
            analyse=AnalyseForm.save()
            analyse.doctorId=request.user.id
            analyse.patientId=patieniID
            analyse.date=date.today()
            analyse.save()
            dict1={
                'analyse':analyse,
                'analyse_date':analyse.date,
            }

            #Create a block
            new_block = Block()
            new_block.index = len(blockchain.chain)
            new_block.previous_block_hash = last_block_hash

            #Create a Transaction
            new_transaction = transaction(
            doctor.identity,
            patient.identity,
            hashlib.sha256((str(dict1)).encode('ascii')).hexdigest()
            )

            #signature = new_transaction.sign_transaction()
            new_block.verified_transactions.append(new_transaction.to_dict())

            new_block.Nonce = mine (str(new_block))[0]

            digest = mine (str(new_block))[1]
            new_block.hash = digest
            last_block_hash = digest
            blockchain.chain.append(new_block)
            new_block.saveTOjson()

        return HttpResponseRedirect('/doctor-view-document')

    return render(request,'hospital/doctor_add_analyse.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_comment(request, patieniID):
    global blockchain 
    global last_block_hash
    global digest
    
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    patient=models.Patient.objects.get(user_id=patieniID)
    CommentForm = forms.CommentForm()
    mydict ={   'CommentForm':CommentForm,
                'doctor':doctor,
                'doctorName':doctor.get_name,
                'doctorDepartment':doctor.department,
                'todayDate':date.today(),
                'patientName':patient.get_name,
                'patientAge':patient.age,
            }
    if request.method=='POST':
        CommentForm = forms.CommentForm(request.POST)
        if CommentForm.is_valid():
            comment=CommentForm.save()
            comment.doctorId=request.user.id
            comment.patientId=patieniID
            comment.date=date.today()
            comment.save()
            dict1={
                'comment':comment,
                'comment_date':comment.date,
            }

            #Create a block
            new_block = Block()
            new_block.index = len(blockchain.chain)
            new_block.previous_block_hash = last_block_hash

            #Create a Transaction
            new_transaction = transaction(
            doctor.identity,
            patient.identity,
            hashlib.sha256((str(dict1)).encode('ascii')).hexdigest()
            )

            #signature = new_transaction.sign_transaction()
            new_block.verified_transactions.append(new_transaction.to_dict())

            new_block.Nonce = mine (str(new_block))[0]

            digest = mine (str(new_block))[1]
            new_block.hash = digest
            last_block_hash = digest
            blockchain.chain.append(new_block)
            new_block.saveTOjson()

        return HttpResponseRedirect('/doctor-view-document')

    return render(request,'hospital/doctor_add_comment.html',context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
        'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)





@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def search_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ----------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'hospital/patient_book_appointment.html',context=mydict)



def patient_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})



def search_doctor_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors=models.Doctor.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})




@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------



#---------------------------------------------------------------------------------
#------------------------ RECEPTIONIST RELATED VIEWS START ----------------------------
#---------------------------------------------------------------------------------


@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def receptionist_dashboard_view(request):
    #for both table in admin dashboard
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    doctors=models.Doctor.objects.all().filter(status=True,department=receptionist.department).order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True,department=receptionist.department).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    
    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    mydict={
        'receptionist':receptionist,
        'doctors':doctors,
        'patients':patients,
        'doctorcount':doctorcount,
        'patientcount':patientcount,
        'pendingpatientcount':pendingpatientcount,
        'appointmentcount':appointmentcount,
    }
    return render(request,'hospital/receptionist_dashboard.html',context=mydict)


@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def receptionist_view_doctor_view(request):
    receptionist=models.Receptionist.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    doctors=models.Doctor.objects.all().filter(status=True,department=receptionist.department)
    return render(request,'hospital/receptionist_view_doctor.html',{'receptionist':receptionist,'doctors':doctors})


@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def receptionist_patient_view(request):
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    return render(request,'hospital/receptionist_patient.html',{'receptionist':receptionist})


@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def receptionist_view_patient_view(request):
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/receptionist_view_patient.html',{'receptionist':receptionist,'patients':patients})


@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def update_patient_view(request,pk):
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'receptionist':receptionist,'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('receptionist-view-patient')
    return render(request,'hospital/receptionist_update_patient.html',context=mydict)


@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def delete_patient_from_hospital_view(request,pk):
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    global blockchain 
    global last_block_hash
    global digest
    
    #Create a block
    new_block = Block()
    new_block.index = len(blockchain.chain)
    new_block.previous_block_hash = last_block_hash

    #Create a Transaction
    new_transaction = transaction(
        receptionist.identity,
        patient.identity,
        hashlib.sha256(("DELETE PATIENT").encode('ascii')).hexdigest()
    )

    #signature = new_transaction.sign_transaction()
    new_block.verified_transactions.append(new_transaction.to_dict())

    new_block.Nonce = mine (str(new_block))[0]

    digest = mine (str(new_block))[1]
    new_block.hash = digest
    last_block_hash = digest
    blockchain.chain.append(new_block)
    new_block.saveTOjson()
    user.delete()
    patient.delete()

    return redirect('receptionist-view-patient')


@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def receptionist_add_patient_view(request):
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    
    global blockchain 
    global last_block_hash
    global digest
    out_dict = {}
    list1 = []
    dict1 = {}
    
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'receptionist':receptionist,'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            today = date.today()
            patient.age = today.year - patient.brth_day.year
            #Create a wallet for admin user
            new_wallet = Wallet()
            patient.identity = new_wallet.identity
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
           
            #Save the wallet in json file
            out_dict["public_key"]=new_wallet._public_key.exportKey().decode()
            out_dict["private_key"]=new_wallet._private_key.exportKey().decode()
            list1.append(out_dict)
            dict1["walletinfo"]=list1
            with open("hospital/AddPatient_Wallet_details.json","w") as fil:
                fil.write(json.dumps(dict1))
    
            #Create a block
            new_block = Block()
            new_block.index = len(blockchain.chain)
            new_block.previous_block_hash = last_block_hash

            #Create a Transaction
            new_transaction = transaction(
                receptionist.identity,
                patient.identity,
                hashlib.sha256(("ADD PATIENT").encode('ascii')).hexdigest()
            )

            #signature = new_transaction.sign_transaction()
            new_block.verified_transactions.append(new_transaction.to_dict())

            new_block.Nonce = mine (str(new_block))[0]

            digest = mine (str(new_block))[1]
            new_block.hash = digest
            last_block_hash = digest
            blockchain.chain.append(new_block)
            new_block.saveTOjson()

        return HttpResponseRedirect('receptionist-view-patient')
    return render(request,'hospital/receptionist_add_patient.html',context=mydict)


#------------------FOR APPROVING PATIENT BY RECEPTIONIST----------------------
@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def receptionist_approve_patient_view(request):
    #those whose approval are needed
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'hospital/receptionist_approve_patient.html',{'receptionist':receptionist,'patients':patients})



@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def approve_patient_view(request,pk):
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()

    global blockchain 
    global last_block_hash
    global digest
    
    #Create a block
    new_block = Block()
    new_block.index = len(blockchain.chain)
    new_block.previous_block_hash = last_block_hash

    #Create a Transaction
    new_transaction = transaction(
        receptionist.identity,
        patient.identity,
        hashlib.sha256(("APPROVE PATIENT").encode('ascii')).hexdigest()
    )

    #signature = new_transaction.sign_transaction()
    new_block.verified_transactions.append(new_transaction.to_dict())

    new_block.Nonce = mine (str(new_block))[0]

    digest = mine (str(new_block))[1]
    new_block.hash = digest
    last_block_hash = digest
    blockchain.chain.append(new_block)
    new_block.saveTOjson()

    return redirect(reverse('receptionist-approve-patient'))



@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def reject_patient_view(request,pk):
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()

    global blockchain 
    global last_block_hash
    global digest
    
    #Create a block
    new_block = Block()
    new_block.index = len(blockchain.chain)
    new_block.previous_block_hash = last_block_hash

    #Create a Transaction
    new_transaction = transaction(
        receptionist.identity,
        patient.identity,
        hashlib.sha256(("REJECT PATIENT").encode('ascii')).hexdigest()
    )

    #signature = new_transaction.sign_transaction()
    new_block.verified_transactions.append(new_transaction.to_dict())

    new_block.Nonce = mine (str(new_block))[0]

    digest = mine (str(new_block))[1]
    new_block.hash = digest
    last_block_hash = digest
    blockchain.chain.append(new_block)
    new_block.saveTOjson()
    
    return redirect('admin-approve-patient')


#--------------------- FOR DISCHARGING PATIENT BY RECEPTIONIST START-------------------------
@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def receptionist_discharge_patient_view(request):
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/receptionist_discharge_patient.html',{'receptionist':receptionist,'patients':patients})



@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def discharge_patient_view(request,pk):
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'receptionist':receptionist,
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'hospital/patient_final_bill.html',context=patientDict)
    return render(request,'hospital/patient_generate_bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing----------------
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)


@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def receptionist_appointment_view(request):
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    return render(request,'hospital/receptionist_appointment.html',{'receptionist':receptionist})


@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def receptionist_view_appointment_view(request):
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'hospital/receptionist_view_appointment.html',{'receptionist':receptionist,'appointments':appointments})


@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def receptionist_add_appointment_view(request):
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    appointmentForm=forms.AppointmentForm()
    mydict={'receptionist':receptionist,'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('receptionist-view-appointment')
    return render(request,'hospital/receptionist_add_appointment.html',context=mydict)



@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def receptionist_approve_appointment_view(request):
    #those whose approval are needed
    receptionist=models.Receptionist.objects.get(user_id=request.user.id)
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'hospital/receptionist_approve_appointment.html',{'receptionist':receptionist,'appointments':appointments})



@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('receptionist-approve-appointment'))



@login_required(login_url='receptionistlogin')
@user_passes_test(is_receptionist)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('receptionist-approve-appointment')

#------------------------ RECEPTIONIST RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------
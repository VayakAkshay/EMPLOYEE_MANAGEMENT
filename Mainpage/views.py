from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ImageForm
from .models import Profiles,TaskManager,LeaveManager,attendacemanager,Roles,SalaryTable
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

# Create your views here.

def Home(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("pass")
        cpass = request.POST.get("cpass")
        if password == cpass:
            myuser = User.objects.create_user(email,mobile,password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            user = authenticate(username = email,password = password)
            login(request,user)
            messages.success(request,"You are Logged in successfully")
            return redirect("/profile/")
        else:
            messages.warning(request,"Password is not matched ")
            return redirect("/password/")
    return render(request, "Mainpage/index.html")


def aboutpage(request):
    return render(request, 'Mainpage/About.html')

def taskpage(request):
    user = request.user
    allows = 0
    if Profiles.objects.filter(email_id = user).all().exists():
        allows = 1
        tasks = TaskManager.objects.filter(emp_id = user.id).all()
        return render(request,"Mainpage/tasks.html",{"Tasks":tasks,"allows":allows})
    else:
        allows = 0
        messages.warning(request,"Please first complete profile after then see the tasks.")
        return render(request,"Mainpage/tasks.html",{"allows":allows})

def taskdetail(request):
    if request.method == "POST":
        ids = request.POST.get("id")
        taskdata = TaskManager.objects.filter(id = ids).values()
        return render(request, "Mainpage/taskdetail.html",{"taskdata":taskdata})
    return redirect("/")

def completetask(request):
    if request.method == "POST":
        ids = request.POST.get("id")
        taskdata = TaskManager.objects.filter(id = ids).update(status = "Completed")
    return redirect("/tasks/")

def profilepage(request):
    user = request.user
    available = 0
    leaves_data = LeaveManager.objects.filter(emp_id = user.id).all().values()
    total_days = 0
    for i in range(len(leaves_data)):
        dates= leaves_data[i]["end_date"] - leaves_data[0]["start_date"]
        days = dates.days
        total_days = total_days + days
    tasks_data = TaskManager.objects.filter(emp_id = user.id).all().values()
    total_remaining = 0
    for i in range(len(tasks_data)):
        if tasks_data[i]["status"] == "Remaining":
            total_remaining = total_remaining + 1
    if(Profiles.objects.filter(email_id = user)):
        available = 1
        profile_data = Profiles.objects.filter(email_id = user).values()
        department = Profiles.objects.filter(email_id = user).values()[0]["department_name"].split(",")[1:]
        return render(request,"Mainpage/profile.html",{"profile_data":profile_data,"department":department,"total_days":total_days,"total_remaining":total_remaining})
    else:
        available = 0
        profile_data = Profiles()
        full_name = user.first_name + " " + user.last_name
        email_id = user.username
        mobile = user.email
        role = Roles()
        if request.method == "POST":
            profile_data.profile_id = user.id
            profile_data.full_name = full_name
            profile_data.email_id = email_id
            profile_data.mobile_no = mobile
            profile_data.dateofjoin = request.POST.get("joining_date")
            profile_data.dateofbirth = request.POST.get("birth_date")
            profile_data.salary = request.POST.get("salary")
            profile_data.gender = request.POST.get("gender")
            profile_data.address = request.POST.get("address")
            profile_data.department_name = request.POST.get("checkbox_val")
            profile_data.role = request.POST.get("role")
            if len(request.FILES) != 0:
                profile_data.profile_img = request.FILES['profile_img']
            profile_data.save()
            role.role_name = request.POST.get("role")
            role.emp_id = user.id
            role.save()
            profile_datas = Profiles.objects.filter(email_id = user).all().values()[0]
            salary = profile_datas["salary"]
            months = ["January","February","March","April","May","June","July","August","September","Octomber","Navember","December"]
            PF = (salary * 12)/100
            PT = 1000
            gross_deduct = PF + PT
            netpay = salary - gross_deduct
            total_salary = salary * 12
            total_pf = PF * 12
            total_pt = PT * 12
            total_deduct = gross_deduct * 12
            total_netpay = netpay * 12
            today_date = date.today()
            salary_list = []
            for i in range(len(months)):
                salary_dict = {}
                salary_dict["Months"] = months[i]
                salary_dict["Salary"] = salary
                salary_dict["PF"] = PF
                salary_dict["PT"] = PT
                salary_dict["gross"] = gross_deduct
                salary_dict["net"] = netpay
                salary_list.append(salary_dict)
            salary_dict = {}
            salary_dict["Months"] = "Total Salary"
            salary_dict["Salary"] = total_salary
            salary_dict["PF"] = total_pf
            salary_dict["PT"] = total_pt
            salary_dict["gross"] = total_deduct
            salary_dict["net"] = total_netpay
            salary_list.append(salary_dict)
            for i in range(len(salary_list)):
                salary_table = SalaryTable()
                salary_table.emp_id = user.id
                salary_table.months = salary_list[i]["Months"]
                salary_table.gross_salary = salary_list[i]["Salary"]
                salary_table.PF = salary_list[i]["PF"]
                salary_table.PT = salary_list[i]["PT"]
                salary_table.gross_deduct = salary_list[i]["gross"]
                salary_table.Net = salary_list[i]["net"]
                salary_table.status = "Unpaid"
                salary_table.save()
            return redirect("/profile/")
    form = ImageForm()
    return render(request, "Mainpage/profile.html",{"available":available,"form":form,"total_days":total_days,"total_remaining":total_remaining})

def edit_profile(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == "POST":
            full_name = request.POST.get("fname") + " " + request.POST.get("lname")
            Profiles.objects.filter(email_id = user).update(full_name = full_name)
            Profiles.objects.filter(email_id = user).update(dateofjoin = request.POST.get("joining_date"))
            Profiles.objects.filter(email_id = user).update(dateofbirth = request.POST.get("birth_date"))
            Profiles.objects.filter(email_id = user).update(salary = request.POST.get("salary"))
            Profiles.objects.filter(email_id = user).update(gender = request.POST.get("gender"))
            Profiles.objects.filter(email_id = user).update(department_name = request.POST.get("checkbox_val"))
            Profiles.objects.filter(email_id = user).update(role = request.POST.get("role"))
            Profiles.objects.filter(email_id = user).update(address = request.POST.get("address"))
            return redirect("/profile/")
        return render(request,"Mainpage/edit_profile.html")

def Leaves_page(request):
    user = request.user
    allows = 0
    if Profiles.objects.filter(email_id = user).all().exists():
        allows = 1
        if request.method == "POST":
            type = request.POST.get("reason")
            reasion = request.POST.get("leave_reason")
            start = request.POST.get("start")
            end = request.POST.get("end")
            id = user.id
            leave_data = LeaveManager(leave_type = type,leave_reason = reasion,start_date = start,end_date = end,emp_id = id)
            leave_data.save()
        leaves = LeaveManager.objects.filter(emp_id = user.id).all()
        return render(request,"Mainpage/leaves.html",{"leaves":leaves,"allows":allows})
    else:
        allows = 0
        messages.warning(request,"Please first complete profile after then apply for leaves.")
        return render(request,"Mainpage/leaves.html",{"allows":allows})

def salary_slip(request):
    user = request.user
    profile_data = Profiles.objects.filter(email_id = user).all().values()[0]
    name =  profile_data["full_name"]
    Department = profile_data["department_name"][1:]
    role = profile_data["role"]
    start_date = profile_data["dateofjoin"]
    end_date = start_date + relativedelta(years=1)
    salary = profile_data["salary"]
    months = ["January","February","March","April","May","June","July","August","September","Octomber","Navember","December"]
    PF = (salary * 12)/100
    PT = 1000
    gross_deduct = PF + PT
    netpay = salary - gross_deduct
    total_salary = salary * 12
    total_pf = PF * 12
    total_pt = PT * 12
    total_deduct = gross_deduct * 12
    total_netpay = netpay * 12
    today_date = date.today()
    salary_list = []
    for i in range(len(months)):
        salary_dict = {}
        salary_dict["Months"] = months[i]
        salary_dict["Salary"] = salary
        salary_dict["PF"] = PF
        salary_dict["PT"] = PT
        salary_dict["gross"] = gross_deduct
        salary_dict["net"] = netpay
        salary_list.append(salary_dict)
    salary_dict = {}
    salary_dict["Months"] = "Total Salary"
    salary_dict["Salary"] = total_salary
    salary_dict["PF"] = total_pf
    salary_dict["PT"] = total_pt
    salary_dict["gross"] = total_deduct
    salary_dict["net"] = total_netpay
    salary_list.append(salary_dict)
    salary_dict = {}
    salary_dict["Months"] = ""
    salary_dict["Salary"] = ""
    salary_dict["PF"] = ""
    salary_dict["PT"] = ""
    salary_dict["gross"] = "Total Pay"
    salary_dict["net"] = total_netpay
    salary_list.append(salary_dict)
    return render(request, "Mainpage/salary_slip.html",{"salary_list":salary_list,"start_date":start_date,"end_date":end_date,"today_date":today_date,"Department":Department,"name":name,"role":role})

def attendance(request):
    user = request.user
    allows = 0
    if Profiles.objects.filter(email_id = user).all().exists():
        allows = 1
        if request.user.is_authenticated:
            today = datetime.date.today()
            times = datetime.datetime.now().time()
            arrive_time = datetime.time(9,00,00)
            user = request.user
            if attendacemanager.objects.filter(emp_id = user.id).filter(attendance_date = today):
                messages.warning(request, "You are already attended for today")
            else:
                if request.method == "POST":
                    if arrive_time < times:
                        attendance = attendacemanager(emp_id = user.id,attendance_desc="Late")
                        attendance.save()
                    else:
                        attendance = attendacemanager(emp_id = user.id,attendance_desc = "Early")
                        attendance.save()
            attendance = attendacemanager.objects.filter(emp_id = user.id)
            return render(request,"Mainpage/attendance.html",{"attendance":attendance,"allows":allows})
        return render(request,"Mainpage/attendance.html",{"allows":allows})

    else:
        allows = 0
        messages.warning(request,"Please first complete profile after then see the tasks.")
        return render(request,"Mainpage/attendance.html",{"allows":allows})

def mysalary(request):
    user = request.user
    allows = 0
    slip_allow = 0
    profile_data = Profiles.objects.filter(email_id = user).all().values()[0]
    name =  profile_data["full_name"]
    Department = profile_data["department_name"][1:]
    role = profile_data["role"]
    today_date = date.today()
    if Profiles.objects.filter(email_id = user).all().exists():
        profile_data = Profiles.objects.filter(email_id = user).all().values()[0]
        salary = profile_data["salary"]
        allows = 1
        if request.method == "POST":
            slip_allow = 1
            select_value = request.POST.get("selected_data")
            if select_value == "Year":
                salary_table = SalaryTable.objects.filter(emp_id = user.id).all().values()
                print(salary_table)
                return render(request, "Mainpage/salary.html",{"allows" :allows,"salary":salary,"name":name,"department":Department,"role":role,"slip_allow":slip_allow,"salary_table":salary_table,"today_date":today_date})
            else:
                salary_table = SalaryTable.objects.filter(emp_id = user.id).filter(months = select_value).all().values()
                return render(request, "Mainpage/salary.html",{"allows" :allows,"salary":salary,"name":name,"department":Department,"role":role,"slip_allow":slip_allow,"salary_table":salary_table,"today_date":today_date})
        return render(request, "Mainpage/salary.html",{"allows" :allows,"salary":salary,"name":name,"department":Department,"role":role,"slip_allow":slip_allow,"today_date":today_date})
    else:
        allows = 0
        slip_allow = 0
        return render(request, "Mainpage/salary.html",{"allows" :allows,"slip_allow":slip_allow})
def logout_page(request):
    logout(request)
    return redirect("/")
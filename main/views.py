from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import (
    ChangePasswordForm,
    UserFormRegister,
    AddDepartmentForm,
    AddPositionForm,
    AddEmployeeForm,
    EditEmployeeForm,
)
from .models import (
    DataModelUser,
    ExtendUser,
    DepartmentModel,
    PositionModel,
    EmployeeModel,
)


def index(request):
    data = request.POST
    return render(request, "pages/main.html")


def saveuser_db(request):
    login = request.POST.get("login")
    password = request.POST.get("password")
    user = DataModelUser.objects.get(login=login)
    if check_password(password, user.password):
        print(password)
        return HttpResponse("Ты вошел")

    return render(request, "pages/main.html")


class RegisterView(CreateView):
    model = ExtendUser
    template_name = "user/user_register.html"
    form_class = UserFormRegister
    success_url = reverse_lazy("main:profile")


@login_required
def change_password(request):
    if request.method == "POST":
        passwords = request.POST
        user = request.user
        old_password = passwords["old_password"]
        new_password1 = passwords["new_password1"]
        new_password2 = passwords["new_password2"]
        print(old_password)
        if check_password(old_password, user.password):
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                message = "Ваш пароль успешно изменен"
                return render(
                    request, "user/change_password.html", context={"message": message}
                )
            else:
                error = "Пароли не совпадают"
                return render(request, "user/profile.html", context={"error": error})
    form = ChangePasswordForm()
    return render(request, "user/change_password.html", context={"form": form})


class LogoutUserView(LoginRequiredMixin, LogoutView):
    template_name = "pages/main.html"


@login_required
def profile_user(request):
    data = request.POST
    dataDepartment = DepartmentModel.objects.all()
    dataPosition = PositionModel.objects.all()
    dataEmployee = EmployeeModel.objects.all()

    return render(
        request,
        "user/profile.html",
        {
            "dataDepartment": dataDepartment,
            "dataPosition": dataPosition,
            "dataEmployee": dataEmployee,
        },
    )


class LoginUserView(LoginView):
    template_name = "user/login.html"
    redirect_field_name = "profile.html"


def all_employees_view(request, id=None):
    all_employees = EmployeeModel.objects.prefetch_related().all()
    context = {"all_employees": all_employees}
    if id:
        employee = EmployeeModel.objects.get(id=id)
        context["employee"] = employee
    return render(request, "user/employees.html", context)


def all_departments_view(request, id=None):
    all_departments = DepartmentModel.objects.prefetch_related().all()
    context = {"all_departments": all_departments}
    if id:
        department = DepartmentModel.objects.get(id=id)
        context["department"] = department
    return render(request, "pages/departments.html", context)


def all_position_view(request, id=None):
    all_positions = PositionModel.objects.prefetch_related().all()
    context = {"all_positions": all_positions}
    if id:
        position = PositionModel.objects.get(id=id)
        context["position"] = position
    return render(request, "pages/positions.html", context)


def add_employee_view(request):
    newemp = EmployeeModel.objects.all()
    if request.method == "POST":
        newemp_form = AddEmployeeForm(request.POST)
        if newemp_form.is_valid():
            newemp_form.save()
            return render(
                request,
                "user/profile.html",
                {"text": "Сотрудник добавлен", "newemp": newemp},
            )
        else:
            return render(
                request,
                "user/add_employee.html",
                {"text": "Форма оформлена не правильно", "newemp": newemp},
            )
    else:
        newemp_form = AddEmployeeForm()
        return render(request, "user/add_employee.html", {"form": newemp_form})


def add_department_view(request):
    newdep = DepartmentModel.objects.all()
    if request.method == "POST":
        newdep_form = AddDepartmentForm(request.POST)
        if newdep_form.is_valid():
            newdep_form.save()
            return render(
                request,
                "user/profile.html",
                {"text": "Подразделение добавлено", "newdep": newdep},
            )
        else:
            return render(
                request,
                "pages/add_department.html",
                {"text": "Форма оформлена не правильно", "newdep": newdep},
            )
    else:
        newdep_form = AddDepartmentForm()
        return render(request, "pages/add_department.html", {"form": newdep_form})


def add_position_view(request):
    newpos = PositionModel.objects.all()
    if request.method == "POST":
        newpos_form = AddPositionForm(request.POST)
        if newpos_form.is_valid():
            newpos_form.save()
            return render(
                request,
                "user/profile.html",
                {"text": "Должность добавлена", "newpos": newpos},
            )
        else:
            return render(
                request,
                "pages/add_position.html",
                {"text": "Форма оформлена не правильно", "newpos": newpos},
            )
    else:
        newpos_form = AddPositionForm()
        return render(request, "pages/add_position.html", {"form": newpos_form})


def edit(request, id):
    edit_employee = EmployeeModel.objects.get(id=id)

    if request.method == "POST":
        edit_form = EditEmployeeForm(request.POST, instance=edit_employee)
        if edit_form.is_valid():
            edit_form.save()

            return render(
                request,
                "user/profile.html",
                {"text": "Сотрудник переведен в другой отдел", "edit_form": edit_form},
            )
        else:
            return render(
                request,
                "user/edit_employee.html",
                {"text": "Форма оформлена не правильно", "edit_form": edit_form},
            )
    else:
        edit_form = EditEmployeeForm()
        return render(request, "user/edit_employee.html", {"form": edit_form})


def del_position(request, id=None):
    position = PositionModel.objects.get(id=id)
    position.delete()
    return render(request, "user/profile.html", {"text": "Должность удалена"})


def del_employee(request, id=None):
    employee = EmployeeModel.objects.get(id=id)
    employee.delete()
    return render(request, "user/profile.html", {"text": "Сотрудник удален"})


def del_department(request, id=None):
    department = DepartmentModel.objects.get(id=id)
    department.delete()
    return render(request, "user/profile.html", {"text": "Подразделение удалено"})

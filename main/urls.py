from django.urls import path
from .views import (
    index,
    saveuser_db,
    RegisterView,
    change_password,
    LogoutUserView,
    profile_user,
    LoginUserView,
    add_employee_view,
    add_department_view,
    add_position_view,
    all_employees_view,
    all_position_view,
    all_departments_view,
    del_position,
    del_employee,
    del_department,
    edit,
)


app_name = "main"


urlpatterns = [
    path("", index, name="main"),
    path("saveuser/", saveuser_db, name="saveuser"),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/change_password/", change_password, name="change_password"),
    path("accounts/logout/", LogoutUserView.as_view(), name="logout"),
    path("accounts/profile/", profile_user, name="profile"),
    path("accounts/login/", LoginUserView.as_view(), name="login"),
    path("add_employee/", add_employee_view, name="add_employee"),
    path("employees/<int:id>/", all_employees_view, name="employee"),
    path("employees/", all_employees_view, name="employees"),
    path("employees/del_employee/<int:id>/", del_employee, name="del_employee"),
    path("add_department/", add_department_view, name="add_department"),
    path("departments/<int:id>/", all_departments_view, name="department"),
    path("departments/", all_departments_view, name="departments"),
    path(
        "departments/del_department/<int:id>/", del_department, name="del_departments"
    ),
    path("add_position/", add_position_view, name="add_position"),
    path("positions/<int:id>/", all_position_view, name="position"),
    path("positions/", all_position_view, name="positions"),
    path("positions/del_position/<int:id>/", del_position, name="del_position"),
    path("employees/<int:id>/edit/", edit, name="edit"),
]

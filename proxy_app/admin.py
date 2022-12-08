from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class ProxyAdmin(admin.ModelAdmin):
    list_display = ["name", "type"]
    list_per_page = 25




# ---------------------- EXAMPLE --------------------

# In [1]: from proxy_app.models import Employee, ManagerEmployee
# In [2]: e1 = Employee.objects.create(name="Raju")
# In [3]: e1
# Out[3]: <Employee: Al Amin>   # Employee object created with type 'D'

# In [4]: e1.type
# Out[4]: u'D'
# In [2]: e2 = ManagerEmployee.objects.create(name="Raju")
# In [6]: e2
# Out[6]: <ManagerEmployee: Raju>    # object created with type 'M' for model ManagerEmployee(original model Employee)

# In [3]: e2.type
# Out[3]: u'M'

# In [4]: ManagerEmployee.objects.all()    # To get all ManagerEmployee objects(or type 'M') as we defined in ManagerEmpManager class.
# Out[4]: <QuerySet [<ManagerEmployee: Raju>]>

# In [5]: Employee.objects.all()
# Out[5]: <QuerySet [<Employee: Raju>, <Employee: Raju>]>

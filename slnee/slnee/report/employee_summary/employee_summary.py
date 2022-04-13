import frappe
from frappe import _
from erpnext.hr.doctype.leave_application.leave_application import get_leave_details

def execute(filters=None):


	if not filters:
		filters = {}
	columns=get_columns()
	data,chart,summary=get_data(filters)
	return columns,data,None,chart,summary

def get_columns():
	return[
	_('Employee') + ":Link/Employee:120",
	 _('Full Name') + ":Data:160",
	_('Designation') + ":Data:120",
	_('Passport Number') + ":Data:120",
	_('Nationality') + ":Data:120",
	_('Date of birth') + ":Data:120",
	_('Salary') + ":Data:120",
	_('Bank account number') + ":Data:120",
	_('Phone number') + ":Data:120",
	_('Email') + ":Data:120",
	_('Vacation leave balance') + ":Data:120",
	_('On Leave') + ":Data:120",
	_('Status') + ":Data:120",
	]
def get_data(filters):
	flags={}
	stats=filters["status"]
	if "sort" in list(filters.keys()):
		if filters["sort"]=="Name":
			sort="employee_name"
		elif filters["sort"]=="Last modified on":
			sort="modified"
		else:
			sort="salary"
	else:
		sort="first_name"
	if filters["type"]=="Ascending":
		type=" asc"
	else:
		type=" desc"
	filters.pop("type")
	try:
		filters.pop("sort")
	except:
		pass
	active=0
	if "greater_than" in list(filters.keys()) and filters["greater_than"]:
		try:
			salary_limit=float(filters["greater_than"])
		except:
			pass
	else:
		salary_limit=0
	f=[]
	if "on_leave" in list(filters.keys()) and filters["on_leave"]!="" :
		f=[]
		if "employee" in list(filters.keys()) and filters["employee"] != "":
			emp=[filters["employee"]]
			e=frappe.db.get_list("Attendance",filters={"status":"On Leave","attendance_date":frappe.utils.nowdate(),"employee":emp[0]},fields={"employee"})
			if len(e)==0 and filters["on_leave"]=="Yes":
				emp=[]
			if len(e)>0 and filters["on_leave"]=="No":
				emp=[]
			filters.pop("employee")
			f.append(["name","in",emp])
		else:
			emp=frappe.db.get_list("Attendance",filters={"status":"On Leave","attendance_date":frappe.utils.nowdate()},fields={"employee"})
			emp=[e["employee"] for e in emp]
			if filters["on_leave"]=="Yes":
				f.append(["name","in",emp])
			if filters["on_leave"]=="No":
				f.append(["name","not in",emp])
	else:
		if "employee" in list(filters.keys()) and filters["employee"] != "":
			f.append(["employee","in",[filters["employee"]]])
	if "designation" in list(filters.keys()):
		f.append(["designation",'in',filters["designation"]])
	if "nationality" in list(filters.keys()):
		f.append(["nationality",'in',filters["nationality"]])
	if "company" in list(filters.keys()):
		f.append(["company",'in',[filters["company"]]])
	
	filters=f
	try:
		filters.pop("on_leave")
	except:
		pass
	try:
		filters.pop("greater_than")
	except:
		pass
	try:
		filters.pop("status")
	except:
		pass
	if stats:
		filters.append(["status","in",stats])
	order=sort+type
	if sort=="salary":
		order=""
	ll=frappe.db.get_list("Employee",filters=filters,fields=["status","name","employee_name","designation","passport_number","date_of_birth","bank_ac_no","cell_number","personal_email","nationality"],order_by=order)
	data=[]
	labels=[]
	values=[]
	values2=[]
	total_salary=0
	active=0
	total_on_leaves=0
	for i in ll:
		d={}
		d["employee"]=i["name"]
		d["full_name"]=i["employee_name"]
		d["designation"]=i["designation"]
		d["passport_number"]=i["passport_number"]
		d["date_of_birth"]=i["date_of_birth"]
		struct=get_salary_structure(i["name"])
		if struct:
			doc = frappe.get_doc("Salary Structure Assignment", struct)
			dataa={}
			dataa['base']=doc.base
			dataa['variable']=doc.variable
			struct=doc.salary_structure
			doc=frappe.get_doc("Salary Structure",struct)
			amount=0
			try:
				ishp=frappe.db.get_value("Employee",i["name"],"is_household_provided")
				dataa["is_household_provided"]=ishp
			except:
				dataa["is_household_provided"]=0
			for e in doc.earnings:
				if e.abbr in ["base","housing","var"]:
					f=e.formula
					for j in list(dataa.keys()):
						f=f.replace(j,"dataa['"+str(j)+"']")
					new=eval(f.replace('\n',""))
					dataa[e.abbr]=new
					amount+=new
			d["salary"]=amount
		else:
			d["salary"]=0
		if d["salary"]>= salary_limit:
			total_salary+=d["salary"]
			d["bank_account_number"]=i["bank_ac_no"]
			d["phone_number"]=i["cell_number"]
			d["email"]=i["personal_email"]
			leave = get_leave_details(i['name'],frappe.utils.nowdate())["leave_allocation"]
			l=0
			if "vacation" in list(leave.keys()):
				l=leave["vacation"]["remaining_leaves"]
			d["vacation_leave_balance"]=l
			d["on_leave"]="No"
			if i["nationality"] not in list(flags.keys()):
				flags[i["nationality"]]=frappe.db.get_value("Country",i["nationality"],"flag")
			lab=i["employee_name"]
			if i["designation"]:
				lab+= " ("+i["designation"]+")"
			if i["nationality"] :
				if flags[i["nationality"]]:
					lab+="<br><img src='"+flags[i["nationality"]]+"' style='margin-left:-2px;height:10px;width:auto' alt='' /> "+i["nationality"]
					d["nationality"]="<img src='"+flags[i["nationality"]]+"' style='margin-left:-2px;height:10px;width:auto' alt='' /> " + i["nationality"]
				else:
					lab+="<br>"+i["nationality"]
					d["nationality"]=i["nationality"]
			if i["cell_number"]:
				lab+="<br><img src='/files/telephone-fill.svg' style='height:10px;width:auto' alt='' /> "+i["cell_number"]
			if i["personal_email"]:
				lab+="<br><img src='/files/envelope.svg' style='height:10px;width:auto' alt='' /> "+i["personal_email"]
			if i["bank_ac_no"]:
				lab+="<br><img src='/files/bank.svg' style='height:10px;width:auto' alt='' /> "+i["bank_ac_no"]
			labels.append(lab)
			if i["status"]=="Active":
				active+=1
				d["status"]="<span style='color:green;'>"+i["status"]+"</span>"
			elif i["status"]=="Inactive" or i["status"]=="Left":
				d["status"]="<span style='color:black;'>"+i["status"]+"</span>"
			else:
				d["status"]="<span style='color:red;'>"+i["status"]+"</span>"
			data.append(d)
			values.append(d["salary"])
			values2.append(d["vacation_leave_balance"])
	leave=frappe.db.get_list("Attendance",filters={"status":"On Leave","attendance_date":frappe.utils.nowdate()},fields={"employee"})
	leave=[l["employee"] for l in leave]
	for ii in range(len(data)):
		d=data[ii]
		if d["employee"] in leave:
			total_on_leaves+=1
			d["on_leave"]="<span style='color:red;'>Yes</span>"
	#chart = {'data':{'labels':labels,"datasets": [{"name": "full_name", "values": "salary"}]}}
	nn=len(data)
	if nn==0:
		average=0
	else:
		average = total_salary/len(data)
	if sort=="Salary":
		data9=[]
		labels9=[]
		values9=[]
		values29=[]
		for i in range(nn):
			ind=max_salary(data)
			data9.append(data[ind])
			labels9.append(labels[ind])
			values9.append(values[ind])
			values29.append(values2[ind])
			data.pop(ind)
			labels.pop(ind)
			values.pop(ind)
			values2.pop(ind)
	chart = {'data':{'labels':labels,'datasets':[{'name':'salary','values':values} , {'name':'Leave Balance','values': values2}]},'type':'bar'}
	report_summary = [	{"label":"Total Employees","value":nn,'indicator':'Blue',"width":50},
				{"label":"Active","value":active,'indicator':'Green'},
				{"label":"On Leave today","value":"<span style='color:#f78d02'>"+str(total_on_leaves)+"</span>",'indicator':'f78d02'},
				{"label":"Total Salary","value":"{:,.2f} SAR".format(total_salary),'indicator':'Red'},
				{"label":"Average Salary","value":"<span style='color:#6402f7;'>"+"{:,.2f} SAR".format(average)+"</span>"}]
	return(data,chart,report_summary)



def get_salary_structure(employee):
	cond = """and sa.employee=%(employee)s and (sa.from_date <= %(start_date)s or
				sa.from_date <= %(end_date)s )"""
	st_name = frappe.db.sql(
			"""
			select sa.name
			from `tabSalary Structure Assignment` sa join `tabSalary Structure` ss
			where sa.salary_structure=ss.name
				and sa.docstatus = 1 and ss.docstatus = 1 and ss.is_active ='Yes' %s
			order by sa.from_date desc
			limit 1
		"""
			% cond ,
			{
				"employee": employee,
				"start_date":frappe.utils.nowdate(),
				"end_date": frappe.utils.nowdate(),
			},
		)
	if st_name:
		return(st_name[0][0])
	return None




def max_salary(data):
	if len(data)==1:
		return(data[0])
	ind=0
	ma=data[0]["salary"]
	for i in range(1,len(data())):
		if data[i]["salary"]> ma:
			ind=i
			ma=data[i]["salary"]
	return(ind)

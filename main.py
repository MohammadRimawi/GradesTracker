
import os,pathlib,csv,json,math,webbrowser
from pprint import pprint
from tabulate import tabulate

config ={
    
}

class _Course:
    def __init__(self,):
        self.id=""
        self.name_en = ""
        self.name_ar = ""
        self.credit=0
        self.result=""
        self.status=""
        self.prerequisite=""
        self.first_mark=0
        self.second_mark=0
        self.third_mark=0
        self.final_mark=0
        self.day=""
        self.time=""
        self.year=0
        self.semester=0
        self.section=""
        self.is_pass_fail=False
        self.type=""

    def read_semester(self,course_dict):
        self.id=course_dict["Course Number"]
        self.name_en= course_dict["Course Title"]
        self.credit=course_dict["Course Hours"]
        self.section=course_dict["Section"]
        self.day=course_dict["Day"]
        self.time=course_dict["Time"]
        self.first_mark=course_dict["First Mark"]
        self.second_mark=course_dict["Second"]
        self.third_mark=course_dict["Third"]
        self.final_mark=course_dict["Final Exam"]
        self.result=course_dict["Result"]
        self.status=course_dict["Course Status"]
        self.is_pass_fail=course_dict["pass_fail"]
        self.year=course_dict["year"]
        self.semester=course_dict["semester"]

    def get_mark(self):
        try:
            if(int(self.credit)==0):
                return 0
            else:
                return math.ceil(float(self.first_mark)+float(self.second_mark)+float(self.third_mark)+float(self.final_mark))
        except:
            pprint(self.__dict__)
        return 0  


courses =[]

def passed(courses_list=[]):
    passed_courses=[]
    if len(courses_list)==0:
        courses_list=courses
    for c in courses_list:
        if c.result.lower()=="pass":
            passed_courses.append(c)
    return passed_courses

def pass_fail():
    pass_fail_courses=[]
    for c in courses:
        if c.is_pass_fail:
            pass_fail_courses.append(c)
    return pass_fail_courses

def calc_avg(courses_list=[]):
    total_marks = 0
    total_hours = 0
    pass_fail_hours=0
    pass_fail_marks=0
    if len(courses_list)==0:
        courses_list=passed()
    for c in courses_list:
            
        if c.result.lower()=="pass":
            mark = c.get_mark()
            credit = c.credit
            # print(mark,credit)
            if c.is_pass_fail:
                pass_fail_marks += int(mark)*int(credit)
                pass_fail_hours += int(credit)
            total_marks += int(mark)*int(credit)
            total_hours += int(credit)
    # print("Without Pass/Fail:")
    # print("Total hours:",total_hours,"Total marks:", total_marks,"Average:",round(total_marks/total_hours,1))
    # print("With Pass/Fail:")
    # print("Total hours:",total_hours-pass_fail_hours,"Total marks:", total_marks-pass_fail_marks,"Average:",round((total_marks-pass_fail_marks)/(total_hours-pass_fail_hours),1))
    return (total_hours,round(total_marks/total_hours,1),total_hours-pass_fail_hours,round((total_marks-pass_fail_marks)/(total_hours-pass_fail_hours),1),)

def get_semester(year ,semester):
    semester_courses=[]
    for c in courses:
        if int(c.year)==year and int(c.semester)==semester:
            semester_courses.append(c)
    return semester_courses

def load_semesters():
    for path in pathlib.Path("semesters").iterdir():
    
        if path.is_file():
            current_file = open(path, "r")
            header = current_file.readline().strip().split('\t')
            # print(header)
            file_name =current_file.name.split('\\')[1].split('.tsv')[0]

            for line in current_file:
                course_info = line.strip().split('\t')
                # print(course_info)
                
                course = {}
                c = _Course()
                for i in range(len(header)):
                    course[header[i]]=course_info[i]
                course["pass_fail"]=line[0]==" "
                course["year"]=file_name[1]
                course["semester"]=file_name[3]
                # print(course)
                c.read_semester(course)
                
                courses.append(c)
def analysis():
    cumulative_list=[]
    table=[]
    header=["Semester","Avg.\nBefore","Semester\nAvg.","Avg.\nAfter","Delta","Hours","no.\ncourses"]
    for y in range(1,5):
        for s in range(1,4):
            courses_list=get_semester(y,s)
            row=[]
            if len(courses_list)!=0:
                print("Y"+str(y)+"S"+str(s))
                row.append("Y"+str(y)+"S"+str(s))
                
                t1,m1,pt1,pm1=calc_avg(cumulative_list) #before

                t2,m2,pt2,pm2=calc_avg(courses_list) 
                
                cumulative_list.extend(courses_list) #after
                t3,m3,pt3,pm3=calc_avg(cumulative_list)

                row.extend([pm1,pm2,pm3])
                delta=""
                if round(pm3-pm1,1)<0:
                    delta="\033[0;31m "+str(round(pm3-pm1,1))+"  \033[0;0m"
                else:
                    delta="\033[0;32m  "+str(round(pm3-pm1,1))+"  \033[0;0m"
                row.append(round(pm3-pm1,1))
                row.append(t2)
                row.append(len(passed(courses_list)))
                table.append(row)
                # print(x,y,z,e)
    print(tabulate(table, header, tablefmt="pretty"))
    return table,header
    


def summary(row):
    output=""
    for item in row:
        output+="<td>"+str(item)+"</td>"
    return output

def semester_info(semester):
    courses_list=get_semester(int(semester[1]),int(semester[3]))
    table=" <thead><tr>"
    table +='<th scope="col">ID</th>'
    table +='<th scope="col">Name</th>'
    table +='<th scope="col">First</th>'
    table +='<th scope="col">Second</th>'
    table +='<th scope="col">Third</th>'
    table +='<th scope="col">Final</th>'
    table +='<th scope="col">Total</th>'
    table +='<th scope="col">Result</th>'
    table +='<th scope="col">Status</th>'
    table+= '</tr></thead><tbody>'                 
    for c in courses_list:
        print(c.__dict__)
        pass_fail="table-success"
        if c.is_pass_fail:
            pass_fail="table-warning"
        if c.status.lower()=="withdrawal":
            pass_fail="table-danger"
        table+="<tr class="+pass_fail+">"
        table+='<th scope="col">'+c.id+'</th>'
        table+='<th scope="col">'+c.name_en+'</th>'
        table+='<th scope="col">'+c.first_mark+'</th>'
        table+='<th scope="col">'+c.second_mark+'</th>'
        table+='<th scope="col">'+c.third_mark+'</th>'
        table+='<th scope="col">'+c.final_mark+'</th>'
        table+='<th scope="col">'+str(c.get_mark())+'</th>'
        table+='<th scope="col">'+c.result+'</th>'
        table+='<th scope="col">'+c.status+'</th>'
        table+="</tr>"

    table+="</tbody>"
    print(table)
    return table

def build_accordions():
 
    table,header = analysis()
    accordions=""
    for row in table:
        accordions+='''
        <div class="accordion-item">
        <div class="accordion-header" id="'''+str(row[0])+'''1">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                data-bs-target="#'''+str(row[0])+'''" aria-expanded="false" aria-controls="'''+str(row[0])+'''1">
                                <table class="table">
                                    <tr>
                                        '''+summary(row)+''' 
                                    </tr>
                                </table>
                            </button>
                        </div>
                        <div id="'''+str(row[0])+'''" class="accordion-collapse collapse" aria-labelledby="'''+str(row[0])+'''"
                            data-bs-parent="#accordionExample">
                            <div class="accordion-body">
                                <table class="table table-striped">
                
                                    '''+semester_info(row[0])+'''
                                    
                                </table>
                            </div>
                        </div>
                    </div>    
        '''
    return accordions
def build_body():
   
    body ='''  <body>

            <div class="accordion" id="accordionExample">
            ''' +build_accordions()+'''
            </div>
        </body>'''
    

    return body



def build_html():

    head= '''
    <!DOCTYPE html>
    <html lang="en">

    <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous">
    </script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">

    <style>
        .table{
            border-color: white !important;
            margin: 0 !important;
            border-width: 0 !important;
        }
        .PassFail{
            background: lightslategrey;
        }
        .accordion-body{
            padding:0;
        }
    </style>
        </head>'''+ build_body()+''' 
 

    </html>
            '''

    return head

if __name__ == "__main__":

    load_semesters()
  
    # analysis()

    # with open("test.html","w") as f:
    #     f.write(build_html())
    # f.close()
    # webbrowser.open("test.html")

    # print(build_accordions())


    # for path in pathlib.Path("courses").iterdir():
    #     if path.is_file():
    #         current_file = open(path, "r")
    #         header = current_file.readline().strip().split('\t')

    #         file_name =current_file.name.split('\\')[1].split('.tsv')[0]
    #         for line in current_file:
    #             course_info = line.strip().split('\t')
    #             # print(course_info)
    #             course = {}
    #             for i in range(len(header)):
    #                 if(i>=len(course_info)):
    #                     course[header[i]]=""
    #                 else:   
    #                     course[header[i]]=course_info[i]
    #             course["type"]=file_name
    #             courses[course["Course Number"]]=course

    #         # pprint(courses)
    #         current_file.close()
    # print("31153" in passed())
   

    # pprint(passed(),indent=4)
            # exit()

    # pprint(pass_fail(), indent=4, width=200, sort_dicts=False)
    # s=_Course()
    # pprint(s.__dict__, indent=4, width=200, sort_dicts=False)
        
 



                # pprint(c.__dict__, indent=4, width=200, sort_dicts=False)
    
    # for c in passed():
    #     pprint(c.__dict__, indent=4, width=200, sort_dicts=False)


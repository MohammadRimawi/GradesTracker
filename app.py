from flask import Flask,render_template,request
import os,pathlib,csv,json,math,webbrowser
from pprint import pprint
from tabulate import tabulate

app=Flask(__name__)


tast=["hello","fathi"]
class Semester:
    semesters=[]

    def __init__(self,):
        self.year=0
        self.semester=0
        self.courses=[]
        self.number_of_course=0
        self.semester_hours=0
        self.semester_pass_fail_hours=0
        self.semester_sum=0
        self.semester_pass_fail_sum=0
        self.semester_average=0
        self.cumulative_sum=0
        self.cumulative_average=0
        self.cumulative_hours=0
        self.cumulative_pass_fail_hours=0
        self.cumulative_pass_fail_sum=0
        self.number_of_pass_fail_courses=0
        self.performance="N/A"

    @staticmethod
    def update_semesters():
        
        s = Semester()
        Semester.semesters=[]

        sem = 0
        year = 0
        
        cumulative_pass_fail_hours=0
        cumulative_pass_fail_sum=0
        cumulative_sum=0
        cumulative_hours=0



        

        for c in Course.courses:
            if(c.year!=year or c.semester != sem):
                prev=0
                try:
                    prev=round((cumulative_sum-cumulative_pass_fail_sum)/(cumulative_hours-cumulative_pass_fail_hours),1)
                except:
                    prev="N/A"
                if len(s.courses)!=0:
                    print(s.year,s.semester)
                    cumulative_pass_fail_hours+= s.semester_pass_fail_hours
                    s.cumulative_pass_fail_hours = cumulative_pass_fail_hours

                    cumulative_pass_fail_sum+=s.semester_pass_fail_sum
                    s.cumulative_pass_fail_sum = cumulative_pass_fail_sum

                    cumulative_hours += s.semester_hours
                    s.cumulative_hours = cumulative_hours

                    cumulative_sum += s.semester_sum
                    s.cumulative_sum = cumulative_sum

                    try:
                        s.semester_average=round((s.semester_sum-s.semester_pass_fail_sum)/(s.semester_hours-s.semester_pass_fail_hours),1)
                    except:
                        s.semester_average=0
                    try:
                        s.cumulative_average=round((s.cumulative_sum-s.cumulative_pass_fail_sum)/(s.cumulative_hours-s.cumulative_pass_fail_hours),1)
                    except:
                        s.cumulative_average=0


                    if prev!="N/A":
                        if round(s.cumulative_average-prev,1)>0:
                            s.performance= "+"+str(round(s.cumulative_average-prev,1))
                        else:
                            s.performance= str(round(s.cumulative_average-prev,1))
                    Semester.semesters.append(s)

                s = Semester()
                year =c.year
                sem = c.semester
                s.year=year
                s.semester=sem

            if c.result.lower()=="pass":
                s.semester_hours+=c.credit
                s.number_of_course+=1
                s.semester_sum+=c.get_mark()*c.credit
                
            if c.is_pass_fail: 
                s.semester_pass_fail_hours+=c.credit
                s.number_of_pass_fail_courses+=1
                s.semester_pass_fail_sum+=c.get_mark()*c.credit
                
            s.courses.append(c)

        prev=0
        try:
            prev=round((cumulative_sum-cumulative_pass_fail_sum)/(cumulative_hours-cumulative_pass_fail_hours),1)
        except:
            prev="N/A"
        print(s.year,s.semester)
        cumulative_pass_fail_hours+= s.semester_pass_fail_hours
        s.cumulative_pass_fail_hours = cumulative_pass_fail_hours

        cumulative_pass_fail_sum+=s.semester_pass_fail_sum
        s.cumulative_pass_fail_sum = cumulative_pass_fail_sum

        cumulative_hours += s.semester_hours
        s.cumulative_hours = cumulative_hours

        cumulative_sum += s.semester_sum
        s.cumulative_sum = cumulative_sum
        try:
            s.semester_average=round((s.semester_sum-s.semester_pass_fail_sum)/(s.semester_hours-s.semester_pass_fail_hours),1)
        except:
            s.semester_average=0
        try:
            s.cumulative_average=round((s.cumulative_sum-s.cumulative_pass_fail_sum)/(s.cumulative_hours-s.cumulative_pass_fail_hours),1)
        except:
            s.cumulative_average=0

        if prev!="N/A":
            if round(s.cumulative_average-prev,1)>0:
                s.performance= "+"+str(round(s.cumulative_average-prev,1))
            else:
                s.performance= str(round(s.cumulative_average-prev,1))
        Semester.semesters.append(s)
     
    

    @staticmethod
    def load_semesters():
        cumulative_pass_fail_hours=0
        cumulative_pass_fail_sum=0
        cumulative_sum=0
        cumulative_hours=0
        for path in pathlib.Path("semesters").iterdir():
        
            prev=0
            try:
                prev=round((cumulative_sum-cumulative_pass_fail_sum)/(cumulative_hours-cumulative_pass_fail_hours),1)
            except:
                prev="N/A"

            if path.is_file():
                current_file = open(path, "r")
                header = current_file.readline().strip().split('\t')
                # print(header)
                file_name =current_file.name.split('\\')[1].split('.tsv')[0]
                s = Semester()
                s.year=int(file_name[1])
                s.semester=int(file_name[3])

                for line in current_file:
                    course_info = line.strip().split('\t')
                    # print(course_info)
                    
                    course = {}
                    c = Course()

                    for i in range(len(header)):
                        course[header[i]]=course_info[i]

                    course["pass_fail"]=line[0]==" "
                    course["year"]=file_name[1]
                    course["semester"]=file_name[3]
                    # print(course)
                    c.read_course(course)
                    # print(c.result)    

  
                    if c.result.lower()=="pass":
                        s.semester_hours+=c.credit
                        s.number_of_course+=1
                        s.semester_sum+=c.get_mark()*c.credit
                      

                    if c.is_pass_fail: 
                        s.semester_pass_fail_hours+=c.credit
                        s.number_of_pass_fail_courses+=1
                        s.semester_pass_fail_sum+=c.get_mark()*c.credit
                        

                    s.courses.append(c)
                    Course.courses.append(c)

                cumulative_pass_fail_hours+= s.semester_pass_fail_hours
                s.cumulative_pass_fail_hours = cumulative_pass_fail_hours

                cumulative_pass_fail_sum+=s.semester_pass_fail_sum
                s.cumulative_pass_fail_sum = cumulative_pass_fail_sum

                cumulative_hours += s.semester_hours
                s.cumulative_hours = cumulative_hours

                cumulative_sum += s.semester_sum
                s.cumulative_sum = cumulative_sum

                try:
                    s.semester_average=round((s.semester_sum-s.semester_pass_fail_sum)/(s.semester_hours-s.semester_pass_fail_hours),1)
                except:
                    s.semester_average=0
                try:
                    s.cumulative_average=round((s.cumulative_sum-s.cumulative_pass_fail_sum)/(s.cumulative_hours-s.cumulative_pass_fail_hours),1)
                except:
                    s.cumulative_average=0
                    
                if prev!="N/A":
                    if round(s.cumulative_average-prev,1)>0:
                        s.performance= "+"+str(round(s.cumulative_average-prev,1))
                    else:
                        s.performance= str(round(s.cumulative_average-prev,1))
                Semester.semesters.append(s)
            

    @staticmethod
    def semesters_names():
        names=[]
        for s in Semester.semesters:
            names.append("Y"+str(s.year)+"S"+str(s.semester))
        return names

    @staticmethod
    def with_pass_fail():
        with_pass_fail=[]
        for s in Semester.semesters:
            with_pass_fail.append(round((s.cumulative_sum-s.cumulative_pass_fail_sum)/(s.cumulative_hours-s.cumulative_pass_fail_hours),1))
        return with_pass_fail

    @staticmethod
    def without_pass_fail():
        without_pass_fail=[]
        for s in Semester.semesters:
            without_pass_fail.append(round((s.cumulative_sum)/(s.cumulative_hours),1))
        return without_pass_fail
    
    @staticmethod
    def print_semesters():
        for s in Semester.semesters:
            print("Y"+str(s.year)+"S"+str(s.semester))
            for c in s.courses:
                 pprint(c.__dict__, indent=4, width=200, sort_dicts=False)
            print("***************************************************")
                
 


class Course:


    courses =[]
    passed_courses=[]
    pass_fail_courses=[]

    @staticmethod
    def change_pass_fail(id):
        for c in Course.courses:
            if c.id == id :
                c.is_pass_fail= not c.is_pass_fail

    @staticmethod
    def get_semester(year ,semester):
        semester_courses=[]
        for c in Course.courses:
            if int(c.year)==year and int(c.semester)==semester:
                semester_courses.append(c)
        return semester_courses


    @staticmethod
    def print_courses():
        for c in Course.courses:
            pprint(c.__dict__, indent=4, width=200, sort_dicts=False)


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


    def read_course(self,course_dict):
        self.id=course_dict["Course Number"]
        self.name_en= course_dict["Course Title"]
        self.credit=int(course_dict["Course Hours"])
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
            pass
            # pprint(self.__dict__)
        return 0  

def calculate_average(y,c):
    s = Semester.semesters[len(Semester.semesters)*0]
    pprint(s.__dict__)
    print(s.cumulative_hours-s.cumulative_pass_fail_hours,s.cumulative_sum-s.cumulative_pass_fail_sum)
    return round((y*(s.cumulative_hours-s.cumulative_pass_fail_hours+c)-(s.cumulative_sum-s.cumulative_pass_fail_sum))/c,1)
    # print()



dark_mode=True
dark_mode=False

@app.route('/')
def index():
    return render_template("index.html",Semester=Semester,dark_mode=dark_mode)

@app.route('/change_pass_fail', methods=['POST'])
def change_pass_fail():
    id = request.form['id']
    Course.change_pass_fail(id)
    Semester.update_semesters()

    print(id)
    return index()
    # your code
    # return a response

@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
    print(projectpath)
    return index()
    # your code
    # return a response

if __name__=="__main__":
    # print("hello")
    Semester.load_semesters()
    # Course.change_pass_fail("31111")
    # Semester.update_semesters()
    # print(calculate_average(80.6,16))
    app.run(host='0.0.0.0',debug=True)
    # Semester.print_semesters()
    # Course.print_courses()    

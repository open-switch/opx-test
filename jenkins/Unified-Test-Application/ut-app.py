#!/usr/bin/python

from flask import Flask, jsonify, render_template, flash, redirect, url_for, session, logging, request, send_file, Response
import os
import fnmatch
import sys
import subprocess
import jenkins
import yaml, re, json
import unicodedata, string
import ConfigParser

app = Flask(__name__)
app.secret_key = 'random string'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

#Store each playbook role details to diplay on GUI
master_dict={}
#Set an empty default value 
test=''

#Decorator to display list of roles and ansible files to select

@app.route('/GetStarted', methods=['GET', 'POST'])
def GetStarted():
    #Store list of roles for each module 
    role_data={}
    #Store the tags selected for each playbook
    global tags_selected
    tags_selected={}
    module_list=[]
    #recursive search of site.yml
    filename='site.yml'
    #Set the root path for ansible
    global root
    temp_root='/etc/ansible/playbook'
    global site_path
    try:
      site_path,root =find_path(filename, temp_root)
      print "the site_path is", site_path
    except:
      return '''<html> <h3> error: no site.yml file found in directory %s </h3> </html>'''%temp_root	    
    #Get the hosts file path from ansible.cfg
    global host_path
    config = ConfigParser.ConfigParser()
    config.read('/etc/ansible/ansible.cfg')
    host_path=config.get('defaults','hostfile')
    data=yaml.load(open(site_path,'r'))
    print data
    for i in range(0,len(data)):
        temp= data[i]['roles'][0]['role'].split('/')
        module_list.append(temp[0])
        module_list=list(set(module_list))
    for module in module_list:
        master_dict[module]={}
        role_data[module]={}
        for role_name in os.listdir(root+module+'/roles'):
            master_dict[module][role_name]={}
            role_data[module][role_name]={} #send to the tree
            master_dict[module][role_name]['varfile']="Edit/View"
            master_dict[module][role_name]['playbook']=role_name
            meta_dir=root+module+'/roles/'+role_name+'/meta'
            print "meta_dir is", meta_dir
            if os.path.isdir(meta_dir):
                print "inside the meta dir"
                for files in os.listdir(meta_dir):
                    print "the files,is",files
                    stream = open(meta_dir+'/'+files, 'r')
                    data=yaml.load(stream)
                    try:
                      master_dict[module][role_name]['meta']=data['galaxy_info']['testbed']
                    except:
                      master_dict[module][role_name]['meta']="not defined in meta/main.yml"
                    stream.close()
    print "the role data is", role_data 
    print "The master dict is", master_dict
    return render_template('GetStarted.html', roles=role_data)


#Find path for the file name and root dir given
def find_path(filename,root_path):
    file_path=""
    dir_path=""    
    for root_path, dirs, files in os.walk(root_path):
      if filename in files:
        file_path= os.path.join(root_path, filename)
        dir_path=root_path+'/'
        break
    return (file_path, dir_path)


#Return the role(key) specific details(files) from the master dictionary
def find(key, master_dict):
    print"inside find", key , "dict is", master_dict
    for k, v in master_dict.iteritems():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                global module
		module=k
    		#global test
    		role_name=key
		global var_dir
		var_dir= root+module+"/roles/"+role_name+"/vars/"
		global playbook_dir
		playbook_dir= root+module+"/roles/"+role_name+"/tasks/"	
                yield result		
	else:
		 print"no match found"


#Code to find tags/tasks for the role name given 
def finditem(key,lst):
    for dictionary in lst: #element is dictionary
      for k, v in dictionary.iteritems():
          if k=='roles':
              #print v
              if isinstance(v, list):
                for d in v:
                  for k,v in d.iteritems():
                      if v==key:
                          print dictionary
                          tag=find_tag('tags', dictionary)
			  print "****the tags is*****",tag
			  return tag
def find_tag(key, dictionary):
    for k, v in dictionary.iteritems():
        if k == key:
            if isinstance(v, list):
                return v[0]
            else:
                return v
        if isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    find(key, d)


#Read the role selected and return the role specific files to display in table row
@app.route('/read', methods=['GET','POST'])
def read_jstree():
    role = request.form['jsfields'] 
    role = role.encode('ascii','ignore')
    #global test
    test= role
    #Get the role specfic files in dictionary-result
    result= list(find(test,master_dict))
    print "the result is", result
    if test == "img_install":
        task_tags = ""
    else:
	    command="sudo ansible-playbook -i %s, %s --list-tags | grep %s | grep 'TASK TAGS'" %(host_path, site_path, test)
	    output=subprocess.check_output(command,shell=True)
	    out=str(output)
	    print "out--- for task tags", out
	    task_tags=out.split(':')[-1]
	    task_tags=task_tags.strip(' ')
	    task_tags=task_tags.strip('\n')
	    task_tags=task_tags.strip('[]')
	    print "task_tags are", task_tags
	    #task_tags= re.sub(' ','',task_tags)
	    task_tags.replace(', ',',') 
	    tags_list= task_tags.split(',')
	    for i in range(len(tags_list)):
		    tags_list[i]=tags_list[i].strip()
	    print "the tags list is", tags_list
	    for tst in ['sanity','full']:
		if tst in tags_list:
			tags_list.remove(tst)
		if tst.upper() in tags_list:
			tags_list.remove(tst.upper())
		tst_upper_first_letter= tst[0].upper()+tst[1:]
		if (tst_upper_first_letter) in tags_list:
			tags_list.remove(tst_upper_first_letter)
	    task_tags=','.join(tags_list)
	    print "the tasks result is", task_tags, tags_list
    result[0]['TaskTags']= task_tags
    return jsonify(result)


# Read the selected task_Tags
@app.route('/read_tags', methods=['GET','POST'])
def read_tags():
#function to return the selected playbook data : meta and host
    global tags_value
    key= request.form['td_first_popup']
    print "read_tags the key is", key
    key=key.encode('ascii','ignore')
    tags_value= request.form['tags_selected']
    tags_value=tags_value.encode('ascii','ignore')
    if tags_value=="":
        print "no tags selected"
        return jsonify("success but nothing selected")
    print "adding tags_value to key", tags_value,key
    tags_selected[key]=tags_value
    print "**tags_selected dictionary is ***", tags_selected 
    return jsonify("success getting tags") #{'smoketest': {'meta': '1host', 'vars': 'opx_smoke_vars.yml'}


@app.route('/editSite/')
def editSite():   
    submit_route="submitSite"
    f=open(site_path , "r")
    contents =f.read()
    f.close()
    return render_template('view_contents.html', contents=contents, submit_route=submit_route, file_location=site_path)


@app.route('/editSite/submitSite', methods=['POST'])
def submit_site():
     text=request.form["text"]
     with open(site_path,"w") as f:
         f.write(text)
     f=open(site_path, "r")
     contents =f.read()
     f.close()
     return render_template('view_changes_saved.html', package=contents, file_location=site_path)


@app.route('/editGrpVars/')
def editGrpVars():   
    grp_var_path=root+"/group_vars/all"
    f=open(grp_var_path , "r")
    contents =f.read()
    f.close()
    return render_template('view_contents.html', submit_route="submitGrpVar", contents=contents, file_location=grp_var_path)           


@app.route('/editGrpVars/submitGrpVar', methods=['POST'])
def submit_grpvars():
     text=request.form["text"]
     grp_var_path=root+"group_vars/all"
     with open(grp_var_path,"w") as f:
         f.write(text)        
     f=open(grp_var_path, "r")
     contents =f.read()
     print contents
     f.close()
     return render_template('view_changes_saved.html', package=contents, file_location=grp_var_path)


#used for displaying role independent scripts and hostvars
def view_files(abs_path, req_path, route):
    if os.path.isfile(abs_path):
         print "the abs_path is",abs_path
         with open(abs_path, 'rb') as f:
             content =f.read()
         return render_template('view_multi_files.html', content=content, file_path=abs_path)         
    final_files = []
    if os.path.isdir(abs_path):
        files = os.listdir(abs_path)
        for file in files:
            temp_file = os.path.join(req_path, file)
            print "the temp file", temp_file
            print temp_file
            final_files.append(temp_file)
    return render_template('files_list_view.html', files=final_files, route=route)


@app.route("/scripts/", defaults={'req_path': ''})
@app.route('/scripts/<path:req_path>')
def scripts(req_path):
    route="scripts"
    base_dir = "/etc/ansible"
    abs_path = os.path.join(base_dir, req_path)
    print "the req path and the abs path is ", abs_path, req_path
    return view_files(abs_path, req_path, route)


@app.route('/editHostVars/', defaults={'req_path': ''})
@app.route('/editHostVars/<req_path>')
def editHostVars(req_path):
    route="editHostVars"
    print "the result list",list(find(test,master_dict))
    abs_path = os.path.join(root+'host_vars', req_path)
    print "the req path and the abs path is ", abs_path, req_path
    return view_files(abs_path, req_path, route)


@app.route('/files/submit', methods=['POST'])
def submit_viewFiles():
	print "inside files/submit"
	text=request.form["text"]
	file_path=request.form["file-path"]
	print "--file path is", file_path 
	print file_path
	if os.path.isfile(file_path):
		with open(file_path,"w") as f:
			f.write(text)
	 	f=open(file_path, "r")
	 	contents =f.read()
	 	f.close()
	 	return render_template('view_changes_saved.html', package=contents, file_location=file_path)
	else:
		return '''<html><h3> file does not exist <h3> <html>'''


# Send the files list or indivisual file contetns (var file and playbook)
def view_files_role(abs_path, req_path, route, role_name):
        if os.path.isfile(abs_path):
             with open(abs_path, 'rb') as f:
	         content=f.read()
             return render_template('view_files.html', content=content, file_path=abs_path)	     
        final_files = []
        if os.path.isdir(abs_path):
            files = os.listdir(abs_path)
            for files in files:
                temp_file = os.path.join(req_path,files)
                print temp_file
                final_files.append(temp_file)
            return render_template('files.html', files=final_files, test=role_name, route=route)


@app.route("/editVar")
@app.route('/editVar/<test>', defaults={'req_path': ''})
@app.route('/editVar/<req_path>/<test>')
def editVar(req_path, test):
    role_name=test
    route='editVar'
    print "the result list",list(find(test,master_dict))
    print "the VAR DIR is", var_dir 
    list_files=os.listdir(var_dir)
    print "the test is--",test
    if len(list_files)>1:
        abs_path = os.path.join(var_dir, req_path)
	print "the req path and the abs path is ", abs_path, req_path
        return view_files_role(abs_path, req_path, route,role_name)
    else:
	var_path=os.path.join(var_dir,list_files[0])
        f=open(var_path , "r")    
        contents =f.read()
	print contents
        f.close()
        return render_template('view_files.html', content=contents, file_path=var_path)


@app.route("/editPlaybook/")
@app.route('/editPlaybook/<test>/', defaults={'req_path': ''})
@app.route('/editPlaybook/<test>/<req_path>')
def editPlaybook(test,req_path):
    role_name=test
    print "the result list:",list(find(role_name,master_dict))	    
    list_files=os.listdir(playbook_dir)
    if len(list_files)>1:
        route='editPlaybook'
        abs_path = os.path.join(playbook_dir, req_path)
        return view_files_role(abs_path, req_path, route,role_name)
    else:
	playbook_path=os.path.join(playbook_dir,list_files[0])
        f=open(playbook_path , "r")    
        contents =f.read()
        f.close()
        return render_template('view_contents.html', submit_route="submitPlaybook", contents=contents, file_location=playbook_path)


@app.route('/editPlaybook/submitPlaybook', methods=['POST'])
def submit_playbook():
     text=request.form["text"]    
     file_path=request.form["file_location"]
     with open(file_path,"w") as f:
         f.write(text)
     ff=open(playbook_file, "r")
     contents =ff.read()
     print contents
     ff.close()
     return render_template('view_changes_saved.html', package=contents, file_location=playbook_file)


@app.route("/editHost")
def editHost():
    print "the host_path is", host_path
    f=open(host_path, "r")
    contents =f.read()
    f.close()
    return render_template('view_contents.html', submit_route="submitHost", contents=contents, file_location=host_path)


@app.route('/submitHost', methods=['POST'])
def submit_host():
     text=request.form["text"]
     with open(host_path,"w") as f:
         f.write(text)
         f.close()
     ff=open(host_path, "r")
     contents =ff.read()
     print contents
     ff.close()
     return render_template('view_changes_saved.html', package=contents, file_location=host_path)


@app.route('/GetStarted/Ansible/Jenkins_Job', methods=['GET', 'POST'])
def GetStarted_Ansible_Jenkins_Job():
    global list_check
    list_check =  request.form['list_selected']
    #print "the image path is", image_path
    email= request.form['email']
    print "original list", list_check
    list_check= list_check.strip().split(',')
    list_check=[job.encode('ascii','ignore') for job in list_check]
    site_data=yaml.load(open(site_path, 'r'))
    print "the DATA IS",site_data
    global first_job  
    first_job=list_check[0] 
    for playbook in list_check:
        playbook=playbook.encode('ascii','ignore')
	global job_path
    	job_path='/home/jenkins/jenkins/Jenkins-Jobs-ansible/%s_job.yaml'%playbook   
    	jjbName= playbook    
    	jjb=job_path         
    	template= '/home/jenkins/jenkins/ansible_jjb_template.yaml'
    	stream = open(template, 'r')  #keep template
    	data = yaml.load(stream)
	#this will set right global values
        result= list(find(playbook,master_dict))
	role= module+"/roles/"+playbook
	print "The role is",role
    	data[0]['job-template']['builders'][0]['opx-test']['playbookPath'] = str(site_path)
	print "**host_path for test",host_path,playbook                   
    	data[0]['job-template']['builders'][0]['opx-test']['hostsPath'] = str(host_path)
    	if playbook in tags_selected:  #tags_value:
		data[0]['job-template']['builders'][0]['opx-test']['tags'] = '"'+str(tags_selected[playbook])+'"'
	else:
		tag= finditem(role,site_data)
		data[0]['job-template']['builders'][0]['opx-test']['tags'] = str(playbook)
        image_path= request.form['imagePath']
	if image_path == "":
	    data[0]['job-template']['builders'][0]['opx-test']['extraVars'] = "" #if nothing given default value will be taken	      
        else:
	    data[0]['job-template']['builders'][0]['opx-test']['extraVars'] = "image="+str(image_path)	      
    	data[0]['job-template']['publishers'][1]['email-ext']['recipients'] = str(email)
    	data[0]['job-template']['name'] = str(jjbName)
    	data[1]['project']['jobs'][0]= str(jjbName)
    	data[1]['project']['name'] = str(jjbName)
    	with open(jjb, 'w') as yaml_file:
        	yaml_file.write( yaml.dump(data, default_flow_style=False))
    if len(list_check)>1: 
        list_check=[job.encode('ascii','ignore') for job in list_check]
    	first_job=list_check[0] # .encode('ascii','ignore')
    
	for i in range(len(list_check)-1):
    	    job_path='/home/jenkins/jenkins/Jenkins-Jobs-ansible/%s_job.yaml'%list_check[i]
            stream = open(job_path, 'r')  #keep template
    	    data = yaml.load(stream)
	    stream.close()
	   
	    sec_job=list_check[i+1] #.encode('ascii','ignore')
            data[0]['job-template']['publishers'][2]['raw']['xml']=data[0]['job-template']['publishers'][2]['raw']['xml'].replace('xxx',sec_job )    
	    print"*****data", data 
    	    with open(job_path, 'w') as yaml_file:
        	yaml_file.write( yaml.dump(data, default_flow_style=False))
        	yaml_file.close()
    p=subprocess.Popen("/home/jenkins/jenkins/Unified-Test-Application/APIkey.sh",stdout=subprocess.PIPE)
    out,err=p.communicate()
    print out
    out1 = out.split()
    out2 = out1.pop()
    print out2  #jenkins token
    with open('/home/jenkins/jenkins/Jenkins-Jobs-ansible/jenkins_jobs.def', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('changeme',out2)
    with open('/home/jenkins/jenkins/Jenkins-Jobs-ansible/jenkins_jobs.ini', 'w') as file:
        file.write(filedata)
    print "the list check is ", list_check
    command="/usr/local/bin/jenkins-jobs --conf /home/jenkins/jenkins/Jenkins-Jobs-ansible/jenkins_jobs.ini update /home/jenkins/jenkins/Jenkins-Jobs-ansible"
    print "the command is",command
    proc=subprocess.Popen(command,shell=True, stdout=subprocess.PIPE)
    out,err=proc.communicate()
    print out
    first_job_path='/home/jenkins/jenkins/Jenkins-Jobs-ansible/%s_job.yaml'%first_job
    server=jenkins.Jenkins('http://localhost:8080', username="admin", password="admin")
    jobs = server.get_jobs()
    print server.jobs_count() 
    print "the jobs are", jobs
    jobTrigger=server.build_job(first_job)
    out=subprocess.Popen(["/bin/bash", "/home/jenkins/jenkins/Unified-Test-Application/getmanagement.sh"], stdout=subprocess.PIPE)

    out,err=out.communicate()
    out1=out.strip()
    print out1
    return redirect('http://%s:8080/' %(out1))


# Search tags for the test type selected (sanity/full)
@app.route('/search', methods=['GET','POST'])
def search():
    global site_path
    temp_root="/etc/ansible"
    filename='site.yml'
    try:
      site_path,root =find_path(filename, temp_root)
    except:
      return '''<html> <h3> error: no site.yml file found in directory %s </h3> </html>'''%temp_root	
    option_list=[]   
    global option
    option = request.form['testtype']
    option_list.append(option)
    option_list.append(option.upper())
    option_list.append(string.capwords(option))    
    tasks2 = []
    print site_path
    final_output=""
    for opt in option_list:
        command1="sudo ansible-playbook %s -t %s --list-tags | grep 'TASK TAGS' | cut -d: -f2 | grep %s | sed 's/[][]//g' | tr '\n' ','"%(site_path,opt,opt)
        try:
          output=subprocess.check_output(command1,shell=True)
          output = output.replace(', ',',')              
          final_output += output
        except:
          output=''
          final_output += output
    tags_list =final_output.split(',')
    key = option
    contents=open(site_path, 'r')
    data=yaml.load(contents) #data is a list of dictioanries
    role_tags=[]
    for dictionary in data: #element is dictionary
      for k, v in dictionary.iteritems():
        if k=='roles':
          value=v[0]['tags'][0]
          role_tags.append(value) 
    searchReg = ['nightly','sanity','full']  
    searchReg += role_tags
    tags_list= [v.strip() for v in tags_list]	
    for tst in searchReg:
        if tst in tags_list:
                tags_list[:]= (value for value in tags_list if value != tst)
        if tst.upper() in tags_list:
                tags_list[:]= (value for value in tags_list if value != (tst.upper))
        tst_upper_first_letter= string.capwords(tst)#tst[0].upper()+tst[1:]
        if (tst_upper_first_letter) in tags_list:
            tags_list[:]= (value for value in tags_list if value != tst_upper_first_letter)
    tags_list=[tag for tag in tags_list if tag !='']	 
    print option
    return render_template('search.html',finalTasks=tags_list, option = option)


#Display Jenkins Job for test type(sanity/full) and tags selected
@app.route('/Ansible/test_Job', methods=['GET', 'POST'])
def Ansible_test_Job():
    email=  request.form['email']
    task_check =  request.form['task_selected'] #string 
    task_check = task_check.encode('ascii','ignore')
    print "tasks list", task_check
    test_type=option
    job_path='/home/jenkins/jenkins/Jenkins-Jobs-ansible/%s_job.yaml'%test_type   
    jjbName= test_type    
    jjb=job_path         
    template= '/home/jenkins/jenkins/ansible_jjb_template.yaml'
    stream = open(template, 'r')  #keep template
    data = yaml.load(stream)
    data[0]['job-template']['builders'][0]['opx-test']['playbookPath'] = str(site_path)                   
    global host_path
    config = ConfigParser.ConfigParser()
    config.read('/etc/ansible/ansible.cfg')
    host_path=config.get('defaults','hostfile') #config['defaults']['hostfile']
    data[0]['job-template']['builders'][0]['opx-test']['hostsPath'] = str(host_path)
    data[0]['job-template']['builders'][0]['opx-test']['tags'] = '"'+task_check+'"'
    print "*******tags_Selected*****",task_check
    data[0]['job-template']['publishers'][1]['email-ext']['recipients'] = str(email)
    data[0]['job-template']['name'] = str(jjbName)
    data[1]['project']['jobs'][0]= str(jjbName)
    data[1]['project']['name'] = str(jjbName)
    with open(jjb, 'w') as yaml_file:
        yaml_file.write( yaml.dump(data, default_flow_style=False))
        yaml_file.close()
    p=subprocess.Popen("/home/jenkins/jenkins/Unified-Test-Application/APIkey.sh",stdout=subprocess.PIPE)
    out,err=p.communicate()
    print out
    out1 = out.split()
    out2 = out1.pop()
    print out2  #jenkins token
    with open('/home/jenkins/jenkins/Jenkins-Jobs-ansible/jenkins_jobs.def', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('changeme',out2)
    with open('/home/jenkins/jenkins/Jenkins-Jobs-ansible/jenkins_jobs.ini', 'w') as file:
        file.write(filedata)
    proc=subprocess.Popen(["/usr/local/bin/jenkins-jobs --conf /home/jenkins/jenkins/Jenkins-Jobs-ansible/jenkins_jobs.ini update /home/jenkins/jenkins/Jenkins-Jobs-ansible"],shell=True, stdout=subprocess.PIPE) 
    out,err=proc.communicate()
    print out
    f=open(job_path, "r")
    contents =f.read()
    f.close()
    return render_template('testbed_ansible_yaml.html',data=contents)


#Run Jenkins Job for test type(sanity/full) 
@app.route('/Run_test')
def GetStarted_Ansible_Run_test():
    server=jenkins.Jenkins('http://localhost:8080', username="admin", password="admin")
    jobs = server.get_jobs()
    print server.jobs_count() 
    print "the jobs are", jobs
    jobTrigger=server.build_job(option)
    out=subprocess.Popen(["/bin/bash", "/home/jenkins/jenkins/Unified-Test-Application/getmanagement.sh"], stdout=subprocess.PIPE)
    out,err=out.communicate()
    out=out.strip()
    print out
    return redirect('http://%s:8080/' %(out))


if __name__ == "__main__":
        
    app.run(host="0.0.0.0", port=80, debug=True)



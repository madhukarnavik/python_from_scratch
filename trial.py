import os
import enum

# =============================================== #
# below lines required to create the main folder
# =============================================== #
project_name = "hello"                            # Edit only this line to provide name to the folder 
temp_path = os.getcwd()
path = temp_path + "/" + project_name
os.mkdir(path)
# =============================================== #

# ================================================= #
# below is the database for structure of the code
# Edit/add/remove the folder/class names from below
# The array names will be created as folder and 
# the elements inside it will be created as files 
# ================================================= #
class project(enum.Enum):
  agent         = ["agent","driver","sequencer","monitor","agent_pkg"]
  sequence      = ["seq","seq_pkg"]
  environment   = ["environment","scoreboard","env_pkg"]
  test          = ["test","test_pkg"]
  tb            = ["top"]
  interface     = ["interface"]
  design        = ["design"]
# ====================================================== #


# ====================================================== #
# ====================================================== #


# ====================================================== #
# below lines required to create the custom folder names
# and their respective files
# ====================================================== #
for x in project:
   custom_path = path + "/" + project_name + "_" + x.name
   os.mkdir(custom_path)
   os.chdir(custom_path)
   
   for j in x.value:

# =============creating file============================ #
     partial_file_name = project_name+"_"+j
     f = open(partial_file_name+".sv","w")
# ====================================================== #

# =============adding guardband========================= #
     guardband_start ="""`ifndef {}
`define {}\n""".format(partial_file_name.upper(),partial_file_name.upper())
     f.write(guardband_start)
# ====================================================== #

# =============adding class declaration and registering to factory============================ #
     class_declaration = """\nclass {} extends;
\n`uvm_component_utils({})\n""".format(partial_file_name, partial_file_name)
     if(j.find("pkg") == -1):
       f.write(class_declaration)
# ====================================================== #

# =============addding default constructor============================ #
     default_constructor ="""\nfunction new(string name = {}, uvm_component parent = null);
  super.new(name,parent);
endfunction\n""".format(partial_file_name)
     if(j.find("pkg") == -1):
       f.write(default_constructor)
# ====================================================== #

# =================Adding the phases===================== #
     phases = ["build","connect","end_of_elaboration","start_of_simulation","run","extract","check","report","final"]
     for k in phases:
       phase_defination = """\nfunction void {}_phase(uvm_phase phase);
  super.{}_phase(phase);
  `uvm_info(get_full_name,"Inside the {} phase of {}");
endfunction\n""".format(k,k,k,partial_file_name)
       if(j.find("pkg") == -1):
         if(k != "run"):
           f.write(phase_defination)                  
# ====================================================== #

# =================Ending the class===================== #
     if(j.find("pkg") == -1):
       f.write("\nendclass :{}\n".format(partial_file_name))
# ====================================================== #

# =================Closing the guardbands===================== #
     f.write("\n`endif")
# ====================================================== #

# =================closing the file===================== #
     f.close()
# ====================================================== #


   os.chdir("../")
# ====================================================== #


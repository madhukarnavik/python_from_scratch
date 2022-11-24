import os
import enum

# =============================================== #
# below lines required to create the main folder
# =============================================== #
project_name = "apb"                            # Edit only this line to provide name to the folder 
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
  agent         = ["transaction","driver","sequencer","monitor","agent","agent_pkg"]
  sequence      = ["sequence","seq_pkg"]
  environment   = ["scoreboard","environment","env_pkg"]
  test          = ["test","test_pkg"]
  tb            = ["top"]
  interface     = ["interface"]
  design        = ["design"]


phases        = ["build","connect","end_of_elaboration","start_of_simulation","run","extract","check","report","final"] # This is independent array and not part of enum
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
     class_declaration = """\n//==========================================={}======================================================//
class {} extends;\n""".format(partial_file_name,partial_file_name)
     factory_registration_component = "\n    `uvm_component_utils({})\n".format(partial_file_name)
     factory_registration_object    = "\n    `uvm_object_utils({})\n".format(partial_file_name)
     pkg_declaration = "\npackage {};".format(partial_file_name)
     if(j.find("pkg") == -1):
       f.write(class_declaration)
       if 'transaction' in j or j=='sequence':
         f.write(factory_registration_object)
       else:
         f.write(factory_registration_component)
# ================Adding package declaration====================================== #
     elif(j.find("pkg")):
       f.write(pkg_declaration)
# ====================================================== #
# ================Adding imports and includes to packge====================================== #
       f.write("\n\nimport uvm_pkg::*;")
       f.write("\n`include \"uvm_macros.svh\"")
       for temp in x.value:
         includes = "\n`include \"{}.sv\"".format(project_name+"_"+temp)
         if(temp.find("pkg") == -1):
           f.write(includes)
# ====================================================== #

# =========================Adding extern functions================================= #
     extern_function_new = "\n    extern function new(string name = {}, uvm_component parent = null);".format(partial_file_name)
     if(j.find("pkg") == -1):
       f.write(extern_function_new)
     
     for l in phases:
       extern_function_phases = "\n    extern function void {}_phase(uvm_phase phase);".format(l)
       if(l != "run"):
         if j.find("pkg") == -1 and j.find("transaction") == -1 and j!= 'sequence':
           f.write(extern_function_phases)
# ====================================================== #

# =================Ending the class===================== #
     if(j.find("pkg") == -1):
       f.write("""\n\nendclass :{}
//======================================End of {}===============================================//\n""".format(partial_file_name,partial_file_name))
     elif(j.find("pkg")):
       f.write("\n\nendpackage\n")
# ====================================================== #

# =============addding default constructor============================ #
     default_constructor ="""\n//=======================================Default Constructor=======================================//
function {} :: new(string name = {}, uvm_component parent = null);
  super.new(name,parent);
endfunction
//===================================End of Default constructor====================================//\n""".format(partial_file_name,partial_file_name)
     if(j.find("pkg") == -1):
       f.write(default_constructor)
# ====================================================== #

# =================Adding the phases===================== #
     for k in phases:
       phase_defination = """\n//======================================={} phase=======================================//
function void {} :: {}_phase(uvm_phase phase);
  super.{}_phase(phase);
  `uvm_info(get_full_name,"Inside the {} phase of {}");
endfunction
//===================================End of {} phase====================================//\n""".format(k,partial_file_name,k,k,k,partial_file_name,k)
       if(j.find("pkg") == -1):
         if k != "run" and j.find("transaction") == -1 and j!= 'sequence':
           f.write(phase_defination)                  
# ====================================================== #

# =================Closing the guardbands===================== #
     f.write("\n`endif")
# ====================================================== #

# =================closing the file===================== #
     f.close()
# ====================================================== #


   os.chdir("../")
# ====================================================== #


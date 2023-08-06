from multiprocessing import cpu_count
from XME.XMElib.ArrayOperator import ArrayOperator
from XME.XMElib.Executor import Executor
from XME.XMElib.Logputter import Logputter
from XME.XMElib.version_info import XME_Version_info
def get_par(args,name,default=None):
	try:
		return args[name]
	except:
		return default
class XME:
	aoobj_array=[]
	exobj_array=[]
	class Array:
		def __init__(self,array):
			self.array=array
			self.length=len(array)
	def __init__(self,*fun,**args):
		self.pnum=get_par(args,"pnum",cpu_count())
		self.funs=[]
		if get_par(args,"do_with_log",True):
			self.logobj=Logputter(get_par(args,"logfile"),XME_Version_info,get_par(args,"show_version_info",True))
			self.logobj.print_in_screen=get_par(args,"print_in_screen",True)
		else:
			self.logobj=None
		for fu in fun:
			def func(*targ,**args):
				args.update({"logobj":self.logobj})
				if self.logobj!=None:
					args.update({"print":self.logobj.write_log})
				calnum=get_par(args,"calnum",0)
				if calnum==0:
					for i in targ:
						if type(i)==self.Array:
							calnum=max(calnum,i.length)
					for i in args.keys():
						if type(args[i])==self.Array:
							calnum=max(calnum,args[i].length)
				ao=self.ao(calnum,self.pnum)
				for i in targ: #first set
					if type(i)!=self.Array:
						ao.add_common_args(i)
					else:
						ao.add_argscut(i.array)
				for i in fu.__code__.co_varnames: #follow sequence
					if i in args.keys():
						if type(args[i])!=self.Array:
							ao.add_common_args(args[i])
						else:
							ao.add_agrscut(args[i].array)
				ex=self.ex(fu,pnum=self.pnum)
				ex.build_from_ao(ao)
				ao.result_combine()
				return ao.results
			self.funs.append(func)
		if len(self.funs)>0:
			self.fun=self.funs[-1]
	def build_ao(self,calnum,pnum=None): #v1.2 compatible
		return self.ao(calnum=calnum,pnum=pnum)
	def ao(self,calnum,pnum=None):
		if pnum==None:
			pnum=self.pnum
		self.aoobj_array.append(ArrayOperator(cal_num=calnum,pnum=pnum))
		return self.aoobj_array[-1]
	def build_ex(self,*fun,**args): #v1.2 compatible
		return self.ex(*fun,**args)
	def ex(self,*fun,**args):
		self.exobj_array.append(Executor(*fun,**args))
		return self.exobj_array[-1]
	def clean(self):
		self.aoobj_array=[]
		self.exobj_array=[]
def build(*fun,**args):
	return XME(*fun,**args)

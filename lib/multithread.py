#from multiprocessing import Pipe, Process
#from functools import partial

#methods_dict: {class method : [args]}

from threading import Thread

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return

def run_methods_parallel(methods_arr):
    proc = []
    results = []
    for fn_and_args in methods_arr:
        fn = fn_and_args[0]
        args = fn_and_args[1:]
        p = ThreadWithReturnValue(target=fn, args=args)
        p.start()
        proc.append(p)
    for p in proc:
        res = p.join() #ensure you are outputting an array
        results = results + res #add up the arrays from all threads
    return results

#custom methods to allow multithreading of python class methods with parameters
#def _pickle_method(method):
#	func_name = method.im_func.__name__
#	obj = method.im_self
#	cls = method.im_class
#	if func_name.startswith('__') and not func_name.endswith('__'): #deal with mangled names
#		cls_name = cls.__name__.lstrip('_')
#		func_name = '_' + cls_name + func_name
#	return _unpickle_method, (func_name, obj, cls)
#
#def _unpickle_method(func_name, obj, cls):
#	for cls in cls.__mro__:
#		try:
#			func = cls.__dict__[func_name]
#		except KeyError:
#			pass
#		else:
#			break
#	return func.__get__(obj, cls)
#
#import copy_reg
#import types
#copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)
#
#class someClass(object):
#	def __init__(self):
#		pass
#	
#	def f(self, x=None):
#		#can put something expensive here to verify CPU utilization
#		if x is None: return 99
#		return x*x
#
#	def go(self):
#		pool = Pool()             
#		print pool.map(self.f, range(10))
#
#if __name__=='__main__':
#	sc = someClass()
#	sc.go()
#	x=[someClass(),someClass(),someClass()]
#	p=Pool()
#	filled_f=partial(someClass.f,x=9)
#	print p.map(filled_f,x)
#	print p.map(someClass.f,x)

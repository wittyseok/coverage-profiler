import ast
import argparse
import sys
import io
from copy import deepcopy
import test_pcov

def print_result(verbose:bool, stmt_covered:int, stmt_total:int, stmt_missing:list[str], branch_covered:int, branch_total:int, branch_missing:list[str]):
	
	stmt_coverage = 0 if stmt_total == 0 else stmt_covered / stmt_total * 100
	branch_coverage = 0 if branch_total == 0 else branch_covered / branch_total * 100

	print("=====================================")
	print("Statements Coverage: {0:.2f} ({1}/{2})".format(stmt_coverage, stmt_covered, stmt_total))
	if verbose:
		print("Missing Statements: {}".format(", ".join([str(line_num) for line_num in stmt_missing])))
	#print("=====================================")
	print("Branch Coverage: {0:.2f} ({1}/{2})".format(branch_coverage, branch_covered, branch_total))
	if verbose:
		print("Missing Branches: {}".format(", ".join([str(line_num) for line_num in branch_missing])))
	print("=====================================")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Measures coverage.')
	parser.add_argument('-v', '--verbose', action="store_true")
	parser.add_argument('-t', '--target', required=True)
	parser.add_argument("remaining", nargs="*")
	args = parser.parse_args()

	target = args.target
	lines = open(target, "r").readlines()
	root = ast.parse("".join(lines), target)
	
	# instrument the target script
	# ...
	executed_line = []
	for line in lines:
		executed_line.append(line) 

	executed_root = ast.parse("".join(executed_line),target)

	sys.argv = []
	sys.argv.append(target)
	for item in args.remaining:
		sys.argv.append(item)


	class CoverageStmtVisitor(ast.NodeTransformer):
		def __init__(self):
			self.loc_stmt = set()
			self.loc_branch = set()
			self.num_branch = 0

		def visit_If(self,node):
			if (node.lineno,'elif') in self.loc_branch:
				pass
			else:
				self.loc_branch.add( (node.lineno,'if') )
				self.num_branch+=2
			
			inner_node = node
			#cover elif, else block
			while isinstance(inner_node.orelse,list) and inner_node.orelse:
				elif_node = inner_node.orelse[0]

				if isinstance(elif_node,ast.If) and ((node.lineno,'elif') not in self.loc_branch):
					self.loc_branch.add( (elif_node.lineno,'elif') )
					self.num_branch+=2
				else:
					self.loc_branch.add( (elif_node.lineno,'else') )
					break
				inner_node = elif_node

			self.generic_visit(node)
			return node

		def visit_Try(self, node):
			self.loc_branch.add( (node.lineno,'try') )
			self.num_branch+=2
			for handler in node.handlers: #except
				self.loc_branch.add( (handler.lineno,'except'))
				#self.num_branch+=1
			self.generic_visit(node)
			return node

		def visit_For(self,node):
			if isinstance(node,ast.For):
				self.loc_branch.add((node.lineno,'for'))
				self.num_branch+=2
			self.generic_visit(node)
			return node


		def generic_visit(self,node):
			if hasattr(node,'lineno'):
				self.loc_stmt.add(node.lineno)
				"""
				executed_flag = ast.Expr(value = ast.Call(func=ast.Name(id='log_execution',ctx=ast.Load()),
											  args=[ast.Constant(value=node.lineno)],
											  keywords=[]
											  ))
				if isinstance(node,(ast.FunctionDef,ast.ClassDef,ast.Module)):
					node.body.insert(0,executed_flag)
				"""
			return super().generic_visit(node)


	class LoggingTransformer(ast.NodeTransformer):
		def __init__(self):
			self.is_first_if = True

		def insert_log_call(self, node):
			log_call = ast.Expr(value=ast.Call(
				func=ast.Name(id='log_execution', ctx=ast.Load()),
				args=[ast.Constant(value=node.lineno)],
				keywords=[]
			))
			return ast.copy_location(log_call,node) # to adjust lineno, col_lineno offsets
	
		def visit_FunctionDef(self, node):
			node.body.insert(0, self.insert_log_call(node))
			self.generic_visit(node)  # internal node
			return node

		def visit_ClassDef(self, node):
			node.body.insert(0, self.insert_log_call(node))
			self.generic_visit(node)  # internal node
			return node

		def visit_Try(self, node):
			# case try
			node.body.insert(0, self.insert_log_call(node))

			# case except
			for handler in node.handlers:
				handler.body.insert(0, self.insert_log_call(handler))

			# case final
			if node.finalbody:
				node.finalbody.insert(0, self.insert_log_call(node))
			self.generic_visit(node)
			return node
		

		def visit_If(self, node):
			new_body = [self.insert_log_call(node)]
			for body_node in node.body:
				new_body.append(body_node)
				if hasattr(body_node, 'lineno'):
					new_body.append(self.insert_log_call(body_node))
			
			node.body = new_body
			
			# process elif-else 
			if node.orelse:
				new_orelse = []
				for orelse_node in node.orelse:
					if isinstance(orelse_node, ast.If):  # elif block
						self.visit(orelse_node)
						#print(ast.dump(orelse_node,indent=4))
					else:
						new_orelse.insert(0,self.insert_log_call(orelse_node))
					new_orelse.append(orelse_node)
				node.orelse = new_orelse
			#self.visit(node)
			return [self.insert_log_call(node),node]
		def visit_For(self, node):
			log_call = self.insert_log_call(node)
			new_body = []
			for body_node in node.body:
				if isinstance(body_node,ast.If):
					self.visit(body_node)
				log_call = self.insert_log_call(body_node)
				new_body.append(log_call)
				new_body.append(body_node)
			node.body = new_body
			self.generic_visit(node)  # visit intenal for-loop
			return [self.insert_log_call(node),node]  
			
		def generic_visit(self, node):

			if isinstance(node, (ast.stmt,ast.expr,ast.Expr)): #and not isinstance(node, ast.Module):
				log_call = self.insert_log_call(node)
				return [log_call, node]
			return super().generic_visit(node)		



	# execute the instrumented target script 
	# ...
	executed_line = set()


	def log_execution(lineno):
		executed_line.add(lineno)


	Code_visitor = CoverageStmtVisitor()
	executed_root = Code_visitor.visit(root)

	transformer = LoggingTransformer()
	modified_tree = transformer.visit(executed_root)
	ast.fix_missing_locations(modified_tree)

	"""
	for node in ast.walk(modified_tree):
		if isinstance(node,(ast.stmt,ast.ExceptHandler)):
			if hasattr(node,'lineno'):
				print(node.lineno)
			print(ast.dump(node,indent=5))
			print("==========================================")
	"""
	#print(ast.dump(modified_tree,indent=5))
	def suppress_stdout(func, *args, **kwargs):
		original_stdout = sys.stdout
		sys.stdout = io.StringIO()
		try:
			func(*args, **kwargs)
			redirected_output = sys.stdout.getvalue()
		finally:
			sys.stdout = original_stdout
		return redirected_output

	def excute_code(code,global_dic, execute_dic):
		exec(code,global_dic, execute_dic)

	compiled_code = compile(modified_tree, filename="<ast>", mode="exec")
	output = suppress_stdout(excute_code,compiled_code, globals(), {'log_execution': log_execution})
	


	# collect coverage
	# ...
	
	verbose = args.verbose
	#process collect statement
	stmt_missing = []
	temp = list(Code_visitor.loc_stmt-executed_line)
	temp.sort()
	for item in temp:
		stmt_missing.append(str(item))

	stmt_covered = len(executed_line)
	stmt_total = len(Code_visitor.loc_stmt)
	#process collect branch
	temp = list(Code_visitor.loc_branch)
	branch_list = []
	for loc,stmt in temp:
		branch_list.append(loc)
	branch_list.sort()	

	branch_missing = []
	if 'else' in [stmt for _,stmt in Code_visitor.loc_branch]: #if-else block
		for i in range(len(branch_list)):
			if i != len(branch_list)-1:
				if branch_list[i+1] == branch_list[len(branch_list)-1]:
					branch_missing.append(str(branch_list[i])+'->'+str(branch_list[i+1]))
				else:
					branch_missing.append(str(branch_list[i])+'->'+str(branch_list[i+1]-1))
			else:
				pass

	else: # no else block
		for i in range(len(branch_list)):
			if i != len(branch_list)-1:
				if branch_list[i+1] == branch_list[len(branch_list)-1]:
					branch_missing.append(str(branch_list[i])+'->'+str(branch_list[i+1]))
				else:
					branch_missing.append(str(branch_list[i])+'->'+str(branch_list[i+1]-1))
			else:
				branch_missing.append(str(branch_list[i])+'->'+str(-1))

	branch_total = Code_visitor.num_branch
	branch_covered = branch_total - len(branch_missing) 
	

	print_result(verbose, stmt_covered, stmt_total, stmt_missing, branch_covered, branch_total, branch_missing)

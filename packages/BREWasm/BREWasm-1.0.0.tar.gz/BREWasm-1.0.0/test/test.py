from BREWasm import *

# binary = BREWasm("benchmark/base64-cli.wasm")
# rewriter = SectionRewriter(binary.module,
#                            customsec=binary.module.custom_secs)
#
# # query = Type(arg_types=["i32"])
# # query = Import()
# # query = Function(typeidx=5)
# # query = Import(importidx=1)
# # query = Function(funcidx=10)
# # query = Table(min=250)
# # query = Memory(min=17)
# # query = Global(globalidx=0)
# # query = Export(exportidx=4)
# # query = Element(tableidx=0)
# # query = Code(funcidx=10)
# query = CustomName(FunctionName, idx=1)
# result = rewriter.select(query)
#
# # a = Code(local_vec=[Local(0, ValTypeI32), Local(1, ValTypeI32)], instr_list=[Instruction(Nop)])
# # a = Type(arg_types=["i32", "i64"], ret_types=["i64"])
# # a = Import(module="aaaa", name="111111", typeidx=2)
# # a = Function(typeidx=5)
# # a = Table(max = 500)
# # a = Memory(max=100)
# # a = Global(valtype=ValTypeI64, mut=1, val=200)
# # a = Export(name="aaaaaaa", funcidx=10)
# # a = Element(offset=20, funcidx_list=[1, 2, 3, 4])
# # a = Code(local_vec=[Local(0, ValTypeI32), Local(1, ValTypeI64)], instr_list=[Instruction(Nop)])
# a = CustomName(name="2222222")
# rewriter.update(result[0], a)
#
# # a = all((True, False, False, False))
# print("111")


# ======================================================== semantics

binary = BREWasm("../benchmark/base64-cli.wasm")

# global variable
# append
rewriter = SemanticsRewriter.GlobalVariable(binary.module)
rewriter.append_global_variable(I32, 200)

# insert
# rewriter = SemanticsRewriter.GlobalVariable(binary.module)
# rewriter.insert_global_variable(1, F32, 200)

# delete
# rewriter = SemanticsRewriter.GlobalVariable(binary.module)
# rewriter.delete_global_variable(1)

# modify
# rewriter = SemanticsRewriter.GlobalVariable(binary.module)
# rewriter.modify_global_variable(1, F64, 2.2222)

# Import

# append
# rewriter = SemanticsRewriter.ImportExport(binary.module)
# rewriter.append_import_function("123", "aaa", [I32, F64], [I32])

# insert
# rewriter = SemanticsRewriter.ImportExport(binary.module)
# rewriter.insert_import_function(1, "123", "aaa", [I32, F64], [I32])

# modify
# rewriter = SemanticsRewriter.ImportExport(binary.module)
# rewriter.modify_import_function(1, "123", "aaa", [I32, F64], [I32])

# delete
# rewriter = SemanticsRewriter.ImportExport(binary.module)
# rewriter.delete_import_function(1)

# Export

# append
# rewriter = SemanticsRewriter.ImportExport(binary.module)
# rewriter.append_export_function("123", 10)

# insert
# rewriter = SemanticsRewriter.ImportExport(binary.module)
# rewriter.insert_export_function(1, "123", 10)

# modify
# rewriter = SemanticsRewriter.ImportExport(binary.module)
# rewriter.modify_export_function(5, "123", 10)

# delete
# rewriter = SemanticsRewriter.ImportExport(binary.module)
# rewriter.delete_export_function(7)

# Function
# rewriter = SemanticsRewriter.Function(binary.module)
# rewriter.insert_internal_function(10, [I32, I64], [F32], [Local(0, I32)], [Instruction(I32Const, 1), Instruction(Drop), Instruction(F32Const, 1.11)])

# indirect function
# rewriter = SemanticsRewriter.Function(binary.module)
# rewriter.insert_indirect_function(10, [I32, I64], [F32], [Local(0, I32)], [Instruction(I32Const, 1), Instruction(Drop), Instruction(F32Const, 1.11)])

# hook function
# rewriter = SemanticsRewriter.Function(binary.module)
# rewriter.insert_hook_function(20, 10, [I32, I64], [F32], [Local(0, I32)], [Instruction(I32Const, 1), Instruction(Drop), Instruction(F32Const, 1.11)])

# delete function instr
# rewriter = SemanticsRewriter.Function(binary.module)
# rewriter.delete_func_instr(10, 2)

# delete function instr
rewriter = SemanticsRewriter.Function(binary.module)
rewriter.insert_func_instrs(10, 2)

print("11111")
binary.emit_binary("a.wasm")



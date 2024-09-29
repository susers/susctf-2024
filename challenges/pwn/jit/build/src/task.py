import ast
import ctypes
import mmap
import struct

white_list = [
    ast.Module,
    ast.Assign, ast.Name, ast.Constant, ast.Store, ast.Load,
    ast.For, ast.BinOp,
    ast.Call # range(x) only
]
supported_op = [
    ast.Add, ast.Sub, ast.Mult, ast.FloorDiv
]

def p64(x):
    return struct.pack("<q", x)
def p32(x):
    return struct.pack("<i", x)

class JIT:
    def __init__(self):
        self.global_var_map = {}
        self.global_offset = 0x0
        self.local_var_set = set()
    def new_local_var(self):
        for offset in range(0x8, 0x80000000, 8):
            if -offset not in self.local_var_set:
                self.local_var_set.add(-offset)
                return -offset
        raise Exception("too many local variables")
    def free_local_var(self, var):
        assert type(var) == int
        assert var in self.local_var_set ,\
            f"try to free a non-exist variable <{var}>"
        self.local_var_set.discard(var)
    def set_global_var(self, id):
        # rax -> [rdi+global_var_id]
        if id not in self.global_var_map:
            self.global_var_map[id] = self.global_offset
            self.global_offset += 8
        return [b"H\x89\x87" + p32(self.global_var_map[id])] # mov [rdi+id], rax
    def get_global_var(self, id):
        assert id in self.global_var_map, \
            f"global variable <{id}> should be assigned before use"
        var = self.new_local_var()
        return var, [
            b"H\x8b\x87" + p32(self.global_var_map[id]), # mov rax, [rdi+id]
            b"H\x89\x84$" + p32(var) # mov [rsp+var], rax
        ]
    def ast_to_asm(self, tree: ast.AST):
        code = []
        if type(tree) == ast.Assign:
            assert len(tree.targets) == 1, \
                "not support multi-assign yet"
            assert type(tree.targets[0]) == ast.Name, \
                "only supports assigning values to a variable"
            var_name = tree.targets[0].id
            ret, code = self.ast_to_asm(tree.value)
            assert ret, "try to assign non-value to variable"
            code.append(b"H\x8b\x84$" + p32(ret)) # mov rax, [rsp+ret]
            code += self.set_global_var(var_name)
            if ret in self.local_var_set:
                self.free_local_var(ret)
            return None, code
        if type(tree) == ast.Name:
            return self.get_global_var(tree.id)
        if type(tree) == ast.Constant:
            assert type(tree.value) == int, "only support int constant"
            ret_var = self.new_local_var()
            code.append(b"H\xb8" + p64(tree.value)) # mov rax, tree.value
            code.append(b"H\x89\x84$" + p32(ret_var)) # mov [rsp+ret_var], rax
            return ret_var, code
        if type(tree) == ast.Module:
            for statement in tree.body:
                ret, statement_code = self.ast_to_asm(statement)
                code += statement_code
                if ret and ret in self.local_var_set:
                    self.free_local_var(ret)
            return None, code
        if type(tree) == ast.BinOp:
            left, left_code = self.ast_to_asm(tree.left)
            right, right_code = self.ast_to_asm(tree.right)
            assert left and right, "try to operate on non-value"
            code += left_code + right_code
            ret_var = self.new_local_var()
            if left in self.local_var_set:
                self.free_local_var(left)
            if right in self.local_var_set:
                self.free_local_var(right)
            code.append(b"H\x8b\x84$" + p32(left)) # mov rax, [rsp+left]
            code.append(b"H\x8b\x8c$" + p32(right)) # mov rcx, [rsp+right]
            if type(tree.op) == ast.Add:
                code.append(b"H\x01\xc8") # add rax, rcx
            elif type(tree.op) == ast.Sub:
                code.append(b"H)\xc8") # sub rax, rcx
            elif type(tree.op) == ast.Mult:
                code.append(b"H\xf7\xe9") # imul rcx
            elif type(tree.op) == ast.FloorDiv:
                code.append(b"H\x99H\xf7\xf9") # cqo; idiv rcx
            else:
                raise NotImplementedError(f"not support {type(tree.op)} yet")
            code.append(b"H\x89\x84$" + p32(ret_var)) # mov [rsp+ret_var], rax
            return ret_var, code
        if type(tree) == ast.For:
            assert type(tree.target) == ast.Name, "only supports single iter var"
            assert len(tree.iter.args) == 1, "multi-args are not supported in for loop"
            try:
                assert type(tree.iter) == ast.Call
                assert tree.iter.func.id == "range"
                assert len(tree.iter.args) == 1
                for arg in tree.iter.args:
                    assert type(arg) == ast.Constant and type(arg.value) == int
            except AssertionError:
                assert False, "for loop with non-simple-range iter is not supported"
            iter_var = tree.target.id
            for i in range(tree.iter.args[0].value):
                code.append(b"H\xb8" + p64(i)) # mov rax, i
                code += self.set_global_var(iter_var)
                for s in tree.body:
                    ret, statement_code = self.ast_to_asm(s)
                    code += statement_code
                    if ret and ret in self.local_var_set:
                        self.free_local_var(ret)
            return None, code
        raise NotImplementedError
    def complie(self, tree):
        for node in ast.walk(tree):
            if type(node) not in white_list:
                if type(node) not in supported_op:
                    raise NotImplementedError(f"不支持的{type(node)}")
        page = mmap.mmap(-1, mmap.PAGESIZE, prot=mmap.PROT_READ|mmap.PROT_WRITE|mmap.PROT_EXEC)
        page_addr = ctypes.addressof(ctypes.c_int.from_buffer(page))
        ret, code = self.ast_to_asm(tree)
        code = [
            b"UH\x89\xe5", # push rbp; mov rbp, rsp
            b"H1\xf6H1\xd2", # xor rsi, rsi; xor rdx, rdx
            b"H\xbf" + p64(page_addr), # mov rdi, page_addr
            b"H\xbc" + p64(page_addr + mmap.PAGESIZE), # mov rsp, page_addr + page_size
        ] + code + [
            b"\xc9\xc3" # leave; ret
        ]
        code = b"".join(code)
        page.seek(self.global_offset)
        page.write(code)
        func = ctypes.CFUNCTYPE(None)(page_addr + self.global_offset)
        def func_wrapper():
            func()
            ret = {}
            for k, v in self.global_var_map.items():
                ret[k] = struct.unpack("<q", page[v:v+8])[0]
            return ret
        return func_wrapper
    
if __name__ == "__main__":
    code = input("code: ").replace("@", "\n")
    try:
        tree = ast.parse(code)
        jit = JIT()
        func = jit.complie(tree)
        print("result:", func())
    except Exception as e:
        print("ERROR:", e.with_traceback(e.__traceback__))

"""
# example 1

a = 0@for i in range(10): a = a + i

# example 2

a = 1@b = 2@c = a + (b + 1)*4

# internal structure

page_addr = [mmap anonymous page (RWX)]
global_offset = len(global_var_map) * 8
mmap.PAGESIZE = 4096
rsi = 0
rdi = 0
rbp = [old rsp]

reg / var         offset (real_address = page_addr + offset)
[rdi]              0
global_var_map[0]  0
global_var_map[1]  8
global_var_map[2]  16
...
code               global_offset
...
...

...
local_var_2        mmap.PAGESIZE - 16
local_var_1        mmap.PAGESIZE - 8
[rsp]              mmap.PAGESIZE
"""

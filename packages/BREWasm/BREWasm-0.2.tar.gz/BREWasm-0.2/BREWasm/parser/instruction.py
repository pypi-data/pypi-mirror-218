# -*- coding: UTF-8 -*-
"""
@Project ：wasmObfuscator 
@File    ：instruction.py
@Author  ：格友
"""

from ..parser.opnames import opnames


class Expr(list):
    """
    表达式
    expr  : instr*|0x0b
    """

    def __init__(self):
        super().__init__()


class Instruction:
    """指令结构，数值指令，变量指令，跳转指令，直接函数调用指令"""

    def __init__(self, opcode=None, args=None):
        # 操作码
        self.opcode = opcode
        # 操作数
        self.args = args

    def get_opname(self):
        return opnames[self.opcode]

    def __str__(self):
        return opnames[self.opcode]


class BlockArgs:

    def __init__(self, bt=None, instrs=None):
        # block type:
        # -1表示i32类型结果，-2表示i64类型结果，
        # -3表示f32类型结果，-4表示f64类型结果，
        # -64表示没有结果
        self.bt = bt
        # 内嵌的指令序列
        self.instrs = instrs


class IfArgs:

    def __init__(self):
        # block type
        self.bt = None
        self.instrs1 = []
        self.instrs2 = []


class BrTableArgs:

    def __init__(self, labels=None, default=None):
        # 跳转表
        if labels is None:
            labels = []
        self.labels = labels
        # 默认跳转标签
        self.default = default


class MemArg:

    def __init__(self, align=0, offset=0):
        # 对齐提示
        self.align = align
        # 内存偏移量
        self.offset = offset

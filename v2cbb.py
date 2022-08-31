#!/usr/bin/env python
from turtle import st
import fire
import re
import json
from enum import Enum, unique
from loguru import logger


class JsonAble:
    def toJson(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class ChiselAbel:
    def genHead(self) -> None:
        self.code = [
            "class hpRam extends BlackBox {",
            "  val io = IO(new Bundle {",
        ]

    def genBody(self) -> None:
        self.code += [
            "    //not implement"
        ]

    def genTail(self) -> None:
        self.code += [
            "  })",
            "}",
            "",
        ]

    def gen(self) -> str:
        self.genHead()
        self.genBody()
        self.genTail()

        return '\n'.join(self.code)

    def toChisel(self) -> str:
        return self.gen()


@unique
class ModuleIOType(str, Enum):
    WIRE = 'wire'
    REG = 'reg'


@unique
class ModuleIODir(str, Enum):
    INPUT = 'input'
    OUTPUT = 'output'
    INOUT = 'inout'


class ModuleIO(JsonAble):
    def __init__(self, name: str, direction: ModuleIODir, width: int = 1, shape: tuple = (1), iotype: ModuleIOType = ModuleIOType.WIRE) -> None:
        # reg [7:0] name   [0:3]    [0:3];
        #  |    |     |      |        |
        # type width name shape(0) shape(1)

        self.name = name
        self.direction = direction
        self.width = width
        self.shape = shape  # todo: shape not support at this time
        self.iotype = iotype
        pass

    @staticmethod
    def GetWidth(widthstr: str):
        if widthstr == '' or widthstr == None:
            return 1

        bit = widthstr.removeprefix('[').removesuffix(']').split(':')
        width = int(bit[0]) - int(bit[1]) + 1
        logger.debug("multibit: {bit}, width {width}", bit=bit, width=width)

        return width


class ModuleParameter(JsonAble):
    def __init__(self) -> None:
        # todo: parameter not support this time
        pass


class Module(JsonAble, ChiselAbel):
    def __init__(self, name) -> None:
        self.name = name

        self.io = []
        self.parameter = []

        # internal var
        self.wrap = "    "
        self.dirstrlut = {
            'input': 'Input',
            'output': 'Output',
            'inout': 'Analog',
        }
        pass

    def genBodyIOLine(self, io: ModuleIO) -> str:
        dirstr = self.dirstrlut[io.direction]
        parastr = ''

        if(io.width == 1 and (dirstr == 'Input' or dirstr == 'Output')):
            if ('clk' in io.name):
                parastr = 'Clock()'
            elif ('clock' in io.name):
                parastr = 'Clock()'
            elif ('rst' in io.name):
                parastr = 'Reset()'
            elif ('reset' in io.name):
                parastr = 'Reset()'
            else:
                parastr = 'Bool()'
        elif (dirstr == 'Input' or dirstr == 'Output'):
            parastr = 'UInt({width}.W)'.format(width=io.width)
        elif(dirstr == 'Analog'):
            parastr = '{width}.W'.format(width=io.width)

        return "{wrap}val {name} = {dir}({para})".format(wrap=self.wrap, name=io.name, dir=dirstr, para=parastr)

    def genBody(self) -> None:
        self.code.append(self.wrap + "// IO")

        for io in self.io:
            self.code.append(self.genBodyIOLine(io))


class Compiler:
    def __init__(self, verilog) -> None:
        self.name = self.__class__.__name__
        self.verilog = verilog
        self.module = None
        self._compiled = False
        pass

    def parseModuleName(self) -> None:
        self.module = Module(self.name)
        logger.info('Find Module: {name}', name=self.name)
        pass

    def parseParameter(self) -> None:
        pass

    def parseIO(self) -> None:
        pass

    def compile(self) -> None:
        if self._compiled:
            return

        self.parseModuleName()
        self.parseParameter()
        self.parseIO()
        self._compiled = True

    def compileIR(self) -> str:
        self.compile()

        return self.module.toJson()

    def compileChisel(self) -> str:
        self.compile()

        return self.module.toChisel()


class Gowin(Compiler):
    def parseModuleName(self) -> None:
        matches = re.findall(
            r"^\s+(\w+)\s+(\w+)\s*\(", self.verilog, re.MULTILINE)

        if(len(matches) == 1):
            self.module = Module(matches[0][0])
        else:
            logger.error("GOWIN: module name match error")

        pass

    def parseParameter(self) -> None:
        pass

    def _parseIO(self, match) -> ModuleIO:
        logger.debug('match: {match}', match=match)

        m = ModuleIO(match[0], ModuleIODir(
            match[2]), ModuleIO.GetWidth(match[3]), (1), ModuleIOType.WIRE)
        self.module.io.append(m)

        pass

    def parseIO(self) -> None:
        matches = re.findall(
            r"^\s+\.(\w+)\((\w+)\),?\s*\/\/(\w+)\s+(\[\d+\:0\])?\s*(\w+)", self.verilog, re.MULTILINE)

        for match in matches:
            self._parseIO(match)

        pass


class Process(object):
    def gowin(self, file, genIR=False, output: str = ''):
        if output == '':
            output = file + '.scala'

        with open(file, mode='r') as f:
            logger.info('process {file}', file=file)
            gowinmodule = Gowin(f.read())

            if genIR:
                with open(output+'.json', mode='w') as o:
                    o.write(gowinmodule.compileIR())

            with open(output, mode='w') as o:
                o.write(gowinmodule.compileChisel())

        return


if __name__ == '__main__':
    fire.Fire(Process)

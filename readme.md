# hdl generator

## Introduct

  verilog                              Verilog
  VHDL       -----> Module IR -------> Chisel
  ...                                  ...

## RoadMap:

### parser
- [X] parse verilog module declare

### IR
- [X] JSON

### emitter
- [X] chisel BlackBox emitter

## Example 

### input
``` verilog
HyperRAM_Memory_Interface_Top your_instance_name(
	.clk(clk_i), //input clk
	.memory_clk(memory_clk_i), //input memory_clk
	.pll_lock(pll_lock_i), //input pll_lock
	.rst_n(rst_n_i), //input rst_n
	.O_hpram_ck(O_hpram_ck_o), //output [0:0] O_hpram_ck
	.O_hpram_ck_n(O_hpram_ck_n_o), //output [0:0] O_hpram_ck_n
	.IO_hpram_dq(IO_hpram_dq_io), //inout [7:0] IO_hpram_dq
	.IO_hpram_rwds(IO_hpram_rwds_io), //inout [0:0] IO_hpram_rwds
	.O_hpram_cs_n(O_hpram_cs_n_o), //output [0:0] O_hpram_cs_n
	.O_hpram_reset_n(O_hpram_reset_n_o), //output [0:0] O_hpram_reset_n
	.wr_data(wr_data_i), //input [31:0] wr_data
	.rd_data(rd_data_o), //output [31:0] rd_data
	.rd_data_valid(rd_data_valid_o), //output rd_data_valid
	.addr(addr_i), //input [21:0] addr
	.cmd(cmd_i), //input cmd
	.cmd_en(cmd_en_i), //input cmd_en
	.init_calib(init_calib_o), //output init_calib
	.clk_out(clk_out_o), //output clk_out
	.data_mask(data_mask_i) //input [3:0] data_mask
);
```
### output
``` scala
class hpRam extends BlackBox {
  val io = IO(new Bundle {
    // IO
    val clk = Input(Clock())
    val memory_clk = Input(Clock())
    val pll_lock = Input(Bool())
    val rst_n = Input(Reset())
    val O_hpram_ck = Output(Bool())
    val O_hpram_ck_n = Output(Bool())
    val IO_hpram_dq = Analog(8.W)
    val IO_hpram_rwds = Analog(1.W)
    val O_hpram_cs_n = Output(Bool())
    val O_hpram_reset_n = Output(Reset())
    val wr_data = Input(UInt(32.W))
    val rd_data = Output(UInt(32.W))
    val rd_data_valid = Output(Bool())
    val addr = Input(UInt(22.W))
    val cmd = Input(Bool())
    val cmd_en = Input(Bool())
    val init_calib = Output(Bool())
    val clk_out = Output(Clock())
    val data_mask = Input(UInt(4.W))
  })
}

```

### IR JSON Output
``` JSON
{
    "dirstrlut": {
        "inout": "Analog",
        "input": "Input",
        "output": "Output"
    },
    "io": [
        {
            "direction": "input",
            "iotype": "wire",
            "name": "clk",
            "shape": 1,
            "width": 1
        },
        {
            "direction": "input",
            "iotype": "wire",
            "name": "memory_clk",
            "shape": 1,
            "width": 1
        },
        {
            "direction": "input",
            "iotype": "wire",
            "name": "pll_lock",
            "shape": 1,
            "width": 1
        },
        {
            "direction": "input",
            "iotype": "wire",
            "name": "rst_n",
            "shape": 1,
            "width": 1
        },
        {
            "direction": "output",
            "iotype": "wire",
            "name": "O_hpram_ck",
            "shape": 1,
            "width": 1
        },
        {
            "direction": "output",
            "iotype": "wire",
            "name": "O_hpram_ck_n",
            "shape": 1,
            "width": 1
        },
        {
            "direction": "inout",
            "iotype": "wire",
            "name": "IO_hpram_dq",
            "shape": 1,
            "width": 8
        },
        {
            "direction": "inout",
            "iotype": "wire",
            "name": "IO_hpram_rwds",
            "shape": 1,
            "width": 1
        },
        {
            "direction": "output",
            "iotype": "wire",
            "name": "O_hpram_cs_n",
            "shape": 1,
            "width": 1
        },
        {
            "direction": "output",
            "iotype": "wire",
            "name": "O_hpram_reset_n",
            "shape": 1,
            "width": 1
        },
        {
            "direction": "input",
            "iotype": "wire",
            "name": "wr_data",
            "shape": 1,
            "width": 32
        },
        {
            "direction": "output",
            "iotype": "wire",
            "name": "rd_data",
            "shape": 1,
            "width": 32
        },
        {
            "direction": "output",
            "iotype": "wire",
            "name": "rd_data_valid",
            "shape": 1,
            "width": 1
        },
        {
            "direction": "input",
            "iotype": "wire",
            "name": "addr",
            "shape": 1,
            "width": 22
        },
        {
            "direction": "input",
            "iotype": "wire",
            "name": "cmd",
            "shape": 1,
            "width": 1
        },
        {
            "direction": "input",
            "iotype": "wire",
            "name": "cmd_en",
            "shape": 1,
            "width": 1
        },
        {
            "direction": "output",
            "iotype": "wire",
            "name": "init_calib",
            "shape": 1,
            "width": 1
        },
        {
            "direction": "output",
            "iotype": "wire",
            "name": "clk_out",
            "shape": 1,
            "width": 1
        },
        {
            "direction": "input",
            "iotype": "wire",
            "name": "data_mask",
            "shape": 1,
            "width": 4
        }
    ],
    "name": "HyperRAM_Memory_Interface_Top",
    "parameter": [],
    "wrap": "    "
}
```

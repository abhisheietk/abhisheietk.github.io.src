Title: MyHDL Primer -FIFO (First In First Out)
Date: 2016-11-14 16:47:21
Category: Myhdl
Tags: python, Myhdl
Slug: myhdl_primer
Authors: Abhishek Bajpai
Summary: Tutorial for writing MyHDL Code

image: assets/images/MyHDL.jpg

[MyHDL](http://www.myhdl.org) is a python based HDL language developed by Jan Decaluwe. Here we will talk about how to write code in MyHDL.

For purpose of simplicity we will try to create FIFO and its test bench.

# What is FIFO?

FIFO is an acronym for first in, first out, a method for organizing and manipulating a data buffer, where the oldest (first) entry, or 'head' of the queue, is processed first. It is analogous to processing a queue with first-come, first-served (FCFS) behaviour: where the people leave the queue in the order in which they arrive. curtsy [wikipedia](https://en.wikipedia.org/wiki/FIFO_%28computing_and_electronics%29)

So lets talk about interface signals for a FIFO module.

## Half full FIFO model

* clk    : input signal for clock
* inbusy : input bus is busy
* we     : input bus write enable
* din    : input bus data input
* outbusy: output bus is busy
* rd     : output bus read enable
* dout   : output bus data output
* rdout  : output bus data valid
* rst    : input reset

These are the obvious signals one should have in the FIFO module. "inbusy" and "outbusy" signals are important in order to signal master that the buffer overflow or underflow event has occured.

```python
from myhdl import block

DATA=8         #Size of Data bus
WORD=8         #Size of Data bus
ADDR=8         #Size of address bus
LOWER=2        #lower limit for FIFO read
UPPER=(2**8)-8 #upper limit for FIFO write
OFFSET=(2**8)-8 #upper limit for FIFO write

@block
def fifo(clk, inbusy, we, din, outbusy, rd, dout, rdout, rst,
          DATA=DATA, ADDR=ADDR, LOWER=LOWER, UPPER=UPPER, OFFSET=OFFSET):
    return instances()
```

Here @block represents module in HDL. And instances() return all the instences defined in the module. Presently no instances are defined.

## Signals (wire/registers)

Lets define some memory for fifo. Here "DATA" is the bus width for the mem register array and "2\*\*ADDR" is the count of total such registers.


```python
    mem = [Signal(modbv(0)[DATA:]) for i in range(2**ADDR)]
```

Lets define some signals. "in_addr" and "out_addr" are two pointer signals which points to the present memory address for the corresponding input and output buses.

```python
    in_addr, out_addr, diff = [Signal(modbv(0)[ADDR+1:]) for i in range(3)]
    noread.next  = Signal(bool(0))
```

Now lets write some instances. "@always_seq(clk.posedge, reset = rst)" emplies a sequential instance where event trigers on positive clock edge. Further all registers gets reset to their initial values on reset event.

### Write Logic instances
```python
    @always_seq(clk.posedge, reset = rst)
    def write_port():
        if we:
            in_addr.next = in_addr + modbv(1)[ADDR+1:]
        if (diff >= UPPER): # Logic for buff overflow
            inbusy.next = bool(1)
        else:
            inbusy.next = bool(0)
                
    @always(inclk.posedge)
    def write_mem_logic():
        if we:
            mem[in_addr[ADDR:]].next = din

```

### Read Logic instances

```python         
    @always_seq(clk.posedge, reset = rst) #    @always(outclk.posedge)
    def read_port():
        dout.next = mem[out_addr[ADDR:]]
        if rd and not noread:
            out_addr.next = out_addr + modbv(1)[ADDR+1:]
            rdout.next = rd
        else:                
            rdout.next = bool(0)        
```

In order to avoid buffer overflow and underflow events we have to take care of the gap between "in_addr" and "out_addr"

```python
    @always_comb
    def diffLogic():
        diff.next = in_addr - out_addr
 
    @always_comb
    def outbusyLogic():
        if (diff <= LOWER): # Logic for buff underflow
            outbusy.next = bool(1)
            noread.next  = bool(1)
        else:
            outbusy.next = bool(0)
            noread.next  = bool(0)
```

Let us see the complete code 

```python
#fifo.py
from myhdl import block

DATA=8         #Size of Data bus
WORD=8         #Size of Data bus
ADDR=8         #Size of address bus
LOWER=2        #lower limit for FIFO read
UPPER=(2**8)-8 #upper limit for FIFO write
OFFSET=(2**8)-8 #upper limit for FIFO write

@block
def cfifo(clk, inbusy, we, din, outbusy, rd, dout, rdout, rst,
          DATA=DATA, ADDR=ADDR, LOWER=LOWER, UPPER=UPPER, OFFSET=OFFSET):

    in_addr, out_addr, diff = [Signal(modbv(0)[ADDR+1:]) for i in range(3)]
    
    mem = [Signal(modbv(0)[DATA:]) for i in range(2**ADDR)]    
       
    @always_seq(clk.posedge, reset = rst)
    def write_port():
        if we:
            in_addr.next = in_addr + modbv(1)[ADDR+1:]
        if (diff >= UPPER):
            inbusy.next = bool(1)
        else:
            inbusy.next = bool(0)
                
    @always(inclk.posedge)
    def write_mem_logic():
        if we:
            mem[in_addr[ADDR:]].next = din

            
    @always_seq(clk.posedge, reset = rst) #    @always(outclk.posedge)
    def read_port():
        dout.next = mem[out_addr[ADDR:]]
        if rd and not noread:
            out_addr.next = out_addr + modbv(1)[ADDR+1:]
            rdout.next = rd
        else:                
            rdout.next = bool(0)
        
    @always_comb
    def diffLogic():
        diff.next = in_addr - out_addr
        
    @always_comb
    def outbusyLogic():
        #level.next = diff
        if (diff <= LOWER):
            outbusy.next = bool(1)
            noread.next = bool(1)
        else:
            outbusy.next = bool(0)
            noread.next = bool(0)
            
    return instances()
```

### Test Bench

In order to write a test bench we will use a puthon's unit test framework. In order to use this frame work we will write a testcase class. 

At first lets write a skelton class "TestFifo" which actually does noting.

```python
#test_fifo.py
from unittest import TestCase
import unittest

class TestFifo(TestCase):
    
    def testFifoBuffer(self):
        """ Check that fifo can be write and read """     
        @block
        def test_fifo(): 
                
            return instances()
        
        
        tb = test_cfifo()
        tb.config_sim(trace=True)
        tb.run_sim(duration=1500)
        tb.quit_sim()


```

On running the test output is as follows.

```bash
abhishek@abhishek:~/2016/MyHDL_tutorial$ python -m test_fifo
<class 'myhdl.StopSimulation'>: No more events
.
----------------------------------------------------------------------
Ran 1 test in 0.017s

OK
```

Now lets populate the test bench. "createbuff" creates a test buffer that we will write to the fifo later.

```python
    def testBuffer(self):
        """ Check that buffer can be write and read """
        ADDR = 4
        DATA = 16
        OFFSET = 8
        LOWER = 4
        UPPER =2**ADDR-4
        WATCHDOG = 3000
        
        def createbuff(DATA, ADDR):
            return [Signal(intbv(randrange(2**DATA))) for i in range(2**4)]
```

Now here again "@block" we are defining a test bench module to test fifo. Various signals have been defined. "fifo_inst" that is device under test, also defined here.

```python
            clk = Signal(bool(0))
            rst = ResetSignal(0, active=1, async=False)
            
            we, rd, inbusy, outbusy, hfull, rdout = [Signal(bool(0)) for i in range(6)]
            din, dout = [Signal(intbv(0)[DATA:]) for i in range(2)]
            
            fifo_inst = fifo(clk, inbusy, we, din, 
                      outbusy, rd, dout, rdout, rst,
                      ADDR=ADDR, DATA=DATA, OFFSET=OFFSET, LOWER=LOWER, UPPER=UPPER)
```

"fifo_inst.convert" converts fifo MyHDL model to the verilog.

```python
            fifo_inst.convert(hdl='Verilog', name='fifo_' + str(ADDR)+'_'+ str(DATA)+'_'
                          + str(OFFSET)+'_'+ str(LOWER)+'_'+ str(UPPER))
```

Lets generate "clk" and "rst" logic signals.

```python
            @always(delay(8))
            def clkgen():
                clk.next = not clk
            
            rambuff = createbuff(DATA, ADDR) 
            
            @instance
            def stimulus():
                yield delay(20)
                rst.next = 1
                yield delay(20)
                rst.next = 0
                yield delay(20)
```

Lets logic for writing to and reading from fifo.

```python
            @instance
            def write():
                we.next = Signal(bool(0))
                yield delay(50)
                
                for data in rambuff:                        
                    yield clk.posedge
                    while inbusy:
                        we.next = 0
                        yield clk.posedge
                        
                    we.next = 1                    
                    din.next = data                        
                        
                yield clk.posedge
                we.next = 0
                #din.next = 0
                
            @instance
            def read():
                watchdog = 30
                watchctr = 0
                yield delay(250)
                j = 0
                while 1:
                    yield clk.posedge
                    if watchctr == watchdog:
                        watchctr = 0
                        break
                        
                    if not outbusy:
                        rd.next = Signal(bool(1))
                    else:
                        rd.next = Signal(bool(0))
                        watchctr = watchctr + 1
                        #print watchctr
                        
                    if (rdout):
                        print hex(dout), hex(rambuff[j])
                        #self.assertEqual(dout, rambuff[j])
                        j = j + 1
                        
                yield clk.posedge
                rd.next = Signal(bool(0))
```

Here is the complete code for test bench.

```python
from unittest import TestCase
import unittest
from myhdl import block, instances, Signal, modbv, ResetSignal, intbv, always, delay, instance
from fifo import fifo
from random import randrange

class TestFifo(TestCase):
    
    def testFifoBuffer(self):
        """ Check that fifo can be write and read """
        ADDR = 4
        DATA = 16
        OFFSET = 8
        LOWER = 4
        UPPER =2**ADDR-4
        WATCHDOG = 3000
        def createbuff(DATA, ADDR):
            return [Signal(intbv(randrange(2**DATA))) for i in range(2**4)]
     
        @block
        def tb_fifo(): 
            clk = Signal(bool(0))
            rst = ResetSignal(0, active=1, async=False)
            
            we, rd, inbusy, outbusy, hfull, rdout = [Signal(bool(0)) for i in range(6)]
            din, dout = [Signal(intbv(0)[DATA:]) for i in range(2)]
            
            fifo_inst = fifo(clk, inbusy, we, din, 
                      outbusy, rd, dout, rdout, rst,
                      ADDR=ADDR, DATA=DATA, OFFSET=OFFSET, LOWER=LOWER, UPPER=UPPER)
            
            fifo_inst.convert(hdl='Verilog', name='fifo_' + str(ADDR)+'_'+ str(DATA)+'_'
                          + str(OFFSET)+'_'+ str(LOWER)+'_'+ str(UPPER))
                          
            @always(delay(8))
            def clkgen():
                clk.next = not clk
            
            rambuff = createbuff(DATA, ADDR) 
            
            @instance
            def stimulus():
                yield delay(20)
                rst.next = 1
                yield delay(20)
                rst.next = 0
                yield delay(20)
                
            @instance
            def write():
                we.next = Signal(bool(0))
                yield delay(50)
                
                for data in rambuff:                        
                    yield clk.posedge
                    while inbusy:
                        we.next = 0
                        yield clk.posedge
                        
                    we.next = 1                    
                    din.next = data                        
                        
                yield clk.posedge
                we.next = 0
                #din.next = 0
                
            @instance
            def read():
                watchdog = 30
                watchctr = 0
                yield delay(250)
                j = 0
                while 1:
                    yield clk.posedge
                    if watchctr == watchdog:
                        watchctr = 0
                        break
                        
                    if not outbusy:
                        rd.next = Signal(bool(1))
                    else:
                        rd.next = Signal(bool(0))
                        watchctr = watchctr + 1
                        #print watchctr
                        
                    if (rdout):
                        print hex(dout), hex(rambuff[j])
                        #self.assertEqual(dout, rambuff[j])
                        j = j + 1
                        
                yield clk.posedge
                rd.next = Signal(bool(0))
                
                
            return instances()
        
        
        tb = tb_fifo()
        tb.config_sim(trace=True)
        tb.run_sim(duration=1500)
        tb.quit_sim()

if __name__ == '__main__':
    unittest.main()
```

here is the output while execution of the test bench.

```bash
abhishek@abhishek:~/2016/MyHDL_tutorial$ python2 -m test_fifo
0xd71e 0xd71e
0xdfcb 0xdfcb
0xdb09 0xdb09
0xaa7a 0xaa7a
0x7166 0x7166
0xf851 0xf851
0x2fbf 0x2fbf
0x4cb1 0x4cb1
0x5f3d 0x5f3d
0x32f4 0x32f4
0x67ac 0x67ac
0x4273 0x4273
<class 'myhdl._SuspendSimulation'>: Simulated 1500 timesteps
.
----------------------------------------------------------------------
Ran 1 test in 0.064s

OK
```

 It also generates signal traces that we can see by reading generated *.vcd file in gtkwave.
 
 ![TestBench]({{ site.url }}/assets/images/myhdl_fifo.png){:height="450px"}
 
 Finally lets see the converted design.
 
```verilog
// File: fifo_4_16_8_4_12.v
// Generated by MyHDL 1.0dev
// Date: Sat Nov 19 08:42:16 2016


`timescale 1ns/10ps

module fifo_4_16_8_4_12 (
    clk,
    inbusy,
    we,
    din,
    outbusy,
    rd,
    dout,
    rdout,
    rst
);


input clk;
output inbusy;
reg inbusy;
input we;
input [15:0] din;
output outbusy;
reg outbusy;
input rd;
output [15:0] dout;
reg [15:0] dout;
output rdout;
reg rdout;
input rst;

reg [4:0] out_addr;
reg [4:0] in_addr;
reg noread;
wire [4:0] diff;
reg [15:0] mem [0:16-1];



always @(posedge clk) begin: FIFO_4_16_8_4_12_WRITE_PORT
    if (rst == 1) begin
        inbusy <= 0;
        in_addr <= 0;
    end
    else begin
        if (we) begin
            in_addr <= (in_addr + 5'h1);
        end
        if ((diff >= 12)) begin
            inbusy <= (1 != 0);
        end
        else begin
            inbusy <= (0 != 0);
        end
    end
end


always @(posedge clk) begin: FIFO_4_16_8_4_12_READ_PORT
    if (rst == 1) begin
        out_addr <= 0;
        rdout <= 0;
        dout <= 0;
    end
    else begin
        dout <= mem[out_addr[4-1:0]];
        if ((rd && (!noread))) begin
            out_addr <= (out_addr + 5'h1);
            rdout <= rd;
        end
        else begin
            rdout <= (0 != 0);
        end
    end
end


always @(posedge clk) begin: FIFO_4_16_8_4_12_WRITE_MEM_LOGIC
    if (we) begin
        mem[in_addr[4-1:0]] <= din;
    end
end



assign diff = (in_addr - out_addr);


always @(diff) begin: FIFO_4_16_8_4_12_OUTBUSYLOGIC
    if ((diff <= 4)) begin
        outbusy = (1 != 0);
        noread = (1 != 0);
    end
    else begin
        outbusy = (0 != 0);
        noread = (0 != 0);
    end
end

endmodule
```
 
 
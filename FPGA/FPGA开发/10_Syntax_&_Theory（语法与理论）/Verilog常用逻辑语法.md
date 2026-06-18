---
tags:
  - FPGA/语法
  - Verilog
date: 2023-10-27
status: draft
---

# Verilog 常用逻辑语法

## 1. 位顺序反转


    写法一：
        module top_module( 
            input [7:0] in,
            output [7:0] out
        );
            always @(*) begin	
                for (int i=0; i<8; i++)	// int is a SystemVerilog type. Use integer for pure Verilog.
                    out[i] = in[8-i-1];
            end
        endmodule

    写法二：
        module top_module( 
            input [7:0] in,
            output [7:0] out
        );
            generate
                genvar i;
                for (i=0; i<8; i = i+1) begin: my_block_name
                    assign out[i] = in[8-i-1];
                end
            endgenerate
        endmodule

## 2. 模块实例化
        module top_module (
            input a,
            input b,
            output out
        );

            // Create an instance of "mod_a" named "inst1", and connect ports by name:
            mod_a inst1 ( 
                .in1(a), 	// Port"in1"connects to wire "a"
                .in2(b),	// Port "in2" connects to wire "b"
                .out(out)	// Port "out" connects to wire "out" 
                        // (Note: mod_a's port "out" is not related to top_module's wire "out". 
                        // It is simply coincidence that they have the same name)
            );

        /*
            // Create an instance of "mod_a" named "inst2", and connect ports by position:
            mod_a inst2 ( a, b, out );	// The three wires are connected to ports in1, in2, and out, respectively.
        */
            
        endmodule

## 3. 1位全加器
$a$：加数（本位）$b$：被加数（本位）$cin$：来自更低位的进位输入 (Carry-in)
求和信号sum：
    sum = a ^b ^cin   //只有在输入（a、b、cin）中存在奇数个1求和结果sum才会是1，否则本位位0
进位信号cout：
    cout = (a&b) | (a&cin) | (b&cin)  //只要三个输入（a、b、cin两个或着以上进位置1）

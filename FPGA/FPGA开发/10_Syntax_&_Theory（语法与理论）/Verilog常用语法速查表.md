---
tags:
  - FPGA/语法速查
  - Verilog
date: 2026-04-30
---

# 🚀 Verilog 常用语法速查表

> [!info] 提示
> 本文档用于快速查阅常用的 Verilog 语法和代码片段。建议结合 `Ctrl/Cmd + F` 快速搜索关键字（如 "位拼接", "状态机"）。

## 1. 基础数据类型

**线网型 (Wire)**
主要用于连续赋值语句（`assign`）和模块实例化时的连接。
Verilog
```
wire [7:0] data_bus; // 8位宽的线网
```

**向量的使用：**
module top_module( 
    input wire [15:0] in,
    output wire [7:0] out_hi,
    output wire [7:0] out_lo );
    assign out_hi [7:0] = in [15:8];
    assign out_lo [7:0] = in [7:0];
endmodule
```

**向量的逻辑配置：**
module top_module(
	input [2:0] a, 
	input [2:0] b, 
	output [2:0] out_or_bitwise,
	output out_or_logical,
	output [5:0] out_not
);
	
	assign out_or_bitwise = a | b;
	assign out_or_logical = a || b;

	assign out_not[2:0] = ~a;	// Part-select on left side is o.
	assign out_not[5:3] = ~b;	//Assigning to [5:3] does not conflict with [2:0]
	
endmodule
````

**寄存器型 (Reg)** 主要用于过程块（`always`, `initial`）中被赋值的变量。_注意：reg类型在综合后不一定是物理寄存器。_

Verilog
```
reg [3:0] counter;   // 4位宽的寄存器
```

## 2. 赋值方式对比 (重点🔥)

> [!warning] 避坑指南：阻塞与非阻塞 这是 FPGA 学习中最容易犯错的地方，务必牢记以下原则！

**阻塞赋值 （=）**

- **用法**：常用于组合逻辑电路（如 `always @(*)`）。
    
- **特点**：顺序执行，上一句没执行完，下一句不能执行。
    

Verilog

```
always @(*) begin
    a = b;
    c = a; // c 最终等于 b
end
```

**非阻塞赋值 (`<=`)**

- **用法**：常用于时序逻辑电路（如 `always @(posedge clk)`）。
    
- **特点**：并行执行，所有赋值在 always 块结束时同时生效。
    

Verilog

```
always @(posedge clk) begin
    a <= b;
    c <= a; // c 最终等于 a 的旧值，相当于打了一拍
end
```

## 3. 常用控制结构

**If-Else 语句**

Verilog

```
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        q <= 1'b0;
    end else if (enable) begin
        q <= d;
    end else begin
        q <= q; // 保持不变
    end
end
```

**Case 语句** (常用于状态机或多路选择器)

Verilog

```
always @(*) begin
    case (sel)
        2'b00: out = in_a;
        2'b01: out = in_b;
        2'b10: out = in_c;
        default: out = 1'b0; // 必须写 default，防止生成锁存器！
    endcase
end
```

## 4. 实用语法糖

**位拼接运算符 `{}`** 常用于移位操作或将多个信号合并。

Verilog

```
wire [3:0] a = 4'b1010;
wire [3:0] b = 4'b0101;
wire [7:0] c = {a, b}; // c = 8'b1010_0101
```

## 5. 常用运算符 (Operators)

**逻辑运算符 (Logical)**
经常用于 `if` 等条件判断中，结果只有 1 (true)、0 (false) 或 x (未知)。
- `&&` : 逻辑与 (AND)
- `||` : 逻辑或 (OR)
- `!`  : 逻辑非 (NOT)

**按位运算符 (Bitwise)**
对信号进行**逐位**逻辑操作，多用于组合逻辑。
- `&`  : 按位与
- `|`  : 按位或
- `~`  : 按位非
- `^`  : 按位异或 (XOR)
- `~^` 或 `^~` : 按位同或 (XNOR)

**缩减/归约运算符 (Reduction)**
作用于单操作数，对它的所有位进行累积运算，最终得出一个 **1位** 的结果。
- `&a` : a 的所有位连按位与 (常用于判断是否全为 1)
- `|a` : a 的所有位连按位或 (常用于判断是否含 1)
- `^a` : a 的所有位连按位异或 (常用于奇偶校验)

**关系与相等运算符 (Relational & Equality)**
- `>`, `<`, `>=`, `<=` : 大于、小于、大于等于、小于等于
- `==` : 逻辑相等
- `!=` : 逻辑不等

## 6. 连接运算符
    {}，{nm{vector}}

{5{1'b1}} // 5'b11111（或 5'd31 或 5'h1f）
{2{a,b,c}} // 等同于 {a,b,c,a,b,c}
{3'd5, {2{3'd6}}} // 9'b101_110_110。它是 101 与 的连接。
                    // 第二个向量，即 3'b110 的两个副本。


## 7. 复制运算符
构建一个电路，将 8 位数字符号扩展为 32 位。这需要将 24 个符号位（即，复制 bit[7] 24 次）连接起来，然后是 8 位数字本身。
module top_module (
    input [7:0] in,
    output [31:0] out );//

    // assign out = { replicate-sign-bit , the-input };
    assign out = {{24{in[7]}} , in };
endmodule

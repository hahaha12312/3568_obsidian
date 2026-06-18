# 模块名称：{{title}}
**创建时间**：{{date}}
**标签**：#FPGA/模块 #Verilog 

## 1. 模块功能描述
（简要描述该模块的作用，例如：这是一个采用 One-Hot 编码的三段式状态机，用于控制 ADC 采样时序。）

## 2. 接口定义 (I/O)
| 端口名 | 方向 | 位宽 | 描述 |
| :--- | :--- | :--- | :--- |
| clk | input | 1 | 系统时钟 |
| rst_n | input | 1 | 低电平异步复位 |

## 3. Verilog 核心代码
```verilog
// 在 Obsidian 中使用 verilog 代码块可以自动语法高亮
always @ (posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // 复位逻辑
    end else begin
        // 状态转移逻辑
    end
end
\```
（注意：实际模板中去掉结尾反引号前的转义符`\`）
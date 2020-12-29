`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2020/12/16 22:07:49
// Design Name: 
// Module Name: ledtest
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module ledtest(clk,data,sw);
input clk;
input[0:3] sw
output[15:0] data;
reg clk1s,dir;
reg[15:0] led_r;
reg[15:0] led;
reg [2:0] cnt2;
parameter max=5000000;
reg[3:0] state=2'b00;
reg[30:0] n;
reg[15:0] data = 16'h0000;
always @(posedge clk)begin
    if(n==max)begin
        if(!clk1s)clk1s<=1'b1;
        else clk1s<=1'b0;
        n<=0;
        end
    else n<=n+1;
end
always @(posedge clk1s)begin
    case(sw)
    4'b0000:begin
        if(date==16'h8000)begin
        date <=16'h0001;
        end
        else begin
        date<=date<<1'b1;  
        end     
    end 
    4'b1000:begin
        if(date =16'h0000)begin
            data<=16'haaaa;
        end
        else begin
            data<=date^16'h1111;
        end
    end
    4'b0100:begin
    if(date==16'h8000)begin
            date <=16'h0001;
            end
            else begin
            date<=date<<2'b11;  
            end     
    end    
    4'b0010:begin
    if(date==16'hff00)begin
            date <=16'h00ff;
            end
            else begin
            date<=date<<1'b1;  
            end     
    end    
    4'b0001:begin
        
        if(date[7:0]==8'h80)begin
            date[7:0]<=8'h01;
            end
        else begin
            date[7:0]<=date[7:0]<<1'b1;  
        end 
        if(date[15:8]==8'h01)begin
            date[15:8]<=8'h80;
            end
        else begin
            date[15:8]<=date[15:8]>>1'b1;  
        end         
    end
    4'b1100:begin
        
        if(date[15:8]==8'h80)begin
            date[15:8]<=8'h01;
            end
        else begin
            date[15:8]<=date[15:8]<<1'b1;  
        end 
        if(date[7:0]==8'h01)begin
            date[7:0]<=8'h80;
            end
        else begin
            date[7:0]<=date[7:0]>>1'b1;  
        end         
    end  
    4'b1010:begin
        
        if(date[15:8]==8'h80)begin
            date[15:8]<=8'h01;
            end
        else begin
            date[15:8]<=date[15:8]<<1'b1;  
        end 
        if(date[7:0]==8'h01)begin
            date[7:0]<=8'h80;
            end
        else begin
            date[7:0]<=date[7:0]>>1'b1;  
        end         
    end
    4'b1001:begin        
        //从两侧向中间逐渐点亮，再依次熄灭
            if(date = 16'h0000)
            begin
                led_r = 16'b0000_0000_0000_0001;
                led_r1= 16'b1000_0000_0000_0000;
            end
            else if(date = 16'hffff)begin
                date = 16'h0000;
            end
            else begin 
                led_r=(led_r<<1)|led_r;
                led_r1=(led_r1>>1)|led_r1;
                date <=led_r|ledl_r1;
            end
        end
    4'b1110:begin
        
    end
    4'b1101:begin
        
    end   
endcase
end
endmodule  
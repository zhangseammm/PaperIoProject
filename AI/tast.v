`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create led: 2020/12/16 22:07:49
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


module ledtest(clk,led,sw);
input clk;
input[3:0] sw;
output[15:0] led = 16'h0000;
reg clk1s;
reg[3:0] sws=4'b0000;
reg[4:0] count = 0;
reg[3:0] count2 = 0;
reg[15:0] led_r,led_r1;
parameter max=5000000;
reg[30:0] n;
reg[15:0] led;
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
    4'b0000:begin//可用
        sws <= 4'b0000;
        if(led==16'h8000)begin
        led <=16'h0001;
        end
        else if(led==16'h0000)begin
            led<=16'h0001;
        end
        else begin
        led<=led<<1'b1;  
        end     
    end 
    4'b1000:begin       
        
            if(led[7:0]==8'h80)begin
            led[7:0]<=8'h01;
            led[15:8]<=8'h80;
            end
        else if(led[7:0]==8'h00)begin
            led[7:0]<=8'h01;
            led[15:8]<=8'h80; 
        end
        else if(led==16'hffff)begin
        led<=16'h0000;
        end
        else begin
            led[7:0]<=(led[7:0]<<1'b1|led[7:0]); 
            led[15:8]<=(led[15:8]>>1'b1|led[7:0]); 
        end 
        end
    4'b0100:begin//更快流水灯可用
    sws <= 4'b0100;
    if(led==16'h8000)begin
            led <=16'h0001;
        end
        else if(led==16'h0000)begin
            led<=16'h0001;
        end
        else begin
            led<=led<<2'b11;  
        end     
    end    
    4'b0010:begin//太僵硬可用
    if(led==16'hffff)begin
            led<=led<<1'b1;
            led_r <=16'h0001;
        end
        else if(led==16'h0000)begin
            led<=16'hffff;
            led_r <=16'h0001; 
        end
        else begin
            led<=(led<<1'b1|led_r);
            led_r <=16'h0001;  
        end     
    end    
    4'b0001:begin//可用
        sws <= 4'b0001;
        if(led[7:0]==8'h80)begin
            led[7:0]<=8'h01;
            led[15:8]<=8'h80;
            end
        else if(led[7:0]==8'h00)begin
            led[7:0]<=8'h01;
            led[15:8]<=8'h80;
        end
        else begin
            led[7:0]<=led[7:0]<<1'b1; 
            led[15:8]<=led[15:8]>>1'b1; 
        end 
        
    end
    4'b1100:begin//可用
        sws <= 4'b1100;
        if(led[15:8]==8'h80)begin
            led[15:8]<=8'h01;
            end
        else if(led[15:8]==8'h00)begin
            led[15:8]<=8'h01;
        end
        else begin
            led[15:8]<=led[15:8]<<1'b1;  
        end 
        if(led[7:0]==8'h01)begin
            led[7:0]<=8'h80;
            end
        else if(led[7:0]==8'h00)begin
            led[7:0]<=8'h80;
        end
        else begin
            led[7:0]<=led[7:0]>>1'b1;  
        end         
    end  
    4'b1010:begin//meiyong
    sws <= 4'b1010;
            if(count == 0)begin
                led_r = 16'b0000_0000_0000_0001;
                led_r=(led_r<<1)|led_r;
                led <=led_r;
                count<=count+1;
            end
            else if(led == 16'hffff)begin
                led = 16'h0000;
                count<=0;
            end
            else begin 
                led_r=(led_r<<1)|led_r;
                led <=led_r;
            end
           
    end
    4'b1001:begin//meiyong 
    sws <= 4'b1001;       
        //从两侧向中间逐渐点亮，再依次熄灭
            if(count ==0 )
            begin
                led_r = 16'b0000_0000_0000_0001;
                led_r1= 16'b1000_0000_0000_0000;
                led_r=(led_r<<1)|led_r;
                led_r1=(led_r1>>1)|led_r1;
                led <=led_r|led_r1;
                count<=count+1;
            end
            else if(led == 16'hffff)begin
                count <=0; 
            end
            else begin 
                led_r=(led_r<<1)|led_r;
                led_r1=(led_r1>>1)|led_r1;
                led <=led_r|led_r1;
            end
        end
    4'b1110:begin//xiugai
    sws <= 4'b1110;
        if(led!=16'b0110_0110_0110_0110)begin
        led_r = 16'b0110_0110_0110_0110;
        led<=led_r;
        end
        else begin
            led<=~led;
        end
    end
    4'b1101:
    begin//count一来为0
    if(count==16)begin
            count<=1;
            led <= 16'h0001;
            led_r <= 16'h0000;
    end
    else if(led[16-count]==1) begin
            count <= count+1;
            led_r <= led;
            led[15:0]<=(16'd0001|led_r);
    end
    else if(count ==0)begin
        led <= 16'h0001;
         led_r <= 16'h0000;
        count<=count+1;
    end
    else begin
        led[15:0]<=((led[15:0]<<1)|led_r);
    end
    end
     4'b1111:begin
     led = 16'h0000;
     count <= 0;
     end
endcase
end
endmodule  

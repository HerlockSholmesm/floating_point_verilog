module tb_dp;

  reg clk, reset, strt;
  reg [63:0] a,b;
  wire [63:0] z;


  initial
  begin
    clk <= 0;
    a <= 64'b011111111110100000000000000000000000000000000000000000000000000;
    b <= 64'b011111111111000000000000000000000000000000000000000000000000000;
    reset <= 0;
    strt <= 1;
    strt <= #40 0;
    forever
    begin
      #5 clk = ~clk;
    end
  end

  div_dp dv(clk,strt,a,b,reset,z);


endmodule

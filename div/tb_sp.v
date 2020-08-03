module tb_sp;

  reg clk, reset, strt;
  reg [31:0] a,b;
  wire [31:0] z;


  initial
  begin
    clk <= 0;
    a <= 32'b01000001010010000000000000000000;
    b <= 32'b01000000001000000000000000000000;
    reset <= 0;
    strt <= 1;
    #10 strt <= 1;
    #30 strt <= ~strt;
    forever
    begin
      #5 clk = ~clk;
    end
  end

  div_sp dv(clk,strt,a,b,reset,z);


endmodule
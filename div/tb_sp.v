module tb_sp;

  reg clk, reset, strt;
  reg [31:0] a,b;
  wire [31:0] z;

integer file_in;
integer file_count;
  initial
  begin
    clk <= 0;
    file_in = $fopen("input.txt", "r");
    file_count = $fscanf(file_in, "%b\n", a);
    file_count = $fscanf(file_in, "%b\n", b);
    //a <= 32'b01000001010010000000000000000000;
    //b <= 32'b01000000001000000000000000000000;
    reset <= 0;
    strt <= 1;
    #10 strt <= 1;
    #30 strt <= ~strt;
    forever
    begin
      #5 clk = ~clk;
    end
  end

//applying inputs and monitoring the results
integer out;

  initial
    begin
      out = $fopen("sim_out.txt", "w");

      $timeformat(-9, 4, " ns", 20);

      $fdisplay(out, "\n\n");
      $fdisplay(out, "------------------------------------------------------");
      //$printtimescale;
      //$fdisplay(out, "Clock period is: %g in the mentioned time unit", clk);
      //$fdisplay(out, "Clock frequency is: %g MHz", (1000/clk)); //showing real number in form of real or scientific; whichever is shorter
      $fdisplay(out, "Simulation started...\n");
      $fmonitor (out, "@%10t", $realtime, ":  a = %b,  b = %b , out = %b", a, b, dv.o_z);

      
      #(300);
      $fclose(out);
      $stop;
    end


  div_sp dv(clk,strt,a,b,reset,z);


endmodule
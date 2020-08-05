module dp_sqrt_tb;


reg [63:0]in;
wire [63:0]out;

dp_sqrt s(.x(in), .y(out));


integer out_file;
integer i;
initial begin
	out_file = $fopen("dp_sim_out.txt", "w");
	$fdisplay(out_file, "the current module name is = %m");
	$fdisplay(out_file, "-----------------------------------------");
	$timeformat(-9, 4, " ns", 5);

	$fmonitor(out_file, "@%10g", $realtime, ": input is %h, and output is %h with remainder %h", in, out, s.r);

	for(i = 100000; i > 0; i = i - 1) begin
		in = $random;
		#10;
	end
	$fclose(out_file);
	$stop;
end
endmodule


















module fp_sqrt_sp (x,y);
input [31:0]x;
output [31:0]y;
reg [31:0]y;
integer i;

function [63:0]bit2bit_sq(input [31:0]x);
  reg[63:0]y;
  for (int i =31; i > 0; i=i-1) begin
     y [2*i] = x[i]; 
     y [(2*i)+1] = 1'b0;
  end 
  return y;
endfunction


   always@(x)
begin
reg[22:0]x_mantissa;
reg[7:0]x_exponent;
reg x_sign;
reg[22:0]y_mantissa;
reg[7:0]y_exponent;
reg y_sign;
reg[25:0]ix;

reg[51:0]a;

reg[25:0]biti;

    reg[51:0]r;
    reg[52:0]rt;

    x_mantissa=x[22:0];
    x_exponent=x[30:23];
    x_sign=x[31];
    y_sign=1'b0;

if(x_exponent==8'b00000000)
begin
    y_exponent=8'b0;
    y_mantissa=23'b0;
end
else if (x_exponent==8'b11111111)
begin
    y_exponent=8'b1;
    y_mantissa=23'b0;
end
else
begin
    if(x_exponent[0]==1'b1)
    begin
        y_exponent={1'b0,x_exponent[7:1]}+64;
        ix={2'b01,x_mantissa,1'b0};
    end
    else
    begin
        y_exponent={1'b0,x_exponent[7:1]}+63;
        ix={1'b1,x_mantissa,2'b00};
    end
a=52'b0;
biti={2'b10,x<=000000};
r[51:26]=ix;
r[25:0]=26'b0;
begin
    for(i=25;i>=0;i=i-1)
    begin
        rt={{1'b0,r}-{{1'b0,{a|bit2bit_sq(biti)}}}};
        a={a[51:1],1'b0};
        if(rt[52]==1'b0)
        begin
            r=rt[51:0];
            a=a|bit2bit_sq;
        end
            biti={biti[25:1],1'b0};
        end
    end
    a[24:2]=a[24:2]+a[1];
    y_mantissa=a[24:2];
end

y[22:0]=y_mantissa;
y[30:23]=y_exponent;
y[31]=y_sign;
end
endmodule
















///         translate to vhdl 


//library IEEE;
//use IEEE.STD_LOGIC_1164.ALL;
//use IEEE.STD_LOGIC_ARITH.ALL;
//use IEEE.STD_LOGIC_UNSIGNED.ALL;
//-- use STD.textio.all;                     -- basic I/O
//-- use IEEE.std_logic_textio.all;          -- I/O for logic types

//entity sqrt is
  //  Port ( x : in  STD_LOGIC_VECTOR (31 downto 0);
    //       y : out  STD_LOGIC_VECTOR (31 downto 0));
//end sqrt;

//architecture Behavioral of sqrt is

	//function bit2bit_sq(x: STD_LOGIC_VECTOR) return STD_LOGIC_VECTOR is
//		variable y : STD_LOGIC_VECTOR(2*x'left+1 downto 0);
//	-- Returns x^2 by intercalating zeros in the argument,
//	-- were x has only one bit different from zero.
//	begin
//		for i in x'left downto 0 loop
//			-- x'right must be zero
//			y(2*i):=x(i);
//			y(2*i+1):='0';
//		end loop;
//		return y;
//	end;

//begin
//	process(x)
//		variable x_mantissa : STD_LOGIC_VECTOR (22 downto 0);
//		variable x_exponent : STD_LOGIC_VECTOR (7 downto 0);
//		variable x_sign : STD_LOGIC;
//		variable y_mantissa : STD_LOGIC_VECTOR (22 downto 0);
//		variable y_exponent : STD_LOGIC_VECTOR (7 downto 0);
//		variable y_sign : STD_LOGIC;
//		
//		variable ix: STD_LOGIC_VECTOR (25 downto 0);
//		variable a : STD_LOGIC_VECTOR (51 downto 0);
//		variable biti : STD_LOGIC_VECTOR (25 downto 0);
//		variable r : STD_LOGIC_VECTOR (51 downto 0);
//		variable rt : STD_LOGIC_VECTOR (52 downto 0);
//		
//		-- variable my_line : line;  -- type 'line' comes from textio
 //  begin
//		x_mantissa := x(22 downto 0);
//		x_exponent := x(30 downto 23);
//		x_sign := x(31);
//		
//		y_sign := '0';
//		
//		if (x_exponent="00000000") then -- zero
//			y_exponent := (others=>'0');
//			y_mantissa := (others=>'0');
//		elsif (x_exponent="11111111") then -- infinity
		//	y_exponent := (others=>'1');
	//		y_mantissa := (others=>'0');
	//	else
	//		
	//		if (x_exponent(0)='1') then -- exponent-127 is even
	//			y_exponent := '0' & x_exponent(7 downto 1) + 64;
	//			ix := "01" & x_mantissa & '0'; 
	//		else -- exponent-127 is odd
	//			-- shift mantissa one to the left and subtract one from x_exponent
	//			y_exponent := '0' & x_exponent(7 downto 1) + 63;
	//			ix := '1' & x_mantissa & "00";
	//		end if;
	//		-- mantissa is m=ix/2^24 
	//		-- (one zero was added to the right to make the power even)
	//		-- let the result of the integer square root algorithm be iy (26 bits)
	//		-- iy = sqtr(ix)*2^13
	//		-- resulting that sqrt(m)=iy/2^25
	//	
	///		-- Integer input N bits square root algorithm:
		//	-- r is be the reminder, r=ix-z^2, and z(N+1) the result, 
		//	-- 	with bit(N)=1/2^(N/2), and bit(n)=2^(N/2-n)
		//	-- Test each bit in the result, from the most significative to the least
		//	/-- significative: n goes from zero no N.
			//-- if bit is one: r(n+1) = ix - (z(n)+bit(n))^2 = 
			//-- 								r(n) - 2z(n)bit(n) - bit(n)^2
			//-- else           r(n+1) = r(n)
			//-- bit will be one if the resulting remainder is positive.
			//-- making a(n) = 2z(n)bit(n), one has, 
			//-- if bit is one: a(n+1) = 2(z(n)+bit(n))bit(n)/2 = 
			//--									a(n)/2+bit(n)^2
			//-- else           a(n+1) = a(n)/2
			//-- and a(N+1) = 2z(N+1)/2^(N/2+1) = z(N+1)/2^(N/2)
			
			//-- VHDL Implementation
			
			//a := (others=>'0');
	
			//biti := "10" & x"000000"; -- 2^(25)
			//-- biti has the bit being evaluated equal to one
			//r(51 downto 26):= ix; -- r is in Q26
		//	r(25 downto 0):=(others=>'0');
			
			//for i in 25 downto 0 loop
			//	rt := ('0' & r) - ('0' & (a or bit2bit_sq(biti))); 
			//	-- trial for the new value for the reminder
			//	a := '0' & a(51 downto 1); -- srl
			//	if (rt(52)='0') then -- rt>=0
			//		r := rt(51 downto 0);
			//		a := a or bit2bit_sq(biti); -- the adder is safelly replaced by an or
			//	end if;
			//	biti := '0' & biti(25 downto 1); -- srl 1
			//end loop;
	
			//a(24 downto 2) := a(24 downto 2)+a(1); -- round
			//-- even for ix = all '1' a will not oveflow
		//	
		//	-- a is the result
			//y_mantissa := a(24 downto 2);
		///	
	//	end if;
//
//		y(22 downto 0) <= y_mantissa;
	//	y(30 downto 23) <= y_exponent;
//		y(31) <= y_sign;
   //end process;
//end Behavioral;
module div_sp(
        input clk, start,
        input [31:0] i_a, i_b,
        input reset,
        output [31:0] o_z);

  reg a_sign, b_sign, z_sign;
  reg [22:0] a_mantis, b_mantis, z_mantis;
  reg [7:0] a_exp, b_exp, z_exp;
  reg [48:0] A,M;
  reg [47:0] Q;
  reg [3:0] count;
  reg [1:0] state = 0;
  reg [31:0] z;
  parameter S_START = 2'b00,
            S_DIVIDE = 2'b01,
            S_FINISH = 2'b10,
            S_IDLE = 2'b11;

  always @(posedge clk)
  begin
    if (~reset)
    begin
      case(state)

        S_START:
        begin

          a_mantis <= i_a[22 : 0];
          b_mantis <= i_b[22 : 0];
          a_sign <= i_a[31];
          b_sign <= i_b[31];
          a_exp <= i_a[30:23] - 127;
          b_exp <= i_b[30:23] - 127;
          Q <= {1'b1,i_a[22:0]} << 24;
          A <= 0;
          M <= {1'b1,i_b[22:0]};
          count <= 0;
          //a=NaN or b=NaN -> z=NaN
          if ((a_exp==128 && a_mantis!=0) || (b_exp==128 && b_mantis!=0))
          begin
            z_sign <= 1'b0;
            z_exp <= 128;
            z_mantis <= 1;
            state <= S_FINISH;
          end

          //a=inf or b=inf -> z=inf
          else if ((a_exp==128 && a_mantis==0 && !(b_exp==-127 && b_mantis==0)) || (b_exp==128 && b_mantis==0 && !(b_exp==-127&&b_mantis==0)))
          begin
            z_sign <= a_sign ^ b_sign;
            z_exp <= 128;
            z_mantis <= 0;
            state <= S_FINISH;
          end

          //a=0,b=inf or a=inf,b=0 -> z=NaN
          else if((a_exp==128 && a_mantis==0 && b_exp==-127 && b_mantis==0) || (b_exp==128 && b_mantis==0 && b_exp==-127&&b_mantis==0))
          begin
            z_sign <= 0;
            z_exp <= 128;
            z_mantis <= 1;
            state <= S_FINISH;
          end
          state<= S_DIVIDE;
        end

        S_DIVIDE:
        begin
        if (A[48])
          begin
            {A,Q} = {A,Q} << 1;
            A = A+M;
          end
        else
          begin
            {A,Q} = {A,Q} << 1;
            A = A-M;
          end
        if (A[48])
          begin
            Q[0]=0;
          end
        else
          begin
            Q[0] =1;
          end
          if (A[48])
          begin
            {A,Q} = {A,Q} << 1;
            A = A+M;
          end
        else
          begin
            {A,Q} = {A,Q} << 1;
            A = A-M;
          end
        if (A[48])
          begin
            Q[0]=0;
          end
        else
          begin
            Q[0] =1;
          end
          if (A[48])
          begin
            {A,Q} = {A,Q} << 1;
            A = A+M;
          end
        else
          begin
            {A,Q} = {A,Q} << 1;
            A = A-M;
          end
        if (A[48])
          begin
            Q[0]=0;
          end
        else
          begin
            Q[0] =1;
          end
          if (A[48])
          begin
            {A,Q} = {A,Q} << 1;
            A = A+M;
          end
        else
          begin
            {A,Q} = {A,Q} << 1;
            A = A-M;
          end
        if (A[48])
          begin
            Q[0]=0;
          end
        else
          begin
            Q[0] =1;
          end
          count = count+1;
          if (count == 12)
            state = S_FINISH;
        end

        S_FINISH:
        begin
          if(~Q[25])
          begin
            Q <= Q << 1;
            z_exp <= z_exp-1;
          end
          //underflow,overflow
          z_mantis <= Q[24:1];
          z_exp <= 127 + a_exp - b_exp;
          z_sign <= a_sign ^ b_sign;
          state <= S_IDLE;
        end

      S_IDLE:
      begin
        if (start == 1)
          state = S_START;
      end
      endcase
    end
    else
    begin
      state <= S_IDLE;
      z_exp <= 0;
      z_mantis <= 0;
      z_exp <= 0;
      z <= 0;
    end

  end

assign o_z = {z_sign,z_exp,z_mantis};
endmodule

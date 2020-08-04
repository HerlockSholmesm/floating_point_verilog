module div_dp
    (input clk, start,
        input [63:0] i_a, i_b,
        input reset,
        output [63:0] o_z);

    reg a_sign, b_sign, z_sign;
    reg [51:0] a_mantis, b_mantis, z_mantis;
    reg [10:0] a_exp, b_exp, z_exp;
    reg [106:0] A, M;
    reg [105:0] Q;
    reg [4:0] count;
    reg [1:0] state =0;
    parameter S_IDLE=2'b00,
              S_START=2'b01,
              S_DIVIDE=2'b10,
              S_FINISH=2'b11;

    always @(posedge clk)
        begin
            if (~reset)
                begin
                    case (state)

                        S_START:
                            begin

                                a_mantis <= i_a[51:0];
                                b_mantis <= i_b[51:0];
                                a_sign <= i_a[63];
                                b_sign <= i_b[63];
                                a_exp <= i_a[62:52]-1023;
                                b_exp <= i_b[62:52]-1023;
                                Q <= {1'b1, i_a[51:0]} << 53;
                                A <= 0;
                                M <= {1'b1, i_b[51:0]};
                                count <= 0;
                                //a=NaN or b=NaN -> z=NaN
                                if ((a_exp == 1024 && a_mantis != 0) || (b_exp == 1024 && b_mantis != 0))
                                    begin
                                        z_sign <= 1'b0;
                                        z_exp <= 1024;
                                        z_mantis <= 1;
                                        state <= S_FINISH;
                                    end

                                    //a=inf or b=inf -> z=inf
                                else if ((a_exp == 1024 && a_mantis == 0 && !(b_exp == -1023 && b_mantis == 0)) || (b_exp == 1024 && b_mantis == 0 && !(b_exp == -1023 && b_mantis == 0)))
                                    begin
                                        z_sign <= a_sign ^ b_sign;
                                        z_exp <= 1024;
                                        z_mantis <= 0;
                                        state <= S_FINISH;
                                    end

                                    //a=0,b=inf or a=inf,b=0 -> z=NaN
                                else if ((a_exp == 1024 && a_mantis == 0 && b_exp == -1023 && b_mantis == 0) || (b_exp == 1024 && b_mantis == 0 && b_exp == -1023 && b_mantis == 0))
                                    begin
                                        z_sign <= 0;
                                        z_exp <= 1024;
                                        z_mantis <= 1;
                                        state <= S_FINISH;
                                    end
                                state <= S_DIVIDE;
                            end

                        S_DIVIDE:
                            begin
                                if (A[106])
                                    begin
                                        {A, Q} = {A, Q} << 1;
                                        A = A+M;
                                    end
                                else
                                    begin
                                        {A, Q} = {A, Q} << 1;
                                        A = A-M;
                                    end
                                if (A[106])
                                    begin
                                        Q[0] = 0;
                                    end
                                else
                                    begin
                                        Q[0] = 1;
                                    end
                                if (A[106])
                                    begin
                                        {A, Q} = {A, Q} << 1;
                                        A = A+M;
                                    end
                                else
                                    begin
                                        {A, Q} = {A, Q} << 1;
                                        A = A-M;
                                    end
                                if (A[106])
                                    begin
                                        Q[0] = 0;
                                    end
                                else
                                    begin
                                        Q[0] = 1;
                                    end
                                if (A[106])
                                    begin
                                        {A, Q} = {A, Q} << 1;
                                        A = A+M;
                                    end
                                else
                                    begin
                                        {A, Q} = {A, Q} << 1;
                                        A = A-M;
                                    end
                                if (A[106])
                                    begin
                                        Q[0] = 0;
                                    end
                                else
                                    begin
                                        Q[0] = 1;
                                    end
                                if (A[106])
                                    begin
                                        {A, Q} = {A, Q} << 1;
                                        A = A+M;
                                    end
                                else
                                    begin
                                        {A, Q} = {A, Q} << 1;
                                        A = A-M;
                                    end
                                if (A[106])
                                    begin
                                        Q[0] = 0;
                                    end
                                else
                                    begin
                                        Q[0] = 1;
                                    end
                                count = count+1;
                                if (count == 26)
                                    begin
                                        state = S_FINISH;
                                        if (A[106])
                                            begin
                                                {A, Q} = {A, Q} << 1;
                                                A = A+M;
                                            end
                                        else
                                            begin
                                                {A, Q} = {A, Q} << 1;
                                                A = A-M;
                                            end
                                        if (A[106])
                                            begin
                                                Q[0] = 0;
                                            end
                                        else
                                            begin
                                                Q[0] = 1;
                                            end
                                        if (A[106])
                                            begin
                                                {A, Q} = {A, Q} << 1;
                                                A = A+M;
                                            end
                                        else
                                            begin
                                                {A, Q} = {A, Q} << 1;
                                                A = A-M;
                                            end
                                        if (A[106])
                                            begin
                                                Q[0] = 0;
                                            end
                                        else
                                            begin
                                                Q[0] = 1;
                                            end

                                    end
                            end

                        S_FINISH:
                            begin
                                if (~Q[53])
                                    begin
                                        Q = Q << 1;
                                        a_exp = a_exp-1;
                                    end
                                z_mantis = Q[52:1];
                                z_exp = 1023+a_exp-b_exp;
                                z_sign = a_sign ^ b_sign;
                                state = S_IDLE;
                                //underflow,overflow
                                if (z_exp > 2046)
                                    begin
                                        z_sign = a_sign ^ b_sign;
                                        z_exp = 1024;
                                        z_mantis = 0;
                                    end
                                if (z_exp < 1)
                                    begin
                                        z_sign = a_sign ^ b_sign;
                                        z_exp = 0;
                                        z_mantis = 0;
                                    end
                            end

                        S_IDLE:
                            begin
                                if (start)
                                  state <= S_START;
                            end
                    endcase
                end
            else
                begin
                    state <= S_IDLE;
                    z_exp <= 0;
                    z_mantis <= 0;
                    z_exp <= 0;
                end

        end

    assign o_z = {z_sign, z_exp, z_mantis};
endmodule

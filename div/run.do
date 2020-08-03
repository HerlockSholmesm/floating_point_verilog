vlog -work work -vopt -stats=none {C:\Users\Mohammad\Desktop\dsd\New folder\tb_sp.v}

vsim -gui work.tb_sp -novopt

add wave  \
sim:/tb_sp/clk \
sim:/tb_sp/strt \
sim:/tb_sp/a \
sim:/tb_sp/b \
sim:/tb_sp/z \


run 400 ns


// Speed probe for the deck's "Speed, Accuracy and Effort" slide: the same RTL (ntt_core from
// RTL_CoSim_NTT) simulated by an event-driven simulator (Icarus Verilog) and a cycle-based,
// compiled one (Verilator). The testbench streams REPS transforms of one input vector and checks
// every output word against the golden NTT written by run_rtl_speed.py, so the run being timed is
// a correct one. It prints the number of clock cycles simulated.
`timescale 1ns/1ps
module tb_ntt_speed;
    localparam int W = 50, LOGN = 10, P = 4, N = 1 << LOGN;
    parameter int REPS = 10;

    logic clk = 0, rst_n = 0;
    logic [W-1:0] cfg_q;
    logic [W:0] cfg_mu;
    logic [4:0] cfg_logn = LOGN;
    logic tw_we = 0;
    logic [LOGN-2:0] tw_addr = 0;
    logic [W-1:0] tw_data = 0;
    logic in_valid = 0, in_ready, out_valid, out_ready = 1, busy;
    logic [P*W-1:0] in_data = 0, out_data;
    logic [31:0] stat_compute_cycles;

    logic [W-1:0] q_mem [0:0];
    logic [W:0] mu_mem [0:0];
    logic [W-1:0] tw [0:N/2-1];
    logic [W-1:0] x [0:N-1];
    logic [W-1:0] want [0:N-1];

    ntt_core #(.W(W), .LOGN(LOGN), .P(P)) dut (.*);

    longint unsigned cycles = 0;
    always #1 clk = ~clk;
    always @(posedge clk) cycles <= cycles + 1;

    int errors = 0, beat_in, beat_out, rep_out;
    initial begin
        $readmemh("cfg_q.hex", q_mem);
        $readmemh("cfg_mu.hex", mu_mem);
        $readmemh("tw.hex", tw);
        $readmemh("x.hex", x);
        $readmemh("want.hex", want);
        cfg_q = q_mem[0];
        cfg_mu = mu_mem[0];
        repeat (3) @(posedge clk);
        rst_n = 1;
        for (int k = 0; k < N / 2; k++) begin
            @(negedge clk);
            tw_we = 1; tw_addr = k[LOGN-2:0]; tw_data = tw[k];
        end
        @(negedge clk) tw_we = 0;
        fork
            // driver: REPS transforms, back to back
            begin
                for (int r = 0; r < REPS; r++)
                    for (beat_in = 0; beat_in < N / P; beat_in++) begin
                        for (int l = 0; l < P; l++) in_data[l*W +: W] = x[beat_in*P + l];
                        in_valid = 1;
                        do @(posedge clk); while (!in_ready);
                        #0.1;
                    end
                in_valid = 0;
            end
            // monitor: compare every output word with the golden NTT
            for (rep_out = 0; rep_out < REPS; rep_out++)
                for (beat_out = 0; beat_out < N / P; beat_out++) begin
                    do @(posedge clk); while (!out_valid);
                    for (int l = 0; l < P; l++)
                        if (out_data[l*W +: W] !== want[beat_out*P + l]) errors++;
                end
        join
        $display("REPS=%0d CYCLES=%0d ERRORS=%0d", REPS, cycles, errors);
        $finish;
    end
endmodule

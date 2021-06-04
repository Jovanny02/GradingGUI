
try {
    vsim -c -quiet work.adder_true_testbench_config
    add wave *
    run -all
} on error {msg} {
    puts "SIMULATION FAILED"
    puts $msg
    quit -sim
}
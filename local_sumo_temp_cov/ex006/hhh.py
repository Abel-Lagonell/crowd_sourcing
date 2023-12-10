import pantherine as purr
import systematicSim2 as ss2
from simSync import SimulationSychronizer

def main():
    sim = purr.load("temp/ss.pybin")
    sim.run_geometric(max_iter=100)
    return

if __name__ == "__main__":
    main()

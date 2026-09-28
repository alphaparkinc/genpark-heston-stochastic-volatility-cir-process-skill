"""Example demonstrating Heston model simulation."""
from client import HestonSimulator

def main():
    res = HestonSimulator.simulate_paths(s0=100.0, v0=0.04, mu=0.03, kappa=2.0, theta=0.04, xi=0.3, rho=-0.7, t_max=1.0, steps=10)
    print("Feller Condition Satisfied:", res["feller_satisfied"])
    print("Final Price:", res["price_path"][-1])
    print("Final Variance:", res["variance_path"][-1])

if __name__ == "__main__":
    main()

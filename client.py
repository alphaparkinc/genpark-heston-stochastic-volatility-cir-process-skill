"""Heston Stochastic Volatility & CIR Process Simulator.
100% Python Standard Library.
"""

import math
import random

class HestonSimulator:
    """Simulates correlated price and variance paths under Heston dynamics."""
    @staticmethod
    def verify_feller_condition(kappa, theta, xi):
        return (2.0 * kappa * theta) > (xi**2)

    @staticmethod
    def simulate_paths(s0, v0, mu, kappa, theta, xi, rho, t_max, steps, seed=42):
        rng = random.Random(seed)
        dt = t_max / steps
        sqrt_dt = math.sqrt(dt)
        
        s_path = [s0]
        v_path = [v0]
        s = s0
        v = v0
        
        for _ in range(steps):
            z1 = rng.gauss(0.0, 1.0)
            z2 = rng.gauss(0.0, 1.0)
            dw_v = z1 * sqrt_dt
            dw_s = (rho * z1 + math.sqrt(max(0.0, 1.0 - rho**2)) * z2) * sqrt_dt
            
            v_pos = max(v, 0.0)
            dv = kappa * (theta - v_pos) * dt + xi * math.sqrt(v_pos) * dw_v
            v = max(v + dv, 0.0)
            
            ds = mu * s * dt + math.sqrt(v_pos) * s * dw_s
            s += ds
            
            s_path.append(round(s, 4))
            v_path.append(round(v, 6))
            
        return {"price_path": s_path, "variance_path": v_path, "feller_satisfied": HestonSimulator.verify_feller_condition(kappa, theta, xi)}
